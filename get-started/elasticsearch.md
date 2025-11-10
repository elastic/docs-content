---
products:
  - id: elasticsearch
applies_to:
  stack:
---

# {{es}} overview [elasticsearch-overview]

{{es}} is a distributed datastore that ingests, indexes, and manages various types of data in near real-time, making them both searchable and analyzable. Built on Apache Lucene, {{es}} scales horizontally across multiple nodes to handle large data volumes while maintaining fast query performance.

At its core, {{es}} solves the problem of making large amounts of data quickly searchable. Whether you're building a product search for an e-commerce site, implementing semantic search with AI, or analyzing log data, {{es}} provides the foundation for these use cases through its powerful indexing and query capabilities.

## Distributed architecture [elasticsearch-distributed-architecture]

{{es}} distributes data across multiple nodes in a cluster. Each node holds a portion of the data in shards, which are self-contained indexes that can be stored on any node. 

This distribution enables:

* Horizontal scaling: Add more nodes to increase capacity
* High availability: Data is replicated across nodes to prevent loss
* Parallel processing: Queries execute across shards simultaneously

## Near real-time indexing [elasticsearch-near-real-time-indexing]

When you send documents to Elasticsearch, they become searchable within about one second. This near real-time capability makes Elasticsearch suitable for applications that require immediate data availability, such as:

* Live dashboards showing current system metrics
* Product catalogs that update as inventory changes
* User-generated content that appears in search results immediately

## Schema-on-write with dynamic mapping [elasticsearch-schema-on-write-with-dynamic-mapping]

Elasticsearch automatically detects field types when you index documents. If you send a document with a price field containing 29.99, Elasticsearch infers it's a floating-point number. You can also define explicit mappings to control exactly how data is stored and indexed. 

Mappings are important for:

* Optimizing storage and query performance
* Enabling specific search features (like autocomplete or geo-search)
* Ensuring data consistency across documents

## Vector capabilities [elasticsearch-vector-capabilities]

Elasticsearch serves as a vector database for AI and machine learning applications. It stores dense vector embeddings alongside traditional text and numeric data, enabling:

* Semantic search: Find content by meaning rather than exact keywords
* Hybrid search: Combine keyword and vector search for best results
* RAG systems: Provide relevant context to large language models

## How Elasticsearch works [how-elasticsearch-works]

### Data flow [elasticsearch-data-flow]

1. Ingestion: Data enters Elasticsearch through the REST API, client libraries, or integrations
2. Analysis: Text is processed through analyzers (tokenization, stemming, etc.)
3. Indexing: Documents are stored in shards with inverted indexes for fast retrieval
4. Querying: Search requests are distributed to relevant shards and results are merged
5. Response: Results are returned, typically in milliseconds

### Storage model [elasticsearch-storage-model]

Elasticsearch stores data in indices, which are collections of documents with similar characteristics. Each document is a JSON object with fields. 

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

Under the hood, Elasticsearch creates inverted indexes that map each unique term to the documents containing it, enabling fast full-text search.

### Query execution [elasticsearch-query-execution]

When you search, Elasticsearch:

1. Parses your query (e.g., "wireless headphones under $100")
2. Determines which shards might contain matching documents
3. Executes the query on each relevant shard in parallel
4. Scores results by relevance
5. Merges and sorts results from all shards
6. Returns the top results
7. This distributed query execution is why Elasticsearch can search petabytes of data in milliseconds.

## Use cases [elasticsearch-use-cases]

Elasticsearch excels in scenarios requiring fast search and analysis across large datasets.

### Full-text and hybrid search [elasticsearch-full-text-hybrid-search]

* E-commerce product catalogs: Fast product discovery with filters, facets, and autocomplete
* Enterprise knowledge bases: Search across documents, wikis, and databases with permission controls
* Content platforms: Search articles, videos, and user-generated content by relevance

### AI-powered applications [elasticsearch-ai-powered-applications]

* Semantic search: Find documents by meaning using vector embeddings from models like BERT or OpenAI
* Chatbots and RAG systems: Retrieve relevant context from knowledge bases to enhance LLM responses
* Recommendation engines: Surface similar items based on vector similarity

### Geospatial search [elasticsearch-geospatial-search]

* Location-based services: Find nearby restaurants, stores, or services
* Delivery routing: Optimize routes based on geographic data
* Geofencing: Trigger actions when users enter specific areas

### Analytics and monitoring [elasticsearch-analytics-monitoring]

* Log analytics: Centralize and analyze application and system logs
* Security analytics: Detect threats and anomalies in security events
* Business metrics: Analyze user behavior, sales trends, and KPIs

## When to use Elasticsearch [when-to-use-elasticsearch]

Use Elasticsearch when you need:

* Fast search across large volumes of text, numeric, or vector data
* Complex queries with filters, aggregations, and relevance scoring
* Near real-time data availability (seconds, not minutes)
* Scalability to handle growing data volumes
* Flexibility to handle various data types and evolving schemas

## Architecture considerations [elasticsearch-architecture-considerations]

### Deployment options [elasticsearch-deployment-options]

* Elasticsearch Serverless: Fully managed, auto-scaling deployment (recommended for new projects)
* Elastic Cloud: Managed Elasticsearch with more configuration control
* Self-managed: Install and operate Elasticsearch yourself (requires expertise)

### Cluster sizing [elasticsearch-cluster-sizing]

* Small deployments: 3-5 nodes for development and small production use cases
* Medium deployments: 10-20 nodes for moderate data volumes and query loads
* Large deployments: 50+ nodes for high-volume production systems

### Data modeling best practices [elasticsearch-data-modeling-best-practices]

* One document type per index: Keep related data together
* Denormalize data: Include related information in documents to avoid "joins"
* Use appropriate field types: Match data types to query patterns
* Plan for growth: Consider time-based indices for logs and events

## Next steps [elasticsearch-next-steps]

Ready to try Elasticsearch? Here's how to get started:

* Get started with Elasticsearch - Run your first queries in 5 minutes
* Tutorial: Build a search application - Create a full-featured search experience
* Understanding Elasticsearch architecture - Deep dive into distributed systems concepts

For specific use cases:

* Implementing semantic search - Add AI-powered search
* Building geospatial applications - Work with location data
* Analyzing logs and metrics - Set up observability