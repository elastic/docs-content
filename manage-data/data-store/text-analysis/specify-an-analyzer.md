---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/specify-analyzer.html
applies_to:
  stack: ga
  serverless: ga
---

# Specify an analyzer [specify-analyzer]

{{es}} offers a variety of ways to specify built-in or custom analyzers:

* By `text` field, index, or query
* For [index or search time](index-search-analysis.md)

::::{admonition} Keep it simple
:class: tip

The flexibility to specify analyzers at different levels and for different times is great…​ *but only when it’s needed*.

In most cases, a simple approach works best: Specify an analyzer for each `text` field, as outlined in [Specify the analyzer for a field](#specify-index-field-analyzer).

This approach works well with {{es}}'s default behavior, letting you use the same analyzer for indexing and search. It also lets you quickly see which analyzer applies to which field using the [get mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping).

If you don’t typically create mappings for your indices, you can use [index templates](../templates.md) to achieve a similar effect.

::::


## How {{es}} determines the index analyzer [specify-index-time-analyzer]

{{es}} determines which index analyzer to use by checking the following parameters in order:

1. The [`analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) mapping parameter for the field. See [Specify the analyzer for a field](#specify-index-field-analyzer).
2. The `analysis.analyzer.default` index setting. See [Specify the default analyzer for an index](#specify-index-time-default-analyzer).

If none of these parameters are specified, the [`standard` analyzer](elasticsearch://reference/data-analysis/text-analysis/analysis-standard-analyzer.md) is used.


## Specify the analyzer for a field [specify-index-field-analyzer]

When mapping an index, you can use the [`analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) mapping parameter to specify an analyzer for each `text` field.

The following [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request sets the `whitespace` analyzer as the analyzer for the `title` field.

```console
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace"
      }
    }
  }
}
```


## Specify the default analyzer for an index [specify-index-time-default-analyzer]

In addition to a field-level analyzer, you can set a fallback analyzer for using the `analysis.analyzer.default` setting.

The following [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request sets the `simple` analyzer as the fallback analyzer for `my-index-000001`.

```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        }
      }
    }
  }
}
```


## How {{es}} determines the search analyzer [specify-search-analyzer]

::::{warning}
In most cases, specifying a different search analyzer is unnecessary. Doing so could negatively impact relevancy and result in unexpected search results.

If you choose to specify a separate search analyzer, we recommend you thoroughly [test your analysis configuration](/manage-data/data-store/text-analysis/test-an-analyzer.md) before deploying in production.

::::


At search time, {{es}} determines which analyzer to use by checking the following parameters in order:

1. The [`analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) parameter in the search query. See [Specify the search analyzer for a query](#specify-search-query-analyzer).
2. The [`search_analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/search-analyzer.md) mapping parameter for the field. See [Specify the search analyzer for a field](#specify-search-field-analyzer).
3. The `analysis.analyzer.default_search` index setting. See [Specify the default search analyzer for an index](#specify-search-default-analyzer).
4. The [`analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) mapping parameter for the field. See [Specify the analyzer for a field](#specify-index-field-analyzer).

If none of these parameters are specified, the [`standard` analyzer](elasticsearch://reference/data-analysis/text-analysis/analysis-standard-analyzer.md) is used.


## Specify the search analyzer for a query [specify-search-query-analyzer]

When writing a [full-text query](elasticsearch://reference/query-languages/full-text-queries.md), you can use the `analyzer` parameter to specify a search analyzer. If provided, this overrides any other search analyzers.

The following [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) request sets the `stop` analyzer as the search analyzer for a [`match`](elasticsearch://reference/query-languages/query-dsl-match-query.md) query.

```console
GET my-index-000001/_search
{
  "query": {
    "match": {
      "message": {
        "query": "Quick foxes",
        "analyzer": "stop"
      }
    }
  }
}
```
%  TEST[s/^/PUT my-index-000001\n/]


## Specify the search analyzer for a field [specify-search-field-analyzer]

When mapping an index, you can use the [`search_analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) mapping parameter to specify a search analyzer for each `text` field.

If a search analyzer is provided, the index analyzer must also be specified using the `analyzer` parameter.

The following [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request sets the `simple` analyzer as the search analyzer for the `title` field.

```console
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace",
        "search_analyzer": "simple"
      }
    }
  }
}
```


## Specify the default search analyzer for an index [specify-search-default-analyzer]

When [creating an index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create), you can set a default search analyzer using the `analysis.analyzer.default_search` setting.

If a search analyzer is provided, a default index analyzer must also be specified using the `analysis.analyzer.default` setting.

The following  [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request sets the `whitespace` analyzer as the default search analyzer for the `my-index-000001` index.

```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        },
        "default_search": {
          "type": "whitespace"
        }
      }
    }
  }
}
```


