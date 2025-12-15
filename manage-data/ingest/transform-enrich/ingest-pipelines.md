---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Elasticsearch ingest pipelines [ingest]

{{es}} ingest pipelines let you perform common transformations on your data before indexing. For example, you can use pipelines to remove fields, extract values from text, and enrich your data.

A pipeline consists of a series of configurable tasks called [processors](elasticsearch://reference/enrich-processor/index.md). Each processor runs sequentially, making specific changes to incoming documents. After the processors have run, {{es}} adds the transformed documents to your data stream or index.

:::{image} /manage-data/images/elasticsearch-reference-ingest-process.svg
:alt: Ingest pipeline diagram
:::

You can create and manage ingest pipelines using {{kib}}'s **Ingest Pipelines** feature or the [ingest APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ingest). {{es}} stores pipelines in the [cluster state](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-state).

## Prerequisites [ingest-prerequisites]

* Nodes with the [`ingest`](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#node-ingest-node) node role handle pipeline processing. To use ingest pipelines, your cluster must have at least one node with the `ingest` role. For heavy ingest loads, we recommend creating [dedicated ingest nodes](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#node-ingest-node).
* If the {{es}} security features are enabled, you must have the `manage_pipeline` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) to manage ingest pipelines. To use {{kib}}'s **Ingest Pipelines** feature, you also need the `cluster:monitor/nodes/info` cluster privileges.
* Pipelines including the `enrich` processor require additional setup. See [*Enrich your data*](data-enrichment.md).


## Create and manage pipelines [create-manage-ingest-pipelines]

In {{kib}}, go to the **Ingest Pipelines** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

From the list view, you can:

* View a list of your pipelines and drill down into details
* Edit or clone existing pipelines
* Delete pipelines

:::{image} /manage-data/images/elasticsearch-reference-ingest-pipeline-list.png
:alt: Kibana's Ingest Pipelines list view
:screenshot:
:::

To create a pipeline, click **Create pipeline > New pipeline**. For an example tutorial, see [Example: Parse logs](example-parse-logs.md).

::::{tip}
The **New pipeline from CSV** option lets you use a CSV to create an ingest pipeline that maps custom data to the [Elastic Common Schema (ECS)](ecs://reference/index.md). Mapping your custom data to ECS makes the data easier to search and lets you reuse visualizations from other datasets. To get started, check [Map custom data to ECS](ecs://reference/ecs-converting.md).
::::


You can also use the [ingest APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ingest) to create and manage pipelines. The following [create pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) request creates a pipeline containing two [`set`](elasticsearch://reference/enrich-processor/set-processor.md) processors followed by a [`lowercase`](elasticsearch://reference/enrich-processor/lowercase-processor.md) processor. The processors run sequentially in the order specified.

```console
PUT _ingest/pipeline/my-pipeline
{
  "description": "My optional pipeline description",
  "processors": [
    {
      "set": {
        "description": "My optional processor description",
        "field": "my-long-field",
        "value": 10
      }
    },
    {
      "set": {
        "description": "Set 'my-boolean-field' to true",
        "field": "my-boolean-field",
        "value": true
      }
    },
    {
      "lowercase": {
        "field": "my-keyword-field"
      }
    }
  ]
}
```


## Manage pipeline versions [manage-pipeline-versions]

When you create or update a pipeline, you can specify an optional `version` integer. You can use this version number with the [`if_version`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline#put-pipeline-api-query-params) parameter to conditionally update the pipeline. When the `if_version` parameter is specified, a successful update increments the pipeline’s version.

```console
PUT _ingest/pipeline/my-pipeline-id
{
  "version": 1,
  "processors": [ ... ]
}
```

To unset the `version` number using the API, replace or update the pipeline without specifying the `version` parameter.


## Test a pipeline [test-pipeline]

Before using a pipeline in production, we recommend you test it using sample documents. When creating or editing a pipeline in {{kib}}, click **Add documents**. In the **Documents** tab, provide sample documents and click **Run the pipeline**.

:::{image} /manage-data/images/elasticsearch-reference-test-a-pipeline.png
:alt: Test a pipeline in Kibana
:screenshot:
:::

You can also test pipelines using the [simulate pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate). You can specify a configured pipeline in the request path. For example, the following request tests `my-pipeline`.

```console
POST _ingest/pipeline/my-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "my-keyword-field": "FOO"
      }
    },
    {
      "_source": {
        "my-keyword-field": "BAR"
      }
    }
  ]
}
```

Alternatively, you can specify a pipeline and its processors in the request body.

```console
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "lowercase": {
          "field": "my-keyword-field"
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "my-keyword-field": "FOO"
      }
    },
    {
      "_source": {
        "my-keyword-field": "BAR"
      }
    }
  ]
}
```

The API returns transformed documents:

```console-result
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_version": "-3",
        "_source": {
          "my-keyword-field": "foo"
        },
        "_ingest": {
          "timestamp": "2099-03-07T11:04:03.000Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_version": "-3",
        "_source": {
          "my-keyword-field": "bar"
        },
        "_ingest": {
          "timestamp": "2099-03-07T11:04:04.000Z"
        }
      }
    }
  ]
}
```


## Add a pipeline to an indexing request [add-pipeline-to-indexing-request]

Use the `pipeline` query parameter to apply a pipeline to documents in [individual](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) or [bulk](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) indexing requests.

```console
POST my-data-stream/_doc?pipeline=my-pipeline
{
  "@timestamp": "2099-03-07T11:04:05.000Z",
  "my-keyword-field": "foo"
}

PUT my-data-stream/_bulk?pipeline=my-pipeline
{ "create":{ } }
{ "@timestamp": "2099-03-07T11:04:06.000Z", "my-keyword-field": "foo" }
{ "create":{ } }
{ "@timestamp": "2099-03-07T11:04:07.000Z", "my-keyword-field": "bar" }
```

You can also use the `pipeline` parameter with the [update by query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) or [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) APIs.

```console
POST my-data-stream/_update_by_query?pipeline=my-pipeline

POST _reindex
{
  "source": {
    "index": "my-data-stream"
  },
  "dest": {
    "index": "my-new-data-stream",
    "op_type": "create",
    "pipeline": "my-pipeline"
  }
}
```


## Set a default pipeline [set-default-pipeline]

Use the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) index setting to set a default pipeline. {{es}} applies this pipeline to indexing requests if no `pipeline` parameter is specified.


## Set a final pipeline [set-final-pipeline]

Use the [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting to set a final pipeline. {{es}} applies this pipeline after the request or default pipeline, even if neither is specified.


## Pipelines for {{beats}} [pipelines-for-beats]

To add an ingest pipeline to an Elastic Beat, specify the `pipeline` parameter under `output.elasticsearch` in `<BEAT_NAME>.yml`. For example, for {{filebeat}}, you’d specify `pipeline` in `filebeat.yml`.

```yaml
output.elasticsearch:
  hosts: ["localhost:9200"]
  pipeline: my-pipeline
```


## Pipelines for {{fleet}} and {{agent}} [pipelines-for-fleet-elastic-agent]

{{agent}} integrations ship with default ingest pipelines that preprocess and enrich data before indexing. [{{fleet}}](/reference/fleet/index.md) applies these pipelines using [index templates](../../data-store/templates.md) that include [pipeline index settings](ingest-pipelines.md#set-default-pipeline). {{es}} matches these templates to your {{fleet}} data streams based on the [stream’s naming scheme](/reference/fleet/data-streams.md#data-streams-naming-scheme).

Each default integration pipeline calls a nonexistent, unversioned `*@custom` ingest pipeline. If unaltered, this pipeline call has no effect on your data. However, you can modify this call to create custom pipelines for integrations that persist across upgrades. Refer to [Tutorial: Transform data with custom ingest pipelines](/reference/fleet/data-streams-pipeline-tutorial.md) to learn more.

{{fleet}} doesn’t provide a default ingest pipeline for the **Custom logs** integration, but you can specify a pipeline for this integration using an [index template](ingest-pipelines.md#pipeline-custom-logs-index-template) or a [custom configuration](ingest-pipelines.md#pipeline-custom-logs-configuration).

$$$pipeline-custom-logs-index-template$$$
**Option 1: Index template**

1. [Create](ingest-pipelines.md#create-manage-ingest-pipelines) and [test](ingest-pipelines.md#test-pipeline) your ingest pipeline. Name your pipeline `logs-<dataset-name>-default`. This makes tracking the pipeline for your integration easier.

    For example, the following request creates a pipeline for the `my-app` dataset. The pipeline’s name is `logs-my_app-default`.

    ```console
    PUT _ingest/pipeline/logs-my_app-default
    {
      "description": "Pipeline for `my_app` dataset",
      "processors": [ ... ]
    }
    ```

2. Create an [index template](../../data-store/templates.md) that includes your pipeline in the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Ensure the template is [data stream enabled](../../data-store/data-streams/set-up-data-stream.md#create-index-template). The template’s index pattern should match `logs-<dataset-name>-*`.

    You can create this template using {{kib}}'s [**Index Management**](/manage-data/data-store/index-basics.md#index-management-manage-index-templates) feature or the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template).

    For example, the following request creates a template matching `logs-my_app-*`. The template uses a component template that contains the `index.default_pipeline` index setting.

    ```console
    # Creates a component template for index settings
    PUT _component_template/logs-my_app-settings
    {
      "template": {
        "settings": {
          "index.default_pipeline": "logs-my_app-default",
          "index.lifecycle.name": "logs"
        }
      }
    }

    # Creates an index template matching `logs-my_app-*`
    PUT _index_template/logs-my_app-template
    {
      "index_patterns": ["logs-my_app-*"],
      "data_stream": { },
      "priority": 500,
      "composed_of": ["logs-my_app-settings", "logs-my_app-mappings"]
    }
    ```

3. When adding or editing your **Custom logs** integration in {{fleet}}, click **Configure integration > Custom log file > Advanced options**.
4. In **Dataset name**, specify your dataset’s name. {{fleet}} will add new data for the integration to the resulting `logs-<dataset-name>-default` data stream.

    For example, if your dataset’s name was `my_app`, {{fleet}} adds new data to the `logs-my_app-default` data stream.

    :::{image} /manage-data/images/elasticsearch-reference-custom-logs.png
    :alt: Set up custom log integration in Fleet
    :screenshot:
    :::

5. Use the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover) to roll over your data stream. This ensures {{es}} applies the index template and its pipeline settings to any new data for the integration.

    ```console
    POST logs-my_app-default/_rollover/
    ```


$$$pipeline-custom-logs-configuration$$$
**Option 2: Custom configuration**

1. [Create](ingest-pipelines.md#create-manage-ingest-pipelines) and [test](ingest-pipelines.md#test-pipeline) your ingest pipeline. Name your pipeline `logs-<dataset-name>-default`. This makes tracking the pipeline for your integration easier.

    For example, the following request creates a pipeline for the `my-app` dataset. The pipeline’s name is `logs-my_app-default`.

    ```console
    PUT _ingest/pipeline/logs-my_app-default
    {
      "description": "Pipeline for `my_app` dataset",
      "processors": [ ... ]
    }
    ```

2. When adding or editing your **Custom logs** integration in {{fleet}}, click **Configure integration > Custom log file > Advanced options**.
3. In **Dataset name**, specify your dataset’s name. {{fleet}} will add new data for the integration to the resulting `logs-<dataset-name>-default` data stream.

    For example, if your dataset’s name was `my_app`, {{fleet}} adds new data to the `logs-my_app-default` data stream.

4. In **Custom Configurations**, specify your pipeline in the `pipeline` policy setting.

    :::{image} /manage-data/images/elasticsearch-reference-custom-logs-pipeline.png
    :alt: Custom pipeline configuration for custom log integration
    :screenshot:
    :::


**{{agent}} standalone**

If you run {{agent}} standalone, you can apply pipelines using an [index template](../../data-store/templates.md) that includes the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Alternatively, you can specify the `pipeline` policy setting in your `elastic-agent.yml` configuration. See [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md).


## Pipelines for search indices [pipelines-in-enterprise-search]

When you create Elasticsearch indices for search use cases, for example, using the [web crawler^](https://www.elastic.co/guide/en/enterprise-search/current/crawler.html) or [connectors](elasticsearch://reference/search-connectors/index.md), these indices are automatically set up with specific ingest pipelines. These processors help optimize your content for search. See [*Ingest pipelines in Search*](../../../solutions/search/ingest-for-search.md) for more information.


## Access source fields in a processor [access-source-fields]

Processors have read and write access to an incoming document’s source fields. To access a field key in a processor, use its field name. The following `set` processor accesses `my-long-field`.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "field": "my-long-field",
        "value": 10
      }
    }
  ]
}
```

You can also prepend the `_source` prefix.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "field": "_source.my-long-field",
        "value": 10
      }
    }
  ]
}
```

Use dot notation to access object fields.

::::{important}
If your document contains flattened objects, use the [`dot_expander`](elasticsearch://reference/enrich-processor/dot-expand-processor.md) processor to expand them. If you wish to maintain your document structure, use the [`flexible`](ingest-pipelines.md#access-source-pattern-flexible) access pattern in your pipeline definition. Otherwise Ingest processors cannot access dotted field names.
::::


```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "dot_expander": {
        "description": "Expand 'my-object-field.my-property'",
        "field": "my-object-field.my-property"
      }
    },
    {
      "set": {
        "description": "Set 'my-object-field.my-property' to 10",
        "field": "my-object-field.my-property",
        "value": 10
      }
    }
  ]
}
```

$$$template-snippets$$$
Several processor parameters support [Mustache](https://mustache.github.io) template snippets. To access field values in a template snippet, enclose the field name in triple curly brackets:`{{{field-name}}}`. You can use template snippets to dynamically set field names.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Set dynamic '<service>' field to 'code' value",
        "field": "{{{service}}}",
        "value": "{{{code}}}"
      }
    }
  ]
}
```

## Ingest field access pattern [access-source-pattern]
```{applies_to}
serverless: ga
stack: ga 9.2
```

The default ingest pipeline access pattern does not recognize dotted field names in documents. Retrieving flattened and dotted field names from an ingest document requires a different field retrieval algorithm that does not have this limitation. We know that some pipelines have come to rely on these dotted field name limitations in their logic. In order to continue supporting the original behavior while still adding support for dotted field names, ingest pipelines now support configuring an access pattern to use for all processors in the pipeline.

The `field_access_pattern` property on an ingest pipeline defines how ingest document fields are read and written for all processors in the current pipeline. It accepts two values: `classic` (which is the default) and `flexible`.

```console
PUT _ingest/pipeline/my-pipeline
{
  "field_access_pattern": "classic", <1>
  "processors": [
    {
      "set": {
        "description": "Set some searchable tags in our document's flattened field",
        "field": "event.tags.ingest.processed_by", <2>
        "value": "my-pipeline"
      }
    }
  ]
}
```
1. All processors in this pipeline will use the `classic` access pattern.
2. The logic for resolving field paths used by processors to read and write values to ingest documents is based on the access pattern.

### Classic field access pattern [access-source-pattern-classic]

The `classic` access pattern is the default access pattern that has been around since ingest node first released. Field paths given to processors (for example, `event.tags.ingest.processed_by`) are split on the dot character (`.`). The processor then uses the resulting field names to traverse the document until a value is found. When writing a value to a document, if its parent fields do not exist in the source, the processor will create nested objects for the missing fields.

```console
POST /_ingest/pipeline/_simulate
{
  "pipeline" : {
    "description": "example pipeline",
    "field_access_pattern": "classic", <1>
    "processors": [
      {
        "set" : {
          "description" : "Copy the foo.bar field into the a.b.c.d field if it exists",
          "copy_from" : "foo.bar", <2>
          "field" : "a.b.c.d", <3>
          "ignore_empty_value": true
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo": {
          "bar": "baz" <4>
        }
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo.bar": "baz" <5>
      }
    }
  ]
}
```
1. Explicitly declaring to use the `classic` access pattern in the pipeline. This is the default value.
2. We are reading a value from the field `foo.bar`.
3. We are writing its value to the field `a.b.c.d`.
4. This document uses nested json objects in its structure.
5. This document uses dotted field names in its structure.

```console-result
{
   "docs": [
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
              "foo": {
                "bar": "baz" <1>
              },
              "a": {
                "b": {
                  "c": {
                    "d": "baz" <2>
                  }
                }
              }
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.187Z"
            }
         }
      },
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
               "foo.bar": "baz" <3>
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.188Z"
            }
         }
      }
   ]
}
```
1. The first document's `foo.bar` field is located, because it uses nested json. The processor looks for a `foo` field, and then a `bar` field.
2. The value from the `foo.bar` field is written to a nested json structure at field `a.b.c.d`. The processor creates objects for each field in the path.
3. The second document uses a dotted field name for `foo.bar`. The `classic` access pattern does not recognize dotted field names, and so nothing is copied.

If the documents you are ingesting contain dotted field names, to read them with the `classic` access pattern, you must use the [`dot_expander`](elasticsearch://reference/enrich-processor/dot-expand-processor.md) processor. This approach is not always reasonable though. Consider the following document:

```json
{
  "event": {
    "tags": {
      "http.host": "localhost:9200",
      "http.host.name": "localhost",
      "http.host.port": 9200
    }
  }
}
```
If the `event.tags` field was processed with the [`dot_expander`](elasticsearch://reference/enrich-processor/dot-expand-processor.md) processor, the field values would collide. The `http.host` field cannot be a text value and an object value at the same time.

### Flexible field access pattern [access-source-pattern-flexible]

The `flexible` access pattern allows for ingest pipelines to access both nested and dotted field names without using the [`dot_expander`](elasticsearch://reference/enrich-processor/dot-expand-processor.md) processor. Additionally, when writing a value to a field that does not exist, any parent fields that are missing are concatenated to the start of the new key. Use the `flexible` access pattern if your documents have dotted field names, and also if you prefer to write missing fields to the document with dotted names.

```console
POST /_ingest/pipeline/_simulate
{
  "pipeline" : {
    "description": "example pipeline",
    "field_access_pattern": "flexible", <1>
    "processors": [
      {
        "set" : {
          "description" : "Copy the foo.bar field into the a.b.c.d field if it exists",
          "copy_from" : "foo.bar", <2>
          "field" : "a.b.c.d", <3>
          "ignore_empty_value": true
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo": {
          "bar": "baz" <4>
        },
        "a": {} <5>
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo.bar": "baz", <6>
      }
    }
  ]
}
```
1. Using the `flexible` access pattern in the pipeline.
2. We are reading a value from the field `foo.bar`.
3. We are writing its value to the field `a.b.c.d`.
4. The first document uses nested json objects in its structure.
5. The first document has an existing `a` field in the root.
6. The second document uses a dotted field name.

```console-result
{
   "docs": [
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
              "foo": {
                "bar": "baz" <1>
              },
              "a": {
                "b.c.d": "baz" <2>
              }
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.187Z"
            }
         }
      },
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
               "foo.bar": "baz", <3>
               "a.b.c.d": "baz" <4>
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.188Z"
            }
         }
      }
   ]
}
```
1. The `flexible` access pattern supports nested object fields. The processor looks for a `foo` field, and then a `bar` field.
2. The value from the `foo.bar` field is written to the dotted field name `b.c.d` underneath the field `a`. The processor concatenates the missing field names together as a prefix on the key.
3. The `flexible` access pattern also supports dotted field names. The processor looks for a field named `foo`, and after not finding it, looks for a field named `foo.bar`.
4. The value from the `foo.bar` field is written to the dotted field name `a.b.c.d`. Since none of those fields exist in the document yet, they are concatenated together into a dotted field name.

## Access metadata fields in a processor [access-metadata-fields]

Processors can access the following metadata fields by name:

* `_index`
* `_id`
* `_routing`
* `_dynamic_templates`

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Set '_routing' to 'geoip.country_iso_code' value",
        "field": "_routing",
        "value": "{{{geoip.country_iso_code}}}"
      }
    }
  ]
}
```

