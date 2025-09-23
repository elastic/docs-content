---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-overview.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Overview [sql-overview]

Elasticsearch SQL aims to provide a powerful yet lightweight SQL interface to {{es}}.


## Introduction [sql-introduction] 

Elasticsearch SQL is a feature that allows SQL-like queries to be executed in real-time against {{es}}. Whether using the REST interface, command-line or JDBC, any client can use SQL to search and aggregate data *natively* inside {{es}}. One can think of Elasticsearch SQL as a *translator*, one that understands both SQL and {{es}} and makes it easy to read and process data in real-time, at scale by leveraging {{es}} capabilities.


## Why Elasticsearch SQL ? [sql-why] 

Native integration
:   Elasticsearch SQL is built from the ground up for {{es}}. Each and every query is efficiently executed against the relevant nodes according to the underlying storage.

No external parts
:   No need for additional hardware, processes, runtimes or libraries to query {{es}}; Elasticsearch SQL eliminates extra moving parts by running *inside* the {{es}} cluster.

Lightweight and efficient
:   Elasticsearch SQL does not abstract {{es}} and its search capabilities - on the contrary, it embraces and exposes SQL to allow proper full-text search, in real-time, in the same declarative, succinct fashion.

