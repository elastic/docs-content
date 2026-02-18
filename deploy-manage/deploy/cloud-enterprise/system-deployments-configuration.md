---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-system-clusters-configuration.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# System deployments configuration [ece-system-clusters-configuration]

When installing ECE, you will notice that several {{es}} clusters get created as part of the installation process. Those are the *system deployments* which are part of the ECE control plane. You must make sure that they are configured and sized correctly to ensure you have a production-ready installation.

We will review each cluster and provide recommendations to make sure that you are following best practices when starting your ECE journey.

::::{note} 
By default, the system deployments have a dedicated `system_owned` flag set to `true` to avoid mistakenly changing the configuration of those clusters. Most configuration changes suggested in this section do not require this flag to be set to `false`, but there are some cases where changing the flag might be required. If you do change this flag, always make sure to set it back to `true` once you have completed the changes. The flag can be set by navigating to the **Data** section in the **Advanced cluster configuration** page.
::::

:::{warning}
Independent upgrades should only be performed when Elastic Support explicitly instructs you to do so.
:::


## Overview of system deployments [ece_overview_of_system_deployments] 

Admin console - `admin-console-elasticsearch`
:   Stores the state of your deployments, plans, and other operational data. If this cluster is not available, there will be several unexpected behaviors in the Cloud UI, such as stale or wrong status indicators for deployments, allocators, hosts, and more.

Logging and metrics - `logging-and-metrics`
:   As part of an ECE environment, a Beats sidecar with Filebeat and Metricbeat is installed on each ECE host. The logs and metrics collected by those beats are indexed in the `logging-and-metrics` cluster. This includes ECE service logs, such as proxy logs, director logs, and more. It also includes hosted deployments logs, security cluster audit logs, and metrics, such as CPU and disk usage. Data is collected from all hosts. This information is critical in order to be able to monitor ECE and troubleshoot issues. You can also use this data to configure watches to alert you in case of an issue, or machine learning jobs that can provide alerts based on anomalies or forecasting.

Security - `security`
:   When you enable the user management feature, you trigger the creation of a third system deployment named `security`. This cluster stores all security-related configurations, such as native users and the related native realm, integration with SAML or LDAP as external authentication providers and their role mapping, and the realm ordering. The health of this cluster is critical to provide access to the ECE Cloud UI and REST API. To learn more, check [Configure role-based access control](../../users-roles/cloud-enterprise-orchestrator/manage-users-roles.md). Beginning with {{ece}} 2.5.0 the `security` cluster is created automatically for you. It is recommended to use the [dedicated API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-update-security-deployment) to manage the cluster.


## High availability [ece_high_availability] 

ECE supports the concept of [availability zones](ece-ha.md) and requires three availability zones to be configured for the best fault tolerance.

The system deployments are created when you install ECE or enable the user management feature, at which point they are not yet configured for high availability. As soon as you finish the installation process, you should change the configuration to ensure your system deployments are highly available and deployed across two or three availability zones. To configure your system deployments to be highly available, navigate to the **Edit** page for the cluster and change the number of availability zones under **Fault tolerance**.

For the `logging-and-metrics` cluster, you might want to also make sure that your {{kib}} instance and other components are deployed across multiple availability zones, since you will often access that cluster using {{kib}}. You can change the availability zones for {{kib}} on the same **Edit** page.

::::{note} 
For the `security` cluster, the number of zones must be set to 3 for high availability, otherwise you may encounter errors when trying to upgrade ECE versions.
::::

## Backup and restore [ece_backup_and_restore] 

ECE lets you manage snapshot repositories, so that you can back up and restore your clusters. This mechanism allows you to centrally manage your snapshot repositories, assigning them to deployments, and restoring snapshots to an existing or new deployment. Since the `admin-console-elasticsearch` and `security` clusters have a key role in making sure your ECE installation is operational, it’s important that you configure a snapshot repository after you complete your ECE installation and enable snapshots for both the `admin-console-elasticsearch` and `security` clusters, so that you can easily restore them if needed.

As mentioned earlier, the `logging-and-metrics` cluster stores important information about your environment logs and metrics. There are also additional configurations provided out-of-the-box, such as data views (formerly *index patterns*), visualizations, and dashboards, that will require running an external script to recreate if you do not have a snapshot to restore from. We recommend that you also back up the `logging-and-metrics` cluster, though it is up to you to decide if that information should be available to be restored.

To configure snapshot repositories, check [Add snapshot repository configurations](../../tools/snapshot-and-restore/cloud-enterprise.md).

## Sizing [ece_sizing] 

Both the `admin-console-elasticsearch` and `security` clusters require relatively small amounts of RAM and almost no disk space, so increasing their size to 4 GB or 8 GB RAM per data node should be sufficient.

Undersizing the `logging-and-metrics` cluster can lead to saturation and degrade the health of that cluster, and eventually prevent you from monitoring your ECE installation and its hosted deployments.

When sizing your `logging-and-metrics` cluster, consider:

* the expected workload, which affects the daily ingest size.
* the number of ECE hosts, deployments, and log types you want to enable, such as slow logs or audit logs.
* the desired [retention period for the data](/deploy-manage/monitor/orchestrators/ece-monitoring-ece-set-retention.md). As with any other time-series data, you must properly manage your indices and delete old indices based on that retention period.

## Access to system deployments [ece_access_to_system_deployments] 

In the case of the `admin-console-elasticsearch` and `security` system deployments, the team managing ECE and assigned to the platform admin role should have permission to change each system deployment configuration and also to access each cluster itself.

The `logging-and-metrics` cluster is different since, as an ECE admin, you likely want to provide users with access to the cluster in order to troubleshoot issues without your assistance, for example. In order to manage access to that cluster, you can configure roles that will provide access to the relevant indices, map those to users, and manage access to {{kib}} by leveraging the Elastic security integration with your authentication provider, such as LDAP, SAML, or AD. To configure one of those security realms, check [LDAP](../../users-roles/cluster-or-deployment-auth/ldap.md), [Active Directory](../../users-roles/cluster-or-deployment-auth/active-directory.md) or [SAML](../../users-roles/cluster-or-deployment-auth/saml.md).

::::{note} 
The `logging-and-metrics` cluster is only intended for troubleshooting ECE deployment issues. If your use case involves modifying or normalizing logs from {{es}} or {{kib}}, use a separate [dedicated monitoring deployment](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) instead.
::::

You can’t use ECE’s single sign-on (SSO) to access system deployments.

::::{note} 
Enabling integration with external authentication provider requires that you set the `system_owned` flag to `false` in order to change the elasticsearch.yaml configuration. Remember to set the flag back to `true` after you are done.
::::
