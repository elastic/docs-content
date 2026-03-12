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

An _index_ is the fundamental unit of storage in {{es}}, and the level at which you interact with your data. Behind the scenes, {{es}} divides each index into _shards_ and distributes them across the nodes in your cluster. This allows it to scale horizontally to handle large volumes of data. Replica shards provide fault tolerance, keeping your data available even when individual nodes fail.

To store a document, you add it to a specific index. To search, you target one or more indices and {{es}} searches all data within them and returns any matching documents. You can target your data by index name, through an [alias](/manage-data/data-store/aliases.md) that points to one or more indices or through a [data stream](/manage-data/data-store/data-streams.md) that routes requests to the appropriate backing indices.

You can store many independent datasets side by side, each in its own index, and search them individually or together.

This page explains the core parts of an index (_documents_, _metadata fields_, and _mappings_), describes how {{es}} physically stores index data using _shards_, and highlights common design decisions.

:::{note}
:applies_to: {"serverless": "ga"}

In {{serverless-full}}:
* Shards, replicas, and nodes are fully managed for you. The platform automatically scales resources based on your workload, so you don't need to configure or monitor these details. The shard-related content on this page explains how {{es}} works under the hood.
* Each project supports up to 15,000 indices. This limit helps ensure reliable performance and stability. If you need a higher limit, you can [request an increase](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#index-and-resource-limits). For index sizing recommendations, refer to [index sizing guidelines](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-index-size).

:::

## Index components

An index is made up of the following components:

* [**Documents**](#elasticsearch-intro-documents-fields): The JSON objects that hold your data. Understanding their structure is essential for indexing data correctly.
* [**Metadata fields**](#elasticsearch-intro-documents-fields-data-metadata): System-managed fields like `_index` and `_id` that appear in query results and API responses.
* [**Mappings**](#elasticsearch-intro-documents-fields-mappings): Field-level definitions that control how data is indexed and queried. Understanding field types helps you write effective queries and avoid indexing problems.

### Documents [elasticsearch-intro-documents-fields]

{{es}} serializes and stores data in the form of JSON documents. A document is a set of fields, which are key-value pairs that contain your data. Each document has a unique ID, which you can create or have {{es}} auto-generate.

A simple {{es}} document might look like this:

```js
{
  "_index": "my-first-elasticsearch-index",
  "_id": "DyFpo5EBxE8fzbb95DOa",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
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

### Metadata fields [elasticsearch-intro-documents-fields-data-metadata]

An indexed document includes both document fields you define and system-managed metadata. [Metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md) are fields that describe the document and how {{es}} stores it. In {{es}}, metadata fields are prefixed with an underscore. For example:

* `_index`: The name of the index where the document is stored.
* `_id`: The document's ID. IDs must be unique per index.

For example, an API response includes these metadata fields alongside the document body:

```js
{
  "_index": "my-first-elasticsearch-index", <1>
  "_id": "DyFpo5EBxE8fzbb95DOa", <1>
  "_version": 1, <1>
  "_source": { <2>
    "email": "john@smith.com",
    "first_name": "John"
  }
}
```
1. These metadata fields describe the document.
2. The `_source` field contains the original document body as submitted.

### Mappings and data types [elasticsearch-intro-documents-fields-mappings]

Each index has a [mapping](/manage-data/data-store/mapping.md) that defines field types and indexing behavior. A mapping defines the [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) for each field, how the field should be indexed, and how it should be stored.

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

## How an index stores data

When you create an index, {{es}} doesn't store all its documents in a single location. Instead, it divides the index into one or more _shards_ and distributes those shards across the nodes in your cluster. The primary purpose of shards is to allow an index to scale beyond what a single server could handle. The right number of shards depends on your data volume, query patterns, and cluster topology — there is no single correct answer.

You don't interact with shards directly when indexing or searching. Instead, you target the index by name and {{es}} routes the operation to the appropriate shards. However, the number and size of shards you configure affects performance and stability. Refer to [Common index design decisions](#common-index-design-decisions) for more information.

Each shard is a self-contained instance of [Apache Lucene](https://lucene.apache.org/), the search library that powers {{es}}. A shard holds a subset of the index's documents and can independently handle indexing and search operations. Inside each shard, data is organized into immutable _segments_ that are written as documents are indexed. To learn how segments affect search availability, refer to [Near real-time search](/manage-data/data-store/near-real-time-search.md).

There are two types of shards:

* **Primary shards**: Every document belongs to exactly one primary shard. The number of primary shards is fixed at index creation, either through an [index template](/manage-data/data-store/templates.md) or the [`index.number_of_shards`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-number-of-shards) setting in the create index request.
* **Replica shards**: Copies of primary shards that provide redundancy and serve read requests. You can adjust the number of replicas at any time using the [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) setting.

By distributing shards across multiple nodes, {{es}} can scale horizontally and continue operating even when individual nodes fail. For a detailed explanation of this distributed model, refer to [Clusters, nodes, and shards](/deploy-manage/distributed-architecture/clusters-nodes-shards.md).


## Common index design decisions

Mappings control how fields are indexed, templates standardize configuration across indices, aliases decouple queries from physical index names, and lifecycle policies automate retention and tiering over time.

When working with indices, you typically make decisions that focus on:

* **Naming and aliases**: Use clear naming patterns for your indices and [aliases](/manage-data/data-store/aliases.md) to simplify query targets and support index changes with minimal disruption.
* **Mapping strategy**: Use [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) for speed when exploring data, and [explicit mappings](/manage-data/data-store/mapping/explicit-mapping.md) for production use cases. Choosing the right [field type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) upfront matters because it controls what queries and aggregations are available, and [changing a field type later requires reindexing](/manage-data/data-store/mapping/update-mappings-examples.md).
* **Index or data stream**: Use a regular index when you need frequent updates or deletes. For append-only timestamped data such as logs, events, and metrics, use a [data stream](/manage-data/data-store/data-streams.md) instead, since data streams manage rolling indices automatically.
* **Shard sizing**: For production workloads, the number and size of shards affect query speed and cluster stability. Refer to [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md) for guidelines.

## Next steps

After learning index fundamentals, choose the management path that fits your workflow:

* [](/manage-data/data-store/perform-index-operations.md): Navigate the **Index Management** experience in {{kib}} and run common index operations.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Manage indices and documents with the {{es}} REST API.
