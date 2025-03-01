# Secure settings [secure-settings]

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. For this use case, {{es}} provides a keystore and the [`elasticsearch-keystore` tool](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) to manage the settings in the keystore.

::::{important}
Only some settings are designed to be read from the keystore. Adding unsupported settings to the keystore causes the validation in the `_nodes/reload_secure_settings` API to fail and if not addressed, will cause {{es}} to fail to start. To see whether a setting is supported in the keystore, look for a "Secure" qualifier in the setting reference.
::::


All the modifications to the keystore take effect only after restarting {{es}}.

These settings, just like the regular ones in the `elasticsearch.yml` config file, need to be specified on each node in the cluster. Currently, all secure settings are node-specific settings that must have the same value on every node.


## Reloadable secure settings [reloadable-secure-settings]

Just like the settings values in `elasticsearch.yml`, changes to the keystore contents are not automatically applied to the running {{es}} node. Re-reading settings requires a node restart. However, certain secure settings are marked as **reloadable**. Such settings can be re-read and applied on a running node.

You can define these settings before the node is started, or call the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) after the settings are defined to apply them to a running node.

The values of all secure settings, **reloadable** or not, must be identical across all cluster nodes. After making the desired secure settings changes, using the `bin/elasticsearch-keystore add` command, call:

```console
POST _nodes/reload_secure_settings
{
  "secure_settings_password": "keystore-password" <1>
}
```

1. The password that the {{es}} keystore is encrypted with.


This API decrypts, re-reads the entire keystore and validates all settings on every cluster node, but only the **reloadable** secure settings are applied. Changes to other settings do not go into effect until the next restart. Once the call returns, the reload has been completed, meaning that all internal data structures dependent on these settings have been changed. Everything should look as if the settings had the new value from the start.

When changing multiple **reloadable** secure settings, modify all of them on each cluster node, then issue a [`reload_secure_settings`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) call instead of reloading after each modification.

There are reloadable secure settings for:

* [The Azure repository plugin](../../../deploy-manage/tools/snapshot-and-restore/azure-repository.md)
* [The EC2 discovery plugin](elasticsearch://reference/elasticsearch-plugins/discovery-ec2-usage.md#_configuring_ec2_discovery)
* [The GCS repository plugin](../../../deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md)
* [The S3 repository plugin](../../../deploy-manage/tools/snapshot-and-restore/s3-repository.md)
* [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md)
* [{{watcher}} settings](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md)
* [JWT realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-jwt-settings)
* [Active Directory realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings)
* [LDAP realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings)
* [Remote cluster credentials for the API key based security model](../../../deploy-manage/remote-clusters/remote-clusters-settings.md#remote-cluster-credentials-setting)

