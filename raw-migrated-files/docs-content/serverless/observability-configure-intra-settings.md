# Configure settings [observability-configure-intra-settings]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to configure settings. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


From the main {{obs-serverless}} menu, go to **Infrastructure** → **Infrastructure inventory*** or ***Hosts**, and click the **Settings** link at the top of the page. The following settings are available:

| Setting | Description |
| --- | --- |
| **Name** | Name of the source configuration. |
| **Indices** | {{ipm-cap}} or patterns used to match {{es}} indices that contain metrics. The default patterns are `metrics-*,metricbeat-*`. |
| **Machine Learning** | The minimum severity score required to display anomalies in the Infrastructure UI. The default is 50. |
| **Features** | Turn new features on and off. |

Click **Apply** to save your changes.

If the fields are grayed out and cannot be edited, you may not have sufficient privileges to change the source configuration.
