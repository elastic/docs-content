---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-new-data-stream.html
applies_to:
  stack: ga
  serverless: ga
description: Create an Elasticsearch data stream with a lifecycle. Create an index template with data retention, create a data stream, and confirm the lifecycle.
type: how-to
products:
  - id: elasticsearch
---

# Create a data stream with a lifecycle [tutorial-manage-new-data-stream]

Create a classic {{es}} data stream with a configured lifecycle.
Learn how to set the retention period for your data and to retrieve the lifecycle configuration details.

For wired data streams, go to [](/solutions/observability/streams/get-data-in.md) and [](/solutions/observability/streams/configure-retention.md).

## Before you begin [create-data-stream-lifecycle-prereqs]

To follow these steps, you need:

* [Cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) `manage_index_templates`, to create the index template.
* [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):

  * `create_index`, `create_doc`, and `view_index_metadata` to create the stream, index documents, and read the lifecycle.
  * `auto_configure` if you use the bulk indexing API example, which adds mappings for fields that aren't defined in the template.
  * {applies_to}`stack: ga 9.3+` `manage` if you create the stream in **Streams**, which writes data stream settings.

  Refer to [Granting privileges for data streams and aliases](/deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).
* {applies_to}`stack: ga 9.3+` The **All** privilege for the **Streams** feature in {{kib}}, if you use the **Streams** app.
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` A default snapshot repository and an [appropriate license]({{subscriptions}}) for {{search-snaps}} if you turn on frozen phase transitions. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).

## Create an index template [create-index-template-with-lifecycle]

A data stream requires a matching [index template](/manage-data/data-store/templates.md).
Set the lifecycle on that template, in the same place you set mappings and index settings, so every new stream that matches the pattern inherits the lifecycle details.

:::::{tab-set}
:group: kibana-api

::::{tab-item} {{kib}}
:sync: kibana

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. On the **Index Templates** tab, click **Create template**.
1. On the **Logistics** page, enter a name and an index pattern that matches the data stream. For example, use `my-data-stream-test*` for the index pattern.

   {applies_to}`stack: ga 9.3+` To use the **Streams** app in subsequent steps your index pattern must contain a wildcard (`*`).

1. Turn on **Create data stream**.
1. Select **Delete phase** (**Data retention** in earlier versions), and choose how long to retain your data, in days, hours, minutes, or seconds.
1. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` Optional: Select the **Frozen phase** to choose when to move your data to {{search-snaps}}, in days, hours, minutes, or seconds. This period must be shorter than the delete phase. Refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).
1. In **Priority**, enter a value higher than `200` so it doesn't collide with built-in templates. Refer to [Avoid index pattern collisions](/manage-data/data-store/templates.md#avoid-index-pattern-collisions).
1. Complete the rest of the wizard. On the **Review** page, click **Create template**. For the other wizard pages, refer to [Index templates](/manage-data/data-store/templates.md).
::::
::::{tab-item} API
:sync: api

Use the [create index template API]({{es-apis}}operation/operation-indices-put-index-template).
For example:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream-test*"], <1>
  "data_stream": { }, <2>
  "priority": 500, <3>
  "template": { 
    "lifecycle": { <4>
      "data_retention": "7d" <5>
    }
  },
  "_meta": {
    "description": "Template with data stream lifecycle"
  }
}
```

1. You can use a wildcard (`*`) in the index pattern to match every data stream whose name matches the pattern.
1. Include the `data_stream` object to enable data streams.
1. Set the priority higher than `200` so it doesn't collide with built-in templates. Refer to [Avoid index pattern collisions](/manage-data/data-store/templates.md#avoid-index-pattern-collisions).
1. Define the lifecycle in the template section or in a [component template](/manage-data/data-store/templates.md#component-templates).
1. Choose how long to retain your data, in days, hours, minutes, or seconds.

:::{tip}
:applies_to: {"stack": "ga 9.5+", "serverless": "unavailable"}

To move older backing indices to {{search-snaps}}, include `frozen_after` in the lifecycle on the template. For requirements and how conversion works, refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md). For example:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream-test*"],
  "data_stream": { },
  "priority": 500,
  "template": {
    "lifecycle": {
      "data_retention": "365d",
      "frozen_after": "30d" <1>
    }
  },
  "_meta": {
    "description": "Template with data stream lifecycle and frozen transitions"
  }
}
```

