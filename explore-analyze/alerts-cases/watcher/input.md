---
navigation_title: Inputs
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Inputs [input]

When a watch is triggered, its *input* loads data into the execution context. This payload is accessible during the subsequent watch execution phases. For example, you can base a watch’s condition on the data loaded by its input.

{{watcher}} supports four input types:

* [`simple`](input-simple.md): load static data into the execution context.
* [`search`](input-search.md): load the results of a search into the execution context.
* [`http`](input-http.md): load the results of an HTTP request into the execution context.
* [`chain`](input-chain.md): use a series of inputs to load data into the execution context.

::::{note}
If you don’t define an input for a watch, an empty payload is loaded into the execution context.
::::
