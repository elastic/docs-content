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

An index is the fundamental unit of storage in {{es}}. It is a collection of documents uniquely identified by a name or an [alias](/manage-data/data-store/aliases.md). This unique name is used to target the index in search queries and other operations.

This page introduces what an index contains and how it's structured, and links to related topics depending on what you need to do with your indices.

::::{tip}
A closely related concept is a [data stream](/manage-data/data-store/data-streams.md). This index abstraction is optimized for append-only timestamped data, and is made up of hidden, auto-generated backing indices. If you're working with timestamped data, we recommend the [Elastic Observability](/solutions/observability/get-started.md) solution for additional tools and optimized content.
::::

## Index components

An index is made up of the following components.

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

An indexed document contains data and metadata. [Metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md) are system fields that store information about the documents. In {{es}}, metadata fields are prefixed with an underscore. For example, the following fields are metadata fields:

* `_index`: The name of the index where the document is stored.
* `_id`: The document's ID. IDs must be unique per index.


### Mappings and data types [elasticsearch-intro-documents-fields-mappings]

Each index has a [mapping](/manage-data/data-store/mapping.md) or schema for how the fields in your documents are indexed. A mapping defines the [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) for each field, how the field should be indexed, and how it should be stored.

## Related topics

Depending on your goals, explore the following topics to learn more about working with indices and related data store concepts in {{es}}.

### Configure your indices

* [](/manage-data/data-store/mapping.md): Define how documents and their fields are stored and indexed, using dynamic mapping for automatic field detection or explicit mapping for full control.
* [](/manage-data/data-store/templates.md): Create reusable configurations — including settings, mappings, and aliases — that are automatically applied when new indices or data streams are created.
* [](/manage-data/data-store/aliases.md): Create named references that point to one or more indices or data streams, enabling zero-downtime reindexing and simplified query targeting.
* [](/manage-data/data-store/text-analysis.md): Configure how unstructured text is converted into a structured format optimized for full-text search.

### Manage your indices

* [](/manage-data/data-store/index-management.md): Use {{kib}}'s **Index Management** UI to view and manage your indices, data streams, templates, component templates, and enrich policies.
  * [](/manage-data/data-store/perform-index-operations.md): Perform operations like closing, refreshing, and deleting indices from the **Manage index** menu.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using curl and the {{es}} REST API.

### Work with time series data

* [](/manage-data/data-store/data-streams.md): Store append-only time series data across multiple backing indices while using a single named resource for requests.
* [](/manage-data/data-store/near-real-time-search.md): Understand how {{es}} makes new data searchable within seconds of indexing.
* [](/manage-data/lifecycle.md): Manage your data over time, including retention policies and tiered storage.
