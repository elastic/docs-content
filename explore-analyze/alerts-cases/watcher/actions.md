---
navigation_title: Actions
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/actions.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for action types that execute when watch conditions are met.
---

# Watch actions [actions]

When a watch's condition is met, its actions are executed unless throttled. A watch can perform multiple actions, executed sequentially and independently. Actions have access to the watch payload and can use it to customize their behavior, such as using payload data to populate an email template. {{watcher}} supports email, webhook, index, logging, Slack, PagerDuty, and Jira actions.

::::{note}
If no actions are defined for a watch, no actions are executed. However, a `watch_record` is still written to the watch history.
::::

Actions have access to the payload in the execution context. They can use it to support their execution in any way they need. For example, the payload might serve as a model for a templated email body.

{{watcher}} supports the following actions:

* [`email`](actions-email.md)
* [`webhook`](actions-webhook.md)
* [`index`](actions-index.md)
* [`logging`](actions-logging.md)
* [`slack`](actions-slack.md)
* [`pagerduty`](actions-pagerduty.md)
* [`jira`](actions-jira.md)

## Acknowledgement and throttling [actions-ack-throttle]

During the watch execution, once the condition is met, a decision is made per configured action as to whether it should be throttled. The main purpose of action throttling is to prevent too many executions of the same action for the same watch.

For example, suppose you have a watch that detects errors in an application’s log entries. The watch is triggered every five minutes and searches for errors during the last hour. In this case, if there are errors, there is a period of time where the watch is checked and its actions are executed multiple times based on the same errors. As a result, the system administrator receives multiple notifications about the same issue, which can be annoying.

To address this issue, {{watcher}} supports time-based throttling. You can define a throttling period as part of the action configuration to limit how often the action is executed. When you set a throttling period, {{watcher}} prevents repeated execution of the action if it has already executed within the throttling period time frame (`now - throttling period`).

The following snippet shows a watch for the scenario described above - associating a throttle period with the `email_administrator` action:

```console
PUT _watcher/watch/error_logs_alert
{
  "metadata" : {
    "color" : "red"
  },
  "trigger" : {
    "schedule" : {
      "interval" : "5m"
    }
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
    "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
  },
  "actions" : {
    "email_administrator" : {
      "throttle_period": "15m", <1>
      "email" : { <2>
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
    }
  }
}
```

1. There will be at least 15 minutes between subsequent `email_administrator` action executions.
2. See [Email action](actions-email.md) for more information.

You can also define a throttle period at the watch level. The watch-level throttle period serves as the default throttle period for all of the actions defined in the watch:

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
    "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
  },
  "throttle_period" : "15m", <1>
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

1. There will be at least 15 minutes between subsequent action executions (applies to both `email_administrator` and `notify_pager` actions)

