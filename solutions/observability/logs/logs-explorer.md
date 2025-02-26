---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/explore-logs.html
  - https://www.elastic.co/guide/en/serverless/current/observability-discover-and-explore-logs.html
---

# Logs Explorer [explore-logs]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


With **Logs Explorer**, you can quickly search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. You can also customize and save your searches and place them on a dashboard. Instead of having to log into different servers, change directories, and view individual files, all your logs are available in a single view.

To open **Logs Explorer**, find `Logs Explorer` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} ../../../images/observability-log-explorer.png
:alt: Screen capture of the Logs Explorer
:class: screenshot
:::


## Required {{kib}} privileges [logs-explorer-privileges]

Viewing data in Logs Explorer requires `read` privileges for **Discover**, **Index**, **Logs**, and **Integrations**. For more on assigning {{kib}} privileges, refer to the [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) docs.


## Find your logs [find-your-logs]

By default, Logs Explorer shows all of your logs, according to the index patterns set in the **logs sources** advanced setting. To open **Advanced settings**, find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

If you need to focus on logs from a specific integration, select the integration from the logs menu:

:::{image} ../../../images/observability-log-menu.png
:alt: Screen capture of log menu
:class: screenshot
:::

Once you have the logs you want to focus on displayed, you can drill down further to find the information you need. For more on filtering your data in Logs Explorer, refer to [Filter logs in Logs Explorer](../../../solutions/observability/logs/filter-aggregate-logs.md#logs-filter-logs-explorer).


## Review log data in the documents table [review-log-data-in-the-documents-table]

The documents table in Logs Explorer functions similarly to the table in Discover. You can add fields, order table columns, sort fields, and update the row height in the same way you would in Discover.

Refer to the [Discover](../../../explore-analyze/discover.md) documentation for more information on updating the table.


### Actions column [actions-column]

The actions column provides access to additional information about your logs.

**Expand:** ![The icon to expand log details](../../../images/observability-expand-icon.png "") Open the log details to get an in-depth look at an individual log file.

**Degraded document indicator:** ![The icon that shows ignored fields](../../../images/observability-pagesSelect-icon.png "") Shows if any of the document’s fields were ignored when it was indexed. Ignored fields could indicate malformed fields or other issues with your document. Use this information to investigate and determine why fields are being ignored.

**Stacktrace indicator:** ![The icon that shows if a document contains stack traces](../../../images/observability-apmTrace-icon.png "") Shows if the document contains stack traces. This indicator makes it easier to navigate through your documents and know if they contain additional information in the form of stack traces.


## View log details [view-log-details]

Click the expand icon ![icon to open log details](../../../images/observability-expand-icon.png "") to get an in-depth look at an individual log file.

These details provide immediate feedback and context for what’s happening and where it’s happening for each log. From here, you can quickly debug errors and investigate the services where errors have occurred.

The following actions help you filter and focus on specific fields in the log details:

* **Filter for value (![filter for value icon](../../../images/observability-plusInCircle.png "")):** Show logs that contain the specific field value.
* **Filter out value (![filter out value icon](../../../images/observability-minusInCircle.png "")):** Show logs that do **not** contain the specific field value.
* **Filter for field present (![filter for present icon](../../../images/observability-filter.png "")):** Show logs that contain the specific field.
* **Toggle column in table (![toggle column in table icon](../../../images/observability-listAdd.png "")):** Add or remove a column for the field to the main Logs Explorer table.


## View log data set details [view-log-data-set-details]

Go to **Data Set Quality** to view more details about your data sets and monitor their overall quality. To open **Data Set Quality**, find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Refer to [*Data set quality*](../../../solutions/observability/data-set-quality-monitoring.md) for more information.