---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-services.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-services.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Services [apm-services]

The **Services** inventory provides a quick, high-level overview of the health and general performance of all instrumented services.

::::{note}
A service only appears in the **Services** inventory if it has sent transactions or spans within the selected time window. Services that send only logs are not listed. If a service is missing, verify that it is sending transaction or span data and that the selected time range includes recent activity.
::::

Active alerts for each service are prominently displayed in the service inventory table. Clicking an active alert badge brings you to the [**Alerts**](/solutions/observability/apm/create-apm-rules-alerts.md) tab where you can learn more about the active alert and take action.

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` The **Anomalies** column shows each service's highest [{{ml}}](/solutions/observability/apm/machine-learning.md) anomaly score for the selected time range, replacing the previous health status. To use this feature, {{anomaly-detect}} must be enabled.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` SLOs for each service are also shown in the service inventory table. Use the **Actions** menu on any service row to act on the service directly, or the **Environment** selector to filter the inventory by environment.

{applies_to}`stack: ga 9.0-9.4` To help surface potential issues, services are sorted by their health status: **critical** → **warning** → **healthy** → **unknown**. Health status is powered by [{{ml}}](/solutions/observability/apm/machine-learning.md) and requires {{anomaly-detect}} to be enabled.

## Service groups [service-groups]

::::{note}

For Observability Serverless projects, the **Editor** role or higher is required to create and manage service groups. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::

::::{important}

The Service grouping functionality is in beta and is subject to change. The design and code is less mature than official generally available features and is being provided as-is with no warranties.

::::

Group services together to build meaningful views that remove noise, simplify investigations across services, and combine related alerts.

:::{image} /solutions/images/observability-apm-service-group.png
:alt: Example view of service group in the Applications UI in Kibana
:screenshot:
:::

To create a service group:

1. To open **Service inventory**, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Switch to **Service groups**.
3. Click **Create group**.
4. Specify a name, color, and description.
5. Click **Select services**.
6. Specify a [{{kib}} Query Language (KQL)](/explore-analyze/query-filter/languages/kql.md) query to filter services by one or more of the following dimensions: `agent.name`, `service.name`, `service.language.name`, `service.environment`, `labels.<xyz>`. Services that match the query within the last 24 hours will be assigned to the group.

### Examples [apm-services-examples]

Not sure where to get started? Here are some sample queries you can build from:

* **Group services by environment**: To group "production" services, use `service.environment : "production"`.
* **Group services by name**: To group all services that end in "beat", use `service.name : *beat`. This will match services named "Auditbeat", "Heartbeat", "Filebeat", and so on.