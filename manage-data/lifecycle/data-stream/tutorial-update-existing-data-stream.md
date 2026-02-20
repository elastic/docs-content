---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-existing-data-stream.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Update the lifecycle of a data stream [tutorial-manage-existing-data-stream]

Follow these steps to configure or remove data stream lifecycle settings for an existing, individual data stream.

- [Set a data stream’s lifecycle](#set-lifecycle)
- [Remove the lifecycle for a data stream](#delete-lifecycle)
- [Manage data retention on the Streams page](#data-retention-streams)

These steps are for data stream lifecycle only. For the steps to configure {{ilm}}, refer to the [{{ilm-init}} documentation](/manage-data/lifecycle/index-lifecycle-management.md). For a comparison between the two, refer to [](/manage-data/lifecycle.md).

## Set a data stream’s lifecycle [set-lifecycle]

To add or to change the retention period of your data stream you can use the **Index Management** tools in {{kib}} or the {{es}} [lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle).


:::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To change the data retention settings for a data stream:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Open the **Data Streams** tab.
1. Use the search tool to find the data stream you're looking for.
1. Select the data stream to view its details.
1. In the data stream details pane, select **Manage > Edit data retention** to adjust the settings. You can do any of the following:

    - Select how long to retain your data, in days, hours, minutes, or seconds.
    - Choose to **Keep data indefinitely**, so that your data will not be deleted. Your data stream is still managed but the data will never be deleted. Managing a time series data stream such as for logs or metrics enables {{es}} to better store your data even if you do not use a retention period.
    - Disable **Enable data retention** to turn off data stream lifecycle management for your data stream.

    If the data stream is already managed by [{{ilm-init}}](/manage-data/lifecycle/index-lifecycle-management.md), to edit the data retention settings you must edit the associated {{ilm-init}} policy.


:::

:::{tab-item} API
:sync: api

To change the data retention settings for a data stream:

* You can set infinite retention period, meaning that your data should never be deleted. For example:

    ```console
    PUT _data_stream/my-data-stream/_lifecycle
    { } <1>
    ```

    1. An empty payload means that your data stream is still managed but the data will never be deleted. Managing a time series data stream such as for logs or metrics enables {{es}} to better store your data even if you do not use a retention period.

* Or you can set the retention period of your choice. For example:

    ```console
    PUT _data_stream/my-data-stream/_lifecycle
    {
      "data_retention": "30d" <1>
    }
    ```

    1. The retention period of this data stream is set to 30 days. This means that {{es}} is allowed to delete data that is older than 30 days at its own discretion.
:::
:::::

The changes in the lifecycle are applied on all backing indices of the data stream.

You can see the effect of the change in {{kib}} or using the {{es}} [explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle):

:::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To check the data retention settings for a data stream:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Open the **Data Streams** tab.
1. Use the search tool to find the data stream you're looking for.
1. Select the data stream to view its details. The flyout shows the data retention settings for the data stream. If the data stream is currently managed by an [{{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management.md), the **Effective data retention** may differ from the retention value that you've set in the data stream, as indicated by the **Data retention**.

  :::{image} /manage-data/images/elasticsearch-reference-lifecycle-status.png
  :alt: Index lifecycle status page
  :width: 500px
  :::

:::{tab-item} API
:sync: api

To check the data retention settings for a data stream:

```console
GET .ds-my-data-stream-*/_lifecycle/explain
```

The response will look like:

```console-result
{
  "indices": {
    ".ds-my-data-stream-2023.04.19-000002": {
      "index": ".ds-my-data-stream-2023.04.19-000002",  <1>
      "managed_by_lifecycle": true,                           <2>
      "index_creation_date_millis": 1681919221417,
      "time_since_index_creation": "6.85s",             <3>
      "lifecycle": {
        "enabled": true,
        "data_retention": "30d"                         <4>
      }
    },
    ".ds-my-data-stream-2023.04.17-000001": {
      "index": ".ds-my-data-stream-2023.04.17-000001",  <5>
      "managed_by_lifecycle": true,                           <6>
      "index_creation_date_millis": 1681745209501,
      "time_since_index_creation": "48d",               <7>
      "rollover_date_millis": 1681919221419,
      "time_since_rollover": "6.84s",                   <8>
      "generation_time": "6.84s",                       <9>
      "lifecycle": {
        "enabled": true,
        "data_retention": "30d"                         <10>
      }
    }
  }
}
```

1. The name of the backing index.
2. This index is managed by a data stream lifecycle.
3. The time that has passed since this index has been created.
4. The data retention for this index is at least 30 days, as it was recently updated.
5. The name of the backing index.
6. This index is managed by the built-in data stream lifecycle.
7. The time that has passed since this index has been created.
8. The time that has passed since this index was [rolled over](../index-lifecycle-management/rollover.md).
9. The time that will be used to determine when it’s safe to delete this index and all its data.
10. The data retention for this index as well is at least 30 days, as it was recently updated.

:::
:::::

## Remove the lifecycle for a data stream [delete-lifecycle]

To remove the lifecycle of a data stream you can use the **Index Management** tools in {{kib}} or the {{es}} [delete lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-lifecycle).


:::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To remove a data stream's lifecycle:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Open the **Data Streams** tab.
1. Use the search tool to find the data stream you're looking for.
1. Select the data stream to view its details.
1. In the data stream details pane, select **Manage > Edit data retention**.
1. Turn off the **Enable data retention** option and save your changes. The maintenance operations that were applied by the lifecycle will no longer be applied to the data stream and all of its backing indices.

    You can confirm your changes by reopening the data stream pane. The **Effective data retention** will show a **Disabled** status.

  ::::{image} /manage-data/images/elasticsearch-reference-lifecycle-disabled.png
  :alt: Index lifecycle status is disabled
  :width: 500px
  ::::


:::

:::{tab-item} API
:sync: api

To remove a data stream's lifecycle:

```console
DELETE _data_stream/my-data-stream/_lifecycle
```

After running the API request, the maintenance operations that were applied by the lifecycle will no longer be applied to the data stream and all of its backing indices.

You can then use the [explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle) again to see that the indices are no longer managed.

```console
GET .ds-my-data-stream-*/_lifecycle/explain
```

```console-result
{
  "indices": {
    ".ds-my-data-stream-2023.04.19-000002": {
      "index": ".ds-my-data-stream-2023.04.19-000002",  <1>
      "managed_by_lifecycle": false                           <2>
    },
    ".ds-my-data-stream-2023.04.17-000001": {
      "index": ".ds-my-data-stream-2023.04.19-000001",  <3>
      "managed_by_lifecycle": false                           <4>
    }
  }
}
```

1. The name of the backing index.
2. Indication that the index is not managed by the data stream lifecycle.
3. The name of another backing index.
4. Indication that the index is not managed by the data stream lifecycle.
:::
:::::

## Manage data retention on the Streams page [data-retention-streams]
```{applies_to}
serverless: ga
stack: preview =9.1, ga 9.2+
```

Starting with {{stack}} version 9.2, the **Streams** page provides a centralized interface for common data management tasks in {{kib}}, including getting insight into how your data streams retain data. 

1. Go to the **Streams** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Each stream maps directly to an {{es}} data stream. Select a stream to view its details.
1. Go to the **Retention** tab to set how long your stream retains data and to get insight into your stream's data ingestion and storage size.
1. Select **Edit data retention** and choose to retain your data indefinitely, for a custom period, or by following an existing ILM policy. You can also use the data retention configuration that's set in the index template by enabling the  **Inherit from index template** option. If you use this option, you don't need to specify a custom retention period or policy.

For more information about the retention configuration options, refer to [](/solutions/observability/streams/management/retention.md).

