---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-ingestion-overview.html#es-ingestion-overview-general-content
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-api.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-pipeline-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-your-data.html
---

# Ingest for search use cases

% ----
% navigation_title: "Ingest for search use cases"
% ----

$$$elasticsearch-ingest-time-series-data$$$
::::{note}
This page covers ingest methods specifically for search use cases. If you're working with a different use case, refer to the [ingestion overview](/manage-data/ingest.md) for more options.
::::

Search use cases usually focus on general **content**, typically text-heavy data that does not have a timestamp. This could be data like knowledge bases, website content, product catalogs, and more.

Once you've decided how to [deploy Elastic](/deploy-manage/index.md), the next step is getting your content into {{es}}. Your choice of ingestion method depends on where your content lives and how you need to access it.

There are several methods to ingest data into {es} for search use cases. Choose one or more based on your requirements.

::::{tip}
If you just want to do a quick test, you can load [sample data](/manage-data/ingest/sample-data.md) into your {{es}} cluster using the UI.
::::

## Ingest data using APIs [es-ingestion-overview-apis] 

You can use the [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-document) to add data to your {{es}} indices, using any HTTP client, including the [{{es}} client libraries](/solutions/search/site-or-app/clients.md).

While the {{es}} APIs can be used for any data type, Elastic provides specialized tools that optimize ingestion for specific use cases.

## Specialized tools [es-ingestion-overview-general-content]

You can use these specialized tools to add general content to {{es}} indices.

| Method | Description | Notes |
|--------|-------------|-------|
| [**Web crawler**](https://github.com/elastic/crawler) | Programmatically discover and index content from websites and knowledge bases | Crawl public-facing web content or internal sites accessible via HTTP proxy |
| [**Search connectors**]() | Third-party integrations to popular content sources like databases, cloud storage, and business applications | Choose from a range of Elastic-built connectors or build your own in Python using the Elastic connector framework|
| [**File upload**](/manage-data/ingest/tools/upload-data-files.md)| One-off manual uploads through the UI | Useful for testing or very small-scale use cases, but not recommended for production workflows |

### (Optional) Content processing

You can also transform and enrich your content at ingest time with ingest pipelines, or at query time with runtime fields. Choose the right approach based on your requirements:

| Processing Type | Description | Use cases |
|----------------|-------------|------------|
| **Ingest pipelines** | Choose from a range of built-in processors or create custom processors | Data enrichment, content extraction from PDFs, ML inference, custom business logic |
| **Runtime fields** | Fields computed during query execution | Price calculation with current exchange rates, distance calculations, user-specific scoring |

You can manage ingest pipelines through Elasticsearch APIs or Kibana UIs.

::::{tip}
The UI also has a set of tools for creating and managing indices optimized for search use cases. You can also manage your ingest pipelines in this UI. Learn more in [](search-pipelines.md)
::::