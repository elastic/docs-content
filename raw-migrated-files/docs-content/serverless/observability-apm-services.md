# Services [observability-apm-services]

The **Services** inventory provides a quick, high-level overview of the health and general performance of all instrumented services.

To help surface potential issues, services are sorted by their health status: **critical** → **warning*** → ***healthy** → **unknown**. Health status is powered by [machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md) and requires anomaly detection to be enabled.

In addition to health status, active alerts for each service are prominently displayed in the service inventory table. Selecting an active alert badge brings you to the **Alerts** tab where you can learn more about the active alert and take action.

:::{image} ../../../images/serverless-apm-services-overview.png
:alt: Example view of services table the Applications UI
:class: screenshot
:::


## Service groups [observability-apm-services-service-groups]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to create and manage service groups. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


::::{admonition} Service grouping is in beta
:class: important

The Service grouping functionality is in beta and is subject to change. The design and code is less mature than official generally available features and is being provided as-is with no warranties.

::::


Group services together to build meaningful views that remove noise, simplify investigations across services, and combine related alerts.

:::{image} ../../../images/serverless-apm-service-group.png
:alt: Example view of service group in the Applications UI
:class: screenshot
:::

To create a service group:

1. In your {{obs-serverless}} project, go to **Applications** → **Service Inventory**.
2. Switch to **Service groups**.
3. Click **Create group**.
4. Specify a name, color, and description.
5. Click **Select services**.
6. Specify a [Kibana Query Language (KQL)](../../../explore-analyze/query-filter/languages/kql.md) query to filter services by one or more of the following dimensions: `agent.name`, `service.name`, `service.language.name`, `service.environment`, `labels.<xyz>`. Services that match the query within the last 24 hours will be assigned to the group.


### Examples [observability-apm-services-examples]

Not sure where to get started? Here are some sample queries you can build from:

* **Group services by environment**: To group "production" services, use `service.environment : "production"`.
* **Group services by name**: To group all services that end in "beat", use `service.name : *beat`. This will match services named "Auditbeat", "Heartbeat", "Filebeat", and so on.
