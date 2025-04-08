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

This error indicates that Elasticsearch failed to retrieve a response from any shard involved in a query. This can result from shard allocation issues, misconfiguration, insufficient resources, or unsupported operations such as aggregating on text fields. 

## Fix improper use of text fields

Text fields aren't optimized for operations like sorting or aggregations by default. Attempting these operations may trigger the error.

### Resolution

Use the `.keyword` sub-field:

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

If no `.keyword` sub-field exists, update the mapping to handle multi-fields:

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

## Fix metric aggregations on text fields

Metric aggregations require numeric fields. Attempting them on text fields will fail.

### Resolution

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

## Fix failed shard recovery

A shard failure during recovery can prevent successful queries.

### Resolution

Check cluster health:

```console
GET _cluster/health
```

Identify and resolve the cause. If necessary, and as a last resort, delete the problematic index.

## Fix misused global aggregation

Global aggregations must be top-level. Nesting them incorrectly causes errors.

### Resolution

Structure the query so the `global` aggregation is top-level:

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

## Fix reverse_nested usage errors

The `reverse_nested` aggregation must appear within a `nested` context.

### Resolution

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

## View shard allocation and status

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
