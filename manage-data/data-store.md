---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
---

# The Elasticsearch data store

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene.

The documentation in this section details how {{es}} works as a _data store_ starting with the fundamental unit of storage in Elasticsearch: the index. An index is a collection of documents uniquely identified by a name or an alias. Read more in [Index basics](/manage-data/data-store/index-basics.md) and [Index types](/manage-data/data-store/index-types.md).

Then, learn how these documents and the fields they contain are stored and indexed in [Mapping](/manage-data/data-store/mapping.md), and how unstructured text is converted into a structured format that’s optimized for search in [Text analysis](/manage-data/data-store/text-analysis.md).

You can also read more about working with {{es}} as a data store including how to use [index templates](/manage-data/data-store/templates.md) to tell {{es}} how to configure an index when it is created, how to use [aliases](/manage-data/data-store/aliases.md) to point to multiple indices, and how to use the [command line to manage data](/manage-data/data-store/manage-data-from-the-command-line.md) stored in {{es}}.