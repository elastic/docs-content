---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-get-started.html
applies:
  stack:
  serverless:
---

# Get started

% What needs to be done: Refine




% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$find-cloud-id-cloud-self-managed$$$

$$$create-an-api-key-cloud-self-managed$$$

$$$find-cloud-id-serverless$$$

$$$create-an-api-key-serverless$$$

$$$elasticsearch-get-started-create-project$$$

$$$elasticsearch-follow-guided-index-flow$$$

$$$elasticsearch-follow-in-product-getting-started$$$

$$$elasticsearch-explore-on-your-own$$$

$$$elasticsearch-get-started-create-api-key$$$

$$$full-text-filter-tutorial-create-index$$$


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