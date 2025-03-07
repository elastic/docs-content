---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-search-request.html
applies_to:
  stack: ga
  serverless: ga
---

# Define runtime fields in a search request [runtime-search-request]

You can specify a `runtime_mappings` section in a search request to create runtime fields that exist only as part of the query. You specify a script as part of the `runtime_mappings` section, just as you would if [adding a runtime field to the mappings](map-runtime-field.md).

Defining a runtime field in a search request uses the same format as defining a runtime field in the index mapping. Just copy the field definition from the `runtime` in the index mapping to the `runtime_mappings` section of the search request.

The following search request adds a `day_of_week` field to the `runtime_mappings` section. The field values will be calculated dynamically, and only within the context of this search request:

```console
GET my-index-000001/_search
{
  "runtime_mappings": {
    "day_of_week": {
      "type": "keyword",
      "script": {
        "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ENGLISH))"
      }
    }
  },
  "aggs": {
    "day_of_week": {
      "terms": {
        "field": "day_of_week"
      }
    }
  }
}
```
% TEST[continued]


## Create runtime fields that use other runtime fields [runtime-search-request-examples]

You can even define runtime fields in a search request that return values from other runtime fields. For example, let’s say you bulk index some sensor data:

```console
POST my-index-000001/_bulk?refresh=true
{"index":{}}
{"@timestamp":1516729294000,"model_number":"QVKC92Q","measures":{"voltage":"5.2","start": "300","end":"8675309"}}
{"index":{}}
{"@timestamp":1516642894000,"model_number":"QVKC92Q","measures":{"voltage":"5.8","start": "300","end":"8675309"}}
{"index":{}}
{"@timestamp":1516556494000,"model_number":"QVKC92Q","measures":{"voltage":"5.1","start": "300","end":"8675309"}}
{"index":{}}
{"@timestamp":1516470094000,"model_number":"QVKC92Q","measures":{"voltage":"5.6","start": "300","end":"8675309"}}
{"index":{}}
{"@timestamp":1516383694000,"model_number":"HG537PU","measures":{"voltage":"4.2","start": "400","end":"8625309"}}
{"index":{}}
{"@timestamp":1516297294000,"model_number":"HG537PU","measures":{"voltage":"4.0","start": "400","end":"8625309"}}
```

You realize after indexing that your numeric data was mapped as type `text`. You want to aggregate on the `measures.start` and `measures.end` fields, but the aggregation fails because you can’t aggregate on fields of type `text`. Runtime fields to the rescue! You can add runtime fields with the same name as your indexed fields and modify the data type:

```console
PUT my-index-000001/_mapping
{
  "runtime": {
    "measures.start": {
      "type": "long"
    },
    "measures.end": {
      "type": "long"
    }
  }
}
```
%  TEST[continued]

Runtime fields take precedence over fields defined with the same name in the index mappings. This flexibility allows you to shadow existing fields and calculate a different value, without modifying the field itself. If you made a mistake in your index mapping, you can use runtime fields to calculate values that [override values](override-field-values-at-query-time.md) in the mapping during the search request.

Now, you can easily run an [average aggregation](elasticsearch://reference/data-analysis/aggregations/search-aggregations-metrics-avg-aggregation.md) on the `measures.start` and `measures.end` fields:

```console
GET my-index-000001/_search
{
  "aggs": {
    "avg_start": {
      "avg": {
        "field": "measures.start"
      }
    },
    "avg_end": {
      "avg": {
        "field": "measures.end"
      }
    }
  }
}
```
%  TEST[continued]
%  TEST[s/_search/_search?filter_path=aggregations/]

The response includes the aggregation results without changing the values for the underlying data:

```console-result
{
  "aggregations" : {
    "avg_start" : {
      "value" : 333.3333333333333
    },
    "avg_end" : {
      "value" : 8658642.333333334
    }
  }
}
```

Further, you can define a runtime field as part of a search query that calculates a value, and then run a [stats aggregation](elasticsearch://reference/data-analysis/aggregations/search-aggregations-metrics-stats-aggregation.md) on that field *in the same query*.

The `duration` runtime field doesn’t exist in the index mapping, but we can still search and aggregate on that field. The following query returns the calculated value for the `duration` field and runs a stats aggregation to compute statistics over numeric values extracted from the aggregated documents.

```console
GET my-index-000001/_search
{
  "runtime_mappings": {
    "duration": {
      "type": "long",
      "script": {
        "source": """
          emit(doc['measures.end'].value - doc['measures.start'].value);
          """
      }
    }
  },
  "aggs": {
    "duration_stats": {
      "stats": {
        "field": "duration"
      }
    }
  }
}
```
%  TEST[continued]
%  TEST[s/_search/_search?filter_path=aggregations/]

Even though the `duration` runtime field only exists in the context of a search query, you can search and aggregate on that field. This flexibility is incredibly powerful, enabling you to rectify mistakes in your index mappings and dynamically complete calculations all within a single search request.

```console-result
{
  "aggregations" : {
    "duration_stats" : {
      "count" : 6,
      "min" : 8624909.0,
      "max" : 8675009.0,
      "avg" : 8658309.0,
      "sum" : 5.1949854E7
    }
  }
}
```

