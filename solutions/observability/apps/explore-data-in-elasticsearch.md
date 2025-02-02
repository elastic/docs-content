---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-exploring-es-data.html
---

# Explore data in Elasticsearch [apm-exploring-es-data]

* [{{es}} query examples](#apm-elasticsearch-query-examples)


## {{es}} query examples [apm-elasticsearch-query-examples] 

Elastic APM data is stored in [Data streams](data-streams.md).

The following examples enable you to interact with {{es}}'s REST API. One possible way to do this is using {{kib}}'s [{{dev-tools-app}} console](../../../explore-analyze/query-filter/tools/console.md).

Data streams, templates, and index-level operations can also be manged via {{kib}}'s [Index management](https://www.elastic.co/guide/en/kibana/current/managing-indices.html) panel.

To see an overview of existing data streams, run:

```console
GET /_data_stream/*apm*
```

To query a specific event type, for example, application traces:

```console
GET traces-apm*/_search
```

If you are interested in the *settings* and *mappings* of the Elastic APM indices, first, run a query to find template names:

```console
GET _cat/templates/*apm*
```

Then, retrieve the specific template you are interested in:

```console
GET  /_template/your-template-name
```

