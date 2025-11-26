---
navigation_title: Chain input
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input-chain.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for the chain input type that loads data from multiple sources sequentially.
---

# Chain input [input-chain]

Use the **chain** input to load data from multiple sources into the watch execution context when the watch is triggered. The inputs in a chain are processed sequentially, and data loaded by one input can be accessed by subsequent inputs in the chain, enabling you to build on previous results or combine data from different sources.

The `chain` input enables you to perform actions based on data from multiple sources. You can also use the data collected by one input to load data from another source.

For example, the following chain input loads data from an HTTP server using the path set by a `simple` input:

```js
"input" : {
  "chain" : {
    "inputs" : [ <1>
      {
        "first" : {
          "simple" : { "path" : "/_search" }
        }
      },
      {
        "second" : {
          "http" : {
            "request" : {
              "host" : "localhost",
              "port" : 9200,
              "path" : "{{ctx.payload.first.path}}" <2>
            }
          }
        }
      }
    ]
  }
}
```

1. The inputs in a chain are specified as an array to guarantee the order in which the inputs are processed. (JSON does not guarantee the order of arbitrary objects.)
2. Loads the `path` set by the `first` input.

## Accessing chained input data [_accessing_chained_input_data]

To reference data loaded by a particular input, you use the input’s name, `ctx.payload.<input-name>.<value>`.

## Transforming chained input data [_transforming_chained_input_data]

In certain use-cases the output of the first input should be used as input in a subsequent input. This requires you to do a transform, before you pass the data on to the next input.

In order to achieve this you can use a transform input between the two specified inputs, see the following example. Note, that the first input will still be available in its original form in `ctx.payload.first`.

```js
"input" : {
  "chain" : {
    "inputs" : [
      {
        "first" : {
          "simple" : { "path" : "/_search" }
        }
      },
      {
        "second" : {
          "transform" : {
            "script" : "return [ 'path' : ctx.payload.first.path + '/' ]"
          }
        }
      },
      {
        "third" : {
          "http" : {
            "request" : {
              "host" : "localhost",
              "port" : 9200,
              "path" : "{{ctx.payload.second.path}}"
            }
          }
        }
      }
    ]
  }
}
```
