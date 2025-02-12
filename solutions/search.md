---
applies:
  stack:
  serverless:
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-elasticsearch.html
  - https://www.elastic.co/guide/en/serverless/current/what-is-elasticsearch-serverless.html
---

# Search

{{es}} enables you to build powerful search experiences for websites, applications, and enterprise data using Elastic's unified platform.

## Use cases

Here are a few common real-world applications:

| Use case                             | Business goals                                                     | Technical requirements                                        |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Ecommerce/product catalog search** | Provide fast, relevant, and up-to-date results, faceted navigation | Inventory sync, user behavior tracking, results caching       |
| **Workplace/knowledge base search**  | Search across range of data sources, enforcing permissions         | Third-party connectors, document-level security, role mapping |
| **Website search**                   | Deliver relevant, up-to-date results                               | Web crawling, incremental indexing, query caching             |
| **Customer support search**          | Surface relevant solutions, manage access controls, track metrics  | Knowledge graph, role-based access, analytics                 |
| **Chatbots/RAG**                     | Enable natural conversations, provide context, maintain knowledge  | Vector search, ML models, knowledge base integration          |
| **Geospatial search**                | Process location queries, sort by proximity, filter by area        | Geo-mapping, spatial indexing, distance calculations          |

## Core implementation decisions

% TODO add diagram

Building a search experience with {{es}} requires a number of fundamental implementation decisions:

1. [**Deployment**](/deploy-manage/index.md): Where will you run Elastic?
1. [**Ingestion**](search/ingest-for-search.md): What tools will you use to get your content into {{es}}? 
1. [**Search approaches**](search/search-approaches.md): What search techniques and algorithms will you use to find relevant results? 
1. **Implementation tools**: How will you write queries and interact with {{es}}?
   - Which [programming language client]() matches your application?
   - Which API endpoints and [query language(s)](search/querying-for-search.md) will you use to express your search logic?

Each decision builds on the previous ones, offering flexibility to mix and match approaches based on your needs.

% TODO update/add URLs


% Scope notes: surface key features buried in the search APIs, turn some of the API doc content into feature-specific tutorials  needs some polish to separate use cases from technologies

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/search-with-elasticsearch.md
% - [ ] ./raw-migrated-files/docs-content/serverless/what-is-elasticsearch-serverless.md