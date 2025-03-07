---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-existing-data-stream.html
applies_to:
  stack: ga
  serverless: ga
---

# Tutorial: Update existing data stream [tutorial-manage-existing-data-stream]

To update the lifecycle of an existing data stream you do the following actions:

1. [Set a data stream’s lifecycle](#set-lifecycle)
2. [Remove lifecycle for a data stream](#delete-lifecycle)


## Set a data stream’s lifecycle [set-lifecycle]

To add or to change the retention period of your data stream you can use the [PUT lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle).

* You can set infinite retention period, meaning that your data should never be deleted. For example:

    ```console
    PUT _data_stream/my-data-stream/_lifecycle
    { } <1>
    ```

    1. An empty payload means that your data stream is still managed but the data will never be deleted. Managing a time series data stream such as logs or metrics enables {{es}} to better store your data even if you do not use a retention period.

* Or you can set the retention period of your choice. For example:

    ```console
    PUT _data_stream/my-data-stream/_lifecycle
    {
      "data_retention": "30d" <1>
    }
    ```

    1. The retention period of this data stream is set to 30 days. This means that {{es}} is allowed to delete data that is older than 30 days at its own discretion.


The changes in the lifecycle are applied on all backing indices of the data stream. You can see the effect of the change via the [explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle):

```console
GET .ds-my-data-stream-*/_lifecycle/explain
```
%  TEST[continued]

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
%  TEST[continued]
%  TESTRESPONSE[skip:the result is for illustrating purposes only]


## Remove lifecycle for a data stream [delete-lifecycle]

To remove the lifecycle of a data stream you can use the [delete lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-lifecycle). As consequence, the maintenance operations that were applied by the lifecycle will no longer be applied to the data stream and all its backing indices. For example:

```console
DELETE _data_stream/my-data-stream/_lifecycle
```
%  TEST[continued]

You can then use the [explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle) again to see that the indices are no longer managed.

```console
GET .ds-my-data-stream-*/_lifecycle/explain
```
%  TEST[continued]
%  TEST[teardown:data_stream_cleanup]

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
%  TESTRESPONSE[skip:the result is for illustrating purposes only]

