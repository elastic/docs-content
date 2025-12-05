---
navigation_title: Adding conditions to actions
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/action-conditions.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Instructions for adding per-action conditions to execute different actions based on specific criteria.
---

# Adding conditions to actions [action-conditions]

When a watch is triggered, its condition determines whether to execute the watch actions. You can also add a condition to each individual action, enabling a single watch to execute different actions based on their respective conditions. For example, a watch could always send an email when hits are found but only trigger a pager notification when there are more than 5 hits.

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
          "size" : 0,
          "query" : { "match" : { "status" : "error" } }
        }
      }
    }
  },
  "condition" : {
    "compare" : { "ctx.payload.hits.total" : { "gt" : 0 } }
  },
  "actions" : {
    "email_administrator" : {
      "email" : {
        "to" : "sys.admino@host.domain",
        "subject" : "Encountered {{ctx.payload.hits.total}} errors",
        "body" : "Too many error in the system, see attached data",
        "attachments" : {
          "attached_data" : {
            "data" : {
              "format" : "json"
            }
          }
        },
        "priority" : "high"
      }
    },
    "notify_pager" : {
      "condition": { <1>
        "compare" : { "ctx.payload.hits.total" : { "gt" : 5 } }
      },
      "webhook" : {
        "method" : "POST",
        "host" : "pager.service.domain",
        "port" : 1234,
        "path" : "/{{watch_id}}",
        "body" : "Encountered {{ctx.payload.hits.total}} errors"
      }
    }
  }
}
```

1. A `condition` that only applies to the `notify_pager` action, which restricts its execution to when the condition succeeds (at least 5 hits in this case).
