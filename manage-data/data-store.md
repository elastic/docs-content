---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# The Elasticsearch data store [elasticsearch-intro-what-is-es]

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene.

The documentation in this section details how {{es}} works as a _data store_ starting with the fundamental unit of storage in Elasticsearch: the index. An index is a collection of documents uniquely identified by a name or an alias. Read more in [Index basics](/manage-data/data-store/index-basics.md).

Then, learn how these documents and the fields they contain are stored and indexed in [Mapping](/manage-data/data-store/mapping.md), and how unstructured text is converted into a structured format that’s optimized for search in [Text analysis](/manage-data/data-store/text-analysis.md).

You can also read more about working with {{es}} as a data store including how to use [index templates](/manage-data/data-store/templates.md) to tell {{es}} how to configure an index when it is created, how to use [aliases](/manage-data/data-store/aliases.md) to point to multiple indices, and how to use the [command line to manage data](/manage-data/data-store/manage-data-from-the-command-line.md) stored in {{es}}.

If your use case involves working with continuous streams of time series data, you can consider using a [data stream](./data-store/data-streams.md). These are optimally suited for storing append-only data. You can access the data through a single, named resource, while {{es}} stores it in a series of hidden, auto-generated backing indices.
