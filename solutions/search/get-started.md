---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-get-started.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Get started

## Core implementation decisions

% TODO add diagram

Building a search experience with {{es}} requires a number of fundamental implementation decisions:

1. [**Deployment**](/deploy-manage/index.md): Where will you run Elastic?
1. [**Ingestion**](ingest-for-search.md): What tools will you use to get your content into {{es}}?
1. [**Search approaches**](search-approaches.md): What search techniques and algorithms will you use to find relevant results?
1. **Implementation tools**: How will you write queries and interact with {{es}}?
   - Which programming language client matches your application?
   - Which API endpoints and [query language(s)](querying-for-search.md) will you use to express your search logic?

Each decision builds on the previous ones, offering flexibility to mix and match approaches based on your needs.

::::{tip}
Already have an {{es}} deployment? You can get started with our hands-on [quickstart guides](/solutions/search/get-started/quickstarts.md), or check out our [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks#readme).
::::
