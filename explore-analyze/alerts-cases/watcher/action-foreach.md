---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/action-foreach.html
---

# Running an action for each element in an array [action-foreach]

You can use the `foreach` field in an action to trigger the configured action for every element within that array.

In order to protect from long running watches, you can use the `max_iterations` field to limit the maximum amount of runs that each watch executes. If this limit is reached, the execution is gracefully stopped. If not set, this field defaults to one hundred.

```console
PUT _watcher/watch/log_event_watch
{
  "trigger" : {
    "schedule" : { "interval" : "5m" }
  },
  "input" : {
    "search" : {
      "request" : {
        "indices" : "log-events",
        "body" : {
          "query" : { "match" : { "status" : "error" } }
        }
      }
    }
  },
  "condition" : {
    "compare" : { "ctx.payload.hits.total" : { "gt" : 0 } }
  },
  "actions" : {
    "log_hits" : {
      "foreach" : "ctx.payload.hits.hits", <1>
      "max_iterations" : 500,
      "logging" : {
        "text" : "Found id {{ctx.payload._id}} with field {{ctx.payload._source.my_field}}"
      }
    }
  }
}
```

1. The logging statement will be executed for each of the returned search hits.
