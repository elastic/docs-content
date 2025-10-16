---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-index-template.html
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
---

# Logs index template reference [logs-index-template]

Index templates are used to configure the backing indices of data streams as they’re created. These index templates are composed of multiple [component templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template)—reusable building blocks that configure index mappings, settings, and aliases.

You can view the default `logs` index template in {{kib}}. To open **Index Management**, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Index Templates** and search for `logs`. Select the `logs` index templates to view relevant component templates.

Refer to [Default log component templates](../logs/logs-index-template-defaults.md) for details on the mappings, settings, and pipelines included by default.


## Edit the `logs` index template [custom-logs-template-edit]

The default `logs` index template for the `logs-*-*` index pattern is composed of the following component templates:

* `logs@mappings`
* `logs@settings`
* `logs@custom`
* `ecs@mappings`

You can use the `logs@custom` component template to customize your {{es}} indices. The `logs@custom` component template is not installed by default, but you can create a component template named `logs@custom` to override and extend default mappings or settings. To do this:

1. To open **Index Management**, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Component Templates**.
3. Click **Create component template**.
4. Name the component template `logs@custom`.
5. Add any custom metadata, index settings, or mappings.

Changes to component templates are not applied retroactively to existing indices. For changes to take effect, create a new write index for impacted data streams by triggering a rollover. Do this using the {{es}} [Rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover). For example, to roll over the `logs-generic-default` data stream, run:

```console
POST /logs-generic-default/_rollover/
```


### Set the `default_field` using the custom template [custom-logs-template-default-field]

The `logs` index template uses `default_field: [*]` meaning queries without specified fields will search across all fields. You can update the `default_field` to  search in the `message` field instead of all fields using the `logs@custom` component template.

If you haven’t already created the `logs@custom` component template, create it as outlined in the previous section. Then, follow these steps to update the **Index settings** of the component template:

1. To open **Index Management**, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Component Templates**.
3. Search for `logs` and find the `logs@custom` component template.
4. Open the **Actions** menu and select **Edit**.
5. Select **Index settings** and add the following code:

    ```json
    {
      "index": {
        "query": {
          "default_field": [
            "message"
          ]
        }
      }
    }
    ```

6. Click **Next** through to the **Review** page and save the component template.
