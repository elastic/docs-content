---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: all shards failed"
# is mapped_pages needed for newly created docs?
---

# Fix all shards failed error [all-shards-failed]

```
Error: all shards failed
```

This error indicates that {{es}} failed to retrieve a response from any shard involved in a query. This can result from shard allocation issues, misconfiguration, insufficient resources, or unsupported operations such as aggregating on text fields. 

##  Improper use of text fields

Text fields aren't optimized for operations like sorting or aggregations by default. Attempting these operations may trigger the error.

To fix, use the `.keyword` sub-field:

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

If no `.keyword` sub-field exists, update the mapping to handle [multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md):

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

## Metric aggregations on text fields

[Metric aggregations](elasticsearch://reference/aggregations/metrics.md) require numeric fields. Attempting them on text fields will fail.

Use a script to convert the text to numeric:

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

To confirm, check cluster health:

```console
GET _cluster/health
```

Identify and resolve the cause. If necessary, and as a last resort, delete the problematic index.

## Misused global aggregation

[Global aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-global-aggregation.md) must be top-level. Nesting them incorrectly causes errors.

To fix, structure the query so the `global` aggregation is top-level:

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

The [reverse_nested](elasticsearch://reference/aggregations/search-aggregations-bucket-reverse-nested-aggregation.md) aggregation must appear within a `nested` context.

To fix, structure the query so the `reverse_nested` aggregation is within a `nested` context:

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
