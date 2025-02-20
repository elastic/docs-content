---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-cloud-ingest-data.html
  - https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-your-data.html
  - https://www.elastic.co/customer-success/data-ingestion
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-ingestion-overview.html
  - https://www.elastic.co/guide/en/ingest-overview/current/ingest-intro.html
---

# Ingestion

Bring your data! Whether you call it *adding*, *indexing*, or *ingesting* data, you have to get the data into {{es}} before you can search it, visualize it, and use it for insights.

Our ingest tools are flexible, and support a wide range of scenarios. We can help you with everything from popular and straightforward use cases, all the way to advanced use cases that require additional processing in order to modify or reshape your data before it goes to {{es}}.

You can ingest:

* **General content** (data without timestamps), such as HTML pages, catalogs, and files
* **Time series (timestamped) data**, such as logs, metrics, and traces for Elastic Security, Observability, Search solutions, or for your own custom solutions


## Ingesting general content [ingest-general]

Elastic offer tools designed to ingest specific types of general content. The content type determines the best ingest option.

* To index **documents** directly into {{es}}, use the {{es}} [document APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document).
* To send **application data** directly to {{es}}, use an [{{es}} language client](https://www.elastic.co/guide/en/elasticsearch/client/index.html).
* To index **web page content**, use the Elastic [web crawler](https://www.elastic.co/web-crawler).
* To sync **data from third-party sources**, use [connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html). A connector syncs content from an original data source to an {{es}} index. Using connectors you can create *searchable*, read-only replicas of your data sources.
* To index **single files** for testing in a non-production environment, use the {{kib}} [file uploader](ingest/upload-data-files.md).

If you would like to try things out before you add your own data, try using our [sample data](ingest/sample-data.md).


## Ingesting time series data [ingest-time-series]

::::{admonition} What’s the best approach for ingesting time series data?
The best approach for ingesting data is the *simplest option* that *meets your needs* and *satisfies your use case*.

In most cases, the *simplest option* for ingesting time series data is using {{agent}} paired with an Elastic integration.

* Install [Elastic Agent](https://www.elastic.co/guide/en/fleet/current) on the computer(s) from which you want to collect data.
* Add the [Elastic integration](https://docs.elastic.co/en/integrations) for the data source to your deployment.

Integrations are available for many popular platforms and services, and are a good place to start for ingesting data into Elastic solutions—​Observability, Security, and Search—​or your own search application.

Check out the [Integration quick reference](https://docs.elastic.co/en/integrations/all_integrations) to search for available integrations. If you don’t find an integration for your data source or if you need additional processing to extend the integration, we still have you covered. Refer to [Transform and enrich data](ingest/transform-enrich.md) to learn more.

::::