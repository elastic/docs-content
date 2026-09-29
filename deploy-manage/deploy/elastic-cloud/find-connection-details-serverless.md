---
navigation_title: Project connection details
description: Find your Elasticsearch endpoint, Cloud ID, and API key so that clients and tools can connect to your Elastic Cloud Serverless project.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Find your project connection details [serverless-connection-details]

When you connect clients and tools to an {{serverless-full}} project, these are the main connection details you'll work with:

**{{es}} endpoint**
:   The HTTPS URL you use to send requests to your project. Most clients, SDKs, and integrations connect with this URL plus an API key.

**API key**
:   Authenticates the client to your project. {{serverless-short}} does not support username and password authentication for these connections.

**Cloud ID**
:   A unique, encoded string that represents your project's {{es}} endpoint (and, where applicable, {{kib}} endpoint) in a compact form. Compatible clients can use it instead of configuring host URLs individually: the client resolves those endpoints from the Cloud ID.


[{{beats}}](beats://reference/index.md) and [{{ls}}](logstash://reference/index.md) can use a Cloud ID instead of the endpoint URL. All other clients and tools use the endpoint.

## Find your {{es}} endpoint and Cloud ID [_find_elasticsearch_endpoint]

{applies_to}`elasticsearch: ga` In {{es-serverless}} projects, the **Get started with {{es}}** page shows the {{es}} endpoint directly, so you can copy it from there.

Your endpoint is available in the **Connection details** panel in {{kib}}. 

:::::{stepper}

::::{step} Open the Connection details panel
:anchor: open-connection-details

Open your {{serverless-short}} project, then open the panel in one of these ways:

* Select the **Help menu** {icon}`question`, and then select **Connection details**.
* Select the project selector in the header, and then select **Connection details**.
::::

::::{step} Copy the {{es}} endpoint
From the **Endpoints** tab, copy the **{{es}} endpoint**.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the Elasticsearch endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::
::::

::::{step} Copy the Cloud ID
Turn on **Show Cloud ID**, then copy the value.
::::

:::::


:::{admonition} Other endpoints available in the Cloud UI
Your project also exposes endpoints for other applications, such as {{kib}} and, depending on the project type, {{fleet}} or OpenTelemetry (OTLP). To view them, open the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), select **Manage** next to your project, and find the **Application endpoints, cluster and component IDs** area on your project's **Overview** page. That area also lists your project ID and component IDs. To connect clients and tools to {{es}}, use the **{{es}} endpoint**.
:::

## Create an API key [_create_api_key]

You can create an API key in the **API key** tab of the [**Connection details** panel](#open-connection-details).

Alternatively, you can also create an API key from your project's **API keys** page, which you can access from the navigation menu or with the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For detailed steps, including how to restrict a key's privileges and how to update or delete keys, refer to [](/deploy-manage/api-keys/serverless-project-api-keys.md).

### {{ecloud}} API keys [_cloud_api_key]

Keys created in your project work with that project only. If you want one key to work across several projects, or to manage keys centrally, create an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) in the {{ecloud}} Console instead.

{{ecloud}} API keys manage your organization, deployments, and projects. To also use one in place of a project API key, grant it [{{es}} and {{kib}} API access](/deploy-manage/api-keys/elastic-cloud-api-keys.md#project-access) for the relevant projects.

## Next steps [_next_steps]

After you have your project's connection details, use them to configure a client or data shipper. Explore these pages:

* [Beats for {{es-serverless}}](beats://reference/serverless/beats.md): Configure Beats to send logs, metrics, and other data using your {{es}} endpoint and API key.
* [Sending data to {{es-serverless}}](logstash://reference/connecting-to-serverless.md): Configure {{ls}} to send data to your project.
* [](/reference/fleet/install-elastic-agents.md): Collect and ship data with {{agent}} and Fleet.
* [](/reference/elasticsearch-clients/index.md): Connect applications to your project with an official client library.
* [](/manage-data/ingest.md): Browse other ingest options, from APIs and connectors to OpenTelemetry.

## Related pages [_related_pages]

* [](/solutions/elasticsearch-solution-project/search-connection-details.md): Connection details across deployment types, including {{ech}} and self-managed.
* [Find your Cloud ID](find-cloud-id.md): Cloud ID for {{ech}} deployments.