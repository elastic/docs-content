---
applies_to:
  deployment:
    ece:
    eck:
    self:
    ess:
navigation_title: "Stack settings"
---

# Elastic Stack settings

<!--
## cloud hosted
https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/edit-stack-settings

## cloud enterprise
https://www.elastic.co/docs/deploy-manage/deploy/cloud-enterprise/edit-stack-settings

## eck
https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/node-configuration
https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck
https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-advanced-configuration#k8s-kibana-configuration

## self
https://www.elastic.co/docs/deploy-manage/deploy/self-managed/configure-elasticsearch
https://www.elastic.co/docs/deploy-manage/deploy/self-managed/configure-kibana
-->

{{stack}} settings allow you to customize {{es}}, {{kib}}, and other {{stack}} products to suit your needs. 

## Available settings

The available {{stack}} settings differ depending on your deployment type.

### {{es}} settings

For a complete list of settings that you can apply to your {{es}} cluster, refer to the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

Settings supported on {{ece}} and {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). 
However, some unmarked settings might be supported on {{ece}}. 

{{ech}} and {{ece}} block the configuration of certain settings that could break your cluster if misconfigured. If a setting is not supported, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported.

### {{kib}} settings

{{ech}} supports most of the standard {{kib}} settings. 

Be aware that some settings that could break your cluster if set incorrectly and that the syntax might change between major versions.

Settings supported on {{ece}} and {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). 
However, some unmarked settings might be supported on {{ece}}. 

Some settings are managed by ECK, it is not recommended to change them, refer to [Settings managed by ECK](settings-managed-by-eck.md) for more details.

### Other
 
For APM and Enterprise Search, refer to the product's documentation:

* [APM](/reference/apm/observability/apm-settings.md)
* [Enterprise Search](https://www.elastic.co/guide/en/enterprise-search/8.18/configuration.html)

## Configure {{stack}} settings

The way that you configure your {{stack}} settings is determined by your deployment type.

:::{warning}
You can also update [dynamic {{es}} cluster settings](#dynamic-cluster-settings) using {{es}}'s [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). However, {{ech}} and {{ece}} don’t reject unsafe setting changes made using this API, and should be used with caution in these contexts.
:::

:::::{tab-set}

::::{tab-item} ECH and ECE

For {{ech}} and {{ece}} deployments, you edit {{stack}} settings through the {{ecloud}} Console or ECE Cloud UI. These settings are internally mapped to the appropriate YAML configuration files, such as `elasticsearch.yml` and `kibana.yml`, and they affect all users of that cluster.

{{ech}} and {{ece}} block the configuration of certain settings that could break your cluster if misconfigured. If a setting is not supported, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported.

:::{include} /deploy-manage/_snippets/find-manage-deployment-ech-and-ece.md
:::
1. Under the deployment's name in the navigation menu, select **Edit**.
2. Look for the **Manage user settings and extensions** and **Edit user settings** links for each deployment, and select the one corresponding to the component you want to update, such as {{es}} or {{kib}}.
3. Apply the necessary settings in the **Users Settings** tab of the editor and select **Back** when finished.
4. Select **Save** to apply the changes to the deployment. Saving your changes initiates a configuration plan change that restarts the affected components for you.

For further details and examples, refer to the resource for your deployment type: 

* [{{ech}}](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md)
* [{{ece}}](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md)

::::

::::{tab-item} ECK

Stack settings are defined as part of your resource specification.

#### {{es}}

:::{include} /deploy-manage/deploy/cloud-on-k8s/_snippets/es-config.md
:::

#### {{kib}}

:::{include} /deploy-manage/deploy/cloud-on-k8s/_snippets/kib-config.md
:::

::::

::::{tab-item} Self managed

The method and location where you can update your {{stack}} settings depends on the component and installation method.

#### Elasticsearch (`elasticsearch.yml`)

Most settings can be changed on a running cluster using the [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API.

You can also set {{es}} settings in `elasticsearch.yml`.  Some settings require a cluster restart. To learn more, refer to [Static vs. dynamic {{es}} settings](#static-dynamic).

To learn more about configuring {{es}} in a self-managed environment, refer to [](/deploy-manage/deploy/self-managed/configure-elasticsearch.md).

| Installation method | Default location |
| --- | --- |
| Archive distribution (`tar.gz` or `zip`) | `$ES_HOME/config` ([override](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#archive-distributions)) |
| Package distribution (Debian or RPM) | `/etc/elasticsearch` ([override](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#package-distributions)) |
| Docker | `/usr/share/elasticsearch/config/` ([Learn more](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md)) |

#### Kibana (`kibana.yml`)

To learn more about configuring {{kib}} in a self-managed environment, refer to [](/deploy-manage/deploy/self-managed/configure-kibana.md).

| Installation method | Default location |
| --- | --- |
| Archive distribution (`tar.gz` or `zip`) | `$KIBANA_HOME/config` ([override](/deploy-manage/deploy/self-managed/configure-kibana.md)) |
| Package distribution (Debian or RPM) | `/etc/kibana` ([override](/deploy-manage/deploy/self-managed/configure-kibana.md)) |
| Docker | `/usr/share/kibana/config/` ([Learn more](/deploy-manage/deploy/self-managed/configure-kibana.md)) |

#### Other

For APM and Enterprise Search, refer to the product's documentation:

* [APM](/reference/apm/observability/apm-settings.md)
* [Enterprise Search](https://www.elastic.co/guide/en/enterprise-search/8.18/configuration.html)

#### Config file format

:::{include} /deploy-manage/deploy/self-managed/_snippets/config-file-format.md
:::

#### Environment variable substitution

:::{include} /deploy-manage/deploy/self-managed/_snippets/env-var-setting-subs.md
:::

::::

:::::

## Secure your settings

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. For this use case, {{es}} and {{kib}} provide secure keystores to store sensitive configuration values such as passwords, API keys, and tokens.

Secure settings are often referred to as **keystore settings**, since they must be added to the product-specific keystore rather than the standard `elasticsearch.yml` or `kibana.yml` files. Unlike regular settings, they are encrypted and protected at rest, and they cannot be read or modified through the usual configuration files or environment variables.

To learn how to interact with secure settings, refer to [](/deploy-manage/security/secure-settings.md).

## Static vs. dynamic {{es}} settings [static-dynamic]

{{es}} cluster and node settings can be categorized based on how they are configured:

### Dynamic [dynamic-cluster-setting]

:::{include} /deploy-manage/deploy/self-managed/_snippets/dynamic-settings.md
:::

{{ech}} and {{ece}} don’t reject unsafe setting changes made using this API, and should be used with caution in these contexts.

### Static [static-cluster-setting]

:::{include} /deploy-manage/deploy/self-managed/_snippets/static-settings.md
:::

`elasticsearch.yml` should contain settings which are node-specific (such as `node.name` and paths), or settings which a node requires in order to be able to join a cluster, such as `cluster.name` and `network.host`.