---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrade.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece_re_running_the_ece_upgrade.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

% The upgrade procedure is expected to change with ECE 3.8.0 release. This document is currently a temporary draft, pending to be refined.

# Upgrade {{ece}} [ece-upgrade]

This page provides instructions on how to upgrade the ECE operator.

To learn how to upgrade {{stack}} applications like {{es}} or {{kib}}, refer to [Upgrade the {{stack}} version](../deployment-or-cluster.md).

Periodically, you might need to upgrade an {{ece}} installation as new versions with additional features become available. The upgrade process updates all hosts that are part of an {{ece}} installation to the latest version of ECE, with little or no downtime for managed deployments. To upgrade your deployment to {{stack}} 9.x, the minimum required ECE version is 4.0.0.

Before initiating the ECE upgrade process, review the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) to ensure the operating system (OS), Docker, or Podman versions you're running are compatible with the ECE version you’re upgrading to. We recommend that Docker, Podman, and the operating system are at the target version before starting the ECE upgrade.

:::{note}
During the upgrade window, there might be a short period of time during which you run a combination of versions that is not explicitly supported. For example, if you are on ECE 3.5 with Docker version 18.09 on SLES 12 and plan to upgrade to ECE 3.8 on the same OS, you will need to upgrade Docker to version 24.0 or 25.0 first. In this case, and only during your upgrade window, we will support the mixed OS and container engine versions. In general, this won’t be a problem. However, should anything become a blocker for the upgrade, [reach out to support for help](/troubleshoot/index.md#contact-us).
:::

## The upgrade version matrix [ece-upgrade-version-matrix]

The following table shows the recommended upgrade paths from older {{ece}} versions to {{version.ece}}.

| Upgrade from | Recommended upgrade path to 4.0 |
| --- | --- |
| Any 3.x version | 1. Upgrade to 3.8.0<br>2. Upgrade to {{version.ece}}<br> |
| 2.13 | 1. Upgrade to 3.8.0<br>2. Upgrade to {{version.ece}}<br> |
| 2.5-2.12 | 1. Upgrade to 2.13.4<br>2. Upgrade to 3.8.0<br>3. Upgrade to {{version.ece}}<br> |
| 2.0-2.4 | 1. Upgrade to 2.5.1<br>2. Upgrade to 2.13.4<br>3. Upgrade to 3.8.0<br>4. Upgrade to {{version.ece}}<br> |

If you have to upgrade to any of the intermediate versions, follow the upgrade instructions of the relevant release before upgrading to {{version.ece}}:
- [ECE 2.5 Upgrade](https://www.elastic.co/guide/en/cloud-enterprise/2.5/ece-upgrade.html)
- [ECE 2.13 Upgrade](https://www.elastic.co/guide/en/cloud-enterprise/2.13/ece-upgrade.html)

  :::{note}
  We don't recommend upgrading to 2.13.0, as it can cause issues and you may lose access to the admin console. We strongly recommend upgrading to 2.13.4.
  :::

- [ECE 3.8 Upgrade](https://www.elastic.co/guide/en/cloud-enterprise/3.8/ece-upgrade.html)

## The upgrade process [ece-upgrade-overview]

Upgrading {{ece}} works by replacing the [containers](/reference/glossary/index.md#glossary-container) that ECE itself requires to run on each host. Upgrading ECE does not touch any of the containers that run {{es}} clusters and {{kib}} instances. Each container that needs to be upgraded is renamed and stopped, followed by the creation of a new container with an upgraded instance of the ECE software and its dependencies. When the upgrade process has completed successfully, it cleans up after itself and removes the old containers.

The upgrade process creates a `frc-upgraders-monitor` container on the host where you initiate the process that performs the following actions:

* Back up the ZooKeeper transaction log to `HOST_STORAGE_PATH/RUNNER_ID/services/zookeeper/data/backup`, where `HOST_STORAGE_PATH` and `RUNNER_ID` are specific to an ECE installation.
* Configure {{ece}} to perform the individual container upgrades by creating a `frc-upgraders-upgrader` container on each host that is part of the installation.
* Monitor the upgrade process to ensure that all `frc-upgraders-upgrader` containers perform their part of the upgrade as expected and report their status.
* After all hosts have been upgraded successfully, clean up temporary artifacts created during the upgrade process, and remove the old containers.

The entire process is designed to be failsafe.  Containers get upgraded sequentially and the upgrade status of each container is tracked. The upgrade process also monitors that each new container is viable and continues to run as expected. If there is an issue with any part of the upgrade, [the entire process is rolled back](/troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-troubleshooting-upgrade).

## Recommendations [ece-upgrade-recommendations]

Before starting the upgrade process, check which of the following recommendations may apply for your setup:


* We strongly recommend that you routinely update your ECE installation to the most current version so that any bugs and security issues are fixed promptly. If you need to upgrade but are currently experiencing any issues with your platform, note that as long as ZooKeeper is running and healthy you should be able to upgrade (you can use the [get runners API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-runners) to easily verify the health of the runners on the [ECE allocators](../../../deploy-manage/deploy/cloud-enterprise/ece-architecture.md#ece-architecture-allocators)). That is, healthy system deployments are not required in order to perform an upgrade successfully.
* Review the [known issues](cloud://release-notes/cloud-enterprise/known-issues.md) to find out about limitations and known problems, to ensure a smoother upgrade experience.
* Review the [lists of removals](cloud://release-notes/cloud-enterprise/breaking-changes.md) to find out about features and API endpoints that are no longer supported.
* We strongly recommend that you do not attempt to perform certain actions during the upgrade process, such as:

    * Creating or changing {{es}} clusters and {{kib}} instances
    * Adding new hosts to an installation or removing existing hosts

* As a precaution, we recommend taking snapshots of your {{es}} clusters.
* We recommend that you take a backup snapshot of the `security` [system deployment](../../../deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md). This cluster stores [role-based access control configurations](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md), and a snapshot will allow you to restore those in case the upgrade fails.

## Requirements [ece-upgrade-prereqs]

Before starting the upgrade process, verify that your setup meets the following requirements:

- **XFS with quotas enabled on all allocators.** You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly. To enable XFS quotas, modify the entry for the XFS volume in the `/etc/fstab file` to add pquota and `prjquota`. The default filesystem path used by {{ece}} is `/mnt/data`.

- **Supported Docker / Podman version**.  Make sure that you’re running a supported Docker or Podman version for the version of ECE that you are going to upgrade to. An overview of compatible versions can be found in the [support matrix](https://www.elastic.co/support/matrix#matrix_os&#elastic-cloud-enterprise) and install instructions are available under [Installing {{ece}}](../../../deploy-manage/deploy/cloud-enterprise/install.md).
- **Required user, roles and groups**. To run the script to upgrade {{ece}}, log in as the user used to run {{ece}} (by default called `elastic` with UID/GID 1000). Initiate the upgrade process by running the `elastic-cloud-enterprise.sh` script with the upgrade action on a single host. The host that the script is run on must be a host that holds the director role. You do not need to run the script on additional hosts.
- **Available disk space**. Each host in the {{ece}} installation must have at least 5 GB of disk space available to ensure that the upgrade process can complete successfully.
- **Proxies and load balancing**. To avoid any downtime for {{ece}}, the installation must include more than one proxy and must use a load balancer as recommended. If only a single proxy is configured or if the installation is not using a load balancer, some downtime is expected when the containers on the proxies are upgraded. Each container upgrade typically takes five to ten seconds, times the number of containers on a typical host.
- **For *offline* or *air-gapped* installations**. Additional steps are required to upgrade {{ece}}. After downloading the installation script for the new version, pull and load the required container images and push them to a private Docker registry. To learn more about pulling and loading Docker images, check Install [ECE offline](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md).
- **Check the security cluster’s zone count.** Due to internal limitations in ECE, the built-in security cluster cannot be scaled to two zones during the ECE upgrade procedure. If the zone count is set to 2 zones, scale the cluster to 3 or 1 zone(s) before upgrading ECE.
- **[Verify if you can upgrade directly](#ece-upgrade-version-matrix)**. When upgrading to ECE 4.0 or a higher version:
  - You need to first upgrade to ECE 3.8.0 or later. Refer to the [ECE version 3.8.0 upgrade instructions](https://www.elastic.co/guide/en/cloud-enterprise/3.8/ece-upgrade.html) for details.

  :::{warning}
  Don’t manually upgrade your system deployments if you are on ECE version 2.7.0 or a later version, as it can cause issues and you may lose access to the Cloud UI. Note that the only exception to that rule is when you’re upgrading to ECE 3.6.0 and your system deployments are at a version lower than 7.17.0.
  :::

  - Ensure that your system deployments are at their [expected versions](/deploy-manage/deploy/cloud-enterprise/default-system-deployment-versions.md). Since ECE 3.6.1, the upgrade process automatically upgrades system deployments to the required version. If the {{ece}} platform was upgraded successfully and yet one or more system deployments were not upgraded to [their expected version](/deploy-manage/deploy/cloud-enterprise/default-system-deployment-versions.md) during the very last phase of the {{ece}} upgrade, you can re-run the `elastic-cloud-enterprise.sh upgrade --cloud-enterprise-version <your target version>` command to retry system deployment upgrade only.
  - Check that your deployments are running on {{stack}} version 8.0.0 or above.
- **Before running the upgrade command, ensure that you include the same installation flags that were used during the initial setup.** Some deployment configurations, such as those using Podman or SELinux, require specific flags to be passed again during the upgrade. Failure to do so may result in compatibility errors.

## Certificate rotation [ece-upgrade-certificates]

If your ECE installation is still using the default, auto-generated certificates, we recommend performing one of the following steps to avoid trust errors related to the proxy server certificate after the upgrade. The proxy server certificate is used when connecting to {{kib}} and {{es}} clusters. During the upgrade, the ECE certificate authority generates a new certificate. As with any server certificate rotation, you must add an exception for the new proxy server certificate, unless the certificate authority is present in the trust store of the system or browser. You can perform either of these steps before or after the upgrade:

- Recommended: [Add your organization’s own certificate](../../../deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) to {{ece}}. The upgrade process ensures that the certificates you add do not change, which avoids the trust errors.
- Add the default CA certificate to the trust store of your system or of your browser. Only the server certificate changes during upgrade, but the CA certificate remains the same. Adding the CA certificate to your trust store alone is sufficient to avoid the trust errors.
- Apply a valid license. It is required to have an `Enterprise resource unit`-compatible license applied before upgrading to ECE 2.7 or later. The most reliable way to check if your license is compatible is to use the {{ece}} API and check the value of the license version field:

    ```sh
    curl -X GET -u admin:PASSWORD -k https://$COORDINATOR_HOST:12443/api/v1/platform/license
    {
      "license": {
        "version": 4,
        // other fields
      }
    }
    ```

If the license version is not 4 or higher, you must request an updated license from [Elastic Support](/troubleshoot/index.md#contact-us). Once you receive your new license, make sure {{ece}} is upgraded to at least version 2.5.0, and then upload the new license in the Settings page under the Platform menu.

In versions from 2.6 to 2.10 included, some or all platform certificates are generated with a 398-day expiration. Installations that ran on these versions, even temporarily, must have their certificates rotated manually before expiry. For details, check our [KB article](https://ela.st/ece-certificate-rotation).


## Perform the upgrade [ece-upgrade-steps]

To upgrade an {{ece}} installation, download the latest installation script. Log in as the user used to run {{ece}} (by default called `elastic` with UID/GID 1000), and run the script with the `upgrade` action on a single host that holds the director role:

::::{important}
* If your ECE installation was set up using **Podman** instead of Docker, append the `--podman` flag when running the upgrade command.
* If your installation uses **SELinux**, append the `--selinux` flag when running the upgrade command.
* If you configured a **custom Docker registry** during installation using the `--docker-registry` or `--ece-docker-repository` parameters, include the same parameters when running the upgrade.
* Starting in ECE 3.8.0, `upgrade` requires `--user` and `--pass` arguments, or a path to the `bootstrap-secrets.json` file, if the file does not exist already at the expected default path. See [elastic-cloud-enterprise.sh upgrade](cloud://reference/cloud-enterprise/ece-installation-script-upgrade.md) for details.
::::

```sh
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) upgrade --user admin --pass $PASSWORD
```

You can follow along while each container for {{ece}} is upgraded on the hosts that are part of the installation.

## Upgrade to a specific version

By default, ECE updates to the most current available version. If you want to upgrade to a specific ECE version, use the `--cloud-enterprise-version` option:

```sh subs=true
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) upgrade --user admin --pass $PASSWORD --cloud-enterprise-version {{version.ece}}
```







