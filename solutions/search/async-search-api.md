---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/async-search-intro.html
navigation_title: The `async-search` API
applies:
  stack:
  serverless:
---

# Long running searches with the Async Search API [async-search-intro]

{{es}} generally allows you to quickly search across big amounts of data. There are situations where a search executes on many shards, possibly against large data sets or multiple [remote clusters](../../deploy-manage/remote-clusters.md), for which results are not expected to be returned in milliseconds. When you need to execute long-running searches, synchronously waiting for its results to be returned is not ideal. Instead, Async search lets you submit a search request that gets executed *asynchronously*, monitor the progress of the request, and retrieve results at a later stage. You can also retrieve partial results as they become available but before the search has completed.

You can submit an async search request using the [submit async search](https://www.elastic.co/guide/en/elasticsearch/reference/current/async-search.html#submit-async-search) API. The [get async search](https://www.elastic.co/guide/en/elasticsearch/reference/current/async-search.html#get-async-search) API allows you to monitor the progress of an async search request and retrieve its results. An ongoing async search can be deleted through the [delete async search](https://www.elastic.co/guide/en/elasticsearch/reference/current/async-search.html#delete-async-search) API.

