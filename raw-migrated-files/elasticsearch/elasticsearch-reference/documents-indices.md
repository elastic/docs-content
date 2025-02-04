---
navigation_title: "Indices and documents"
---

# Indices, documents, and fields [documents-indices]


The index is the fundamental unit of storage in {{es}}, a logical namespace for storing data that share similar characteristics. After you have {{es}} [deployed](../../../get-started/deployment-options.md), you’ll get started by creating an index to store your data.

An index is a collection of documents uniquely identified by a name or an [alias](../../../manage-data/data-store/aliases.md). This unique name is important because it’s used to target the index in search queries and other operations.

::::{tip} 
A closely related concept is a [data stream](../../../manage-data/data-store/index-types/data-streams.md). This index abstraction is optimized for append-only timestamped data, and is made up of hidden, auto-generated backing indices. If you’re working with timestamped data, we recommend the [Elastic Observability](https://www.elastic.co/guide/en/observability/current) solution for additional tools and optimized content.

::::



## Documents and fields [elasticsearch-intro-documents-fields] 

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


## Metadata fields [elasticsearch-intro-documents-fields-data-metadata] 

An indexed document contains data and metadata. [Metadata fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-fields.html) are system fields that store information about the documents. In {{es}}, metadata fields are prefixed with an underscore. For example, the following fields are metadata fields:

* `_index`: The name of the index where the document is stored.
* `_id`: The document’s ID. IDs must be unique per index.


## Mappings and data types [elasticsearch-intro-documents-fields-mappings] 

Each index has a [mapping](../../../manage-data/data-store/mapping.md) or schema for how the fields in your documents are indexed. A mapping defines the [data type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html) for each field, how the field should be indexed, and how it should be stored. When adding documents to {{es}}, you have two options for mappings:

* [Dynamic mapping](../../../manage-data/data-store/mapping.md#mapping-dynamic): Let {{es}} automatically detect the data types and create the mappings for you. Dynamic mapping helps you get started quickly, but might yield suboptimal results for your specific use case due to automatic field type inference.
* [Explicit mapping](../../../manage-data/data-store/mapping.md#mapping-explicit): Define the mappings up front by specifying data types for each field. Recommended for production use cases, because you have full control over how your data is indexed to suit your specific use case.

::::{tip} 
You can use a combination of dynamic and explicit mapping on the same index. This is useful when you have a mix of known and unknown fields in your data.

::::


