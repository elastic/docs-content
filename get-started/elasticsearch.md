---
description: An introduction to Elasticsearch. 
applies_to:
  serverless: all
  stack: all
products:
  - id: elasticsearch
---

# {{es}} overview [elasticsearch-overview]

{{es}} is a distributed data store that ingests, indexes, and manages diverse data types in near real time, making your data searchable and analyzable. Built on Apache Lucene, {{es}} scales horizontally across multiple nodes to handle large data volumes while maintaining fast query performance.

{{es}} enables you to make large amounts of data quickly searchable. Whether you’re building an e-commerce product search, implementing semantic search with AI, or analyzing log data, {{es}} provides a powerful foundation with efficient indexing and query capabilities.

## Key concepts [elasticsearch-key-concepts]

### Distributed architecture [elasticsearch-distributed-architecture]

{{es}} distributes data across multiple nodes within a cluster. Each node stores a portion of the data in shards, which are self-contained indexes that can reside on any node in the cluster. 

The distributed {{es}} architecture enables the following:

* **Horizontal scaling** —— Add more nodes to increase capacity
* **High availability** —— Maintained through data replication across nodes to prevent data loss
* **Parallel processing** —— Queries execute across shards simultaneously to deliver fast performance

### Near real-time indexing [elasticsearch-near-real-time-indexing]

When you send documents to {{es}}, they become searchable within about one second. The near real-time capability makes {{es}} ideal for applications that require immediate data availability. 

For example:

* Live dashboards display currently collected system metrics 
* Product catalogs that instantly update as inventory changes
* User-generated content that appears in search results the moment the content is created

### Schema-on-write with dynamic mapping [elasticsearch-schema-on-write-with-dynamic-mapping]

When you index documents, {{es}} automatically detects the field types. For example, when a document includes a `price` field with a `29.99` value, {{es}} infers that the value is a floating-point number. You can also define explicit mappings to control exactly how data is stored and indexed. 

Mappings play a key role in the following:

* Storage and query performance optimization
* Specific search feature enablement, such as autocomplete or geospatial search
* Data consistency across documents

### Vector capabilities [elasticsearch-vector-capabilities]

{{es}} functions as a vector database for AI and {{ml}} applications, storing dense vector embeddings alongside traditional text and numeric data. 

Vector capabilities enable the following:

* **Semantic search** —— Find content based on meaning rather than exact keywords
* **Hybrid search** —— Combine keyword and vector-based search results for greater accuracy
* **Retrieval-augmented generation (RAG) systems** —— Provide relevant context to large language models

## How {{es}} works [how-elasticsearch-works]

To enable fast and scalable search, {{es}} ingests, analyzes, and indexes data so queries execute across shards and return results in milliseconds. 

![How Elasticsearch works](/get-started/images/how-elasticsearch-works.png)


### Storage model [elasticsearch-storage-model]

{{es}} stores data in indices, which are collections of documents with similar characteristics. Each document is a JSON object with fields. 

For example:

```console
{
  "product_id": "abc123",
  "name": "Wireless Headphones",
  "price": 79.99,
  "category": "Electronics",
  "in_stock": true,
  "description": "High-quality wireless headphones with noise cancellation"
}
```

To enable fast full-text search, {{es}} creates inverted indexes that map each unique term to the documents that containin the term.

### Query execution [elasticsearch-query-execution]

To search your data, {{es}} uses distributed query execution.

When you search, {{es}}:

1. Parses your query (e.g., "wireless headphones under $100")
2. Determines the shards that contain the matching documents
3. Executes the query on each relevant shard in parallel
4. Scores results by relevance
5. Merges and sorts results from all shards
6. Returns the top results

## Use cases [elasticsearch-use-cases]

{{es}} is ideal for uses cases that require fast search and analysis across large datasets.

### Full-text and hybrid search [elasticsearch-full-text-hybrid-search]

* **E-commerce product catalogs** —— Fast product discovery with filters, facets, and autocomplete
* **Enterprise knowledge bases** —— Search across documents, wikis, and databases with permission controls
* **Content platforms** —— Search articles, videos, and user-generated content by relevance

### AI-powered applications [elasticsearch-ai-powered-applications]

* **Semantic search** —— Find documents by meaning using vector embeddings from models like BERT or OpenAI
* **Chatbots and RAG systems** —— Retrieve relevant context from knowledge bases to enhance LLM responses
* **Recommendation engines** —— Surface similar items based on vector similarity

### Geospatial search [elasticsearch-geospatial-search]

* **Location-based services** —— Find nearby restaurants, stores, or services
* **Delivery routing** —— Optimize routes based on geographic data
* **Geofencing** —— Trigger actions when users enter specific areas

### Analytics and monitoring [elasticsearch-analytics-monitoring]

* **Log analytics** —— Centralize and analyze application and system logs
* **Security analytics** —— Detect threats and anomalies in security events
* **Business metrics** —— Analyze user behavior, sales trends, and KPIs

## When to use {{es}} [when-to-use-elasticsearch]

Use {{es}} when you need:

* Fast search across large volumes of text, numeric, or vector data
* Complex queries with filters, aggregations, and relevance scoring
* Near real-time access to data
* Scalability to handle growing datasets
* Flexibility to manage diverse data types and evolving schemas

Consider alternatives to {{es}} when:

* You require transactional guarantees and complex joins across multiple entities, which are better handled by relational databases
* Strong consistency is more important than eventual consistency
* Your datasets are small, such as under 1GB, where simpler solutions suffice

## Architecture considerations [elasticsearch-architecture-considerations]

### Deployment options [elasticsearch-deployment-options]

{{es}} offers flexible deployment options to match your organization requirements and level of operational control. 

| Option | Description |
| ----- | ----- |
| **[{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)** | Fully managed, auto-scaling deployment. Recommended for new projects. |
| **[{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)** | Managed {{es}} with more configuration control. |
| **[Self-managed](/deploy-manage/deploy/self-managed.md)** | Install and operate {{es}} yourself. Requires expertise. |

### Cluster sizing [elasticsearch-cluster-sizing]

To make sure your {{es}} deployment performs efficiently and scales with your data and query demands, use the right cluster size. 

| Deployment size | Cluster size |
| ----- | ----- |
| **Small** | 3-5 nodes for development and small production use cases. |
| **Medium** | 10-20 nodes for moderate data volumes and query loads. |
| **Large** | 50 or more nodes for high-volume production systems. |

### Data modeling best practices [elasticsearch-data-modeling-best-practices]

* **One document type per index** —— Keep related data together
* **Denormalize data** —— Include related information in documents to avoid joins
* **Use appropriate field types** —— Match data types to query patterns
* **Plan for growth** —— Consider time-based indices for logs and events

## Next steps [elasticsearch-next-steps]

Ready to try {{es}}? Here's how to get started:

* [Get started](/solutions/search/get-started.md) - Run your first queries in 5 minutes
% how* Tutorial: Build a search application - Create a full-featured search experience
* [Understanding {{es}} architecture](/deploy-manage/distributed-architecture.md) - Deep dive into distributed systems concepts

For specific use cases:

* [Implementing semantic search](/solutions/search/get-started/semantic-search.md) - Add AI-powered search
* [Building geospatial applications](/explore-analyze/geospatial-analysis.md) - Work with location data
* [Analyzing logs and metrics](/solutions/observability/get-started.md) - Set up observability