Use a Mustache template snippet to access metadata field values. For example, `{{{_routing}}}` retrieves a document’s routing value.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Use geo_point dynamic template for address field",
        "field": "_dynamic_templates",
        "value": {
          "address": "geo_point"
        }
      }
    }
  ]
}
```

The set processor above tells ES to use the dynamic template named `geo_point` for the field `address` if this field is not defined in the mapping of the index yet. This processor overrides the dynamic template for the field `address` if already defined in the bulk request, but has no effect on other dynamic templates defined in the bulk request.

::::{warning}
If you [automatically generate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create#create-document-ids-automatically) document IDs, you cannot use `{{{_id}}}` in a processor. {{es}} assigns auto-generated `_id` values after ingest.
::::



## Access ingest metadata in a processor [access-ingest-metadata]

Ingest processors can add and access ingest metadata using the `_ingest` key.

Unlike source and metadata fields, {{es}} does not index ingest metadata fields by default. {{es}} also allows source fields that start with an `_ingest` key. If your data includes such source fields, use `_source._ingest` to access them.

Pipelines only create the `_ingest.timestamp` ingest metadata field by default. This field contains a timestamp of when {{es}} received the document’s indexing request. To index `_ingest.timestamp` or other ingest metadata fields, use the `set` processor.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Index the ingest timestamp as 'event.ingested'",
        "field": "event.ingested",
        "value": "{{{_ingest.timestamp}}}"
      }
    }
  ]
}
```


