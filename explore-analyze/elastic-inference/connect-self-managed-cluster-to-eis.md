---
navigation_title: EIS for self-managed clusters
applies_to:
  stack: ga 9.3
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Use Elastic Inference Service (EIS) with your self-managed, ECE, and ECK clusters through Cloud Connect.
---

# Elastic {{infer-cap}} Service for self-managed clusters

[Elastic {{infer-cap}} Service (EIS)](eis.md) is available with zero setup on Elastic Cloud Hosted and Serverless deployments. To use EIS with other deployment types, you can use [Cloud Connect](/deploy-manage/cloud-connect.md). Cloud Connect enables you to use {{ecloud}} services in your self-managed cluster without having to install and maintain their infrastructure yourself.

You can use EIS to enable features such as:

- [Semantic search](/solutions/search/semantic-search.md)
- [AI Assistants](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md)
- [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md)
- [Attack Discovery](/solutions/security/ai/attack-discovery.md)

For a full list of EIS-powered features, refer to [AI features powered by EIS](/explore-analyze/elastic-inference/eis.md#ai-features-powered-by-eis).

## Prerequisites

Before you can use EIS with your self-managed cluster, ensure you meet the following requirements:

* Your self-managed cluster is on an [Enterprise self-managed license]({{subscriptions}}) or an [active self-managed trial license](https://cloud.elastic.co/registration)
* You have an {{ecloud}} account with either an [active Cloud Trial](https://cloud.elastic.co/registration) or [billing information configured](/deploy-manage/cloud-organization/billing/add-billing-details.md)

## Set up EIS with Cloud Connect


:::::::{stepper}
::::::{step} Open Cloud Connect
In your self-managed {{kib}} instance, navigate to the **Cloud Connect** page using the [search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/cloud-connect-eis.png
:screenshot:
:alt: Screenshot showing Cloud Connect page
:::

::::::

::::::{step} Get your Cloud Connect API key
Sign up or log in to {{ecloud}} and get the Cloud Connect API key:

- If you don’t have an account yet, click **Sign up** and follow the prompts to create your account and start a free Cloud Trial.
- If you already have an {{ecloud}} account, click **Log in**.
::::::

::::::{step} Connect your cluster
Copy the Cloud Connect API key, paste it into your self-managed cluster's Cloud Connect page, then click **Connect**.

::::::

::::::{step} Enable Elastic Inference Service
On the **Cloud connected services** page, click **Connect** for Elastic {{infer-cap}} Service.

:::{image} /explore-analyze/images/eis-cloud-connect-connect-ui.png
:screenshot:
:alt: Screenshot showing Cloud Connect and EIS 
:::

::::::

::::::

:::::::

After you connect Elastic {{infer-cap}} Service through Cloud Connect, {{es}} automatically creates multiple {{infer}} endpoints for search and chat use cases, along with corresponding {{kib}} AI connectors. Supported {{kib}} features now use these connectors automatically.

## Test EIS through Cloud Connect with semantic search

In this example, you create an index with a `semantic_text` field, index a document, then run a query that returns a semantically related match. 

In **{{dev-tools-app}}**, run the following requests:

:::::::{stepper}
::::::{step} Create an index with a `semantic_text` field

```console
PUT /semantic-search-eis
{
  "mappings": {
    "properties": {
      "text": {
        "type": "semantic_text" <1>
      }
    }
  }
}
```

1. Because you already enabled EIS, the `semantic_text` field type uses EIS through the default {{infer}} endpoint (`.elser-2-elastic`). To learn more, refer to [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md).

::::::

::::::{step} Index a document

```console
POST /semantic-search-eis/_doc
{
  "text": "Aberdeen Football Club"
}
```

::::::

::::::{step} Run a search query

```console
GET /semantic-search-eis/_search
{
  "query": {
    "match": {
      "text": "soccer"
    }
  }
}
```

::::::
:::::::

The response should include the indexed document:

```json
{
  "took": 161,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.729913,
    "hits": [
      {
        "_index": "semantic-search-eis",
        "_id": "oyH935sBG2FaZ-zOMrer",
        "_score": 4.729913,
        "_source": {
          "text": "Aberdeen Football Club"
        }
      }
    ]
  }
}
```

## Supported models with EIS through Cloud Connect

Using Elastic {{infer-cap}} Service through Cloud Connect, you have access to all available models listed under [Supported models](/explore-analyze/elastic-inference/eis.md#supported-models), including LLMs, embedding models, and rerankers.

To use these models, you need [{{kib}} connectors](kibana://reference/connectors-kibana.md) (for LLMs) or [{{infer}} endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference). There are preconfigured {{infer}} endpoints for all models. For some LLMs, connectors need to be created manually, depending on the model.

### LLMs 

For the Claude 3.7 and Claude 4.5 models, connectors are preconfigured and ready to be used.

To use other LLMs listed under [Supported models](/explore-analyze/elastic-inference/eis.md#supported-models), you must [create the {{kib}} connectors](kibana://reference/connectors-kibana.md#creating-new-connector) manually. The corresponding {{infer}} endpoints are preconfigured.

### Embedding and rerank models

Predefined {{infer}} endpoints and connectors are available for all models listed under [Embedding models](/explore-analyze/elastic-inference/eis.md#embedding-models) and [Rerankers](/explore-analyze/elastic-inference/eis.md#rerankers).

For these models, you only need to create new {{infer}} endpoints if you want to use custom settings.

## Regions and billing

For information about EIS regions and request routing, refer to [Region and hosting](eis.md#eis-regions).

EIS is billed per million tokens and consumes ECUs. For details on pricing and usage tracking, refer to [Pricing](eis.md#pricing) and [Monitor your token usage](eis.md#monitor-your-token-usage).

