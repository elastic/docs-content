---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-translate.html
---

# SQL Translate API [sql-translate]

The SQL Translate API accepts SQL in a JSON document and translates it into native {{es}} queries. For example:

```console
POST /_sql/translate
{
  "query": "SELECT * FROM library ORDER BY page_count DESC",
  "fetch_size": 10
}
```

Which returns:

```console-result
{
  "size": 10,
  "_source": false,
  "fields": [
    {
      "field": "author"
    },
    {
      "field": "name"
    },
    {
      "field": "page_count"
    },
    {
      "field": "release_date",
      "format": "strict_date_optional_time_nanos"
    }
  ],
  "sort": [
    {
      "page_count": {
        "order": "desc",
        "missing": "_first",
        "unmapped_type": "short"
      }
    }
  ],
  "track_total_hits": -1
}
```

Which is the request that SQL will run to provide the results. In this case, SQL will use the [scroll](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-results) API. If the result contained an aggregation then SQL would use the normal [search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html).

The request body accepts the same [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-search-api.html#sql-search-api-request-body) as the [SQL search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-search-api.html), excluding `cursor`.

