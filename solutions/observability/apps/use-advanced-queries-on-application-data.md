---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-advanced-queries.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-query-your-data.html

navigation_title: "Advanced queries"
---

# Use advanced queries on your application data [apm-advanced-queries]


Querying your APM data is an essential tool that can make finding bottlenecks in your code even more straightforward.

Using the query bar, a powerful data query feature, you can pass advanced queries on your data to filter on specific pieces of information you’re interested in. APM queries entered into the query bar are added as parameters to the URL, so it’s easy to share a specific query or view with others.

The query bar comes with a handy autocomplete that helps find the fields and even provides suggestions to the data they include. You can select the query bar and hit the down arrow on your keyboard to begin scanning recommendations.

When you type, you can begin to see some of the transaction fields available for filtering:

:::{image} ../../../images/observability-apm-query-bar.png
:alt: Example of the Kibana Query bar in Applications UI in Kibana
:class: screenshot
:::

::::{tip}
To learn more about the {{kib}} query language capabilities, see the [Kibana Query Language Enhancements](../../../explore-analyze/query-filter/languages/kql.md) documentation.

::::


### APM queries [apm-app-queries]

APM queries can be handy for removing noise from your data in the [Services](../../../solutions/observability/apps/services.md), [Transactions](../../../solutions/observability/apps/transactions-2.md), [Errors](../../../solutions/observability/apps/errors-2.md), [Metrics](../../../solutions/observability/apps/metrics-2.md), and [Traces](../../../solutions/observability/apps/traces-2.md) views.

For example, in the **Services** view, you can quickly view a list of all the instrumented services running on your production environment: `service.environment : production`. Or filter the list by including the APM agent’s name and the host it’s running on: `service.environment : "production" and agent.name : "java" and host.name : "prod-server1"`.

On the **Traces** view, you might want to view failed transaction results from any of your running containers: `transaction.result :"FAILURE" and container.id : *`.

On the **Transactions** view, you may want to list only the slower transactions than a specified time threshold: `transaction.duration.us > 2000000`. Or filter the list by including the service version and the Kubernetes pod it’s running on: `transaction.duration.us > 2000000 and service.version : "7.12.0" and kubernetes.pod.name : "pod-5468b47f57-pqk2m"`.


## Querying in Discover [discover-advanced-queries]

Alternatively, you can query your APM documents in [**Discover**](../../../explore-analyze/discover.md). Querying documents in **Discover** works the same way as queries in the Applications UI, and **Discover** supports all of the example APM queries shown on this page.


### Discover queries [discover-queries]

One example where you may want to make use of **Discover** is to view  *all* transactions for an endpoint instead of just a sample.

Use the Applications UI to find a transaction name and time bucket that you’re interested in learning more about. Then, switch to **Discover** and make a search:

```shell
processor.event: "transaction" AND transaction.name: "<TRANSACTION_NAME_HERE>" and transaction.duration.us > 13000 and transaction.duration.us < 14000`
```

In this example, we’re interested in viewing all of the `APIRestController#customers` transactions that took between 13 and 14 milliseconds. Here’s what Discover returns:

:::{image} ../../../images/observability-advanced-discover.png
:alt: View all transactions in bucket
:class: screenshot
:::

You can now explore the data until you find a specific transaction that you’re interested in. Copy that transaction’s `transaction.id` and paste it into APM to view the data in the context of the APM:

:::{image} ../../../images/observability-specific-transaction-search.png
:alt: View specific transaction in Applications UI
:class: screenshot
:::

:::{image} ../../../images/observability-specific-transaction.png
:alt: View specific transaction in Applications UI
:class: screenshot
:::