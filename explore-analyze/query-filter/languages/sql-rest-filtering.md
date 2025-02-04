---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-rest-filtering.html
---

# Filtering using Elasticsearch Query DSL [sql-rest-filtering]

One can filter the results that SQL will run on using a standard {{es}} Query DSL by specifying the query in the filter parameter.

```console
POST /_sql?format=txt
{
  "query": "SELECT * FROM library ORDER BY page_count DESC",
  "filter": {
    "range": {
      "page_count": {
        "gte" : 100,
        "lte" : 200
      }
    }
  },
  "fetch_size": 5
}
```

Which returns:

```text
    author     |                name                |  page_count   | release_date
---------------+------------------------------------+---------------+------------------------
Douglas Adams  |The Hitchhiker's Guide to the Galaxy|180            |1979-10-12T00:00:00.000Z
```

::::{tip} 
A useful and less obvious usage for standard Query DSL filtering is to search documents by a specific [routing key](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html#search-routing). Because Elasticsearch SQL does not support a `routing` parameter, one can specify a [`terms` filter for the `_routing` field](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-routing-field.html) instead:

```console
POST /_sql?format=txt
{
  "query": "SELECT * FROM library",
  "filter": {
    "terms": {
      "_routing": ["abc"]
    }
  }
}
```

::::


