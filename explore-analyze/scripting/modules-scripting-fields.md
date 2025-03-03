---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-fields.html
---

# Accessing document fields and special variables [modules-scripting-fields]

Depending on where a script is used, it will have access to certain special variables and document fields.


## Update scripts [_update_scripts]

A script used in the [update](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update), [update-by-query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query), or [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) API will have access to the `ctx` variable which exposes:

`ctx._source`
:   Access to the document [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md).

`ctx.op`
:   The operation that should be applied to the document: `index` or `delete`.

`ctx._index` etc
:   Access to [document metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md), some of which may be read-only.

These scripts do not have access to the `doc` variable and have to use `ctx` to access the documents they operate on.


## Search and aggregation scripts [_search_and_aggregation_scripts]

With the exception of [script fields](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#script-fields) which are executed once per search hit, scripts used in search and aggregations will be executed once for every document which might match a query or an aggregation. Depending on how many documents you have, this could mean millions or billions of executions: these scripts need to be fast!

Field values can be accessed from a script using [doc-values](#modules-scripting-doc-vals), [the `_source` field](#modules-scripting-source), or [stored fields](#modules-scripting-stored), each of which is explained below.


### Accessing the score of a document within a script [scripting-score]

Scripts used in the [`function_score` query](elasticsearch://reference/query-languages/query-dsl-function-score-query.md), in [script-based sorting](elasticsearch://reference/elasticsearch/rest-apis/sort-search-results.md), or in [aggregations](../query-filter/aggregations.md) have access to the `_score` variable which represents the current relevance score of a document.

Here’s an example of using a script in a [`function_score` query](elasticsearch://reference/query-languages/query-dsl-function-score-query.md) to alter the relevance `_score` of each document:

```console
PUT my-index-000001/_doc/1?refresh
{
  "text": "quick brown fox",
  "popularity": 1
}

PUT my-index-000001/_doc/2?refresh
{
  "text": "quick fox",
  "popularity": 5
}

GET my-index-000001/_search
{
  "query": {
    "function_score": {
      "query": {
        "match": {
          "text": "quick brown fox"
        }
      },
      "script_score": {
        "script": {
          "lang": "expression",
          "source": "_score * doc['popularity']"
        }
      }
    }
  }
}
```


### Accessing term statistics of a document within a script [scripting-term-statistics]

Scripts used in a [`script_score`](elasticsearch://reference/query-languages/query-dsl-script-score-query.md) query have access to the `_termStats` variable which provides statistical information about the terms in the child query.

In the following example, `_termStats` is used within a [`script_score`](elasticsearch://reference/query-languages/query-dsl-script-score-query.md) query to retrieve the average term frequency for the terms `quick`, `brown`, and `fox` in the `text` field:

```console
PUT my-index-000001/_doc/1?refresh
{
  "text": "quick brown fox"
}

PUT my-index-000001/_doc/2?refresh
{
  "text": "quick fox"
}

GET my-index-000001/_search
{
  "query": {
    "script_score": {
      "query": { <1>
        "match": {
          "text": "quick brown fox"
        }
      },
      "script": {
        "source": "_termStats.termFreq().getAverage()" <2>
      }
    }
  }
}
```

1. Child query used to infer the field and the terms considered in term statistics.
2. The script calculates the average document frequency for the terms in the query using `_termStats`.


`_termStats` provides access to the following functions for working with term statistics:

* `uniqueTermsCount`: Returns the total number of unique terms in the query. This value is the same across all documents.
* `matchedTermsCount`: Returns the count of query terms that matched within the current document.
* `docFreq`: Provides document frequency statistics for the terms in the query, indicating how many documents contain each term. This value is consistent across all documents.
* `totalTermFreq`: Provides the total frequency of terms across all documents, representing how often each term appears in the entire corpus. This value is consistent across all documents.
* `termFreq`: Returns the frequency of query terms within the current document, showing how often each term appears in that document.

::::{admonition} Functions returning aggregated statistics
:class: note

The `docFreq`, `termFreq` and `totalTermFreq` functions return objects that represent statistics across all terms of the child query.

Statistics provides support for the following methods:

`getAverage()`: Returns the average value of the metric. `getMin()`: Returns the minimum value of the metric. `getMax()`: Returns the maximum value of the metric. `getSum()`: Returns the sum of the metric values. `getCount()`: Returns the count of terms included in the metric calculation.

::::


::::{admonition} Painless language required
:class: note

The `_termStats` variable is only available when using the [Painless](modules-scripting-painless.md) scripting language.

::::



### Doc values [modules-scripting-doc-vals]

By far the fastest most efficient way to access a field value from a script is to use the `doc['field_name']` syntax, which retrieves the field value from [doc values](elasticsearch://reference/elasticsearch/mapping-reference/doc-values.md). Doc values are a columnar field value store, enabled by default on all fields except for [analyzed `text` fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md).

```console
PUT my-index-000001/_doc/1?refresh
{
  "cost_price": 100
}

GET my-index-000001/_search
{
  "script_fields": {
    "sales_price": {
      "script": {
        "lang":   "expression",
        "source": "doc['cost_price'] * markup",
        "params": {
          "markup": 0.2
        }
      }
    }
  }
}
```

Doc-values can only return "simple" field values like numbers, dates, geo- points, terms, etc, or arrays of these values if the field is multi-valued. It cannot return JSON objects.

::::{admonition} Missing fields
:class: note

The `doc['field']` will throw an error if `field` is missing from the mappings. In `painless`, a check can first be done with `doc.containsKey('field')` to guard accessing the `doc` map. Unfortunately, there is no way to check for the existence of the field in mappings in an `expression` script.

::::


::::{admonition} Doc values and `text` fields
:class: note

The `doc['field']` syntax can also be used for [analyzed `text` fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md) if [`fielddata`](elasticsearch://reference/elasticsearch/mapping-reference/text.md#fielddata-mapping-param) is enabled, but **BEWARE**: enabling fielddata on a `text` field requires loading all of the terms into the JVM heap, which can be very expensive both in terms of memory and CPU. It seldom makes sense to access `text` fields from scripts.

::::



### The document `_source` [modules-scripting-source]

The document [`_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) can be accessed using the `_source.field_name` syntax. The `_source` is loaded as a map-of-maps, so properties within object fields can be accessed as, for example, `_source.name.first`.

::::{admonition} Prefer doc-values to _source
:class: important

Accessing the `_source` field is much slower than using doc-values. The _source field is optimised for returning several fields per result, while doc values are optimised for accessing the value of a specific field in many documents.

It makes sense to use `_source` when generating a [script field](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#script-fields) for the top ten hits from a search result but, for other search and aggregation use cases, always prefer using doc values.

::::


For instance:

```console
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "first_name": {
        "type": "text"
      },
      "last_name": {
        "type": "text"
      }
    }
  }
}

PUT my-index-000001/_doc/1?refresh
{
  "first_name": "Barry",
  "last_name": "White"
}

GET my-index-000001/_search
{
  "script_fields": {
    "full_name": {
      "script": {
        "lang": "painless",
        "source": "params._source.first_name + ' ' + params._source.last_name"
      }
    }
  }
}
```


### Stored fields [modules-scripting-stored]

*Stored fields* — fields explicitly marked as [`"store": true`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-store.md) in the mapping — can be accessed using the `_fields['field_name'].value` or `_fields['field_name']` syntax:

```console
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "full_name": {
        "type": "text",
        "store": true
      },
      "title": {
        "type": "text",
        "store": true
      }
    }
  }
}

PUT my-index-000001/_doc/1?refresh
{
  "full_name": "Alice Ball",
  "title": "Professor"
}

GET my-index-000001/_search
{
  "script_fields": {
    "name_with_title": {
      "script": {
        "lang": "painless",
        "source": "params._fields['title'].value + ' ' + params._fields['full_name'].value"
      }
    }
  }
}
```

::::{admonition} Stored vs `_source`
:class: tip

The `_source` field is just a special stored field, so the performance is similar to that of other stored fields. The `_source` provides access to the original document body that was indexed (including the ability to distinguish `null` values from empty fields, single-value arrays from plain scalars, etc).

The only time it really makes sense to use stored fields instead of the `_source` field is when the `_source` is very large and it is less costly to access a few small stored fields instead of the entire `_source`.

::::


