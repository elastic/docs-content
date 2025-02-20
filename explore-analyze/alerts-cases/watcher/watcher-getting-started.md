---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-getting-started.html
---

# Getting started with Watcher [watcher-getting-started]

To set up a watch to start sending alerts:

* [Schedule the watch and define an input](#log-add-input).
* [Add a condition](#log-add-condition) that checks to see if an alert needs to be sent.
* [Configure an action](#log-take-action) to send an alert when the condition is met.

## Schedule the watch and define an input [log-add-input]

A watch [schedule](trigger-schedule.md) controls how often a watch is triggered. The watch [input](input.md) gets the data that you want to evaluate.

To periodically search log data and load the results into the watch, you could use an [interval](/explore-analyze/alerts-cases/watcher/schedule-types.md#schedule-interval) schedule and a [search](input-search.md) input. For example, the following Watch searches the `logs` index for errors every 10 seconds:

```console
PUT _watcher/watch/log_error_watch
{
  "trigger" : {
    "schedule" : { "interval" : "10s" } <1>
  },
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "logs" ],
        "body" : {
          "query" : {
            "match" : { "message": "error" }
          }
        }
      }
    }
  }
}
```

1. Schedules are typically configured to run less frequently. This example sets the interval to 10 seconds so you can easily see the watches being triggered. Since this watch runs so frequently, don’t forget to [delete the watch](#log-delete) when you’re done experimenting.


If you check the watch history you’ll see that the watch is being triggered every 10 seconds. However, the search isn’t returning any results so nothing is loaded into the watch payload.

For example, the following request retrieves the last ten watch executions (watch records) from the watch history:

```console
GET .watcher-history*/_search?pretty
{
  "sort" : [
    { "result.execution_time" : "desc" }
  ]
}
```

## Add a condition [log-add-condition]

A [condition](condition.md) evaluates the data you’ve loaded into the watch and determines if any action is required. Now that you’ve loaded log errors into the watch, you can define a condition that checks to see if any errors were found.

For example, the following compare condition simply checks to see if the search input returned any hits.

```console
PUT _watcher/watch/log_error_watch
{
  "trigger" : { "schedule" : { "interval" : "10s" }},
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "logs" ],
        "body" : {
          "query" : {
            "match" : { "message": "error" }
          }
        }
      }
    }
  },
  "condition" : {
    "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }} <1>
  }
}
```

1. The [compare](condition-compare.md) condition lets you easily compare against values in the execution context.

For this compare condition to evaluate to `true`, you need to add an event to the `logs` index that contains an error. For example, the following request adds a 404 error to the `logs` index:

```console
POST logs/_doc
{
  "timestamp": "2015-05-17T18:12:07.613Z",
  "request": "GET index.html",
  "status_code": 404,
  "message": "Error: File not found"
}
```

Once you add this event, the next time the watch executes its condition will evaluate to `true`. The condition result is recorded as part of the `watch_record` each time the watch executes, so you can verify whether or not the condition was met by searching the watch history:

```console
GET .watcher-history*/_search?pretty
{
  "query" : {
    "bool" : {
      "must" : [
        { "match" : { "result.condition.met" : true }},
        { "range" : { "result.execution_time" : { "gte" : "now-10s" }}}
      ]
    }
  }
}
```

## Configure an action [log-take-action]

Recording watch records in the watch history is nice, but the real power of {{watcher}} is being able to do something when the watch condition is met. A watch’s [actions](actions.md) define what to do when the watch condition evaluates to `true`. You can send emails, call third-party webhooks, write documents to an Elasticsearch index, or log messages to the standard Elasticsearch log files.

For example, the following action writes a message to the Elasticsearch log when an error is detected.

```console
PUT _watcher/watch/log_error_watch
{
  "trigger" : { "schedule" : { "interval" : "10s" }},
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "logs" ],
        "body" : {
          "query" : {
            "match" : { "message": "error" }
          }
        }
      }
    }
  },
  "condition" : {
    "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }}
  },
  "actions" : {
    "log_error" : {
      "logging" : {
        "text" : "Found {{ctx.payload.hits.total}} errors in the logs"
      }
    }
  }
}
```

## Delete the Watch [log-delete]

Since the `log_error_watch` is configured to run every 10 seconds, make sure you delete it when you’re done experimenting. Otherwise, the noise from this sample watch will make it hard to see what else is going on in your watch history and log file.

To remove the watch, use the [delete watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-delete-watch):

```console
DELETE _watcher/watch/log_error_watch
```

## Required security privileges [required-security-privileges]

To enable users to create and manipulate watches, assign them the `watcher_admin` security role. Watcher admins can also view watches, watch history, and triggered watches.

To allow users to view watches and the watch history, assign them the `watcher_user` security role. Watcher users cannot create or manipulate watches; they are only allowed to execute read-only watch operations.

## Where to go next [next-steps]

* See [*How {{watcher}} works*](how-watcher-works.md) for more information about the anatomy of a watch and the watch lifecycle.
* See [*Example watches*](example-watches.md) for more examples of setting up a watch.
* See the [Example Watches](https://github.com/elastic/examples/tree/master/Alerting) in the Elastic Examples repo for additional sample watches you can use as a starting point for building custom watches.
