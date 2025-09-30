---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud/current/ec-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configuring-keystore.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-settings.html
  - https://www.elastic.co/guide/en/kibana/current/secure-settings.html
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
products:
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: elasticsearch
  - id: kibana
---

# Secure your settings

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. For this use case, {{es}} and {{kib}} provide secure keystores to store sensitive configuration values such as passwords, API keys, and tokens.

Secure settings are often referred to as **keystore settings**, since they must be added to the product-specific keystore rather than the standard [`elasticsearch.yml` or `kibana.yml` files](/deploy-manage/stack-settings.md). Unlike regular settings, they are encrypted and protected at rest, and they cannot be read or modified through the usual configuration files or environment variables.

Keystore settings must be handled using a specific tool or method depending on the deployment type. The following table summarizes how {{es}} and {{kib}} keystores are supported and managed across different deployment models:

| Deployment Type      | {{es}} keystore configuration             | {{kib}} keystore configuration         |
|----------------------|--------------------------------------------|----------------------------------------|
| {{serverless-full}}              | Not available                                  | Not available                          |
| {{ech}}              | Cloud UI                                  | Not available                          |
| {{ece}}              | Cloud UI or API                                  | Not available                          |
| {{eck}}              | Kubernetes secrets    | Kubernetes secrets                   |
| Self-managed         | Manual configuration with [`elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) | Manual configuration with `kibana-keystore` |

This section describes how to configure and manage secure settings in each keystore depending on the deployment model:
* [{{es}} secure settings](./secure-settings.md#elasticsearch)
* [{{kib}} secure settings](./secure-settings.md#kibana)

:::{tip}
For information about the APM keystore, refer to [](/solutions/observability/apm/apm-server/secrets-keystore-for-secure-settings.md).
:::

## {{es}} secure settings [elasticsearch]

The {{es}} keystore has some important characteristics and limitations to be aware of:

* **Only specific settings are allowed**: The keystore accepts only settings marked as *secure* in the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md). Adding unsupported settings to the keystore causes the validation in the [`reload_secure_settings` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) to fail and can also prevent {{es}} from starting.
* **Mandatory for secure settings**: Settings marked as secure must be added to the keystore. They cannot be placed in `elasticsearch.yml` or set using environment variables. This differs from the {{kib}} keystore, which supports all settings.
* **Changes require a restart**: Most secure settings take effect only after restarting the nodes. However, some are marked as *reloadable* and can be updated without a restart using the [`reload_secure_settings`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API. Refer to [Reloadable settings](#reloadable-secure-settings) for more information.
* **Keystore is per-node**: Each node in the cluster has its own keystore file. Secure settings must be specified individually on every node and must have the same values across the cluster. Orchestrated deployments, such as ECH, ECE, and ECK, handle this automatically when configuring secure settings.

::::{tip}
To check whether a setting can be added to the keystore and supports reloading without a restart, look for the `Secure` and `Reloadable` qualifiers in the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

For example, you can search for `secure_bind_password` in the [security settings document](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md) to see how these qualifiers appear in context.
::::

The instructions below cover how to manage {{es}} keystore settings for each deployment type.

:::::{tab-set}
:group: deployment-type

::::{tab-item} ECH and ECE
:sync: cloud
% ### ECE and ECH
You can manage {{es}} secure settings in the **Security > {{es}} keystore** section of your deployment page in the {{ecloud}} Console or ECE Cloud UI.

If a feature requires both standard `elasticsearch.yml` settings and secure settings, configure the secure settings first. Updating standard settings can trigger a cluster rolling restart, and if the required secure settings are not yet in place, the nodes may fail to start. In contrast, adding secure settings does not trigger a restart.

:::{note}
{{ece}} also supports managing {{es}} keystore of your deployments through its [RESTful API](https://www.elastic.co/docs/api/doc/cloud-enterprise/). Refer to [Configure {{es}} keystore through ECE API](cloud://reference/cloud-enterprise/ece-restful-api-examples-configuring-keystore.md) for an example.
:::

There are three input formats you can use for secure setting values:

* **Single string**: Associate a secret value to a setting.
* **Multiple strings**: A group of key-value pairs, each stored as part of the setting's value.
* **JSON block/file**: A structured JSON object containing multiple key-value pairs, typically used for more complex secrets like service account credentials.

#### Add secure settings [ec-add-secret-values]

Add settings and secret values to the keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) or [ECE Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Find your deployment and select **Manage**.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, select **Security**.
4. Locate **{{es}} keystore** and select **Add settings**.
5. On the **Create setting** window, select the secret **Type**.
6. Configure the settings, then select **Save**.

    :::{important}
    All modifications to the non-reloadable settings take effect only after restarting {{es}}. [Reloadable](#reloadable-secure-settings) keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request. Adding unsupported settings to the keystore will cause {{es}} to fail to start.
    :::

#### Remove secure settings

When your secure settings are no longer needed, delete them from the keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) or [ECE Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Find your deployment and select **Manage**.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, select **Security**.
4. From the **Existing keystores** list, use the delete icon next to setting that you want to delete.
5. On the **Confirm to delete** window, select **Confirm**.
::::

::::{tab-item} ECK
:sync: eck
% ### ECK
In ECK, the operator simplifies secure settings configuration by relying on Kubernetes secrets.

Refer to [Configure secure settings on ECK](./k8s-secure-settings.md) for details and examples.
::::

::::{tab-item} Self-managed
:sync: self-managed
% ### Self-managed
In self-managed deployments, you're responsible for configuring and maintaining the {{es}} keystore on each node individually.

{{es}} provides the [`elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) command-line tool to help with this task. It allows you to list, add, remove, and update secure settings, as well as protect the keystore with a password if wanted.

