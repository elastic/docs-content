---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-new-data-stream.html
applies_to:
  stack: ga
  serverless: ga
description: Step-by-step tutorial for creating an Elasticsearch data stream with a lifecycle. Set retention on an index template, create the stream, and confirm the lifecycle.
type: tutorial
products:
  - id: elasticsearch
---

# Create a data stream with a lifecycle [tutorial-manage-new-data-stream]

Create a new {{es}} data stream and set how long to keep its data before any documents arrive. This tutorial is for you if you already know [index templates](/manage-data/data-store/templates.md) and [data streams](/manage-data/data-store/data-streams.md), and you want retention in place from the first [backing index](/manage-data/data-store/data-streams.md#backing-indices).

By the end of this tutorial, you can:

* Create an index template that matches a data stream name and sets `data_retention`.
* Create that data stream.
* Read the lifecycle for the data stream and for one backing index.

## Before you begin [create-data-stream-lifecycle-prereqs]

To create the data stream in this tutorial, you need:

* Access to [{{dev-tools-app}} Console](/explore-analyze/query-filter/tools/console.md) in {{kib}}, or another way to send {{es}} API requests.
* These privileges on the data stream name. Privileges on a data stream also apply to its backing indices. Refer to [Granting privileges for data streams and aliases](/deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).
    * [Cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) `manage_index_templates`, to create the index template.
    * [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) `create_index`, `create_doc`, and `view_index_metadata`, to create the stream, index documents with the `create` action, and read the lifecycle.
* {applies_to}`stack: ga 9.3+` The **All** privilege for the **Streams** feature in {{kib}}, if you create the stream in [Streams](/solutions/observability/streams/streams.md). You still need `create_index`.
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` A default snapshot repository, if you move older backing indices to the frozen tier. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).

For an overview of how a data stream lifecycle stores and deletes data, refer to [](/manage-data/lifecycle/data-stream.md).

## Create an index template [create-index-template-with-lifecycle]

A data stream requires a matching [index template](/manage-data/data-store/templates.md).
Set the lifecycle on that template, in the same place you set mappings and index settings, so every new stream that matches the pattern gets the same retention.

Include the `data_stream` object, define the lifecycle in the template (or in a component template), and set the priority higher than `200` so it doesn't collide with built-in templates. Refer to [Avoid index pattern collisions](/manage-data/data-store/templates.md#avoid-index-pattern-collisions).

:::::{tab-set}
:group: kibana-api

::::{tab-item} {{kib}}
:sync: kibana

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. On the **Index Templates** tab, click **Create template**.
1. On the **Logistics** page, enter a name and an index pattern that matches the data stream. For this tutorial, use `my-data-stream-test`.
1. Turn on **Create data stream**.
1. Select **Delete phase**, and set **Delete after** to 7 days. This sets `data_retention` to `7d`.
1. In **Priority**, enter a value higher than `200`.
1. Complete the rest of the wizard. On the **Review** page, click **Create template**. For the other wizard pages, refer to [Index templates](/manage-data/data-store/templates.md).

:::{note}
:applies_to: {"stack": "ga 9.5+", "serverless": "unavailable"}

To move older backing indices to the frozen tier, select **Frozen phase** and set **Move after**. For example, set **Move after** to 30 days and **Delete after** to 365 days. Register a default snapshot repository before you index data. Refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).
:::

::::

::::{tab-item} API
:sync: api

Use the [create index template API]({{es-apis}}operation/operation-indices-put-index-template). 
For example:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream-test"], <1>
  "data_stream": { },
  "priority": 500,
  "template": {
    "lifecycle": {
      "data_retention": "7d"
    }
  },
  "_meta": {
    "description": "Template with data stream lifecycle"
  }
}
```

1. The index template applies to a data stream named `my-data-stream-test`. You can use a wildcard (`*`) in the index pattern to match every data stream whose name matches the pattern, whether you create the stream with the API or by indexing.

:::{tip}
:applies_to: {"stack": "ga 9.5+", "serverless": "unavailable"}

To move older backing indices to the frozen tier, include `frozen_after` in the lifecycle on the template. For requirements and how conversion works, refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md). For example:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream-test"],
  "data_stream": { },
  "priority": 500,
  "template": {
    "lifecycle": {
      "data_retention": "365d",
      "frozen_after": "30d"
    }
  },
  "_meta": {
    "description": "Template with data stream lifecycle and frozen transitions"
  }
}
```

Confirm that a default snapshot repository is registered before you index data. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).
:::

::::

:::::

**Result:** {{es}} acknowledges the template. The later steps use the data stream name `my-data-stream-test`.

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

::::

::::{tab-item} API
:sync: api

Create the stream in either of these ways:

* With the [create data stream API]({{es-apis}}operation/operation-indices-create-data-stream). For example:

    ```console
    PUT _data_stream/my-data-stream-test
    ```

* With an [indexing request](/manage-data/data-store/data-streams/use-data-stream.md#add-documents-to-a-data-stream) that targets the stream name. For example:

    ```console
    PUT my-data-stream-test/_bulk
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }
    ```

::::

:::::

**Result:** The data stream exists and uses the lifecycle from the template. The API examples use the name `my-data-stream-test`.

## Retrieve lifecycle information [retrieve-lifecycle-information]

Confirm that the stream uses the retention from the template, and then check that same lifecycle on one backing index.

:::::{tab-set}
:group: kibana-api

::::{tab-item} {{kib}}
:sync: kibana

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream, and then select it.
1. In the flyout, check **Data retention** and **Effective data retention**. For the stream in this tutorial, both show 7 days.

:::{image} /manage-data/images/elasticsearch-reference-lifecycle-status.png
:alt: Data stream details flyout showing data retention
:screenshot:
:::

::::

::::{tab-item} API
:sync: api

Use the [get data stream lifecycle API]({{es-apis}}operation/operation-indices-get-data-lifecycle) to see the lifecycle on the data stream.
For example:

```console
GET _data_stream/my-data-stream-test/_lifecycle
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
4. The retention period that the data stream lifecycle applies. {{es}} keeps this data for at least 7 days, and can delete it later.

