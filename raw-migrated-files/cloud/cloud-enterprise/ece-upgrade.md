# Upgrade your installation [ece-upgrade]

Periodically, you might need to upgrade an Elastic Cloud Enterprise installation as new versions with additional features become available. The upgrade process updates all hosts that are part of an Elastic Cloud Enterprise installation to the latest version of ECE, with little or no downtime for managed deployments.

Before initiating the ECE upgrade process, consult the [OS & Docker supportability matrix](https://www.elastic.co/support/matrix) to make sure that the Operating System (OS) and Docker versions you run are compatible with the ECE version you’re about to upgrade to. We recommend that Docker and the operating system be at the target version before starting the ECE upgrade procedure.

::::{note}
During the upgrade window, there might be a short time you are on a mix of versions which is not declared explicitly in the support matrix. For example, if you are on ECE 3.5 with Docker version 20.10 on Ubuntu 20.04, and plan to upgrade to ECE 3.7 on same OS, you will need to upgrade Docker to version 24.0 first. In this case, **only during your upgrade window**, we support the mixed OS/Docker versions. In general, this won’t be a problem, however, should anything become a blocker for the upgrade, please [reach out to support for help](../../../troubleshoot/deployments/cloud-enterprise/ask-for-help.md).
::::



## The upgrade version matrix [ece-upgrade-version-matrix]

The following table shows the recommended upgrade paths from older {{ece}} versions to 3.8.1.

| Upgrade from | Recommended upgrade path to 3.8.1 |
| --- | --- |
| Any previous 3.x version (for example, 3.0.0) | Upgrade directly to 3.8.1 |
| 2.13 | Upgrade directly to 3.8.1 |
| 2.5-2.12 | 1. Upgrade to 2.13.4<br>2. Upgrade to 3.8.1<br> |
| 2.0-2.4 | 1. Upgrade to 2.5.1<br>2. Upgrade to 2.13.4<br>3. Upgrade to 3.8.1<br> |


## The upgrade process [ece-upgrade-overview]

Upgrading Elastic Cloud Enterprise works by replacing the [containers](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html#glossary-container) that ECE itself requires to run on each host. Upgrading ECE does not touch any of the containers that run Elasticsearch clusters and Kibana instances. Each container that needs to be upgraded is renamed and stopped, followed by the creation of a new container with an upgraded instance of the ECE software and its dependencies. When the upgrade process has completed successfully, it cleans up after itself and removes the old containers.

The upgrade process creates a `frc-upgraders-monitor` container on the host where you initiate the process that performs the following actions:

* Back up the ZooKeeper transaction log to `HOST_STORAGE_PATH/RUNNER_ID/services/zookeeper/data/backup`, where `HOST_STORAGE_PATH` and `RUNNER_ID` are specific to an ECE installation.
* Configure Elastic Cloud Enterprise to perform the individual container upgrades by creating a `frc-upgraders-upgrader` container on each host that is part of the installation.
* Monitor the upgrade process to ensure that all `frc-upgraders-upgrader` containers perform their part of the upgrade as expected and report their status.
* After all hosts have been upgraded successfully, clean up temporary artifacts created during the upgrade process, and remove the old containers.

The entire process is designed to be failsafe.  Containers get upgraded sequentially and the upgrade status of each container is tracked. The upgrade process also monitors that each new container is viable and continues to run as expected. If there is an issue with any part of the upgrade, [the entire process is rolled back](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-troubleshooting-upgrade).


## Recommendations [ece-upgrade-recommendations]

Before starting the upgrade process, check which of the following recommendations may apply for your setup:

* Upgrading to 2.12.x or 2.13.0 is not recommended as it can cause issues and you may lose access to the admin console. You are strongly advised to upgrade to 2.13.1 and later.
* If you are upgrading to ECE versions 2.10, 2.11, or 2.12, refer to the ECE version 2.12 [upgrade steps](https://www.elastic.co/guide/en/cloud-enterprise/2.12/ece-upgrade.html#ece-upgrade-system-deployments) for guidance about certain default ECE visualizations not working.
* We strongly recommend that you routinely update your ECE installation to the most current version so that any bugs and security issues are fixed promptly. If you need to upgrade but are currently experiencing any issues with your platform, note that as long as ZooKeeper is running and healthy you should be able to upgrade (you can use the [get runners API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-runners) to easily verify the health of the runners on the [ECE allocators](../../../deploy-manage/deploy/cloud-enterprise/ece-architecture.md#ece-architecture-allocators)). That is, healthy system deployments are not required in order to perform an upgrade successfully.
* Before upgrading to Elastic Cloud Enterprise 3.0, refer to the [lists of removals](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-3-0-removals.html) to find out about features and API endpoints that are no longer supported.
* We strongly recommend that you do not attempt to perform certain actions during the upgrade process, such as:

    * Creating or changing Elasticsearch clusters and Kibana instances
    * Adding new hosts to an installation or removing existing hosts

* As a precaution, we recommend that taking current snapshots of the Elasticsearch clusters.
* We recommend that you take a backup snapshot of the `security` [system deployment](../../../deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md). This cluster stores [role-based access control configurations](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md), and a snapshot will allow you to restore those in case the upgrade fails.


## Requirements [ece-upgrade-prereqs]

Before starting the upgrade process, verify that your setup meets the following requirements:

* **XFS with quotas enabled on all allocators.** You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly. To enable XFS quotas, modify the entry for the XFS volume in the `/etc/fstab file` to add `pquota` and `prjquota`. The default filesystem path used by Elastic Cloud Enterprise is `/mnt/data`.
* **Supported Docker / Podman version** Make sure that you run a supported Docker or Podman version for the version of ECE that you are going to upgrade to. An overview of compatible versions can be found in the [support matrix](https://www.elastic.co/support/matrix#matrix_os&#elastic-cloud-enterprise) and install instructions are available under [Installing Elastic Cloud Enterprise](../../../deploy-manage/deploy/cloud-enterprise/install.md).
* **Required user, roles and groups** To run the script to upgrade Elastic Cloud Enterprise, login as the user used to run Elastic Cloud Enterprise (by default called `elastic` with UID/GID 1000). Initiate the upgrade process by running the `elastic-cloud-enterprise.sh` script with the `upgrade` action on a single host. The host that the script is run on must be a host that holds the director role. You do not need to run the script on additional hosts.
* **Available disk space** Each host in the Elastic Cloud Enterprise installation must have at least 5 GB of disk space available to ensure that the upgrade process can complete successfully.
* **Proxies and load balancing** To avoid any downtime for Elastic Cloud Enterprise, the installation must include more than one proxy and must use a load balancer as recommended. If only a single proxy is configured or if the installation is not using a load balancer, some downtime is expected when the containers on the proxies are upgraded. Each container upgrade typically takes five to ten seconds, times the number of containers on a typical host.
* **For *offline* or *air-gapped* installations** Additional steps are required to upgrade Elastic Cloud Enterprise. After downloading the installation script for the new version, pull and load the required container images and push them to a private Docker registry. To learn more about pulling and loading Docker images, check [Install ECE offline](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md).
* **Verify if you can upgrade directly** If you are upgrading to ECE 3.0 or a higher version, you need to upgrade to ECE 2.13.1 or later. Refer to the ECE version 2.13 [upgrade instructions](https://www.elastic.co/guide/en/cloud-enterprise/2.13/ece-upgrade.html) for details.

::::{warning}
Don’t manually upgrade your system deployments if you are on ECE version 2.7.0 or a later version, as it can cause issues and you may lose access to the Cloud UI. Note that the only exception to that rule is when you’re upgrading to ECE 3.6.0 and your system deployments are at a version lower than 7.17.0.
::::


* **If you are on an ECE version below 2.7, verify if the system deployments need to be upgraded**

    * If there are system deployments below version 6.8 or an ECE installation below version 2.7.0, refer to the ECE version 2.7 documentation for the steps to [upgrade your system deployments](https://www.elastic.co/guide/en/cloud-enterprise/2.7/ece-upgrade.html#ece-upgrade-system-deployments). Starting with ECE 2.7, all system deployments are upgraded automatically to their latest supported Elasticsearch version as part of the ECE upgrade process. This means that each system deployment can be upgraded to different major versions. For example, the security cluster could be upgraded to 8.x, while the admin and logging-and-metrics clusters could be upgraded to the latest 7.17.x version.
    * When upgrading from an ECE version between 2.0 and 2.4 included, we recommend to upgrade to ECE 2.5 first, then to manually upgrade system deployments to version 6.8.

* If you are upgrading to ECE 3.6.0, you need to ensure that your system deployments are at version 7.17 because the upgrade process will attempt to upgrade the security cluster to 8.5 or higher. Starting with ECE 3.6.1, the upgrade process automatically upgrades system deployments to the minimum required version. If the Elastic Cloud Enterprise platform was upgraded successfully and yet one or more system deployments were not upgraded to a higher Elastic Stack version during the very last phase of the Elastic Cloud Enterprise upgrade, you can re-run the `elastic-cloud-enterprise.sh upgrade --cloud-enterprise-version <your target version>` command to retry system deployment upgrade only.
* **Check the security cluster’s zone count** Due to internal limitations in ECE, the built-in security cluster cannot be scaled to two zones during the ECE upgrade procedure. If the zone count is set to 2 zones, scale the cluster to 3 or 1 zone(s) before upgrading ECE.
* **Outdated cluster versions** If the ECE installation has clusters using version 5.5 or earlier, upgrading to version 5.6 is mandatory before a major upgrade.


### Certificate rotation [ece-upgrade-certificates]

If your ECE installation is still using the default, auto-generated certificates, we recommend performing one of the following steps to avoid trust errors related to the proxy server certificate after the upgrade. The proxy server certificate is used when connecting to Kibana and Elasticsearch clusters. During the upgrade, the ECE certificate authority generates a new certificate. As with any server certificate rotation, you must add an exception for the new proxy server certificate, unless the certificate authority is present in the trust store of the system or browser. You can perform either of these steps before or after the upgrade:

* Recommended: [Add your organization’s own certificate](../../../deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) to Elastic Cloud Enterprise. The upgrade process ensures that the certificates you add do not change, which avoids the trust errors.
* Add the default CA certificate to the trust store of your system or of your browser. Only the server certificate changes during upgrade, but the CA certificate remains the same. Adding the CA certificate to your trust store alone is sufficient to avoid the trust errors.
* Apply valid license. It is required to have an `Enterprise resource unit`-compatible license applied before upgrading to ECE 2.7+. The most reliable way to check if your license is compatible is to use the Elastic Cloud Enterprise API and check the value of the license version field:

    ```sh
    curl -X GET -u admin:PASSWORD -k https://COORDINATOR_HOST:12443/api/v1/platform/license
    {
      "license": {
        "version": 4,
        // other fields
      }
    }
    ```

    If the version is not 4 or higher, you must request an updated license from [Elastic Support](../../../troubleshoot/deployments/cloud-enterprise/ask-for-help.md). Once you receive your new license, make sure Elastic Cloud Enterprise is upgraded to at least version 2.5.0, and then upload the new license in the **Settings** page under the **Platform** menu.


In versions from 2.6 to 2.10 included, some or all platform certificates are generated with a 398-day expiration. Installations that ran on these versions, even temporarily, must have their certificates rotated manually before expiry. For details, check [our KB article](https://ela.st/ece-certificate-rotation).


## Perform the upgrade [ece-upgrade-steps]

To upgrade an Elastic Cloud Enterprise installation, download the latest installation script. Login as the user used to run Elastic Cloud Enterprise (by default called `elastic` with UID/GID 1000), and run the script with the `upgrade` action on a single host that holds the director role:

::::{important}
If you are using SELinux, make sure you also use `--selinux`.

::::


```sh
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) upgrade
```

You can follow along while each container for Elastic Cloud Enterprise is upgraded on the hosts that are part of the installation.

By default, ECE updates to the most current available version. If you want to upgrade to a specific ECE version, use the `--cloud-enterprise-version` option:

```sh
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) upgrade --user admin --pass $PASSWORD --cloud-enterprise-version 3.0.0
```
