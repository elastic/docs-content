---
applies_to:
  deployment:
    self: ga
products:
  - id: kibana
---

# Upgrade {{kib}} [upgrade-kibana]

When you upgrade {{kib}}, you also upgrade the {{observability}} and {{elastic-sec}} solutions, which use {{kib}} as their main interface.

{{kib}} must always be upgraded after {{es}}, and to the same version. Version mismatches or upgrading in the wrong order can result in failures or unexpected behavior.

::::{warning}
{{kib}} automatically runs saved object migrations when required. To roll back to an earlier version in case of an upgrade failure, you **must** have a [backup snapshot](../../tools/snapshot-and-restore.md) that includes the `kibana` feature state. Snapshots include this feature state by default.

For more information, refer to [Migrate saved objects](saved-object-migrations.md).
::::

## Upgrading multiple {{kib}} instances [_upgrading_multiple_kib_instances]

When upgrading several {{kib}} instances connected to the same {{es}} cluster, ensure that all outdated instances are shut down before starting the upgrade.

Rolling upgrades are unsupported in {{kib}}. However, when outdated instances are shut down, you can start all upgraded instances in parallel, which allows all instances to participate in the upgrade in parallel.

For large deployments with more than 10 {{kib}} instances, and more than 10,000 saved objects, you can reduce the upgrade downtime by bringing up a single {{kib}} instance and waiting for it to complete the upgrade before bringing up the remaining instances.

## Preparing for upgrading [preventing-migration-failures]

Before you start, ensure that you’ve followed the [Plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md) guidelines, completed the [upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md), and [upgraded the {{es}} cluster](./elasticsearch.md).

### Ensure your {{es}} cluster is healthy [_ensure_your_es_cluster_is_healthy]

Problems with your {{es}} cluster can prevent {{kib}} upgrades from succeeding.

During the upgrade process, {{kib}} creates new indices into which updated documents are written. If a cluster is approaching the low watermark, there’s a high risk of {{kib}} not being able to create these. Reading, transforming and writing updated documents can be memory intensive, using more available heap than during routine operation. You must make sure that enough heap is available to prevent requests from timing out or throwing errors from circuit breaker exceptions. You should also ensure that all shards are replicated and assigned.

A healthy cluster has:

* Enough free disk space, at least twice the amount of storage taken up by the `.kibana` and `.kibana_task_manager` indices
* Sufficient heap size
* A "green" cluster status


### Ensure that all {{kib}} instances are the same [_ensure_that_all_kib_instances_are_the_same]

When you perform an upgrade of different {{kib}} versions, the upgrade can fail. Ensure that all {{kib}} instances are running the same version, configuration, and plugins.

## Perform the upgrade [perform-kibana-upgrade]

To upgrade {{kib}}:

1. Shut down all {{kib}} instances. {{kib}} does not support rolling upgrades. **Upgrading while older {{kib}} instances are running can cause data loss or upgrade failures.**
2. To install the `deb` or `rpm` package:
    1. Use `rpm` or `dpkg`. This installs all files in their proper locations and will not overwrite the config files.
    2. Upgrade any plugins by removing the existing plugin and reinstalling the appropriate version using the `kibana-plugin` script. For more information, refer to [{{kib}} plugins](kibana://reference/kibana-plugins.md).

3. To install from a `zip` or `tar.gz` archive:

    1. **Extract the archive to a new directory** to be sure that you don’t overwrite the `config` or `data` directories.
    2. Copy the files from the `config` directory from your old installation to your new installation.
    3. Copy the files from the `data` directory from your old installation to your new installation.

    ::::{important}
    If you use {{monitor-features}}, you must re-use the data directory when you upgrade {{kib}}. Otherwise, the {{kib}} instance is assigned a new persistent UUID and becomes a new instance in the monitoring data.
    ::::

    4. Install the appropriate versions of all your plugins for your new installation using the `kibana-plugin` script. For more information, refer to [{{kib}} plugins](kibana://reference/kibana-plugins.md).

4. Start {{kib}}.

::::{note}
{{kib}} 8.0.0 and later uses a new logging system, so the log formats have changed. For additional information, refer to [Logging configuration changes](kibana://extend/logging-config-changes.md).
::::

## Next steps

Once you've successfully upgraded {{kib}}, [upgrade Elastic APM](/solutions/observability/apm/upgrade.md), then [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md).