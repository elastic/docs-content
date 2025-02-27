---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-transactions.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-transactions.html
---

# Transactions [apm-transactions]

A *transaction* describes an event captured by an Elastic APM agent instrumenting a service. APM agents automatically collect performance metrics on HTTP requests, database queries, and much more.


:::{image} ../../../images/observability-apm-transactions-overview.png
:alt: Example view of transactions table in the Applications UI
:class: screenshot
:::

The **Latency**, **Throughput**, **Failed transaction rate**, **Time spent by span type**, and **Cold start rate** charts display information on all transactions associated with the selected service:

**Latency**
   Response times for the service. Options include average, 95th, and 99th percentile. If there’s a weird spike that you’d like to investigate, you can simply zoom in on the graph - this will adjust the specific time range, and all of the data on the page will update accordingly.

**Throughput**
   Visualize response codes: `2xx`, `3xx`, `4xx`, etc. Useful for determining if more responses than usual are being served with a particular response code. Like in the latency graph, you can zoom in on anomalies to further investigate them.

**Failed transaction rate**
   The failed transaction rate represents the percentage of failed transactions from the perspective of the selected service. It’s useful for visualizing unexpected increases, decreases, or irregular patterns in a service’s transactions.

    ::::{tip}
    HTTP **transactions** from the HTTP server perspective do not consider a `4xx` status code (client error) as a failure because the failure was caused by the caller, not the HTTP server. Thus, `event.outcome=success` and there will be no increase in failed transaction rate.

    HTTP **spans** from the client perspective however, are considered failures if the HTTP status code is ≥ 400. These spans will set `event.outcome=failure` and increase the failed transaction rate.

    If there is no HTTP status, both transactions and spans are considered successful unless an error is reported.

    ::::


**Time spent by span type**
   Visualize where your application is spending most of its time. For example, is your app spending time in external calls, database processing, or application code execution?

    The time a transaction took to complete is also recorded and displayed on the chart under the "app" label. "app" indicates that something was happening within the application, but we’re not sure exactly what. This could be a sign that the APM agent does not have auto-instrumentation for whatever was happening during that time.

    It’s important to note that if you have asynchronous spans, the sum of all span times may exceed the duration of the transaction.


**Cold start rate**
   Only applicable to serverless transactions, this chart displays the percentage of requests that trigger a cold start of a serverless function. See [Cold starts](../../../solutions/observability/apps/observe-lambda-functions.md#apm-lambda-cold-start-info) for more information.


## Transactions table [transactions-table]

The **Transactions** table displays a list of *transaction groups* for the selected service. In other words, this view groups all transactions of the same name together, and only displays one entry for each group.

:::{image} ../../../images/observability-apm-transactions-table.png
:alt: Example view of the transactions table in the Applications UI in Kibana
:class: screenshot
:::

By default, transaction groups are sorted by *Impact*. Impact helps show the most used and slowest endpoints in your service - in other words, it’s the collective amount of pain a specific endpoint is causing your users. If there’s a particular endpoint you’re worried about, you can click on it to view the [transaction details](../../../solutions/observability/apps/transactions-2.md#transaction-details).

::::{important}
If you only see one route in the Transactions table, or if you have transactions named "unknown route", it could be a symptom that the APM agent either wasn’t installed correctly or doesn’t support your framework.

For further details, including troubleshooting and custom implementation instructions, refer to the documentation for each [APM Agent](https://www.elastic.co/guide/en/apm/agent) you’ve implemented.

::::

% Stateful only for RUM

## RUM Transaction overview [rum-transaction-overview]

The transaction overview page is customized for the JavaScript RUM agent. Specifically, the page highlights **page load times** for your service:

:::{image} ../../../images/observability-apm-geo-ui.png
:alt: average page load duration distribution
:class: screenshot
:::

Additional RUM goodies, like core vitals, and visitor breakdown by browser, location, and device, are available in the Observability User Experience tab.


## Transaction details [transaction-details]

Selecting a transaction group will bring you to the **transaction** details. This page is visually similar to the transaction overview, but it shows data from all transactions within the selected transaction group.

:::{image} ../../../images/observability-apm-transactions-overview.png
:alt: Example view of response time distribution
:class: screenshot
:::


### Latency distribution [transaction-duration-distribution]

The latency distribution shows a plot of all transaction durations for the given time period. The following screenshot shows a typical distribution and indicates most of our requests were served quickly — awesome! The requests on the right are taking longer than average; we probably need to focus on them.

:::{image} ../../../images/observability-apm-transaction-duration-dist.png
:alt: Example view of latency distribution graph
:class: screenshot
:::

Click and drag to select a latency duration *bucket* to display up to 500 trace samples.


### Trace samples [transaction-trace-sample]

Trace samples are based on the *bucket* selection in the **Latency distribution** chart; update the samples by selecting a new *bucket*. The number of requests per bucket is displayed when hovering over the graph, and the selected bucket is highlighted to stand out.

Each bucket presents up to ten trace samples in a **timeline**, trace sample **metadata**, and any related **logs**.

**Trace sample timeline**

Each sample has a trace timeline waterfall that shows how a typical request in that bucket executed. This waterfall is useful for understanding the parent/child hierarchy of transactions and spans, and ultimately determining *why* a request was slow. For large waterfalls, expand problematic transactions and collapse well-performing ones for easier problem isolation and troubleshooting.

:::{image} ../../../images/observability-apm-transaction-sample.png
:alt: Example view of transactions sample
:class: screenshot
:::

::::{note}
More information on timeline waterfalls is available in [spans](../../../solutions/observability/apps/trace-sample-timeline.md).

::::


**Trace sample metadata**

Learn more about a trace sample in the **Metadata** tab:

* Labels: Custom labels added by APM agents
* HTTP request/response information
* Host information
* Container information
* Service: The service/application runtime, APM agent, name, etc..
* Process: The process id that served up the request.
* APM agent information
* URL
* User: Requires additional configuration, but allows you to see which user experienced the current transaction.
* FaaS information, like cold start, AWS request ID, trigger type, and trigger request ID

::::{tip}
All of this data is stored in documents in Elasticsearch. This means you can select "Actions - View transaction in Discover" to see the actual Elasticsearch document under the discover tab.

::::


**Trace sample logs**

The **Logs** tab displays logs related to the sampled trace.

Logs provide detailed information about specific events, and are crucial to successfully debugging slow or erroneous transactions.

If you’ve correlated your application’s logs and traces, you never have to search for relevant data; it’s already available to you. Viewing log and trace data together allows you to quickly diagnose and solve problems.

To learn how to correlate your logs with your instrumented services, see [Stream application logs](../../../solutions/observability/logs/stream-application-logs.md)

:::{image} ../../../images/observability-apm-logs-tab.png
:alt: APM logs tab
:class: screenshot
:::


### Correlations [transaction-latency-correlations]

Correlations surface attributes of your data that are potentially correlated with high-latency or erroneous transactions. To learn more, see [Find transaction latency and failure correlations](../../../solutions/observability/apps/find-transaction-latency-failure-correlations.md).

:::{image} ../../../images/observability-correlations-hover.png
:alt: APM lattency correlations
:class: screenshot
:::