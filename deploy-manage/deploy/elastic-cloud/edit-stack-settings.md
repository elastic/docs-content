---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html
  - https://www.elastic.co/guide/en/cloud/current/ec-editing-user-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-add-user-settings.html
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-manage-kibana-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-editing-user-settings.html
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-apm-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-manage-apm-settings.html
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-appsearch-settings.html
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-enterprise-search-settings.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Edit {{stack}} settings

From the {{ecloud}} Console you can customize {{es}}, {{kib}}, and related products to suit your needs. These editors append your changes to the appropriate YAML configuration file and they affect all users of that cluster.

## Available settings

### Elasticsearch settings

:::{important}
If a feature requires both standard `elasticsearch.yml` settings and [secure settings](/deploy-manage/security/secure-settings.md), configure the secure settings first. Updating standard user settings can trigger a cluster rolling restart, and if the required secure settings are not yet in place, the nodes may fail to start. In contrast, adding secure settings does not trigger a restart.
:::

{{ech}} automatically rejects `elasticsearch.yml` settings that could break your cluster.

For a list of supported settings, refer to the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md). Settings supported on {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")).

### Kibana settings

{{ech}} supports most of the standard {{kib}} settings.

Be aware that some settings that could break your cluster if set incorrectly and that the syntax might change between major versions.

For a list of supported settings, check [{{kib}} settings](kibana://reference/cloud/elastic-cloud-kibana-settings.md).

### APM settings

Refer to [APM configuration reference](/solutions/observability/apm/apm-server/configure.md) for information on how to configure the {{fleet}}-managed APM integration.

## Edit settings [ec-add-user-settings]

To add or edit user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

1. Under the deployment's name in the navigation menu, select **Edit**.
2. Look for the **Manage user settings and extensions** and **Edit user settings** links for each deployment, and select the one corresponding to the component you want to update, such as {{es}} or {{kib}}.
3. Apply the necessary settings in the **Users Settings** tab of the editor and select **Back** when finished.
4. Select **Save** to apply the changes to the deployment. Saving your changes initiates a configuration plan change that restarts the affected components for you.

::::{note}
In some cases, you may get a warning saying "User settings are different across {{es}} instances". To fix this issue, ensure that your user settings (including the comments sections and whitespaces) are identical across all {{es}} nodes (not only the data tiers, but also the Master, Machine Learning, and Coordinating nodes).
::::

::::{warning}
You can also update [dynamic cluster settings](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting) using {{es}}'s [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). However, {{ech}} doesn’t reject unsafe setting changes made using this API. Use it with caution.
::::