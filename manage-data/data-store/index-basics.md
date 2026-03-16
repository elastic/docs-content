---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Index basics

An _index_ is the fundamental unit of storage in {{es}}, and the level at which you interact with your data. You can store many independent datasets side by side. 

Behind the scenes, {{es}} divides each index into _shards_ and distributes them across the nodes in your cluster. The horizontal scaling of your _primary_ shard into _replicas_ shards across other nodes allows your index to handle large volumes of traffic. Replica shards provide fault tolerance, keeping your data available even when an individual node's response fails.

To store a document, you add it to a specific index. To search, you target one or more indices and {{es}} searches all data within them and returns any matching documents. You can target your data by index name, through an [alias](/manage-data/data-store/aliases.md) that points to one or more indices or through a [data stream](/manage-data/data-store/data-streams.md) that routes requests to the appropriate backing indices. While you interact with a data stream as a single named resource, the data stream a logical layer that organizes multiple backing indices where your data is physically stored.

This page explains the core parts of an index (_documents_, _metadata fields_, and _mappings_), describes how {{es}} physically stores index data using _shards_, and highlights common design decisions.

:::{note}
:applies_to: {"serverless": "ga"}

In {{serverless-full}}:
* Shards, replicas, and nodes are fully managed for you. The platform automatically scales resources based on your workload, so you don't need to configure or monitor these details. The shard-related content on this page explains how {{es}} works under the hood.
* Each project supports up to 15,000 indices. This limit helps ensure reliable performance and stability. If you need a higher limit, you can [request an increase](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#index-and-resource-limits). For index sizing recommendations, refer to [index sizing guidelines](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-index-size).

:::

## Index components

An index is made up of the following components:

* [**Documents**](#elasticsearch-intro-documents-fields): The JSON objects that hold your data, including system-managed metadata fields like `_index` and `_id`.
* [**Mappings**](#elasticsearch-intro-documents-fields-mappings): Field-level definitions that control how data is indexed and queried. Understanding field types helps you write effective queries and avoid indexing problems.
* [**Settings**](#index-settings): Index-level configuration such as shard count, replica count, and refresh interval that controls storage and performance behavior.

### Documents [elasticsearch-intro-documents-fields]

{{es}} serializes and stores data in the form of JSON documents. A document is a set of fields, which are key-value pairs that contain your data. Each document has a unique ID, which you can create or have {{es}} auto-generate. An indexed document includes both document fields you define and system-managed metadata.

A simple {{es}} document might look like this:

```js
{
  "_index": "my-first-elasticsearch-index", <1>
  "_id": "DyFpo5EBxE8fzbb95DOa", <1>
  "_version": 1, <1>
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": { <2>
    "email": "john@smith.com",
    "first_name": "John",
    "last_name": "Smith",
    "info": {
      "bio": "Eco-warrior and defender of the weak",
      "age": 25,
      "interests": [
        "dolphins",
        "whales"
      ]
    },
    "join_date": "2024/05/01"
  }
}
```
1. [Metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md) are system-managed fields prefixed with an underscore. `_index` identifies which index stores the document and `_id` is the document's unique identifier within that index.
2. The `_source` field contains the original document body as submitted. The fields inside `_source` are the ones you define and control through [mappings](#elasticsearch-intro-documents-fields-mappings).

### Mappings and data types [elasticsearch-intro-documents-fields-mappings]

Each index has a [mapping](/manage-data/data-store/mapping.md) that defines field data types and how field values are analyzed and stored. A mapping defines the [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) for each field, how the field should be indexed, and how it should be stored.

For example, the following mapping defines field types for a few common data types:
```js
{
  "properties": {
    "email":      { "type": "keyword" },
    "first_name": { "type": "text" },
    "age":        { "type": "integer" },
    "join_date":  { "type": "date" }
  }
}
```

### Settings [index-settings]

Each index has settings that control its storage and performance behavior. Settings are specified at index creation, either directly in the [create index request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) or through an [index template](/manage-data/data-store/templates.md). Some index settings can be updated dynamically on a live index.

Common settings include:

* `index.number_of_shards`: The number of primary shards. Fixed at creation.
* `index.number_of_replicas`: The number of replica copies per primary shard. Can be changed at any time.
* `index.refresh_interval`: How often new data becomes searchable. Defaults to `1s`.

For the full list of available settings, refer to [Index settings](elasticsearch://reference/elasticsearch/index-settings/index-modules.md).

## How an index stores data

When you create an index, {{es}} doesn't store all its documents in a single location. Instead, it divides the index into one or more _shards_ and distributes those shards across the nodes in your cluster. Each shard is a self-contained [Apache Lucene](https://lucene.apache.org/) index with practical limits on how much data it can efficiently manage, so splitting data across multiple shards keeps individual shards performant. Distributing those shards across cluster nodes adds horizontal scaling and redundancy. The right number of shards depends on your data volume, query patterns, and cluster topology — there is no single correct answer. Refer to [shard sizing and distribution recommendations](/deploy-manage/production-guidance/optimize-performance/size-shards.md#sizing-shard-guidelines) for more information and best practices.

You don't interact with shards directly when indexing or searching. Instead, you target the index by name and {{es}} routes the operation to the appropriate shards. However, the number and size of shards you configure affects performance and stability. Refer to [Common index design decisions](#common-index-design-decisions) for more information.

A shard holds a subset of the index's documents and can independently handle indexing and search operations. Inside each shard, data is organized into immutable _segments_ that are written as documents are indexed. To learn how segments affect search availability, refer to [Near real-time search](/manage-data/data-store/near-real-time-search.md).

There are two types of shards:

* **Primary shards**: Every document belongs to exactly one primary shard. The number of primary shards is fixed at index creation, either through an [index template](/manage-data/data-store/templates.md) or the [`index.number_of_shards`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-number-of-shards) setting in the create index request.
* **Replica shards**: Copies of primary shards that provide redundancy and serve read requests. You can adjust the number of replicas at any time using the [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) setting.

By distributing shards across multiple nodes, {{es}} can scale horizontally and continue operating even when individual nodes fail. For a detailed explanation of this distributed model, refer to [Clusters, nodes, and shards](/deploy-manage/distributed-architecture/clusters-nodes-shards.md).
To learn how {{es}} coordinates reads and writes across primary and replica shards, refer to [Reading and writing documents](/deploy-manage/distributed-architecture/reading-and-writing-documents.md).


## Common index design decisions

Mappings control how fields are indexed, templates standardize configuration across indices, aliases decouple queries from physical index names, and lifecycle policies automate retention and tiering over time.

When working with indices, you typically make decisions that focus on:

* **Naming and aliases**: Use clear naming patterns for your indices and [aliases](/manage-data/data-store/aliases.md) to simplify query targets and support index changes with minimal disruption.
* **Mapping strategy**: Use [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) for speed when exploring data, and [explicit mappings](/manage-data/data-store/mapping/explicit-mapping.md) for production use cases. Choosing the right [field type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) upfront matters because it controls what queries and aggregations are available, and [changing a field type later requires reindexing](/manage-data/data-store/mapping/update-mappings-examples.md).
* **Index or data stream**: Use a regular index when you need frequent updates or deletes. For append-only timestamped data such as logs, events, and metrics, use a [data stream](/manage-data/data-store/data-streams.md) instead, since data streams manage rolling indices automatically.
* **Shard sizing**: For production workloads, the number and size of shards affect query speed and cluster stability. Refer to [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md) for guidelines.

## Next steps

Now that you understand index fundamentals, explore these pages for hands-on tasks:

* [](/manage-data/data-store/perform-index-operations.md): View, investigate, and perform operations on indices, data streams, and enrich policies in {{kib}}.
* [](/manage-data/data-store/templates.md): Create and manage index templates and component templates.
* [](/manage-data/data-store/data-streams/manage-data-stream.md): Create, monitor, and manage data streams and their backing indices.
* [](/manage-data/ingest/transform-enrich/data-enrichment.md): Set up enrich policies to add data from existing indices to incoming documents.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using the {{es}} REST API.