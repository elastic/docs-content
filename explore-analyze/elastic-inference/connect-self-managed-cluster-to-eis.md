---
navigation_title: EIS for self-managed clusters
applies_to:
  stack: ga 9.3
  deployment:
    self: ga
    ece: ga
    eck: ga
---

# EIS for self-managed clusters

Elastic {{infer-cap}} Service (EIS) for self-managed clusters is available through [Cloud Connect](/deploy-manage/cloud-connect.md). Cloud Connect enables you to use {{ecloud}} services in your self-managed cluster without having to install and maintain their infrastructure yourself.

You can use EIS for [semantic search](/solutions/search/semantic-search.md), [AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md) and [AI Agent](/explore-analyze/ai-features/elastic-agent-builder.md), [Search Playground](/explore-analyze/query-filter/tools/playground.md), [Attack Discovery](/solutions/security/ai/attack-discovery.md), and [SIEM migrations](/solutions/security/get-started/automatic-migration.md).

## Prerequisites

Before you can use EIS with your self-managed cluster, ensure you meet the following requirements:

* Your self-managed cluster is on an [Enterprise self-managed license]({{subscriptions}}) or an [active self-managed trial](https://cloud.elastic.co/registration)
* You have an {{ecloud}} account with either an [active Cloud Trial](https://cloud.elastic.co/registration) or [billing information configured](/deploy-manage/cloud-organization/billing/add-billing-details.md)

## Set up EIS with Cloud Connect

To set up EIS for your self-managed cluster with Cloud Connect:

:::::::{stepper}
::::::{step} Open Cloud Connect
In your self-managed cluster, navigate to the **Cloud Connect** page using the [search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/cloud-connect-eis.png
:screenshot:
:alt: Screenshot showing Cloud Connect page
:::

::::::

::::::{step} Get your Cloud Connect API key
Sign up or log in to {{ecloud}} and get the Cloud Connect API key:

- If you already have an {{ecloud}} account, click **Log in**.
- If you don’t have an account yet, click **Sign up** and follow the prompts to create your account and start a free trial.
::::::

::::::{step} Connect EIS
Copy the Cloud Connect API key, paste it into your self-managed cluster's Cloud Connect page, then click **Connect**.

::::::

::::::{step} Enable Elastic {{infer-cap}} Service
On the **Cloud connected services** page, click **Connect** for Elastic {{infer}} Service.

:::{image} /explore-analyze/images/eis-cloud-connect-connect-ui.png
:screenshot:
:alt: Screenshot showing Cloud Connect and EIS 
:::

::::::

::::::

:::::::

After you connect Elastic {{infer-cap}} Service through Cloud Connect, {{es}} automatically creates multiple {{infer}} endpoints for search and chat use cases, along with corresponding {{kib}} AI connectors. Supported {{kib}} features use these connectors out of the box.

## Test EIS with semantic search

In this example, you’ll create an index with a `semantic_text` field, index a document, then run a query that returns a semantically related match. 

In **{{dev-tools-app}}**, run the following requests:

1. Create an index with a `semantic_text` field:

```console
PUT /semantic-search-eis
{
  "mappings": {
    "properties": {
      "text": {
        "type": "semantic_text"
      }
    }
  }
}
```

2. Index a document:

```console
POST /semantic-search-eis/_doc
{
  "text": "Aberdeen Football Club"
}
```

3. Run a search query:

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

## Regions and billing

For information about EIS regions and request routing, refer to the [Region and hosting](eis.md#eis-regions).

EIS is billed per million tokens. For details on pricing and usage tracking, refer to [Pricing](eis.md#pricing) and [Monitor your token usage](eis.md#monitor-your-token-usage).