1. This period must be shorter than the `data_retention` period if both are specified.
:::
::::
:::::

## Create a data stream [create-data-stream-with-lifecycle]

Create the data stream after the template exists.
The stream name has to match the template's index pattern.
Otherwise, the lifecycle on the template doesn't apply.

:::::{tab-set}
:group: kibana-api

::::{tab-item} {{kib}}
:sync: kibana

* {applies_to}`stack: ga 9.3+` Create a classic stream in [**Streams**](/solutions/observability/streams/streams.md).
    1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    1. Click **Create classic stream**.
    1. Select the index template, enter the stream name, and click **Create**.

<!-- TBD: These steps don't work for my in 9.4.9. It does not find my template. -->

::::

::::{tab-item} API
:sync: api

Create the stream in either of these ways:

* With the [create data stream API]({{es-apis}}operation/operation-indices-create-data-stream). For example:

  ```console
  PUT _data_stream/my-data-stream-test
  ```

  The stream's name must match one of your template's index patterns.

* With an [indexing request](/manage-data/data-store/data-streams/use-data-stream.md#add-documents-to-a-data-stream). For example:

    ```console
    PUT my-data-stream-test/_bulk
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }
    ```

::::
:::::

## Retrieve lifecycle information [retrieve-lifecycle-information]

Confirm that the stream uses the lifecycle from the template and then check the state of a [backing index](/manage-data/data-store/data-streams.md#backing-indices).

:::::{tab-set}
:group: kibana-api

::::{tab-item} {{kib}}
:sync: kibana

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream, and then select it.
1. In the flyout, check **Data retention** and **Effective data retention**. For this example stream, both show 7 days.

:::{image} /manage-data/images/elasticsearch-reference-lifecycle-status.png
:alt: Data stream details flyout showing data retention
:screenshot:
:::

::::

::::{tab-item} API
:sync: api

Use the [get data stream lifecycle API]({{es-apis}}operation/operation-indices-get-data-lifecycle) to see the lifecycle configuration details.
For example:

```console
GET _data_stream/my-data-stream-test*/_lifecycle
```

**Result:**

```console-result
{
  "data_streams": [
    {
      "name": "my-data-stream-test",                                <1>
      "lifecycle": {
        "enabled": true,                                            <2>
        "data_retention": "7d",                                     <3>
        "effective_retention": "7d",                                <4>
        "retention_determined_by": "data_stream_configuration"
      }
    }
  ],
  "global_retention": {}
}
```

1. The name of your data stream.
2. Whether the data stream lifecycle is turned on for this data stream.
3. The retention period configured for data in this data stream.
4. The retention period that the data stream lifecycle applies. {{es}} keeps this data for at least 7 days and can delete it later.

Use the [explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) to view lifecycle details for the backing indices.
For example:

```console
GET my-data-stream-test*/_lifecycle/explain
```

**Result:**

```console-result
  {
    "indices": {
      ".ds-my-data-stream-test-2026.10.23-000001"": {
        "index": ".ds-my-data-stream-test-2026.10.23-000001",      <1>
        "managed_by_lifecycle": true,                               <2>
        "index_creation_date_millis": 1792718438578,
        "time_since_index_creation": "22.79m",                  <3>
        "lifecycle": {                                        <4>
          "enabled": true,
          "data_retention": "7d",
          "effective_retention": "7d",
          "retention_determined_by": "data_stream_configuration"
        }
      }
    }
  }
```

1. The name of the backing index.
2. Whether the data stream lifecycle manages this index.
3. Time since the index was created.
4. The lifecycle configuration applied to this backing index.

::::
:::::

## Next steps [create-data-stream-lifecycle-next-steps]

* To change or remove the lifecycle on a stream that already exists, refer to [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md).
* To see how effective retention is calculated, refer to [Setting retention for {{es}} data streams](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md).

## Related pages [create-data-stream-lifecycle-related]

* [](/manage-data/data-store/data-streams.md)
* [](/manage-data/lifecycle/data-stream.md)
* [](/manage-data/data-store/templates.md)
* [](/solutions/observability/streams/streams.md)
