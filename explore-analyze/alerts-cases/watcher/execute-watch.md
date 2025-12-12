---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-execute-watch.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Instructions for manually executing watches for testing and debugging purposes.
---

# Execute a watch [execute-watch]

The execute watch endpoint lets you manually trigger watch execution for testing or debugging without waiting for its scheduled trigger. You can simulate watch execution, override its input and condition, and control how individual actions behave during the run. 

The examples below show how to execute an existing watch, customize its behavior during execution, and run an inline watch definition.

Here's a detailed example of executing the `my_watch` watch with various optional parameters:

```console
POST _watcher/watch/my_watch/_execute
{
  "trigger_data" : { <1>
     "triggered_time" : "now",
     "scheduled_time" : "now"
  },
  "alternative_input" : { <2>
    "foo" : "bar"
  },
  "ignore_condition" : true, <3>
  "action_modes" : {
    "my-action" : "force_simulate" <4>
  },
  "record_execution" : true <5>
}
```
% TEST[setup:my_active_watch]

1. The triggered and schedule times are provided.
2. The input as defined by the watch is ignored and instead the provided input
    is used as the execution payload.
3. The condition as defined by the watch is ignored and is assumed to
    evaluate to `true`.
4. Forces the simulation of `my-action`. Forcing the simulation means that
    throttling is ignored and the watch is simulated by {watcher} instead of
    being executed normally.
5. The execution of the watch creates a watch record in the watch history,
    and the throttling state of the watch is potentially updated accordingly.

This is an example of the output:

```console
{
  "_id": "my_watch_0-2015-06-02T23:17:55.124Z", <1>
  "watch_record": { <2>
    "@timestamp": "2015-06-02T23:17:55.124Z",
    "watch_id": "my_watch",
    "node": "my_node",
    "messages": [],
    "trigger_event": {
      "type": "manual",
      "triggered_time": "2015-06-02T23:17:55.124Z",
      "manual": {
        "schedule": {
          "scheduled_time": "2015-06-02T23:17:55.124Z"
        }
      }
    },
    "state": "executed",
    "status": {
      "version": 1,
      "execution_state": "executed",
      "state": {
        "active": true,
        "timestamp": "2015-06-02T23:17:55.111Z"
      },
      "last_checked": "2015-06-02T23:17:55.124Z",
      "last_met_condition": "2015-06-02T23:17:55.124Z",
      "actions": {
        "test_index": {
          "ack": {
            "timestamp": "2015-06-02T23:17:55.124Z",
            "state": "ackable"
          },
          "last_execution": {
            "timestamp": "2015-06-02T23:17:55.124Z",
            "successful": true
          },
          "last_successful_execution": {
            "timestamp": "2015-06-02T23:17:55.124Z",
            "successful": true
          }
        }
      }
    },
    "input": {
      "simple": {
        "payload": {
          "send": "yes"
        }
      }
    },
    "condition": {
      "always": {}
    },
    "result": { <3>
      "execution_time": "2015-06-02T23:17:55.124Z",
      "execution_duration": 12608,
      "input": {
        "type": "simple",
        "payload": {
          "foo": "bar"
        },
        "status": "success"
      },
      "condition": {
        "type": "always",
        "met": true,
        "status": "success"
      },
      "actions": [
        {
          "id": "test_index",
          "index": {
            "response": {
              "index": "test",
              "version": 1,
              "created": true,
              "result": "created",
              "id": "AVSHKzPa9zx62AzUzFXY"
            }
          },
          "status": "success",
          "type": "index"
        }
      ]
    },
    "user": "test_admin" <4>
  }
}
```
% TESTRESPONSE[s/my_watch_0-2015-06-02T23:17:55.124Z/$body._id/]
% TESTRESPONSE[s/"triggered_time": "2015-06-02T23:17:55.124Z"/"triggered_time": "$body.watch_record.trigger_event.triggered_time"/]
% TESTRESPONSE[s/"@timestamp": "2015-06-02T23:17:55.124Z"/"@timestamp": "$body.watch_record.trigger_event.triggered_time"/]
% TESTRESPONSE[s/"scheduled_time": "2015-06-02T23:17:55.124Z"/"scheduled_time": "$body.watch_record.trigger_event.manual.schedule.scheduled_time"/]
% TESTRESPONSE[s/"execution_time": "2015-06-02T23:17:55.124Z"/"execution_time": "$body.watch_record.result.execution_time"/]
% TESTRESPONSE[s/"timestamp": "2015-06-02T23:17:55.111Z"/"timestamp": "$body.watch_record.status.state.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-06-02T23:17:55.124Z"/"timestamp": "$body.watch_record.status.actions.test_index.ack.timestamp"/]
% TESTRESPONSE[s/"last_checked": "2015-06-02T23:17:55.124Z"/"last_checked": "$body.watch_record.status.last_checked"/]
% TESTRESPONSE[s/"last_met_condition": "2015-06-02T23:17:55.124Z"/"last_met_condition": "$body.watch_record.status.last_met_condition"/]
% TESTRESPONSE[s/"execution_duration": 12608/"execution_duration": "$body.watch_record.result.execution_duration"/]
% TESTRESPONSE[s/"id": "AVSHKzPa9zx62AzUzFXY"/"id": "$body.watch_record.result.actions.0.index.response.id"/]
% TESTRESPONSE[s/"node": "my_node"/"node": "$body.watch_record.node"/]
1. The id of the watch record as it would be stored in the `.watcher-history` index.
2. The watch record document as it would be stored in the `.watcher-history` index.
3. The watch execution results.
4. The user used to execute the watch.

You can set a different execution mode for every action by associating the mode
name with the action id:

```console
POST _watcher/watch/my_watch/_execute
{
  "action_modes" : {
    "action1" : "force_simulate",
    "action2" : "skip"
  }
}
```
% TEST[setup:my_active_watch]

You can also associate a single execution mode with all the actions in the watch
using `_all` as the action id:

```console
POST _watcher/watch/my_watch/_execute
{
  "action_modes" : {
    "_all" : "force_execute"
  }
}
```
% TEST[setup:my_active_watch]

The following example shows how to execute a watch inline:

```console
POST _watcher/watch/_execute
{
  "watch" : {
    "trigger" : { "schedule" : { "interval" : "10s" } },
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
}
```

All other settings for this API still apply when inlining a watch. In the
following snippet, while the inline watch defines a `compare` condition,
during the execution this condition will be ignored:

```console
POST _watcher/watch/_execute
{
  "ignore_condition" : true,
  "watch" : {
    "trigger" : { "schedule" : { "interval" : "10s" } },
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
}
```