For docker examples, refer to [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md#docker-keystore-bind-mount).

:::{important}
Secure settings must be specified on every node, and must have the same values across the cluster to ensure consistent behavior.

Changes to the keystore take effect only after restarting {{es}}, except for [reloadable settings](#reloadable-secure-settings) that can be refreshed using the API.
:::

#### Create the keystore [creating-keystore]

To create the {{es}} keystore, use the `create` command:

```sh
bin/elasticsearch-keystore create -p
```

You are prompted to enter a keystore password, but setting one is optional. If you press Enter without typing a password, the keystore file will be created without password protection.

The command creates a file named `elasticsearch.keystore` alongside the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file.

#### List settings in the keystore

To list the settings in the keystore, use the `list` command.

```sh
bin/elasticsearch-keystore list
```
If the {{es}} keystore is password protected, you are prompted to enter the password.

#### Add secure settings to the keystore

Sensitive string settings, like authentication credentials for Cloud plugins, can be added with the `add` command:

```sh
bin/elasticsearch-keystore add the.setting.name.to.set
```

You are prompted to enter the value of the setting. If the {{es}} keystore is password protected, you are also prompted to enter the password.

#### Remove secure settings from the keystore

To remove a setting from the keystore, use the `remove` command:

```sh
bin/elasticsearch-keystore remove the.setting.name.to.remove
```

If the {{es}} keystore is password protected, you are prompted to enter the password.

#### Other examples [change-password]

For a full command reference and additional examples, such as displaying stored values or adding entire files as setting values, refer to the [`elasticsearch-keystore` tool documentation](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md).

::::

:::::

### Reloadable secure settings [reloadable-secure-settings]

Just like the settings values in `elasticsearch.yml`, changes to the keystore contents are not automatically applied to the running {{es}} node. Re-reading settings requires a node restart.

However, certain secure settings are marked as `Reloadable` in [{{es}} reference documentation](elasticsearch://reference/elasticsearch/configuration-reference/index.md). Such settings can be re-read and applied on a running node by using the [reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings).

The values of all secure settings, whether reloadable or not, must be identical across all nodes. After making the desired changes, call the following endpoint. If your keystore is password-protected, include the `secure_settings_password` parameter:

```console
POST _nodes/reload_secure_settings
{
  "secure_settings_password": "keystore-password" <1>
}
```
1. Only required if the {{es}} keystore is password-protected.

This API decrypts, re-reads the entire keystore and validates all settings on every cluster node, but only the reloadable secure settings are applied. Changes to other settings do not go into effect until the next restart. Once the call returns, the reload has been completed, meaning that all internal data structures dependent on these settings have been changed. Everything should look as if the settings had the new value from the start.

::::{tip}
When changing multiple reloadable secure settings, modify all of them on each cluster node, then issue a [`reload_secure_settings`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) call instead of reloading after each modification.
::::

Reloadable secure settings are available for snapshot repository plugins, watcher, monitoring, and certain authentication realms. Refer to the relevant documentation for each feature to see if secure settings can be reloaded.

## {{kib}} secure settings [kibana]
```{applies_to}
deployment:
  self: ga
  eck: ga
```

{{kib}} supports secure settings through its own keystore, similar to the {{es}} keystore. It provides a way to protect sensitive configuration values, such as authentication credentials or encryption keys, by storing them securely outside of [`kibana.yml`](/deploy-manage/stack-settings.md).

::::{note}
Unlike with {{es}} keystore, any valid {{kib}} setting can be stored securely in the keystore. However, as with {{es}}, adding invalid, unsupported, or extraneous settings will cause {{kib}} to fail to start. Always ensure the setting exists and is properly formatted in the [configuration reference](kibana://reference/configuration-reference.md) before adding it to the keystore.
::::

This section provides examples of {{kib}} secure settings handling using the `kibana-keystore` command-line tool for self-managed deployments.

For ECK deployments, the configuration process is similar to {{es}} and is documented in the [{{kib}} secure settings section for ECK](./k8s-secure-settings.md#k8s-kibana-secure-settings).

::::{important}
In the following examples, run all commands as the user who runs {{kib}}.
::::

### Create the keystore [creating-keystore]

To create the `kibana.keystore`, use the `create` command:

```sh
bin/kibana-keystore create
```

The file `kibana.keystore` will be created in the `config` directory defined by the environment variable `KBN_PATH_CONF`.

To create a password protected keystore use the `--password` flag. Setting a password is optional.


### List settings in the keystore [list-settings]

A list of the settings in the keystore is available with the `list` command:

```sh
bin/kibana-keystore list
```


### Add string settings [add-string-to-keystore]

::::{note}
Your input will be JSON-parsed to allow for object/array input configurations. To enforce string values, use "double quotes" around your input.
::::


Sensitive string settings, like authentication credentials for {{es}} can be added using the `add` command:

```sh
bin/kibana-keystore add the.setting.name.to.set
```

Once added to the keystore, these setting will be automatically applied to this instance of {{kib}} when started. For example if you do

```sh
bin/kibana-keystore add elasticsearch.username
```

you will be prompted to provide the value for elasticsearch.username. (Your input will show as asterisks.)

The tool will prompt for the value of the setting. To pass the value through stdin, use the `--stdin` flag:

```sh
cat /file/containing/setting/value | bin/kibana-keystore add the.setting.name.to.set --stdin
```


### Remove settings [remove-settings]

To remove a setting from the keystore, use the `remove` command:

```sh
bin/kibana-keystore remove the.setting.name.to.remove
```


### Read settings [read-settings]

To display the configured setting values, use the `show` command:

```sh
bin/kibana-keystore show setting.key
```


### Change password [change-password]

To change the password of the keystore, use the `passwd` command:

```sh
bin/kibana-keystore passwd
```

### Has password [has-password]

To check if the keystore is password protected, use the `has-passwd` command. An exit code of 0 will be returned if the keystore is password protected, and the command will fail otherwise.

```sh
bin/kibana-keystore has-passwd
```

