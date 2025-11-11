---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-ingestion-overview.html#es-ingestion-overview-general-content
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-api.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-pipeline-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-your-data.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---
# Ingest for search use cases

$$$elasticsearch-ingest-time-series-data$$$
::::{note}
This page covers ingest methods specifically for search use cases. If you're working with a different use case, refer to the [ingestion overview](/manage-data/ingest.md) for more options.
::::

Search use cases usually focus on general **content**, typically text-heavy data that does not have a timestamp. This could be data like knowledge bases, website content, product catalogs, and more.

Once you've decided how to [deploy Elastic](/deploy-manage/index.md), the next step is getting your content into {{es}}. Your choice of ingestion method depends on where your content lives and how you need to access it.

There are several methods to ingest data into {{es}} for search use cases.
Choose one or more based on your requirements:

* [Native APIs and language clients](#es-ingestion-overview-apis): Index any JSON document directly using the {{es}} REST API or the official clients for languages like Python, Java, Go, and more.  
* **Web crawler:** Ingest content from public or private websites to make it searchable.  
* **Enterprise connectors:** Use pre-built connectors to sync data from external content sources like SharePoint, Confluence, Jira, and databases like MongoDB or PostgreSQL into {{es}}.


::::{tip}
If you just want to do a quick test, you can load [sample data](/manage-data/ingest/sample-data.md) into your {{es}} cluster using the UI.
::::

## Use APIs [es-ingestion-overview-apis]

You can use the [`_bulk` API]({{es-apis}}group/endpoint-document) to add data to your {{es}} indices, using any HTTP client, including the [{{es}} client libraries](/solutions/search/site-or-app/clients.md).

::::{tip}
To connect to an {{es-serverless}} project, you must [find the connection details](/solutions/search/search-connection-details.md).
::::

While the {{es}} APIs can be used for any data type, Elastic provides specialized tools that optimize ingestion for specific use cases.

## Use specialized tools [es-ingestion-overview-general-content]

You can use these specialized tools to add general content to {{es}} indices.

| Method | Description | Notes |
|--------|-------------|-------|
| [**Elastic Open Web Crawler**](https://github.com/elastic/crawler) | Programmatically discover and index content from websites and knowledge bases | Crawl public-facing web content or internal sites accessible via HTTP proxy |
| [**Content connectors**](elasticsearch://reference/search-connectors/index.md) | Third-party integrations to popular content sources like databases, cloud storage, and business applications | Choose from a range of Elastic-built connectors or build your own in Python using the Elastic connector framework|
| [**File upload**](/manage-data/ingest/upload-data-files.md)| One-off manual uploads through the UI | Useful for testing or very small-scale use cases, but not recommended for production workflows |

### Process data at ingest time

You can also transform and enrich your content at ingest time using [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md).

The Elastic UI has a set of tools for creating and managing indices optimized for search use cases. You can also manage your ingest pipelines in this UI. Learn more in [](search-pipelines.md).