If you do not define a throttle period at the action or watch level, the global default throttle period is applied. Initially, this is set to 5 seconds. To change the global default, configure the `xpack.watcher.execution.default_throttle_period` setting in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.watcher.execution.default_throttle_period: 15m
```

{{watcher}} also supports acknowledgement-based throttling. You can acknowledge a watch using the [ack watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-ack-watch) to prevent the watch actions from being executed again while the watch condition remains `true`. This essentially tells {{watcher}} "I received the notification and I’m handling it, do not notify me about this error again". An acknowledged watch action remains in the `acked` state until the watch’s condition evaluates to `false`. When that happens, the action’s state changes to `awaits_successful_execution`.

To acknowledge an action, you use the [ack watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-ack-watch):

```console
POST _watcher/watch/<id>/_ack/<action_ids>
```

Where `<id>` is the id of the watch and `<action_ids>` is a comma-separated list of the action ids you want to acknowledge. To acknowledge all actions, omit the `actions` parameter.

The following diagram illustrates the throttling decisions made for each action of a watch during its execution:

:::{image} /explore-analyze/images/elasticsearch-reference-action-throttling.jpg
:alt: action throttling
:::

### Example

To demonstrate how throttling works in practice and how it can be configured for individual actions within a watch, let’s walk through the full process step by step.

First, let's create a new watch:

```console
PUT _watcher/watch/my_watch
{
  "trigger" : {
    "schedule" : {
      "yearly" : { "in" : "february", "on" : 29, "at" : "noon" }
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
  "actions": {
    "test_index": {
      "throttle_period": "15m",
      "index": {
        "index": "test"
      }
    }
  }
}
```
% TESTSETUP

The current status of a watch and the state of its actions is returned with the watch definition when you call the [Get Watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-get-watch):

```console
GET _watcher/watch/my_watch
```
% TEST[continued]

The action state of a newly-created watch is `awaits_successful_execution`:

```console

{
  "found": true,
  "_seq_no": 0,
  "_primary_term": 1,
  "_version": 1,
  "_id": "my_watch",
  "status": {
    "version": 1,
    "actions": {
      "test_index": {
        "ack": {
          "timestamp": "2015-05-26T18:04:27.723Z",
          "state": "awaits_successful_execution"
        }
      }
    },
    "state": ...
  },
  "watch": ...
}
```
% TESTRESPONSE[s/"state": \.\.\./"state": "$body.status.state"/]
% TESTRESPONSE[s/"watch": \.\.\./"watch": "$body.watch"/]
% TESTRESPONSE[s/"timestamp": "2015-05-26T18:04:27.723Z"/"timestamp": "$body.status.actions.test_index.ack.timestamp"/]

When the watch executes and the condition matches, the value of the `ack.state` changes to `ackable`. Let’s force execution of the watch and fetch it again to check the status:

```console

POST _watcher/watch/my_watch/_execute
{
  "record_execution" : true
}

GET _watcher/watch/my_watch
```
% TEST[continued]

and the action is now in `ackable` state:

```console

{
  "found": true,
  "_id": "my_watch",
  "_seq_no": 1,
  "_primary_term": 1,
  "_version": 2,
  "status": {
    "version": 2,
    "actions": {
      "test_index": {
        "ack": {
          "timestamp": "2015-05-26T18:04:27.723Z",
          "state": "ackable"
        },
        "last_execution" : {
          "timestamp": "2015-05-25T18:04:27.723Z",
          "successful": true
        },
        "last_successful_execution" : {
          "timestamp": "2015-05-25T18:04:27.723Z",
          "successful": true
        }
      }
    },
    "state": ...,
    "execution_state": "executed",
    "last_checked": ...,
    "last_met_condition": ...
  },
  "watch": ...
}
```
% TESTRESPONSE[s/"state": \.\.\./"state": "$body.status.state"/]
% TESTRESPONSE[s/"watch": \.\.\./"watch": "$body.watch"/]
% TESTRESPONSE[s/"last_checked": \.\.\./"last_checked": "$body.status.last_checked"/]
% TESTRESPONSE[s/"last_met_condition": \.\.\./"last_met_condition": "$body.status.last_met_condition"/]
% TESTRESPONSE[s/"timestamp": "2015-05-26T18:04:27.723Z"/"timestamp": "$body.status.actions.test_index.ack.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-05-25T18:04:27.723Z"/"timestamp": "$body.status.actions.test_index.last_execution.timestamp"/]

Now we can acknowledge it:

```console

PUT _watcher/watch/my_watch/_ack/test_index
GET _watcher/watch/my_watch
```
% TEST[continued]


```console

{
  "found": true,
  "_id": "my_watch",
  "_seq_no": 2,
  "_primary_term": 1,
  "_version": 3,
  "status": {
    "version": 3,
    "actions": {
      "test_index": {
        "ack": {
          "timestamp": "2015-05-26T18:04:27.723Z",
          "state": "acked"
        },
        "last_execution" : {
          "timestamp": "2015-05-25T18:04:27.723Z",
          "successful": true
        },
        "last_successful_execution" : {
          "timestamp": "2015-05-25T18:04:27.723Z",
          "successful": true
        }
      }
    },
    "state": ...,
    "execution_state": "executed",
    "last_checked": ...,
    "last_met_condition": ...
  },
  "watch": ...
}
```
% TESTRESPONSE[s/"state": \.\.\./"state": "$body.status.state"/]
% TESTRESPONSE[s/"watch": \.\.\./"watch": "$body.watch"/]
% TESTRESPONSE[s/"last_checked": \.\.\./"last_checked": "$body.status.last_checked"/]
% TESTRESPONSE[s/"last_met_condition": \.\.\./"last_met_condition": "$body.status.last_met_condition"/]
% TESTRESPONSE[s/"timestamp": "2015-05-26T18:04:27.723Z"/"timestamp": "$body.status.actions.test_index.ack.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-05-25T18:04:27.723Z"/"timestamp": "$body.status.actions.test_index.last_execution.timestamp"/]

Acknowledging an action throttles further executions of that action until its `ack.state` is reset to `awaits_successful_execution`. This happens when the condition of the watch is not met (the condition evaluates to `false`).

You can acknowledge multiple actions by assigning the `actions` parameter a comma-separated list of action ids:

```console
POST _watcher/watch/my_watch/_ack/action1,action2
```

To acknowledge all of the actions of a watch, simply omit the `actions` parameter:

```console
POST _watcher/watch/my_watch/_ack
```
% TEST[s/^/POST _watcher\/watch\/my_watch\/_execute\n{ "record_execution" : true }\n/]

The response looks like a get watch response, but only contains the status:

```console

{
  "status": {
    "state": {
      "active": true,
      "timestamp": "2015-05-26T18:04:27.723Z"
    },
    "last_checked": "2015-05-26T18:04:27.753Z",
    "last_met_condition": "2015-05-26T18:04:27.763Z",
    "actions": {
      "test_index": {
        "ack" : {
          "timestamp": "2015-05-26T18:04:27.713Z",
          "state": "acked"
        },
        "last_execution" : {
          "timestamp": "2015-05-25T18:04:27.733Z",
          "successful": true
        },
        "last_successful_execution" : {
          "timestamp": "2015-05-25T18:04:27.773Z",
          "successful": true
        }
      }
    },
    "execution_state": "executed",
    "version": 2
  }
}
```
% TESTRESPONSE[s/"last_checked": "2015-05-26T18:04:27.753Z"/"last_checked": "$body.status.last_checked"/]
% TESTRESPONSE[s/"last_met_condition": "2015-05-26T18:04:27.763Z"/"last_met_condition": "$body.status.last_met_condition"/]
% TESTRESPONSE[s/"timestamp": "2015-05-26T18:04:27.723Z"/"timestamp": "$body.status.state.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-05-26T18:04:27.713Z"/"timestamp": "$body.status.actions.test_index.ack.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-05-25T18:04:27.733Z"/"timestamp": "$body.status.actions.test_index.last_execution.timestamp"/]
% TESTRESPONSE[s/"timestamp": "2015-05-25T18:04:27.773Z"/"timestamp": "$body.status.actions.test_index.last_successful_execution.timestamp"/]


## Using SSL/TLS with OpenJDK [actions-ssl-openjdk]

As each distributor is free to choose how to package OpenJDK, it may happen, that even despite the exact same version, an OpenJDK distribution contains different parts under different Linux distributions.

This can lead to issues with any action or input that uses TLS, like the `jira`, `pagerduty`, `slack`, or `webhook` one, because of missing CA certs. If you encounter TLS errors, when writing watches that connect to TLS endpoints, you should try to upgrade to the latest available OpenJDK distribution for your platform and if that does not help, try to upgrade to Oracle JDK.
