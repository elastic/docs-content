---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/configure-settings.html
  - https://www.elastic.co/guide/en/serverless/current/observability-configure-intra-settings.html
---

# Configure settings [observability-configure-intra-settings]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to configure settings. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


From the main menu, go to **Infrastructure** → **Infrastructure inventory*** or ***Hosts**, and click the **Settings** link at the top of the page. The following settings are available:

| Setting | Description |
| --- | --- |
| **Name** | Name of the source configuration. |
| **Indices** | {{ipm-cap}} or patterns used to match {{es}} indices that contain metrics. The default patterns are `metrics-*,metricbeat-*`. |
| **Machine Learning** | The minimum severity score required to display anomalies in the Infrastructure UI. The default is 50. |
| **Features** | Turn new features on and off. |

Click **Apply** to save your changes.

::::{note}
The patterns used to match log sources are configured in the Logs app. The default setting is `logs-*,filebeat-*,kibana_sample_data_logs*`. To change the default, refer to [Configure data sources](../../../solutions/observability/logs/configure-data-sources.md).
::::


If the fields are grayed out and cannot be edited, you may not have sufficient privileges to change the source configuration.

% Stateful only for spaces.

::::{tip}
If [Spaces](../../../deploy-manage/manage-spaces.md) are enabled in your {{kib}} instance, any configuration changes you make here are specific to the current space. You can make different subsets of data available by creating multiple spaces with different data source configurations.

::::