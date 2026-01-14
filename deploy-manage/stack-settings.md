---
applies_to:
  deployment:
    ece:
    eck:
    self:
    ess:
navigation_title: Stack settings
products:
   - id: elastic-stack
   - id: elasticsearch
   - id: kibana
---

# Elastic Stack settings

{{stack}} settings allow you to customize {{es}}, {{kib}}, and other {{stack}} products to suit your needs.

:::{admonition} Serverless manages these settings for you
In {{serverless-full}}, cluster-level settings and node-level settings are not required by end users, and are fully managed by Elastic.

Certain [project settings](/deploy-manage/deploy/elastic-cloud/project-settings.md) allow you to customize your project’s performance and general data retention, and enable or disable project features.
:::

## Available settings

The available {{stack}} settings differ depending on your deployment type.

### {{es}} settings

{{es}} settings can be found in the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

| Deployment type | Applicable settings | 
| --- | --- |
| Self managed | All {{es}} settings can be applied to a self-managed cluster. |
| {{ece}}<br><br>{{ech}} | Settings supported on {{ece}} and {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). However, some unmarked settings might also be supported.<br><br>{{ech}} and {{ece}} block the configuration of certain settings that could break your cluster if misconfigured. If a setting is not supported, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported. |
| {{eck}} | Most {{es}} settings can be applied to an ECK-managed {{es}} cluster.<br><br>Some settings are managed by ECK.  It is not recommended to change these managed settings. For a complete list, refer to [Settings managed by ECK](/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck.md). |

### {{kib}} settings

{{kib}} settings can be found in the [{{kib}} configuration reference](kibana://reference/configuration-reference.md).

| Deployment type | Applicable settings | 
| --- | --- |
| Self managed<br><br>{{eck}} | All {{kib}} settings can be applied to a self-managed or ECK instance. |
| {{ece}}<br><br>{{ech}} | Settings supported on {{ece}} and {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). However, some unmarked settings might also be supported.<br><br>{{ech}} and {{ece}} block the configuration of certain settings that could break your cluster if misconfigured. If a setting is not supported, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported. |
| {{eck}} | Most {{es}} settings can be applied to an ECK-managed {{es}} cluster.<br><br>Some settings are managed by ECK.  It is not recommended to change these managed settings. For a complete list, refer to [Settings managed by ECK](/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck.md). |


### Other
 
For APM and Enterprise Search, refer to the product's documentation:

* [APM](/reference/apm/observability/apm-settings.md)
* [Enterprise Search](https://www.elastic.co/guide/en/enterprise-search/8.18/configuration.html)

## Configure {{stack}} settings

The way that you configure your {{stack}} settings is determined by your deployment type.

:::{warning}
* [Dynamic {{es}} cluster settings](#dynamic-cluster-setting) can also be updated using {{es}}'s [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). However, {{ech}} and {{ece}} don’t reject unsafe setting changes made using this API, and should be used with caution in these contexts.
* If a feature requires both standard `elasticsearch.yml` settings and [secure settings](/deploy-manage/security/secure-settings.md), configure the secure settings first. Updating standard user settings can trigger a cluster rolling restart in self managed clusters and ECH and ECE deployments. If the required secure settings are not yet in place, the nodes might fail to start. Adding secure settings does not trigger a restart.
:::

:::::{applies-switch}

::::{applies-item} { ess:, ece: }

For {{ech}} and {{ece}} deployments, you edit {{stack}} settings through the {{ecloud}} Console or ECE Cloud UI. These settings are internally mapped to the appropriate YAML configuration files, such as `elasticsearch.yml` and `kibana.yml`, and they affect all users of that cluster.

{{ech}} and {{ece}} block the configuration of certain settings that could break your cluster if misconfigured. If a setting is not supported, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported.

:::{include} /deploy-manage/_snippets/find-manage-deployment-ech-and-ece.md
:::
4. Under the deployment's name in the navigation menu, select **Edit**.
5. Look for the **Manage user settings and extensions** and **Edit user settings** links for each deployment, and select the one corresponding to the component you want to update, such as {{es}} or {{kib}}.
6. Apply the necessary settings in the **Users Settings** tab of the editor and select **Back** when finished.
7. Select **Save** to apply the changes to the deployment. Saving your changes initiates a configuration plan change that restarts the affected components for you.

For further details and examples, refer to the resource for your deployment type: 

* [{{ech}}](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md)
* [{{ece}}](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md)

::::

::::{applies-item} eck:

Stack settings are defined as part of your resource specification.

#### {{es}}

:::{include} /deploy-manage/deploy/cloud-on-k8s/_snippets/es-config.md
:::

#### {{kib}}

:::{include} /deploy-manage/deploy/cloud-on-k8s/_snippets/kib-config.md
:::

::::

::::{applies-item} self:

The method and location where you can update your {{stack}} settings depends on the component and installation method.

#### Elasticsearch (`elasticsearch.yml`)

Most settings can be changed on a running cluster using the [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API.

You can also set {{es}} settings in `elasticsearch.yml`.  Some settings require a cluster restart. To learn more, refer to [Dynamic and static {{es}} settings](#static-dynamic).

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

If a feature requires both standard `elasticsearch.yml` settings and [secure settings](/deploy-manage/security/secure-settings.md), configure the secure settings first. Updating standard user settings can trigger a cluster rolling restart in self managed clusters and ECH and ECE deployments. If the required secure settings are not yet in place, the nodes might fail to start. Adding secure settings does not trigger a restart.

To learn how to interact with secure settings, refer to [](/deploy-manage/security/secure-settings.md).

## Dynamic and static {{es}} settings [static-dynamic]

{{es}} cluster and node settings can be categorized based on how they are configured:

### Dynamic [dynamic-cluster-setting]

:::{include} /deploy-manage/deploy/self-managed/_snippets/dynamic-settings.md
:::

{{ech}} and {{ece}} don’t reject unsafe setting changes made using this API, and should be used with caution in these contexts.

### Static [static-cluster-setting]

:::{include} /deploy-manage/deploy/self-managed/_snippets/static-settings.md
:::

`elasticsearch.yml` should contain settings which are node-specific (such as `node.name` and paths), or settings which a node requires in order to be able to join a cluster, such as `cluster.name` and `network.host`.