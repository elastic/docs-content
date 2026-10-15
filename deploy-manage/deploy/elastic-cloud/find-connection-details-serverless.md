---
navigation_title: Project connection details
description: Find your Elasticsearch endpoint, Cloud ID, and API key so that clients and tools can connect to your Elastic Cloud Serverless project.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Find your {{serverless-short}} project connection details [serverless-connection-details]

::::{note}
This page is for {{serverless-full}} projects. If you're using an {{ech}} deployment, refer to [](find-cloud-id.md).
::::

When you connect clients and tools to an {{serverless-full}} project, these are the main connection details you'll work with:

**{{es}} endpoint**
:   The HTTPS URL you use to send requests to your project. Most clients, SDKs, and integrations connect with this URL plus an API key.

**API key**
:   Authenticates the client to your project. {{serverless-short}} does not support username and password authentication for these connections.

**Cloud ID**
:   A unique, encoded string that represents your project's {{es}} endpoint (and, where applicable, {{kib}} endpoint) in a compact form. Compatible clients can use it instead of configuring host URLs individually: the client resolves those endpoints from the Cloud ID.


## Find your {{es}} endpoint [_find_elasticsearch_endpoint]

You can copy your endpoint from the {{ecloud}} Console, or from {{kib}}. Use whichever fits your workflow: the Console route doesn't require you to open {{kib}}.

{applies_to}`elasticsearch: ga` In {{es-serverless}} projects, the **Get started with {{es}}** page also shows the endpoint directly.

### From the {{ecloud}} Console [_find_endpoint_console]

:::{include} _snippets/find-endpoint-serverless-console.md
:::

:::{admonition} Other endpoints in this panel
The **Application endpoints, cluster and component IDs** area also lists endpoints for other applications, such as {{kib}} and, depending on the project type, {{fleet}} or OpenTelemetry (OTLP), along with your project ID and component IDs. To connect clients and tools to {{es}}, use the **{{es}} endpoint**.
:::

### From {{kib}} [_find_endpoint_kibana]

1. Open the **Connection details** panel in one of these ways:

    * Select the **Help menu** {icon}`question`, and then select **Connection details**.
    * Select the project selector in the header, and then select **Connection details**.

2. On the **Endpoints** tab, copy the **{{es}} endpoint**.

    :::{image} /solutions/images/kibana-connection-details-endpoints.png
    :alt: The Connection details panel showing the Elasticsearch endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
    :screenshot:
    :width: 50%
    :::

## Find your Cloud ID [_find_cloud_id]

The Cloud ID is available in {{kib}} only. You need it only for [{{beats}}](beats://reference/index.md) and [{{ls}}](logstash://reference/index.md), which can use it in place of the endpoint URL. All other clients and tools use the endpoint.

1. In {{kib}}, open the **Connection details** panel from the **Help menu** {icon}`question` or the project selector in the header.
2. Turn on **Show Cloud ID**, then copy the value.

## Create an API key [_create_api_key]

You can create an API key in the **API key** tab of the [**Connection details** panel](#_find_endpoint_kibana).

Alternatively, you can also create an API key from your project's **API keys** page, which you can access from the navigation menu or with the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For detailed steps, including how to restrict a key's privileges and how to update or delete keys, refer to [](/deploy-manage/api-keys/serverless-project-api-keys.md).

### {{ecloud}} API keys [_cloud_api_key]

Keys created in your project work with that project only. If you want one key to work across several projects, or to manage keys centrally, create an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) in the {{ecloud}} Console instead.

{{ecloud}} API keys manage your organization, deployments, and projects. To also use one in place of a project API key, grant it [{{es}} and {{kib}} API access](/deploy-manage/api-keys/elastic-cloud-api-keys.md#project-access) for the relevant projects.

## Next steps [_next_steps]

After you have your project's connection details, [send a test request](/solutions/elasticsearch-solution-project/search-connection-details.md#elasticsearch-get-started-test-connection) to confirm that your endpoint and API key work, then use them to configure a client or data shipper. Explore these pages:

* [Beats for {{es-serverless}}](beats://reference/serverless/beats.md): Configure Beats to send logs, metrics, and other data using your {{es}} endpoint and API key.
* [Sending data to {{es-serverless}}](logstash://reference/connecting-to-serverless.md): Configure {{ls}} to send data to your project.
* [](/reference/fleet/install-elastic-agents.md): Collect and ship data with {{agent}} and Fleet.
* [](/reference/elasticsearch-clients/index.md): Connect applications to your project with an official client library.
* [](/manage-data/ingest.md): Browse other ingest options, from APIs and connectors to OpenTelemetry.
