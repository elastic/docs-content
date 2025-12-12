---
navigation_title: Chain {{watcher-transform}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-chain.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for the chain transform that executes multiple transforms sequentially.
---

# Chain payload transform [transform-chain]

Use the **chain** {{watcher-transform}} to execute an ordered list of transforms sequentially, where the output of one transform serves as the input of the next. This transform enables you to build complex data processing pipelines by combining search, script, and other chain transforms.

You can use chain {{watcher-transforms}} to build more complex transforms out of the other available transforms. For example, you can combine a [`search`](transform-search.md) {{watcher-transform}} and a [`script`](transform-script.md) {{watcher-transform}}, as shown in the following snippet:

```js
"transform" : {
  "chain" : [ <1>
    {
      "search" : {  <2>
        "request": {
          "indices" : [ "logstash-*" ],
          "body" : {
            "size" : 0,
            "query" : {
              "match" : { "priority" : "error" }
            }
          }
        }
      }
    },
    {
      "script" : "return [ 'error_count' : ctx.payload.hits.total ]"  <3>
    }
  ]
}
```

1. The `chain` {{watcher-transform}} definition
2. The first transform in the chain (in this case, a `search` {{watcher-transform}})
3. The second and final transform in the chain (in this case, a `script` {{watcher-transform}})

This example executes a `count` search on the cluster to look for `error` events. The search results are then passed to the second `script` {{watcher-transform}}. The `script` {{watcher-transform}} extracts the total hit count and assigns it to the `error_count` field in a newly-generated payload. This new payload is the output of the `chain` {{watcher-transform}} and replaces the payload in the watch execution context.
