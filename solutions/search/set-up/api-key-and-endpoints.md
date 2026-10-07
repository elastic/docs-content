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

## Find your {{es}} endpoint [find-your-elasticsearch-endpoint]

::::{include} /solutions/elasticsearch-solution-project/_snippets/find-elasticsearch-endpoint.md
::::

## Create an API key [create-an-api-key]

To create an API key, you need the `manage_api_key` or the `manage_own_api_key` cluster privilege.

::::{include} /solutions/elasticsearch-solution-project/_snippets/create-an-api-key.md
::::

For key types, privileges, and expiration options, refer to [](/deploy-manage/api-keys.md).

## Next step [api-key-and-endpoints-next]

After you have an endpoint and an API key, connect a language client in [](/solutions/search/set-up/connect-through-an-sdk.md).
