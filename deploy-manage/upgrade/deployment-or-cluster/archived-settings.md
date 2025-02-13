---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/archived-settings.html
---

# Archived settings [archived-settings]

If you upgrade a cluster with a deprecated persistent cluster setting to a version that no longer supports the setting, {{es}} automatically archives that setting. Similarly, if you upgrade a cluster that contains an index with an unsupported index setting, {{es}} archives the index setting.

We recommend you remove any archived settings after upgrading. Archived settings are considered invalid and can interfere with your ability to configure other settings.

Archived settings start with the `archived.` prefix.


## Archived cluster settings [archived-cluster-settings] 

Use the following [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) request to check for archived cluster settings. If the request returns an empty object (`{ }`), there are no archived cluster settings.

```console
GET _cluster/settings?flat_settings=true&filter_path=persistent.archived*
```

To remove any archived cluster settings, use the following [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) request.

```console
PUT _cluster/settings
{
  "persistent": {
    "archived.*": null
  }
}
```

{{es}} doesn’t archive transient cluster settings or settings in `elasticsearch.yml`. If a node includes an unsupported setting in `elasticsearch.yml`, it will return an error at startup.


## Archived index settings [archived-index-settings] 

::::{important} 
Before you upgrade, remove any unsupported index settings from index and component templates. {{es}} doesn’t archive unsupported index settings in templates during an upgrade. Attempts to use a template that contains an unsupported index setting will fail and return an error. This includes automated operations, such the {{ilm-init}} rollover action.
::::


Archived index settings don’t affect an index’s configuration or most index operations, such as indexing or search. However, you’ll need to remove them before you can configure other settings for the index, such as `index.hidden`.

Use the following [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) request to get a list indices with archived settings. If the request returns an empty object (`{ }`), there are no archived index settings.

```console
GET */_settings?flat_settings=true&filter_path=**.settings.archived*
```

To remove any archived index settings, use the following [indices update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) request.

```console
PUT /my-index/_settings
{
  "archived.*": null
}
```

