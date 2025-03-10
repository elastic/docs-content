# Upgrade {{kib}} [upgrade]

To upgrade from 7.16.0 or earlier to 9.0.0-beta1, **you must first upgrade to 8.17**, which enables you to use the **Upgrade Assistant** to [prepare for the upgrade](../../../deploy-manage/upgrade/deployment-or-cluster.md#prepare-to-upgrade). Before you upgrade, you must resolve all critical issues identified by the **Upgrade Assistant**.

In addition, we recommend to carefully review the [list of breaking changes and deprecations](kibana://release-notes/breaking-changes.md) and to take any necessary actions to mitigate their impact on the upgrade. You can enable the [deprecated APIs debug logs config](kibana://reference/configuration-reference/logging-settings.md#enable-http-debug-logs) to get information about calls to deprecated APIs.

Rolling upgrades are unsupported in {{kib}}. To upgrade, you must shut down all {{kib}} instances, install the new software, and restart {{kib}}. Upgrading while older {{kib}} instances are running can cause data loss or upgrade failures.

::::{warning}
When required, {{kib}} automatically migrates [saved objects](../../../deploy-manage/upgrade/internal-upgrade-processes/saved-object-migrations.md). In case of an upgrade failure, you can roll back to an earlier version of {{kib}}. To roll back, you **must** have a [backup snapshot](../../../deploy-manage/tools/snapshot-and-restore.md) that includes the `kibana` feature state. By default, snapshots include the `kibana` feature state.

::::


For more information about upgrading, refer to [Upgrading to Elastic 9.0.0-beta1.](../../../deploy-manage/upgrade/deployment-or-cluster.md)

::::{important}
You can upgrade to pre-release versions for testing, but upgrading from a pre-release to the General Available version is unsupported. You should use pre-release versions only for testing in a temporary environment.
::::



## Upgrading multiple {{kib}} instances [_upgrading_multiple_kib_instances]

When upgrading several {{kib}} instances connected to the same {{es}} cluster, ensure that all outdated instances are shut down before starting the upgrade.

Rolling upgrades are unsupported in {{kib}}. However, when outdated instances are shut down, you can start all upgraded instances in parallel, which allows all instances to participate in the upgrade migration in parallel.

For large deployments with more than 10 {{kib}} instances, and more than 10,000 saved objects, you can reduce the upgrade downtime by bringing up a single {{kib}} instance and waiting for it to complete the upgrade migration before bringing up the remaining instances.


## Preparing for migration [preventing-migration-failures]

Take these extra steps to ensure you are ready for migration.


### Ensure your {{es}} cluster is healthy [_ensure_your_es_cluster_is_healthy]

Problems with your {{es}} cluster can prevent {{kib}} upgrades from succeeding.

During the upgrade process, {{kib}} creates new indices into which updated documents are written. If a cluster is approaching the low watermark, there’s a high risk of {{kib}} not being able to create these. Reading, transforming and writing updated documents can be memory intensive, using more available heap than during routine operation. You must make sure that enough heap is available to prevent requests from timing out or throwing errors from circuit breaker exceptions. You should also ensure that all shards are replicated and assigned.

A healthy cluster has:

* Enough free disk space, at least twice the amount of storage taken up by the `.kibana` and `.kibana_task_manager` indices
* Sufficient heap size
* A "green" cluster status


### Ensure that all {{kib}} instances are the same [_ensure_that_all_kib_instances_are_the_same]

When you perform an upgrade migration of different {{kib}} versions, the migration can fail. Ensure that all {{kib}} instances are running the same version, configuration, and plugins.


### Back up your data [_back_up_your_data]

Be sure to have a [snapshot](../../../deploy-manage/tools/snapshot-and-restore.md) of all your data before attempting a migration. If something goes wrong during migration, you can restore from the snapshot and try again.

Review the [common causes of {{kib}} upgrade failures](../../../troubleshoot/kibana/migration-failures.md) and how to prevent them.
