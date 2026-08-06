---
navigation_title: Project connection details
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Find your project connection details [serverless-connection-details]

When you connect clients and tools to a {{serverless-full}} project, these are the main connection details you'll work with:

**{{es}} endpoint**
:   The HTTPS URL you use to send requests to your project. Most clients, SDKs, and integrations connect with this URL plus an API key.

**API key**
:   Authenticates the client to your project. {{serverless-short}} does not support username and password authentication for these connections.

**Cloud ID**
:   A unique, encoded string that represents your project's {{es}} endpoint (and, where applicable, {{kib}} endpoint) in a compact form. Compatible clients can use it instead of configuring host URLs individually: the client resolves those endpoints from the Cloud ID.

## Find your {{es}} endpoint and Cloud ID [_find_elasticsearch_endpoint]

1. Open your {{serverless-short}} project.
2. Select the **Help** icon in the upper right corner, and then select **Connection Details**.
3. From the **Endpoints** tab, copy the **{{es}} endpoint**.

    :::{image} /solutions/images/kibana-serverless-connection-details.png
    :alt: Connection Details flyout showing the Elasticsearch endpoint for a serverless project
    :screenshot:
    :::

4. To copy the **Cloud ID**, enable **Show Cloud ID**, then copy the value.

## Create an API key [_create_api_key]

You can create an API key from your project's home page, or open the **API keys** page from the navigation menu or with the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For steps, privileges, and key types, refer to [Serverless project API keys](/deploy-manage/api-keys/serverless-project-api-keys.md).

## Next steps [_next_steps]

After you have your project's connection details, use them to configure a client or data shipper. Explore these pages:

* [Beats for {{es-serverless}}](beats://reference/serverless/beats.md): Configure Beats to send logs, metrics, and other data using your {{es}} endpoint and API key.
* [Sending data to {{es-serverless}}](logstash://reference/connecting-to-serverless.md): Configure {{ls}} to send data to your project.
* [Install {{agent}}](/reference/fleet/install-elastic-agents.md): Collect and ship data with {{agent}} and Fleet.
* [{{es}} language clients](/reference/elasticsearch-clients/index.md): Connect applications to your project with an official client library.
* [Ingest: Bring your data to Elastic](/manage-data/ingest.md): Browse other ingest options, from APIs and connectors to OpenTelemetry.

