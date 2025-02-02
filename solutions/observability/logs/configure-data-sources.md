---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/configure-data-sources.html
---

# Configure data sources [configure-data-sources]

::::{admonition} There’s a new, better way to explore your logs!
These settings only apply to the Logs Stream app. The Logs Stream app and dashboard panel are deactivated by default. We recommend viewing and inspecting your logs with [Logs Explorer](logs-explorer.md) as it provides more features, better performance, and more intuitive navigation.

To activate the Logs Stream app, refer to [Activate Logs Stream](logs-stream.md#activate-logs-stream).

::::


Specify the source configuration for logs in the [Logs settings](https://www.elastic.co/guide/en/kibana/current/logs-ui-settings-kb.html) in the [{{kib}} configuration file](../../../deploy-manage/deploy/self-managed/configure.md). By default, the configuration uses the index patterns stored in the {{kib}} log sources advanced setting to query the data. The configuration also defines the default columns displayed in the logs stream.

If your logs have custom index patterns, use non-default field settings, or contain parsed fields that you want to expose as individual columns, you can override the default configuration settings.


## Edit configuration settings [edit-config-settings]

1. Find `Logs / Settings` in the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).

    |     |     |
    | --- | --- |
    | **Name** | Name of the source configuration. |
    | **{{kib}} log sources advanced setting** | Use index patterns stored in the {{kib}} **log sources** advanced setting, which provides a centralized place to store and query log index patterns.To open **Advanced settings**, find **Stack Management** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search). |
    | **{{data-source-cap}} (deprecated)** | The Logs UI integrates with {{data-sources}} toconfigure the used indices by clicking **Use {{data-sources}}**. |
    | **Log indices (deprecated)** | {{kib}} index patterns or index name patterns in the {{es}} indicesto read log data from. |
    | **Log columns** | Columns that are displayed in the logs **Stream** page. |

2. When you have completed your changes, click **Apply**.


## Customize Stream page [customize-stream-page]

::::{tip}
If [Spaces](../../../deploy-manage/manage-spaces.md) are enabled in your {{kib}} instance, any configuration changes you make here are specific to the current space. You can make different subsets of data available by creating multiple spaces with other data source configurations.

::::


By default, the **Stream** page within the {{logs-app}} displays the following columns.

|     |     |
| --- | --- |
| **Timestamp** | The timestamp of the log entry from the `timestamp` field. |
| **Message** | The message extracted from the document.The content of this field depends on the type of log message.If no special log message type is detected, the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-base.html)base field, `message`, is used. |

1. To add a new column to the logs stream, select **Settings > Add column**.
2. In the list of available fields, select the field you want to add. To filter the field list by that name, you can start typing a field name in the search box.
3. To remove an existing column, click the **Remove this column** icon.
4. When you have completed your changes, click **Apply**.

If the fields are grayed out and cannot be edited, you may not have sufficient privileges to modify the source configuration. For more information, see [Granting access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).
