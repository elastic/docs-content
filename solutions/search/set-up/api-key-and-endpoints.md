---
applies_to:
  stack:
  serverless:
navigation_title: API key and endpoints
description: Find your Elasticsearch endpoint and create an API key so you can connect a search client.
type: how-to
---

# Get your API key and endpoints [get-your-api-key-and-endpoints]

To connect a client to {{es}} for search, you need the endpoint URL and an API key. The steps depend on where your deployment runs.

:::{include} /solutions/elasticsearch-solution-project/_snippets/deployment-tab-legend.md
:::

## Find your {{es}} endpoint [find-your-elasticsearch-endpoint]

:::{include} /solutions/elasticsearch-solution-project/_snippets/find-elasticsearch-endpoint.md
:::

## Get your API key [get-your-api-key]

If you just created an {{es}} {{vectordb}} project or an {{es}} project, a generated API key is on the **Getting started** {icon}`rocket` page.

Otherwise, create an API key:

:::{include} /solutions/elasticsearch-solution-project/_snippets/create-an-api-key.md
:::

## Next step [api-key-and-endpoints-next]

After you have an endpoint and an API key, connect a language client in [](/solutions/search/set-up/connect-through-an-sdk.md).