To see the lifecycle on one backing index, look up the index name, and then use the [explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle). {{es}} names each backing index `.ds-<stream>-<date>-<generation>`, so a request to `.ds-my-data-stream-test` doesn't match an index.

1. Get the data stream with the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream), and copy an `index_name` from `indices`. For example:

    ```console
    GET _data_stream/my-data-stream-test
    ```

    The name looks like `.ds-my-data-stream-test-2023.04.19-000001`. The date and generation in your response differ.

1. Explain that backing index. This example uses the name from the sample response. Replace it with the `index_name` you copied. For example:

    ```console
    GET .ds-my-data-stream-test-2023.04.19-000001/_lifecycle/explain
    ```

**Result:**

```console-result
{
  "indices": {
    ".ds-my-data-stream-test-2023.04.19-000001": {
      "index": ".ds-my-data-stream-test-2023.04.19-000001",      <1>
      "managed_by_lifecycle": true,                               <2>
      "index_creation_date_millis": 1681918009501,
      "time_since_index_creation": "1.6m",                  <3>
      "lifecycle": {                                        <4>
        "enabled": true,
        "data_retention": "7d"
      }
    }
  }
}
```

1. The name of the backing index.
2. Whether the built-in data stream lifecycle manages this index.
3. Time since the index was created.
4. The lifecycle configuration applied to this backing index.

::::

:::::

## Next steps [create-data-stream-lifecycle-next-steps]

* To change or remove the lifecycle on a stream that already exists, refer to [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md).
* To see how effective retention is calculated, refer to [Setting retention for {{es}} data streams](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md).
* To move older backing indices to searchable snapshots, refer to [{{search-snaps-cap}} for data streams](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).
* To move a stream from {{ilm-init}} to a data stream lifecycle, refer to [Migrating {{ilm-init}}-managed data streams to data stream lifecycle](/manage-data/lifecycle/data-stream/tutorial-migrate-ilm-managed-data-stream-to-data-stream-lifecycle.md).

## Related pages [create-data-stream-lifecycle-related]

* [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
* [Data streams](/manage-data/data-store/data-streams.md)
* [Index templates](/manage-data/data-store/templates.md)
