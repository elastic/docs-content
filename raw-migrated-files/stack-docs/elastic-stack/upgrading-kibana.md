# Upgrade {{kib}} [upgrading-kibana]

::::{warning}
{{kib}} automatically runs saved object migrations when required. To roll back to an earlier version in case of an upgrade failure, you **must** have a [backup snapshot](../../../deploy-manage/tools/snapshot-and-restore.md) that includes the `kibana` feature state. Snapshots include this feature state by default.

For more information, check [Migrate saved objects](../../../deploy-manage/upgrade/internal-upgrade-processes/saved-object-migrations.md).

::::


Before you start, [take the upgrade preparation steps](../../../deploy-manage/upgrade/deployment-or-cluster.md). To upgrade {{kib}}:

1. Shut down all {{kib}} instances. {{kib}} does not support rolling upgrades. **Upgrading while older {{kib}} instances are running can cause data loss or upgrade failures.**
2. To install the `deb` or `rpm` package:

    1. Use `rpm` or `dpkg`. This installs all files in their proper locations and will not overwrite the config files.
    2. Upgrade any plugins by removing the existing plugin and reinstalling the appropriate version using the `kibana-plugin` script. For more information, see [{{kib}} plugins](asciidocalypse://docs/kibana/docs/reference/kibana-plugins.md).

3. To install from a `zip` or `tar.gz` archive:

    1. **Extract the archive to a new directory** to be sure that you don’t overwrite the `config` or `data` directories.
    2. Copy the files from the `config` directory from your old installation to your new installation.
    3. Copy the files from the `data` directory from your old installation to your new installation.

        ::::{important}
        If you use {{monitor-features}}, you must re-use the data directory when you upgrade {{kib}}. Otherwise, the {{kib}} instance is assigned a new persistent UUID and becomes a new instance in the monitoring data.
        ::::

    4. Install the appropriate versions of all your plugins for your new installation using the `kibana-plugin` script. For more information, see [{{kib}} plugins](asciidocalypse://docs/kibana/docs/reference/kibana-plugins.md).

4. Start {{kib}}.

::::{important}
{{kib}} has a new logging system in 8.0 and the log formats have changed. For additional information, see [Logging configuration changes](asciidocalypse://docs/kibana/docs/extend/contribute-to-kibana/logging-config-changes.md).
::::
