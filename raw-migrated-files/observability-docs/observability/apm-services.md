# Services [apm-services]

**Service** inventory provides a quick, high-level overview of the health and general performance of all instrumented services.

To help surface potential issues, services are sorted by their health status: **critical** > **warning*** > ***healthy** > **unknown**. Health status is powered by [machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md) and requires anomaly detection to be enabled.

In addition to health status, active alerts for each service are prominently displayed in the service inventory table. Selecting an active alert badge brings you to the [Alerts](../../../solutions/observability/apps/create-apm-rules-alerts.md) tab where you can learn more about the active alert and take action.

:::{image} ../../../images/observability-apm-services-overview.png
:alt: Example view of services table the Applications UI in Kibana
:class: screenshot
:::

::::{tip}
Want to monitor service logs without instrumenting all your services? Learn about our [Inventory](../../../solutions/observability/apps/inventory.md).
::::



## Service groups [service-groups]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


Group services together to build meaningful views that remove noise, simplify investigations across services, and [combine related alerts](../../../solutions/observability/apps/create-apm-rules-alerts.md#apm-alert-view-group). Service groups are {{kib}} space-specific and available for any users with appropriate access.

:::{image} ../../../images/observability-apm-service-group.png
:alt: Example view of service group in the Applications UI in Kibana
:class: screenshot
:::

To create a service group:

1. To open **Service inventory**, find **Applications** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Switch to **Service groups**.
3. Click **Create group**.
4. Specify a name, color, and description.
5. Click **Select services**.
6. Specify a [{{kib}} Query Language (KQL)](../../../explore-analyze/query-filter/languages/kql.md) query to filter services by one or more of the following dimensions: `agent.name`, `service.name`, `service.language.name`, `service.environment`, `labels.<xyz>`. Services that match the query within the last 24 hours will be assigned to the group.

**Examples**

Not sure where to get started? Here are some sample queries you can build from:

* Group services by environment—​in this example, "production": `service.environment : "production"`
* Group services by name—​this example groups those that end in "beat": `service.name : *beat` (matches services named "Auditbeat", "Heartbeat", "Filebeat", etc.)
