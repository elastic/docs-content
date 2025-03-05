---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-services.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-services.html
applies_to:
  stack: all
  serverless: all
---

# Services [apm-services]

The **Services** inventory provides a quick, high-level overview of the health and general performance of all instrumented services.

To help surface potential issues, services are sorted by their health status: **critical** → **warning** → **healthy** → **unknown**. Health status is powered by [machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md) and requires anomaly detection to be enabled.

In addition to health status, active alerts for each service are prominently displayed in the service inventory table. Selecting an active alert badge brings you to the [**Alerts**](../../../solutions/observability/apps/create-apm-rules-alerts.md) tab where you can learn more about the active alert and take action.

:::{image} ../../../images/observability-apm-services-overview.png
:alt: Example view of services table the Applications UI in Kibana
:class: screenshot
:::

% Stateful only for the following tip?

::::{tip}
Want to monitor service logs without instrumenting all your services? Learn about our [Inventory](../../../solutions/observability/apps/inventory.md).
::::


## Service groups [service-groups]

::::{note}

For Observability Serverless projects, the **Editor** role or higher is required to create and manage service groups. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


::::{important}

The Service grouping functionality is in beta and is subject to change. The design and code is less mature than official generally available features and is being provided as-is with no warranties.

::::


Group services together to build meaningful views that remove noise, simplify investigations across services, and combine related alerts.

:::{image} ../../../images/observability-apm-service-group.png
:alt: Example view of service group in the Applications UI in Kibana
:class: screenshot
:::

To create a service group:

1. To open **Service inventory**, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Switch to **Service groups**.
3. Click **Create group**.
4. Specify a name, color, and description.
5. Click **Select services**.
6. Specify a [{{kib}} Query Language (KQL)](../../../explore-analyze/query-filter/languages/kql.md) query to filter services by one or more of the following dimensions: `agent.name`, `service.name`, `service.language.name`, `service.environment`, `labels.<xyz>`. Services that match the query within the last 24 hours will be assigned to the group.

### Examples [apm-services-examples]

Not sure where to get started? Here are some sample queries you can build from:

* **Group services by environment**: To group "production" services, use `service.environment : "production"`.
* **Group services by name**: To group all services that end in "beat", use `service.name : *beat`. This will match services named "Auditbeat", "Heartbeat", "Filebeat", and so on.