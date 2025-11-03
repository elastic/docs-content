---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-custom-index-template.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# View the Elasticsearch index template [apm-custom-index-template]

Index templates are used to configure the backing indices of data streams as they are created. These index templates are composed of multiple component templates—reusable building blocks that configure index mappings, settings, and aliases.

The default APM index templates can be viewed in {{kib}}. To open **Index Management**, find it in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Index Templates** and search for `apm`. Select any of the APM index templates to view their relevant component templates.

## Edit the {{es}} index template [index-template-view]

::::{warning}
Custom index mappings may conflict with the mappings defined by the {{es}} apm-data plugin and may break the APM integration and Applications UI in {{kib}}. Do not change or customize any default mappings.
::::

The APM index templates by default reference a non-existent `@custom` component template for each data stream. You can create or edit this `@custom` component template to customize your {{es}} indices.

First, determine which [data stream](/solutions/observability/apm/data-streams.md) you’d like to edit in {{kib}}. To open **Index Management**, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Component Templates**.

Custom component templates are named following this pattern: `<name_of_data_stream>@custom`. Search for the name of the data stream, like `traces-apm`, and select its custom component template. Create one if it does not exist. In this example, that’d be, `traces-apm@custom`. Then click **Manage** → **Edit**.

Add any custom metadata, index settings, or mappings.

### Index settings [apm-custom-index-template-index-settings]

In the **Index settings** step, you can specify custom [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md). For example, you could:

* Customize the index lifecycle policy applied to a data stream. See [custom index lifecycle policies](/solutions/observability/apm/index-lifecycle-management.md#apm-data-streams-custom-policy) for a walk-through.
* Change the number of [shards](/deploy-manage/index.md) per index. Specify the number of primary shards:

    ```json
    {
      "settings": {
        "number_of_shards": "4"
      }
    }
    ```

* Change the number of [replicas](/deploy-manage/distributed-architecture/reading-and-writing-documents.md) per index. Specify the number of replica shards:

    ```json
    {
      "index": {
        "number_of_replicas": "2"
      }
    }
    ```

### Mappings [apm-custom-index-template-mappings]

[Mapping](/manage-data/data-store/mapping.md) is the process of defining how a document, and the fields it contains, are stored and indexed. In the **Mappings** step, you can add custom field mappings. For example, you could:

* Add custom field mappings that you can index on and search. In the **Mapped fields** tab, add a new field including the [field type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md):

    :::{image} /solutions/images/observability-custom-index-template-mapped-fields.png
    :alt: Editing a component template to add a new mapped field
    :::

* Add a [runtime field](/manage-data/data-store/mapping/runtime-fields.md) that is evaluated at query time. In the **Runtime fields** tab, click **Create runtime field** and provide a field name, type, and optionally a script:

    :::{image} /solutions/images/observability-custom-index-template-runtime-fields.png
    :alt: Editing a component template to add a new runtime field
    :::

## Roll over the data stream [apm-custom-index-template-rollover]

Changes to component templates are not applied retroactively to existing indices. For changes to take effect, you must create a new write index for the data stream. This can be done with the {{es}} [Rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover). For example, to roll over the `traces-apm-default` data stream, run:

```console
POST /traces-apm-default/_rollover/
```
