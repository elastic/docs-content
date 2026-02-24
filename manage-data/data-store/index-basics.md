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

An _index_ is the fundamental unit of storage in {{es}}: a collection of documents identified by a unique name or an [alias](/manage-data/data-store/aliases.md). This name is used to target the index in search requests and other operations.

This page explains the core parts of an index (_documents_, _metadata fields_, and _mappings_) and highlights common design decisions for working with indices.

:::::{tip}
A closely related concept is a [data stream](/manage-data/data-store/data-streams.md), which is optimized for append-only timestamped data and backed by hidden, auto-generated indices.
:::::

## Index components

Understanding these components helps you design indices that are easier to query, scale, and manage.

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

An indexed document includes both source data and metadata. [Metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md) are system-managed fields that describe the document and how {{es}} stores it. In {{es}}, metadata fields are prefixed with an underscore. For example:

* `_index`: The name of the index where the document is stored.
* `_id`: The document's ID. IDs must be unique per index.

### Mappings and data types [elasticsearch-intro-documents-fields-mappings]

Each index has a [mapping](/manage-data/data-store/mapping.md) that defines field types and indexing behavior. Mappings determine how fields are stored, queried, and aggregated.

## Common index design decisions

When working with indices, you typically make decisions that focus on:

* **Naming and aliases**: Use clear index naming patterns and [aliases](/manage-data/data-store/aliases.md) to simplify query targets and support index changes with minimal disruption.
* **Mapping strategy**: Use dynamic mapping for speed when exploring data, and [explicit mappings](/manage-data/data-store/mapping.md) for production use cases where field control and query behavior matter.
* **Index or data stream**: Use a regular index when you need frequent updates or deletes. Use a [data stream](/manage-data/data-store/data-streams.md) for append-only timestamped data such as logs, events, and metrics.

## Next steps

After learning index fundamentals, choose the management path that fits your workflow:

* [](/manage-data/data-store/perform-index-operations.md): Run common index operations from the **Manage index** menu.
* [](/manage-data/data-store/index-management.md): Navigate the full **Index Management** experience in {{kib}}.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Manage indices and documents with the {{es}} REST API.
