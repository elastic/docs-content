---
applies_to:
  stack:
  serverless:
navigation_title: API key and endpoints
description: Find your {{es}} endpoint and create an API key so you can connect a search client.
type: how-to
---

# Get your {{es}} endpoint and API key [get-your-api-key-and-endpoints]

If you want to work with {{es}} programmatically, you need an endpoint URL and an API key. This page shows how to find the endpoint and create an API key for each deployment type.

## Before you begin

* You need access to your deployment or project, such as an {{es}} {{vectordb}} project, an {{es}} project, or an {{ech}} deployment. If you don't have one yet, refer to [](/solutions/search/set-up/get-elasticsearch-running-for-search.md).
* To create an API key, you need the `manage_api_key` or the `manage_own_api_key` cluster privilege. If you created the deployment or project, you already have this privilege. If you sign in as a different user, an administrator needs to grant it. In this case, refer to [](/deploy-manage/users-roles.md).

## Find your {{es}} endpoint [find-your-elasticsearch-endpoint]

The {{es}} endpoint is the URL your client uses to send requests. Where you find it depends on your deployment type. The following steps show you where to copy it.

:::{include} /solutions/elasticsearch-solution-project/_snippets/find-elasticsearch-endpoint.md
:::

## Create an API key [get-your-api-key]

:::{include} /solutions/elasticsearch-solution-project/_snippets/create-an-api-key.md
:::

:::{tip}
If you just created a {{serverless-short}} project, the **Getting started** {icon}`rocket` page shows a generated API key that you can copy immediately. If you have navigated away from that page, create a new API key as described above.
:::

## Next step [api-key-and-endpoints-next]

After you have an endpoint and an API key, connect a language client in [](/solutions/search/set-up/connect-with-an-sdk.md).
