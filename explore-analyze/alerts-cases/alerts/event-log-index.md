---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/event-log-index.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Event log index [event-log-index]

::::{warning} 
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

Use the event log index to determine:

* Whether a rule ran successfully but its associated actions did not
* Whether a rule was ever activated
* Additional information about errors when the rule ran
* Run durations for the rules and actions

## Example event log queries [_example_event_log_queries]

The following event log query looks at all events related to a specific rule id:

```txt
GET /.kibana-event-log*/_search
{
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "event.provider": {
              "value": "alerting"
            }
          }
        },
        // optionally filter by specific action event
        {
          "term": {
            "event.action": "active-instance"
              | "execute-action"
              | "new-instance"
              | "recovered-instance"
              | "execute"
          }
        },
        // filter by specific rule id
        {
          "nested": {
            "path": "kibana.saved_objects",
            "query": {
              "bool": {
                "filter": [
                  {
                    "term": {
                      "kibana.saved_objects.id": {
                        "value": "b541b690-bfc4-11eb-bf08-05a30cefd1fc"
                      }
                    }
                  },
                  {
                    "term": {
                      "kibana.saved_objects.type": "alert"
                    }
                  }

                ]
              }
            }
          }
        }
      ]
    }
  }
}
```

The following event log query looks at all events related to running a rule or action. These events include duration:

```txt
GET /.kibana-event-log*/_search
{
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "event.action": {
              "value": "execute"
            }
          }
        },
        // optionally filter by specific rule or action id
        {
          "nested": {
            "path": "kibana.saved_objects",
            "query": {
              "bool": {
                "filter": [
                  {
                    "term": {
                      "kibana.saved_objects.id": {
                        "value": "b541b690-bfc4-11eb-bf08-05a30cefd1fc"
                      }
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }
  }
}
```

The following event log query looks at the errors. You should see an `error.message` property in that event, with a message that might provide more details about why the action encountered an error:

```txt
{
  "event": {
    "provider": "actions",
    "action": "execute",
    "start": "2020-03-31T04:27:30.392Z",
    "end": "2020-03-31T04:27:30.393Z",
    "duration": 1000000
  },
  "kibana": {
    "namespace": "default",
    "saved_objects": [
      {
        "type": "action",
        "id": "7a6fd3c6-72b9-44a0-8767-0432b3c70910"
      }
    ],
  },
  "message": "action executed: .server-log:7a6fd3c6-72b9-44a0-8767-0432b3c70910: server-log",
  "@timestamp": "2020-03-31T04:27:30.393Z",
}
```

You might also see the errors for the rules, which can use in the next search query. For example:

```txt
{
  "event": {
    "provider": "alerting",
    "start": "2020-03-31T04:27:30.392Z",
    "end": "2020-03-31T04:27:30.393Z",
    "duration": 1000000
  },
  "kibana": {
    "namespace": "default",
    "saved_objects": [
      {
        "rel" : "primary",
        "type" : "alert",
      	  "id" : "30d856c0-b14b-11eb-9a7c-9df284da9f99"
      }
    ],
  },
  "message": "rule executed: .index-threshold:30d856c0-b14b-11eb-9a7c-9df284da9f99: 'test'",
  "error" : {
    "message" : "Saved object [action/ef0e2530-b14a-11eb-9a7c-9df284da9f99] not found"
  },
}
```

You can also query the event log for failures, which should return more specific details about rules which failed by targeting the event.outcome:

```txt
GET .kibana-event-log-*/_search
{
  "query": {
	"bool": {
  		"must": [
    		{ "match": { "event.outcome": "failure" }}
  	  ]
	  }
  }
}
```

Here’s an example of what failed credentials from Google SMTP might look like from the response:

```txt
"error" : {
  "message" : """error sending email: Invalid login: 535-5.7.8 Username and Password not accepted. Learn more at
535 5.7.8  https://support.google.com/mail/?p=BadCredentials e207sm3359731pfh.171 - gsmtp"""
},
```
