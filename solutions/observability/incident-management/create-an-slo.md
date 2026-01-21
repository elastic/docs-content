---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/slo-create.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-an-slo.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---


# Create an SLO [observability-create-an-slo]

::::{important}

**For Observability serverless projects**, The **Editor** role or higher is required to create SLOs. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

**For Elastic Stack**, to create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) present, and [SLO access](/solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.

::::


To create an SLO, find **SLOs** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md):

* If you’re creating your first SLO, you’ll see an introductory page. Click the **Create SLO** button.
* If you’ve created SLOs before, click the **Create new SLO** button in the upper-right corner of the page.

From here, complete the following steps:

1. [Define your service-level indicator (SLI)](/solutions/observability/incident-management/create-an-slo.md#define-sli).
2. [Set your objectives](/solutions/observability/incident-management/create-an-slo.md#set-slo).
3. [Describe your SLO](/solutions/observability/incident-management/create-an-slo.md#slo-describe).

::::{note}
**For Elastic Stack**, the cluster must include one or more nodes with both `ingest` and `transform` [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles). The roles can exist on the same node or be distributed across separate nodes. On {{ech}} deployments, this is handled by the hot nodes, which serve as both `ingest` and `transform` nodes.

::::

## Define your SLI [define-sli]

The type of SLI to use depends on the location of your data:

* [Custom KQL](/solutions/observability/incident-management/create-an-slo.md#custom-kql): Create an SLI based on raw logs coming from your services.
* [Timeslice metric](/solutions/observability/incident-management/create-an-slo.md#timeslice-metric): Create an SLI based on a custom equation that uses multiple aggregations.
* [Custom metric](/solutions/observability/incident-management/create-an-slo.md#custom-metric): Create an SLI to define custom equations from metric fields in your indices.
* [Histogram metric](/solutions/observability/incident-management/create-an-slo.md#histogram-metric): Create an SLI based on histogram metrics.
* [APM latency and APM availability](/solutions/observability/incident-management/create-an-slo.md#apm-latency-and-availability): Create an SLI based on services using application performance monitoring (APM).


### Custom KQL [custom-kql]

Create an indicator based on any of your {{es}} indices or data views. You define two queries: one that yields the good events from your index, and one that yields the total events from your index.

**Example:** You can define a custom KQL indicator based on the `service-logs` index with the **good query** defined as `nested.field.response.latency <= 100 and nested.field.env : “production”` and the **total query** defined as `nested.field.env : “production”`.

When defining a custom KQL SLI, set the following fields:

* **Index:** The data view or index pattern you want to base the SLI on. For example, `service-logs`.
* **Timestamp field:** The timestamp field used by the index.
* **Query filter:** A KQL filter to specify relevant criteria by which to filter the index documents.
* **Good query:** The query yielding events that are considered good or successful. For example, `nested.field.response.latency <= 100 and nested.field.env : “production”`.
* **Total query:** The query yielding all events to take into account for computing the SLI. For example, `nested.field.env : “production”`.
* **Group by:** The field used to group the data based on the values of the specific field. For example, you could group by the `url.domain` field, which would create individual SLOs for each value of the selected field.


### Custom metric [custom-metric]

Create an indicator to define custom equations from metric fields in your indices.

**Example:** You can define **Good events** as the sum of the field `processor.processed` with a filter of `"processor.outcome: \"success\""`, and the **Total events** as the sum of `processor.processed` with a filter of `"processor.outcome: *"`.

When defining a custom metric SLI, set the following fields:

* **Source**

    * **Index:** The data view or index pattern you want to base the SLI on. For example, `my-service-*`.
    * **Timestamp field:** The timestamp field used by the index.
    * **Query filter:** A KQL filter to specify relevant criteria by which to filter the index documents. For example, `'field.environment : "production" and service.name : "my-service"'`.

* **Good events**

    * **Metric [A-Z]:** The field that is aggregated using the `sum` aggregation for good events. For example, `processor.processed`.
    * **Filter [A-Z]:** The filter to apply to the metric for good events. For example, `"processor.outcome: \"success\""`.
    * **Equation:** The equation that calculates the good metric. For example, `A`.

* **Total events**

    * **Metric [A-Z]:** The field that is aggregated using the `sum` aggregation for total events. For example, `processor.processed`.
    * **Filter [A-Z]:** The filter to apply to the metric for total events. For example, `"processor.outcome: *"`.
    * **Equation:** The equation that calculates the total metric. For example, `A`.

* **Group by:** The field used to group the data based on the values of the specific field. For example, you could group by the `url.domain` field, which would create individual SLOs for each value of the selected field.


### Timeslice metric [timeslice-metric]

Create an indicator based on a custom equation that uses statistical aggregations and a threshold to determine whether a slice is good or bad. Supported aggregations include `Average`, `Max`, `Min`, `Sum`, `Cardinality`, `Last value`, `Std. deviation`, `Doc count`, and `Percentile`. The equation supports basic math and logic.

::::{note}
This indicator requires you to use the `Timeslices` budgeting method.

::::


**Example:** You can define an indicator to determine whether a Kubernetes StatefulSet is healthy. First you set the query filter to `orchestrator.cluster.name: "elastic-k8s" AND kubernetes.namespace: "my-ns" AND data_stream.dataset: "kubernetes.state_statefulset"`. Then you define an equation that compares the number of ready (healthy) replicas to the number of observed replicas: `A == B ? 1 : 0`, where `A` retrieves the last value of `kubernetes.statefulset.replicas.ready` and `B` retrieves the last value of `kubernetes.statefulset.replicas.observed`. The equation returns `1` if the condition `A == B` is true (indicating the same number of replicas) or `0` if it’s false. If the value is less than 1, you can determine that the Kubernetes StatefulSet is unhealthy.

When defining a timeslice metric SLI, set the following fields:

* **Source**

    * **Index:** The data view or index pattern you want to base the SLI on. For example, `metrics-*:metrics-*`.
    * **Timestamp field:** The timestamp field used by the index.
    * **Query filter:** A KQL filter to specify relevant criteria by which to filter the index documents. For example, `orchestrator.cluster.name: "elastic-k8s" AND kubernetes.namespace: "my-ns" AND data_stream.dataset: "kubernetes.state_statefulset"`.

* **Metric definition**

    * **Aggregation [A-Z]:** The type of aggregation to use.
    * **Field [A-Z]:** The field to use in the aggregation. For example, `kubernetes.statefulset.replicas.ready`.
    * **Filter [A-Z]:** The filter to apply to the metric.
    * **Equation:** The equation that calculates the total metric. For example, `A == B ? 1 : 0`.
    * **Comparator:** The type of comparison to perform.
    * **Threshold:** The value to use along with the comparator to determine if the slice is good or bad.



### Histogram metric [histogram-metric]

Histograms record data in a compressed format and can record latency and delay metrics. You can create an SLI based on histogram metrics using a `range` aggregation or a `value_count` aggregation for both the good and total events. Filtering with KQL queries is supported on both event types.

When using a `range` aggregation, both the `from` and `to` thresholds are required for the range and the events are the total number of events within that range. The range includes the `from` value and excludes the `to` value.

**Example:** You can define your **Good events** using the `processor.latency` field with a filter of `"processor.outcome: \"success\""`, and your **Total events** using the `processor.latency` field with a filter of `"processor.outcome: *"`.

When defining a histogram metric SLI, set the following fields:

* **Source**

    * **Index:** The data view or index pattern you want to base the SLI on. For example, `my-service-*`.
    * **Timestamp field:** The timestamp field used by the index.
    * **Query filter:** A KQL filter to specify relevant criteria by which to filter the index documents. For example, `field.environment : "production" and service.name : "my-service"`.

* **Good events**

    * **Aggregation:** The type of aggregation to use for good events, either **Value count** or **Range**.
    * **Field:** The field used to aggregate events considered good or successful. For example, `processor.latency`.
    * **From:** (`range` aggregation only) The starting value of the range for good events. For example, `0`.
    * **To:** (`range` aggregation only) The ending value of the range for good events. For example, `100`.
    * **KQL filter:** The filter for good events. For example, `"processor.outcome: \"success\""`.

* **Total events**

    * **Aggregation:** The type of aggregation to use for total events, either **Value count** or **Range**.
    * **Field:** The field used to aggregate total events. For example, `processor.latency`.
    * **From:** (`range` aggregation only) The starting value of the range for total events. For example, `0`.
    * **To:** (`range` aggregation only) The ending value of the range for total events. For example, `100`.
    * **KQL filter:** The filter for total events. For example, `"processor.outcome : *"`.

* **Group by:** The field used to group the data based on the values of the specific field. For example, you could group by the `url.domain` field, which would create individual SLOs for each value of the selected field.


### APM latency and APM availability [apm-latency-and-availability]

There are two types of SLI you can create based on services using application performance monitoring (APM): APM latency and APM availability.

Use **APM latency** to create an indicator based on latency data received from your instrumented services and a latency threshold.

**Example:** You can define an indicator on an APM service named `banking-service` for the `production` environment, and the transaction name `POST /deposit` with a latency threshold value of 300ms.

Use **APM availability** to create an indicator based on the availability of your instrumented services. Availability is determined by calculating the percentage of successful transactions (`event.outcome : "success"`) out of the total number of successful and failed transactions—unknown outcomes are excluded.

**Example:** You can define an indicator on an APM service named `search-service` for the `production` environment, and the transaction name `POST /search`.

When defining either an APM latency or APM availability SLI, set the following fields:

* **Service name:** The APM service name.
* **Service environment:** Either `all` or the specific environment.
* **Transaction type:** Either `all` or the specific transaction type.
* **Transaction name:** Either `all` or the specific transaction name.
* **Threshold (APM latency only):** The latency threshold in milliseconds (ms) to consider the request as good.
* **Query filter:** An optional query filter on the APM data.


### Synthetics availability [synthetics-availability-sli]

Create an indicator based on the availability of your synthetic monitors. Availability is determined by calculating the percentage of checks that are successful (`monitor.status : "up"`) out of the total number of checks.

**Example**: You can define an indicator based on a HTTP monitor being "up" for at least 99% of the time.

When defining a Synthetics availability SLI, set the following fields:

* **Monitor name** — The name of one or more [synthetic monitors](/solutions/observability/synthetics/configure-projects.md).
* **Project** — The ID of one or more [projects](/solutions/observability/synthetics/configure-projects.md#synthetics-configuration-project) containing synthetic monitors.
* **Tags** — One or more [tags](/solutions/observability/synthetics/configure-projects.md) assigned to synthetic monitors.
* **Query filter** — An optional KQL query used to filter the Synthetics checks on some relevant criteria.

::::{note}
Synthetics availability SLIs are automatically grouped by monitor and location.

::::



## Set your objectives [set-slo]

After defining your SLI, you need to set your objectives. To set your objectives, complete the following:

1. [Select your budgeting method](/solutions/observability/incident-management/create-an-slo.md#slo-budgeting-method)
2. [Set your time window](/solutions/observability/incident-management/create-an-slo.md#slo-time-window)
3. [Set your target/SLO percentage](/solutions/observability/incident-management/create-an-slo.md#slo-target)


### Set your time window and duration [slo-time-window]

Select the durations over which you want to compute your SLO. You can select either a **rolling** or **calendar aligned** time window:

|  |  |
| --- | --- |
| **Rolling** | Uses data from a specified duration that depends on when the SLO was created, for example the last 30 days. |
| **Calendar aligned** | Uses data from a specified duration that aligns with calendar, for example weekly or monthly. |


### Select your budgeting method [slo-budgeting-method]

You can select either an **occurrences** or a **timeslices** budgeting method:

|  |  |
| --- | --- |
| **Occurrences** | Uses the number of good events and the number of total events to compute the SLI. |
| **Timeslices** | Breaks the overall time window into smaller slices of a defined duration, and uses the number of good slices over the number of total slices to compute the SLI. |


### Set your target/SLO (%) [slo-target]

The SLO target objective as a percentage.


## Describe your SLO [slo-describe]

After setting your objectives, give your SLO a name, a short description, and add any relevant tags.


## SLO burn rate alert rule [slo-alert-checkbox]

When you use the UI to create an SLO, a default SLO burn rate alert rule is created automatically. The burn rate rule will use the default configuration and no connector. You must configure a connector if you want to receive alerts for SLO breaches.

For more information about configuring the rule, see [Create an SLO burn rate rule](/solutions/observability/incident-management/create-an-slo-burn-rate-rule.md).

## Add an SLO Overview panel to a custom dashboard [slo-dashboard]

After you’ve created your SLO, you can monitor it from the *SLOs* page in Observability, but you can also add an *SLO Overview* panel to a custom dashboard. Read more about dashboards in [Dashboard and visualizations](/explore-analyze/dashboards.md).

:::{image} /solutions/images/observability-slo-overview-embeddable-widget.png
:alt: Using the Add panel button to add an SLO Overview widget to a dashboard
:screenshot:
:::