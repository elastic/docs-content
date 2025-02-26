---
navigation_title: "Node bootlooping"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-config-change-errors.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-config-change-errors.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-config-change-errors.html
---

# Troubleshoot node bootlooping [ec-config-change-errors]

When you attempt to apply a configuration change to a deployment, the attempt may fail with an error indicating that the change could not be applied, and deployment resources may be unable to restart. In some cases, bootlooping may result, where the deployment resources cycle through a continual reboot process.

:::{image} /images/cloud-ec-ce-configuration-change-failure.png
:alt: A screen capture of the deployment page showing an error: Latest change to {{es}} configuration failed.
:::

To help diagnose these and any other types of issues in your deployments, we recommend [setting up monitoring](/deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md). Then, you can easily view your deployment health and access log files to troubleshoot this configuration failure.

To confirm if your Elasticsearch cluster is bootlooping, you can check the most recent plan under your [Deployment Activity page](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) for the error:

```sh
Plan change failed: Some instances were unable to start properly.
```

If this occurs, correlating {{es}} logs should report:

```sh
fatal exception while booting Elasticsearch
```

Following are some frequent causes of a failed configuration change:

1. [Secure settings](/troubleshoot/monitoring/node-bootlooping.md#ec-config-change-errors-secure-settings)
2. [Expired custom plugins or bundles](/troubleshoot/monitoring/node-bootlooping.md#ec-config-change-errors-expired-bundle-extension)
3. [OOM errors](/troubleshoot/monitoring/node-bootlooping.md#ec-config-change-errors-oom-errors)
4. [Existing index](/troubleshoot/monitoring/node-bootlooping.md#ec-config-change-errors-existing-index)
5. [Insufficient Storage](/troubleshoot/monitoring/node-bootlooping.md#ec-config-change-errors-insufficient-storage)

If you’re unable to remediate the failing plan’s root cause, you can attempt to reset the deployment to the latest successful {{es}} configuration by performing a [no-op plan](/troubleshoot/monitoring/deployment-health-warnings.md). For an example, see this [video walkthrough](https://www.youtube.com/watch?v=8MnXZ9egBbQ).


## Secure settings [ec-config-change-errors-secure-settings]

The most frequent cause of a failed deployment configuration change is due to invalid or mislocated [secure settings](/deploy-manage/security/secure-settings.md). This can frequently be discovered by searching {{es}} logs for one of the following error messages:

```sh
IllegalStateException: security initialization failed
java.lang.IllegalArgumentException: unknown secure setting
```

These are settings typically added to the keystore for the purpose of:

1. Setting up third-party authentication, for example [SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md), [OpenID Connect](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md).
2. Setting up a [custom repository](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md).

The keystore allows you to safely store sensitive settings, such as passwords, as a key/value pair. You can then access a secret value from a settings file by referencing its key. Importantly, not all settings can be stored in the keystore, and the keystore does not validate the settings that you add. Adding unsupported settings can cause {{es}} or other components to fail to restart. To check whether a setting is supported in the keystore, look for a "Secure" qualifier in the [lists of reloadable settings](/deploy-manage/security/secure-settings.md).

The following sections detail some secure settings problems that can result in a configuration change error that can prevent a deployment from restarting. You might diagnose these plan failures via the logs or via their [related exit codes](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#fatal-errors) `1`, `3`, and `78`.


### Invalid or outdated values [ec-config-change-errors-old-values]

The keystore does not validate any settings that you add, so invalid or outdated values are a common source of errors when you apply a configuration change to a deployment.

To check the current set of stored settings:

1. Open the deployment **Security** page.
2. In the **{{es}} keystore** section, check the **Security keys** list. The list is shown only if you currently have settings configured in the keystore.

One frequent cause of errors is when settings in the keystore are no longer valid, such as when SAML settings are added for a test environment, but the settings are either not carried over or no longer valid in a production environment.


### Snapshot repositories [ec-config-change-errors-snapshot-repos]

Sometimes, settings added to the keystore to connect to a snapshot repository may not be valid. When this happens, you may get an error such as `SettingsException[Neither a secret key nor a shared access token was set.]`

For example, when adding an [Azure repository storage setting](/deploy-manage/tools/snapshot-and-restore/azure-repository.md#repository-azure-usage) such as `azure.client.default.account` to the keystore, the associated setting `azure.client.default.key` must also be added for the configuration to be valid.


### Third-party authentication [ec-config-change-errors-third-party-auth]

When you configure third-party authentication, it’s important that all required configuration elements that are stored in the keystore are included in the {{es}} user settings file. For example, when you [create a SAML realm](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-create-realm), omitting a field such as `idp.entity_id` when that setting is present in the keystore results in a failed configuration change.


### Wrong location [ec-config-change-errors-wrong-location]

In some cases, settings may accidentally be added to the keystore that should have been added to the [{{es}} user settings file](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md). It’s always a good idea to check the [lists of reloadable settings](/deploy-manage/security/secure-settings.md) to determine if a setting can be stored in the keystore. Settings that can safely be added to the keystore are flagged as `Secure`.


## Expired custom plugins or bundles [ec-config-change-errors-expired-bundle-extension]

During the process of applying a configuration change, {{ecloud}} checks to determine if any [uploaded custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) are expired.

Problematic plugins produce oscillating {{es}} start-up logs like the following:

```sh
Booting at Sun Sep 4 03:06:43 UTC 2022
Installing user plugins.
Installing elasticsearch-analysis-izumo-master-7.10.2-20210618-28f8a97...
/app/elasticsearch.sh: line 169: [: too many arguments
Booting at Sun Sep 4 03:06:58 UTC 2022
Installing user plugins.
Installing elasticsearch-analysis-izumo-master-7.10.2-20210618-28f8a97...
/app/elasticsearch.sh: line 169: [: too many arguments
```

Problematic bundles produce similar oscillations but their install log would appear like

```sh
2024-11-17 15:18:02   https://found-user-plugins.s3.amazonaws.com/XXXXX/XXXXX.zip?response-content-disposition=attachment%3Bfilename%XXXXX%2F4007535947.zip&x-elastic-extension-version=1574194077471&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20241016T133214Z&X-Amz-SignedHeaders=host&X-Amz-Expires=86400&XAmz-Credential=XXXXX%2F20201016%2Fus-east-1%2Fs3%2Faws4_request&X-AmzSignature=XXXXX
```

Noting in example that the bundle’s expiration `X-Amz-Date=20241016T133214Z` is before than the log timestamp `2024-11-17 15:18:02` so this bundle is considered expired.

To view any added plugins or bundles:

1. Go to the **Features** page and open the **Extensions** tab.
2. Select any extension and then choose **Update extension** to renew it. No other changes are needed, and any associated configuration change failures should now be able to succeed.


## OOM errors [ec-config-change-errors-oom-errors]

Configuration change errors can occur when there is insufficient RAM configured for a data tier. In this case, the cluster typically also shows OOM (out of memory) errors. To resolve these, you need to increase the amount of heap memory, which is half of the amount of memory allocated to a cluster. You might also detect OOM in plan changes via their [related exit codes](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#fatal-errors) `127`, `137`, and `158`.

Check the [{{es}} cluster size](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md#ec-cluster-size) and the [JVM memory pressure indicator](/deploy-manage/monitor/monitoring-data/ec-memory-pressure.md) documentation to learn more.

As well, you can read our detailed blog [Managing and troubleshooting {{es}} memory](https://www.elastic.co/blog/managing-and-troubleshooting-elasticsearch-memory).


## Existing index [ec-config-change-errors-existing-index]

In rare cases, when you attempt to upgrade the version of a deployment and the upgrade fails on the first attempt, subsequent attempts to upgrade may fail due to already existing resources. The problem may be due to the system preventing itself from overwriting existing indices, resulting in an error such as this: `Another Kibana instance appears to be migrating the index. Waiting for that migration to complete. If no other Kibana instance is attempting migrations, you can get past this message by deleting index .kibana_2 and restarting Kibana`.

To resolve this:

1. Check that you don’t need the content.
2. Run an {{es}} [Delete index request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete) to remove the existing index.

    In this example, the `.kibana_2` index is the rollover of saved objects (such as Kibana visualizations or dashboards) from the original `.kibana_1` index. Since `.kibana_2` was created as part of the failed upgrade process, this index does not yet contain any pertinent data and it can safely be deleted.

3. Retry the deployment configuration change.


## Insufficient Storage [ec-config-change-errors-insufficient-storage]

Configuration change errors can occur when there is insufficient disk space for a data tier. To resolve this, you need to increase the size of that tier to ensure it provides enough storage to accommodate the data in your cluster tier considering the [high watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation). For troubleshooting walkthrough, see [Fix watermark errors](/troubleshoot/elasticsearch/fix-watermark-errors.md).