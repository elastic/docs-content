---
applies_to:
  deployment:
    ess: ga
mapped_urls:
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
---

# Edit {{stack}} settings

% What needs to be done: Refine

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud/ec-add-user-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-editing-user-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-add-user-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-manage-kibana-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-manage-kibana-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-editing-user-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-manage-apm-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-manage-apm-settings.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-manage-appsearch-settings.md
%      Notes: specify cluster 8.x or lower
% - [ ] ./raw-migrated-files/cloud/cloud/ec-manage-enterprise-search-settings.md
%      Notes: specify cluster 8.x or lower

$$$ec-add-user-settings$$$

$$$ech-es-elasticsearch-settings$$$

$$$xpack-monitoring-history-duration$$$

$$$ech-edit-apm-standalone-settings$$$

$$$ech-apm-settings$$$

$$$csp-strict$$$

$$$ec-appsearch-settings$$$

$$$ec-es-elasticsearch-settings$$$

From the {{ecloud}} Console you can customize {{es}}, {{kib}}, and related products to suit your needs. These editors append your changes to the appropriate YAML configuration file and they affect all users of that cluster. In each editor you can:


## Edit {{es}} user settings [ec-add-user-settings]

Change how {{es}} runs by providing your own user settings. {{ech}} appends these settings to each node’s `elasticsearch.yml` configuration file.

{{ech}} automatically rejects `elasticsearch.yml` settings that could break your cluster. 

For a list of supported settings, check [Supported {{es}} settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/elastic-cloud-hosted-elasticsearch-settings.md).

::::{warning}
You can also update [dynamic cluster settings](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting) using {{es}}'s [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). However, {{ech}} doesn’t reject unsafe setting changes made using this API. Use it with caution.
::::


To add or edit user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Manage user settings and extensions**.
5. Update the user settings.
6. Select **Save changes**.

::::{note}
In some cases, you may get a warning saying "User settings are different across Elasticsearch instances". To fix this issue, ensure that your user settings (including the comments sections and whitespaces) are identical across all Elasticsearch nodes (not only the data tiers, but also the Master, Machine Learning, and Coordinating nodes).
::::

## Edit Kibana user settings [ec-manage-kibana-settings]

{{ech}} supports most of the standard Kibana and X-Pack settings. Through a YAML editor in the console, you can append Kibana properties to the `kibana.yml` file. Your changes to the configuration file are read on startup.

Be aware that some settings that could break your cluster if set incorrectly and that the syntax might change between major versions.

For a list of supported settings, check [Kibana settings](asciidocalypse://docs/kibana/docs/reference/cloud/elastic-cloud-kibana-settings.md).

To change Kibana settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
5. Update the user settings.
6. Select **Save changes**.

Saving your changes initiates a configuration plan change that restarts Kibana automatically for you.

::::{note}
If a setting is not supported by {{ech}}, you will get an error message when you try to save.
::::

## Edit APM user settings [ec-manage-apm-settings]

Change how Elastic APM runs by providing your own user settings.
Check [APM configuration reference](/solutions/observability/apps/configure-apm-server.md) for information on how to configure the {{fleet}}-managed APM integration.