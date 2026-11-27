---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
description: Create an Elasticsearch ingest pipeline in Kibana or with the API, test it with sample documents, and track its versions.
type: how-to
---

# Create and test an ingest pipeline

An ingest pipeline consists of a series of [processors](elasticsearch://reference/ingest-processor/index.md) that transform a document before {{es}} indexes it. This page describes how to create a pipeline and test it with sample documents before you can apply it to your data.

## Before you begin [ingest-prerequisites]


Before you create a pipeline, check the following:

* In ECH, ECE, ECK, and self-managed clusters, make sure at least one node has the `ingest` role, because pipelines run on those nodes. Nodes have this role by default, so you only need to act if you've customized node roles. For heavy ingest loads, consider dedicated ingest nodes. To learn how to manage node roles, refer to [](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md). In {{serverless-full}} projects, {{es}} manages this for you, so no node configuration is needed.
* If the {{es}} security features are enabled, make sure you have the following [cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster):
  * `manage_pipeline`, to create, edit, and delete pipelines.
  * `monitor`, to use {{kib}}'s **Ingest Pipelines** feature.
* If your pipeline uses a processor that depends on another resource, set up that resource first. For example, the [`enrich`](elasticsearch://reference/ingest-processor/enrich-processor.md) processor needs an enrich policy, as described in [](/manage-data/ingest/transform-enrich/set-up-an-enrich-processor.md), and the [`inference`](elasticsearch://reference/ingest-processor/inference-processor.md) processor needs a deployed model or inference endpoint. Check the reference page of each processor you plan to use for any setup it requires.

## Create a pipeline [create-manage-ingest-pipelines]

You can create and manage pipelines in {{kib}} or with the [ingest APIs]({{es-apis}}group/endpoint-ingest).

:::::{tab-set}
:group: ingest-pipelines-ui-api

::::{tab-item} {{kib}}
:sync: kibana

1. Find **Ingest Pipelines** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create pipeline** → **New pipeline**.
3. Enter a name for the pipeline and, optionally, a description.
4. Select **Add a processor**, choose a processor, and configure it. Repeat for each processor you want to add. Processors run in the order they're listed.
5. Click **Create pipeline**.

If you want to map custom data to the [Elastic Common Schema (ECS)](ecs://reference/index.md), select **Create pipeline** → **New pipeline from CSV** instead. You provide a CSV that describes the mapping, and {{kib}} creates the pipeline from it. Mapping your data to ECS gives it the same field names as other ECS data, so you can use the same queries, dashboards, and visualizations across datasets. To get started, refer to [Map custom data to ECS](ecs://reference/ecs-converting.md).

From the list view, you can view your pipelines and drill down into details, edit or copy existing pipelines, and delete pipelines.

:::{image} /manage-data/images/elasticsearch-reference-ingest-pipeline-list.png
:alt: Kibana's Ingest Pipelines list view
:screenshot:
:::
::::

::::{tab-item} API
:sync: api

Use the [create pipeline API]({{es-apis}}operation/operation-ingest-put-pipeline) to create or update a pipeline. The following request creates a pipeline containing two [`set`](elasticsearch://reference/ingest-processor/set-processor.md) processors followed by a [`lowercase`](elasticsearch://reference/ingest-processor/lowercase-processor.md) processor. The processors run sequentially in the order you specify.

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
::::

:::::

## Test a pipeline [test-pipeline]

Test a pipeline with sample documents to confirm that it changes your documents the way you expect, before you apply it to real data.

:::::{tab-set}
:group: ingest-pipelines-ui-api

::::{tab-item} {{kib}}
:sync: kibana

1. While you create or edit a pipeline, click **Add documents**.
2. In the **Documents** tab, enter your sample documents.
3. Click **Run the pipeline**.

:::{image} /manage-data/images/elasticsearch-reference-test-a-pipeline.png
:alt: Test a pipeline in Kibana
:screenshot:
:::
::::

::::{tab-item} API
:sync: api

Use the [simulate pipeline API]({{es-apis}}operation/operation-ingest-simulate) to test a pipeline without indexing any documents. To test a pipeline you already created, specify it in the request path. The following request tests `my-pipeline`.

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

To try processors before you save a pipeline, specify the pipeline and its processors in the request body instead.

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

The API returns the transformed documents. In this response, the `lowercase` processor changed the value of `my-keyword-field` in each document to lowercase.

```console-result
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_version": "-3",
        "_source": {
          "my-keyword-field": "foo" <1>
        },
        "_ingest": {
          "timestamp": "2099-03-07T11:04:03.000Z" <2>
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
1. The `lowercase` processor changed `FOO` to `foo`. The second document changed from `BAR` to `bar`.
2. The `_ingest.timestamp` metadata field records when {{es}} received the document.

If a processor fails, the API returns an `error` object for that document instead of the transformed document. In the following request, the `lowercase` processor fails because the document doesn't contain `my-keyword-field`.

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
        "my-other-field": "FOO"
      }
    }
  ]
}
```

```console-result
{
  "docs": [
    {
      "error": {
        "root_cause": [
          {
            "type": "illegal_argument_exception",
            "reason": "field [my-keyword-field] not present as part of path [my-keyword-field]"
          }
        ],
        "type": "illegal_argument_exception",
        "reason": "field [my-keyword-field] not present as part of path [my-keyword-field]"
      }
    }
  ]
}
```

To handle failures like this one in a pipeline, refer to [Error handling](/manage-data/ingest/transform-enrich/error-handling.md).
::::

:::::

## Manage pipeline versions [manage-pipeline-versions]

Version a pipeline when more than one person or tool updates it, so you can track changes and avoid overwriting each other's work. When you create or update a pipeline with the API, you can specify an optional `version` integer to track changes to the pipeline. You can use this version number with the [`if_version`]({{es-apis}}operation/operation-ingest-put-pipeline#put-pipeline-api-query-params) parameter to update a pipeline only if its current version matches. This prevents you from overwriting a change that someone else made. When the `if_version` parameter is specified, a successful update increments the pipeline's version.

```console
PUT _ingest/pipeline/my-pipeline-id
{
  "version": 1,
  "processors": [ ... ]
}
```

To unset the `version` number using the API, replace or update the pipeline without specifying the `version` parameter.

## Next steps

To finish setting up your pipeline, [apply it to your data](/manage-data/ingest/transform-enrich/apply-ingest-pipelines.md). A pipeline doesn't process any documents until you tell {{es}} to run it.

To make your pipeline more precise, more resilient, and easier to monitor, or to learn from a complete example, you can:

* Use [document fields in processor settings](/manage-data/ingest/transform-enrich/access-data-in-processors.md), to copy a value, combine values, or route a document.
* Run processors [only for documents that meet a condition](/manage-data/ingest/transform-enrich/conditionally-run-ingest-processors.md), so each processor works only on the documents that need it.
* Add [error handling](/manage-data/ingest/transform-enrich/error-handling.md), so a document can still be indexed when a processor fails.
* [Monitor and troubleshoot](/troubleshoot/elasticsearch/troubleshoot-ingest-pipelines.md) the pipeline, to find slow or failing processors once it's processing data.
* Follow the [Parse logs](/manage-data/ingest/transform-enrich/example-parse-logs.md) example, to see a complete pipeline built step by step.
