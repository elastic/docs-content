# Traces [observability-apm-traces]

::::{tip}
Traces link together related transactions to show an end-to-end performance of how a request was served and which services were part of it. In addition to the Traces overview, you can view your application traces in the [trace sample timeline waterfall](../../../solutions/observability/apps/trace-sample-timeline.md).

::::


**Traces** displays your application’s entry (root) transactions. Transactions with the same name are grouped together and only shown once in this table. If you’re using [distributed tracing](../../../solutions/observability/apps/trace-sample-timeline.md#observability-apm-trace-sample-timeline-distributed-tracing), this view is key to finding the critical paths within your application.

By default, transactions are sorted by *Impact*. Impact helps show the most used and slowest endpoints in your service — in other words, it’s the collective amount of pain a specific endpoint is causing your users. If there’s a particular endpoint you’re worried about, select it to view its [transaction details](../../../solutions/observability/apps/transactions-2.md#transaction-details).

You can also use queries to filter and search the transactions shown on this page. Note that only properties available on root transactions are searchable. For example, you can’t search for `label.tier: 'high'`, as that field is only available on non-root transactions.

:::{image} ../../../images/serverless-apm-traces.png
:alt: Example view of the Traces overview in the Applications UI
:class: screenshot
:::


## Trace explorer [observability-apm-traces-trace-explorer]

**Trace explorer** is an experimental top-level search tool that allows you to query your traces using [Kibana Query Language (KQL)](../../../explore-analyze/query-filter/languages/kql.md) or [Event Query Language (EQL)](../../../explore-analyze/query-filter/languages/eql.md).

Curate your own custom queries, or use the [Service map](../../../solutions/observability/apps/service-map.md) to find and select edges to automatically generate queries based on your selection:

:::{image} ../../../images/serverless-trace-explorer.png
:alt: Trace explorer
:class: screenshot
:::
