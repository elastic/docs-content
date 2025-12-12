---
navigation_title: Inputs
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for watch input types that load data into the execution context.
---

# Watch inputs [input]

When a watch is triggered, its input loads data into the execution context, making the payload accessible during subsequent watch execution phases. You can use this data to evaluate conditions and pass information to actions. {{watcher}} supports four input types: simple, search, HTTP, and chain.

{{watcher}} supports four input types:

* [`simple`](input-simple.md): load static data into the execution context.
* [`search`](input-search.md): load the results of a search into the execution context.
* [`http`](input-http.md): load the results of an HTTP request into the execution context.
* [`chain`](input-chain.md): use a series of inputs to load data into the execution context.

::::{note}
If you don’t define an input for a watch, an empty payload is loaded into the execution context.
::::
