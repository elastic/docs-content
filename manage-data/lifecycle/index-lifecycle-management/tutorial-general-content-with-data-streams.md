---
applies_to:
  stack: ga
products:
  - id: elasticsearch
---


# Manage general content with data streams [manage-general-content-with-data-streams]

Data streams are specifically designed for time series data.
If you want to manage general content (data without timestamps) with data streams, you can set up [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) to transform and enrich your general content by adding a timestamp field at [ingest](/manage-data/ingest.md) time and get the benefits of time-based data management.

For example, search use cases such as knowledge base, website content, e-commerce, or product catalog search, might require you to frequently index general content (data without timestamps). As a result, your index can grow significantly over time, which might impact storage requirements, query performance, and cluster health. Following the steps in this procedure (including a timestamp field and moving to ILM-managed data streams) can help you rotate your indices in a simpler way, based on their size or lifecycle phase.

To roll over your general content from indices to a data stream, you:

1. [Create an ingest pipeline](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-ingest) to process your general content and add a `@timestamp` field.

1. [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-policy) that meets your requirements.

1. [Create an index template](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-template) that uses the created ingest pipeline and lifecycle policy.

1. [Create a data stream](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-create-stream).

1. *Optional:* If you have an existing, non-managed index and want to migrate your data to the data stream you created, [reindex with a data stream](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-reindex).

1. [Update your ingest endpoint](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md#manage-general-content-with-data-streams-endpoint) to target the created data stream.

1. *Optional:* You can use the [ILM explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle) to get status information for your managed indices.
For more information, refer to [Check lifecycle progress](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-check-progress).


## Create an ingest pipeline to transform your general content [manage-general-content-with-data-streams-ingest]

You can create an ingest pipeline that uses the [`set` enrich processor](elasticsearch://reference/enrich-processor/set-processor.md) to add a `@timestamp` field in Kibana or with the [create or update a pipeline](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) API.

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To add an ingest pipeline from {{kib}}, go to **Stack Management > Ingest Pipelines**. From the upper right, select **Create pipeline > New pipeline**.

Configure the pipeline with a name, description, and a **Set** processor that adds the `@timestamp` field with a value of `{{_ingest.timestamp}}`.

:::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-general-content-ingest.png
:alt: Create ingest pipeline
:screenshot:
:::

:::

:::{tab-item} API
:sync: api
Use the API to add an ingest pipeline:

```console
PUT _ingest/pipeline/ingest_time_1
{
  "description": "Add an ingest timestamp",
   "processors": [
    {
      "set": {
        "field": "@timestamp",
        "value": "{{_ingest.timestamp}}"
      }
    }]
}
```
:::
::::

## Create a lifecycle policy [manage-general-content-with-data-streams-policy]

A lifecycle policy specifies the phases in the index lifecycle and the actions to perform in each phase. A lifecycle can have up to five phases: `hot`, `warm`, `cold`, `frozen`, and `delete`.

For example, you might define a policy named `indextods` that is configured to roll over when the shard size reaches 10 GB.

You can create the policy in {{kib}} or with the [create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API. 

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To create the policy from {{kib}}, open the menu and go to **Stack Management > Index Lifecycle Policies**. Click **Create policy**.

In the **Hot phase**, by default, an ILM-managed index [rolls over](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) when either:
* It reaches 30 days of age.
* One or more primary shards reach 50 GB in size.
  
Disable **Use recommended defaults** to adjust these values and roll over when the primary shard reaches 10GB.

:::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-rollover-general-content-create-policy.png
:alt: Create policy page
:screenshot:
:::
:::

:::{tab-item} API
:sync: api
Use the API to create a lifecyle policy:
```console
PUT _ilm/policy/indextods
{
  "policy": {
    "phases": {
      "hot": {
       "min_age": "0ms",
        "actions": {
          "set_priority": {
            "priority": 100
          },
          "rollover": {
           "max_primary_shard_size": "10gb"
          }
        }
      }
    }
  }
}
```
:::
::::

For more information about lifecycle phases and available actions, refer to [Create a lifecycle policy](configure-lifecycle-policy.md#ilm-create-policy).


## Create an index template to apply the ingest pipeline and lifecycle policy [manage-general-content-with-data-streams-template]

To use the created lifecycle policy, you configure an index template that uses it.
When creating the index template, specify the following details:
* the name of the lifecycle policy, which in our example is `indextods`
* the ingest pipeline that enriches the data by adding the `@timestamp` field, which in our example is `ingest_time_1`
* that the template is data stream enabled by including the `data_stream` definition
* the index pattern, which ensures that this template will be applied to matching indices and in our example is `movetods` 

Use the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to create an index template that uses the created ingest pipeline and lifecycle policy:

```console
PUT _index_template/index_to_dot
{
  "template": {
    "settings": {
      "index": {
        "lifecycle": {
          "name": "indextods"
        },
        "default_pipeline": "ingest_time_1"
      }
    },
    "mappings": {
      "_source": {
        "excludes": [],
        "includes": [],
        "enabled": true
      },
      "_routing": {
        "required": false
      },
      "dynamic": true,
      "numeric_detection": false,
      "date_detection": true,
      "dynamic_date_formats": [
        "strict_date_optional_time",
        "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
      ]
    }
  },
  "index_patterns": [
    "movetods"
  ],
  "data_stream": {
    "hidden": false,
    "allow_custom_routing": false
  }
}
```

To create an index template in Kibana, open the main menu and go to **Stack Management > Index Management**. In the **Index Templates** view, click **Create template**.
Refer to [Manage index templates](/manage-data/data-store/index-basics.md#index-management-manage-index-templates) for more information about configuring templates in Kibana.

## Create a data stream [manage-general-content-with-data-streams-create-stream]

Create a data stream using the [_data_stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream):

```console
PUT /_data_stream/movetods
```

You can [view the lifecycle status of your data stream](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md), including details about its associated ILM policy.

### Optional: Reindex your data with a data stream [manage-general-content-with-data-streams-reindex]

If you want to copy your documents from an existing index to the data stream you created, reindex with a data stream using the [_reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex):

```console
POST /_reindex
{
  "source": {
    "index": "indextods"
  },
  "dest": {
    "index": "movetods",
    "op_type": "create"
    
  }
}
```

For more information, check [Reindex with a data stream](../../data-store/data-streams/use-data-stream.md#reindex-with-a-data-stream).

## Update your ingest endpoint to target the created data stream [manage-general-content-with-data-streams-endpoint]

If you use Elastic clients, scripts, or any other third party tool to ingest data to {{es}}, make sure you update these to use the created data stream.