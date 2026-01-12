---
applies_to:
  stack:
navigation_title: "Error: All shards failed"
---

# Fix error: All shards failed [all-shards-failed]

```console
Error: all shards failed
```

The `all shards failed` error indicates that {{es}} couldn't get a successful response from any of the shards involved in the query. Possible causes include shard allocation issues, misconfiguration, insufficient resources, or unsupported operations such as aggregating on text fields. 

##  Unsupported operations on text fields

The `all shards failed` error can occur when you try to sort or aggregate on `text` fields. These fields are designed for full-text search and don't support exact-value operations like sorting and aggregation.

To fix this issue, use a `.keyword` subfield:

```console
GET my-index/_search
{
  "aggs": {
    "names": {
      "terms": {
        "field": "name.keyword"
      }
    }
  }
}
```

If no `.keyword` subfield exists, define a [multi-field](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md#types-multi-fields) mapping:

```console
PUT my-index
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```

### Metric aggregations on text fields

The `all shards failed` error can also occur when you use a metric aggregation on a text field. [Metric aggregations](elasticsearch://reference/aggregations/metrics.md) require numeric fields. 

You can use a script to convert the text value to a number at query time:

```console
GET my-index/_search
{
  "aggs": {
    "total_cost": {
      "sum": {
        "script": {
          "source": "Integer.parseInt(doc.cost.value)"
        }
      }
    }
  }
}
```

Or change the field mapping to a numeric type:

```console
PUT my-index
{
  "mappings": {
    "properties": {
      "cost": {
        "type": "integer"
      }
    }
  }
}
```

## Failed shard recovery

A shard failure during recovery can prevent successful queries.

To identify the cause, check the cluster health:

```console
GET _cluster/health
```

As a last resort, you can delete the problematic index.

## Misused global aggregation

[Global aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-global-aggregation.md) must be defined at the top level of the aggregations object. Nesting can cause errors.

To fix this issue, structure the query so that the `global` aggregation appears at the top level:

```console
GET my-index/_search
{
  "size": 0,
  "aggs": {
    "all_products": {
      "global": {},
      "aggs": {
        "genres": {
          "terms": {
            "field": "cost"
          }
        }
      }
    }
  }
}
```

## Reverse_nested usage errors

Using a [`reverse_nested`](elasticsearch://reference/aggregations/search-aggregations-bucket-reverse-nested-aggregation.md) aggregation outside of a `nested` context causes errors.

To fix this issue, structure the query so that the `reverse_nested` aggregation is inside a `nested` aggregation:

```console
GET my-index/_search
{
  "aggs": {
    "comments": {
      "nested": {
        "path": "comments"
      },
      "aggs": {
        "top_usernames": {
          "terms": {
            "field": "comments.username"
          },
          "aggs": {
            "comment_issue": {
              "reverse_nested": {},
              "aggs": {
                "top_tags": {
                  "terms": {
                    "field": "tags"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Further troubleshooting

Use the `_cat/shards` API to view shard status and troubleshoot further.

```console
GET _cat/shards
```

For a specific index:

```console
GET _cat/shards/my-index
```

Example output:

```console-result
my-index 5 p STARTED    0  283b 127.0.0.1 ziap
my-index 5 r UNASSIGNED
my-index 2 p STARTED    1 3.7kb 127.0.0.1 ziap
my-index 2 r UNASSIGNED
my-index 3 p STARTED    3 7.2kb 127.0.0.1 ziap
my-index 3 r UNASSIGNED
my-index 1 p STARTED    1 3.7kb 127.0.0.1 ziap
my-index 1 r UNASSIGNED
my-index 4 p STARTED    2 3.8kb 127.0.0.1 ziap
my-index 4 r UNASSIGNED
my-index 0 p STARTED    0  283b 127.0.0.1 ziap
my-index 0 r UNASSIGNED
```
