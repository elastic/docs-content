---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Transforms"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform.html
---

# Transforms [transform]

A *{{watcher-transform}}* processes and changes the payload in the watch execution context to prepare it for the watch actions. {{watcher}} supports three types of {{watcher-transforms}}:

* [`search`](transform-search.md)
* [`script`](transform-script.md)
* [`chain`](transform-chain.md)

::::{note}
{{watcher-transforms-cap}} are optional. When none are defined, the actions have access to the payload as loaded by the watch input.
::::

You can define {{watcher-transforms}} in two places:

* As a top level construct in the watch definition. In this case, the payload is transformed before any of the watch actions are executed.
* As part of the definition of an action. In this case, the payload is transformed before that action is executed. The transformation is only applied to the payload for that specific action.

If all actions require the same view of the payload, define a {{watcher-transform}} as part of the watch definition. If each action requires a different view of the payload, define different {{watcher-transforms}} as part of the action definitions so each action has the payload prepared by its own dedicated {{watcher-transform}}.

The following example defines two {{watcher-transforms}}, one at the watch level and one as part of the definition of the `my_webhook` action.

```js
{
  "trigger" : { ...}
  "input" : { ... },
  "condition" : { ... },
  "transform" : { <1>
    "search" : {
      "request": {
        "body" : { "query" : { "match_all" : {} } }
      }
    }
  },
  "actions" : {
    "my_webhook": {
      "transform" : { <2>
      	"script" : "return ctx.payload.hits"
      },
      "webhook" : {
      	"host" : "host.domain",
      	"port" : 8089,
      	"path" : "/notify/{{ctx.watch_id}}"
      }
    }
  ]
}
```

1. A watch level `transform`
2. An action level `transform`
%  NOTCONSOLE