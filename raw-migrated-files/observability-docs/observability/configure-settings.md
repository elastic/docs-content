# Configure settings [configure-settings]

To configure settings for the {{infrastructure-app}}, go to any page under **Infrastructure** and click the **Settings** link at the top of the page.

The following settings are available:

| Setting | Description |
| --- | --- |
| **Name** | Name of the source configuration. |
| **Indices** | {{ipm-cap}} or patterns used to match {{es}} indices that contain metrics. The default patterns are `metrics-*,metricbeat-*`. |
| **{{ml-cap}}** | The minimum severity score required to display anomalies in the {{infrastructure-app}}. The default is 50. |

Click **Apply** to save your changes.

::::{note}
The patterns used to match log sources are configured in the Logs app. The default setting is `logs-*,filebeat-*,kibana_sample_data_logs*`. To change the default, refer to [Configure data sources](../../../solutions/observability/logs/configure-data-sources.md).
::::


If the fields are grayed out and cannot be edited, you may not have sufficient privileges to change the source configuration. For more information see [Granting access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).

::::{tip}
If [Spaces](../../../deploy-manage/manage-spaces.md) are enabled in your {{kib}} instance, any configuration changes you make here are specific to the current space. You can make different subsets of data available by creating multiple spaces with different data source configurations.

::::



## Related settings [_related_settings]

You can configure additional metrics settings in the {{kib}} configuration. For more information, refer to [configuration settings](https://www.elastic.co/guide/en/kibana/current/infrastructure-ui-settings-kb.html) in the {{kib}} documentation.