## Handling pipeline failures [handling-pipeline-failures]

A pipeline’s processors run sequentially. By default, pipeline processing stops when one of these processors fails or encounters an error.

To ignore a processor failure and run the pipeline’s remaining processors, set `ignore_failure` to `true`.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "rename": {
        "description": "Rename 'provider' to 'cloud.provider'",
        "field": "provider",
        "target_field": "cloud.provider",
        "ignore_failure": true
      }
    }
  ]
}
```

Use the `on_failure` parameter to specify a list of processors to run immediately after a processor failure. If `on_failure` is specified, {{es}} afterward runs the pipeline’s remaining processors, even if the `on_failure` configuration is empty.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "rename": {
        "description": "Rename 'provider' to 'cloud.provider'",
        "field": "provider",
        "target_field": "cloud.provider",
        "on_failure": [
          {
            "set": {
              "description": "Set 'error.message'",
              "field": "error.message",
              "value": "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
              "override": false
            }
          }
        ]
      }
    }
  ]
}
```

Nest a list of `on_failure` processors for nested error handling.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "rename": {
        "description": "Rename 'provider' to 'cloud.provider'",
        "field": "provider",
        "target_field": "cloud.provider",
        "on_failure": [
          {
            "set": {
              "description": "Set 'error.message'",
              "field": "error.message",
              "value": "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
              "override": false,
              "on_failure": [
                {
                  "set": {
                    "description": "Set 'error.message.multi'",
                    "field": "error.message.multi",
                    "value": "Document encountered multiple ingest errors",
                    "override": true
                  }
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
```

You can also specify `on_failure` for a pipeline. If a processor without an `on_failure` value fails, {{es}} uses this pipeline-level parameter as a fallback. {{es}} will not attempt to run the pipeline’s remaining processors.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [ ... ],
  "on_failure": [
    {
      "set": {
        "description": "Index document to 'failed-<index>'",
        "field": "_index",
        "value": "failed-{{{ _index }}}"
      }
    }
  ]
}
```

Additional information about the pipeline failure may be available in the document metadata fields `on_failure_message`, `on_failure_processor_type`, `on_failure_processor_tag`, and `on_failure_pipeline`. These fields are accessible only from within an `on_failure` block.

The following example uses the metadata fields to include information about pipeline failures in documents.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [ ... ],
  "on_failure": [
    {
      "set": {
        "description": "Record error information",
        "field": "error_information",
        "value": "Processor {{ _ingest.on_failure_processor_type }} with tag {{ _ingest.on_failure_processor_tag }} in pipeline {{ _ingest.on_failure_pipeline }} failed with message {{ _ingest.on_failure_message }}"
      }
    }
  ]
}
```


## Conditionally run a processor [conditionally-run-processor]

Each processor supports an optional `if` condition, written as a [Painless script](elasticsearch://reference/scripting-languages/painless/painless.md). If provided, the processor only runs when the `if` condition is `true`.

::::{important}
`if` condition scripts run in Painless’s [ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md). In `if` conditions, `ctx` values are read-only.
::::


```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents with 'network.name' of 'Guest'",
        "if": "ctx?.network?.name == 'Guest'"
      }
    }
  ]
}
```

If the [`script.painless.regex.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#script-painless-regex-enabled) cluster setting is enabled, you can use regular expressions in your `if` condition scripts. For supported syntax, see [Painless regular expressions](elasticsearch://reference/scripting-languages/painless/painless-regexes.md).

::::{tip}
If possible, avoid using regular expressions. Expensive regular expressions can slow indexing speeds.
::::


```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "If 'url.scheme' is 'http', set 'url.insecure' to true",
        "if": "ctx.url?.scheme =~ /^http[^s]/",
        "field": "url.insecure",
        "value": true
      }
    }
  ]
}
```

You must specify `if` conditions as valid JSON on a single line. However, you can use the [{{kib}} console](../../../explore-analyze/query-filter/tools/console.md#configuring-console)'s triple quote syntax to write and debug larger scripts.

::::{tip}
If possible, avoid using complex or expensive `if` condition scripts. Expensive condition scripts can slow indexing speeds.
::::


```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that don't contain 'prod' tag",
        "if": """
            Collection tags = ctx.tags;
            if(tags != null){
              for (String tag : tags) {
                if (tag.toLowerCase().contains('prod')) {
                  return false;
                }
              }
            }
            return true;
        """
      }
    }
  ]
}
```

You can also specify a [stored script](../../../explore-analyze/scripting/modules-scripting-store-and-retrieve.md) as the `if` condition.

```console
PUT _scripts/my-prod-tag-script
{
  "script": {
    "lang": "painless",
    "source": """
      Collection tags = ctx.tags;
      if(tags != null){
        for (String tag : tags) {
          if (tag.toLowerCase().contains('prod')) {
            return false;
          }
        }
      }
      return true;
    """
  }
}

PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that don't contain 'prod' tag",
        "if": { "id": "my-prod-tag-script" }
      }
    }
  ]
}
```

Incoming documents often contain object fields. If a processor script attempts to access a field whose parent object does not exist, {{es}} returns a `NullPointerException`. To avoid these exceptions, use [null safe operators](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator), such as `?.`, and write your scripts to be null safe.

For example, `ctx.network?.name.equalsIgnoreCase('Guest')` is not null safe. `ctx.network?.name` can return null. Rewrite the script as `'Guest'.equalsIgnoreCase(ctx.network?.name)`, which is null safe because `Guest` is always non-null.

If you can’t rewrite a script to be null safe, include an explicit null check.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that contain 'network.name' of 'Guest'",
        "if": "ctx.network?.name != null && ctx.network.name.contains('Guest')"
      }
    }
  ]
}
```


## Conditionally apply pipelines [conditionally-apply-pipelines]

Combine an `if` condition with the [`pipeline`](elasticsearch://reference/enrich-processor/pipeline-processor.md) processor to apply other pipelines to documents based on your criteria. You can use this pipeline as the [default pipeline](ingest-pipelines.md#set-default-pipeline) in an [index template](../../data-store/templates.md) used to configure multiple data streams or indices.

```console
PUT _ingest/pipeline/one-pipeline-to-rule-them-all
{
  "processors": [
    {
      "pipeline": {
        "description": "If 'service.name' is 'apache_httpd', use 'httpd_pipeline'",
        "if": "ctx.service?.name == 'apache_httpd'",
        "name": "httpd_pipeline"
      }
    },
    {
      "pipeline": {
        "description": "If 'service.name' is 'syslog', use 'syslog_pipeline'",
        "if": "ctx.service?.name == 'syslog'",
        "name": "syslog_pipeline"
      }
    },
    {
      "fail": {
        "description": "If 'service.name' is not 'apache_httpd' or 'syslog', return a failure message",
        "if": "ctx.service?.name != 'apache_httpd' && ctx.service?.name != 'syslog'",
        "message": "This pipeline requires service.name to be either `syslog` or `apache_httpd`"
      }
    }
  ]
}
```


## Get pipeline usage statistics [get-pipeline-usage-stats]

Use the [node stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) API to get global and per-pipeline ingest statistics. Use these stats to determine which pipelines run most frequently or spend the most time processing.

```console
GET _nodes/stats/ingest?filter_path=nodes.*.ingest
```
