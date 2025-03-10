---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-new-data-stream.html
applies_to:
  stack: ga
  serverless: ga
---

# Tutorial: Create a data stream with a lifecycle [tutorial-manage-new-data-stream]

To create a data stream with a built-in lifecycle, follow these steps:

1. [Create an index template](#create-index-template-with-lifecycle)
2. [Create a data stream](#create-data-stream-with-lifecycle)
3. [Retrieve lifecycle information](#retrieve-lifecycle-information)


## Create an index template [create-index-template-with-lifecycle]

A data stream requires a matching [index template](../../data-store/templates.md). You can configure the data stream lifecycle by setting the `lifecycle` field in the index template the same as you do for mappings and index settings. You can define an index template that sets a lifecycle as follows:

* Include the `data_stream` object to enable data streams.
* Define the lifecycle in the template section or include a composable template that defines the lifecycle.
* Use a priority higher than `200` to avoid collisions with built-in templates. See [Avoid index pattern collisions](../../data-store/templates.md#avoid-index-pattern-collisions).

You can use the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template).

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream*"],
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


## Create a data stream [create-data-stream-with-lifecycle]

You can create a data stream in two ways:

1. By manually creating the stream using the [create data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream). The stream’s name must still match one of your template’s index patterns.

    ```console
    PUT _data_stream/my-data-stream
    ```

2. By [indexing requests](../../data-store/data-streams/use-data-stream.md#add-documents-to-a-data-stream) that target the stream’s name. This name must match one of your index template’s index patterns.

    ```console
    PUT my-data-stream/_bulk
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }
    ```



## Retrieve lifecycle information [retrieve-lifecycle-information]

You can use the [get data stream lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-lifecycle) to see the data stream lifecycle of your data stream and the [explain data stream lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle) to see the exact state of each backing index.

```console
GET _data_stream/my-data-stream/_lifecycle
```
%  TEST[continued]

The result will look like this:

```console-result
{
  "data_streams": [
    {
      "name": "my-data-stream",                                     <1>
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
2. Shows if the data stream lifecycle is enabled for this data stream.
3. The retention period of the data indexed in this data stream, as configured by the user.
4. The retention period that will be applied by the data stream lifecycle. This means that the data in this data stream will be kept at least for 7 days. After that {{es}} can delete it at its own discretion.


If you want to see more information about how the data stream lifecycle is applied on individual backing indices use the [explain data stream lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-explain-data-lifecycle):

```console
GET .ds-my-data-stream-*/_lifecycle/explain
```
%  TEST[continued]

The result will look like this:

```console-result
{
  "indices": {
    ".ds-my-data-stream-2023.04.19-000001": {
      "index": ".ds-my-data-stream-2023.04.19-000001",      <1>
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
%  TESTRESPONSE[skip:the result is for illustrating purposes only]

1. The name of the backing index.
2. If it is managed by the built-in data stream lifecycle.
3. Time since the index was created.
4. The lifecycle configuration that is applied on this backing index.


