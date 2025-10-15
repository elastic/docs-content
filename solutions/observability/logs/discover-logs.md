---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/explore-logs.html
  - https://www.elastic.co/guide/en/serverless/current/observability-discover-and-explore-logs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Explore logs in Discover [explore-logs]

From the `logs-*` or `All logs` data view in Discover, you can quickly search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. You can also customize and save your searches and place them on a dashboard. Instead of having to log into different servers, change directories, and view individual files, all your logs are available in a single view.

To open **Discover**, find `Discover` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select the `logs-*` or `All logs` data view from the **Data view** menu.

:::{note}
For a contextual logs experience, set the **Solution view** for your space to **Observability**. Refer to [Managing spaces](/deploy-manage/manage-spaces.md) for more information.
:::

:::{image} ../../images/observability-log-explorer.png
:alt: Screen capture of Discover
:screenshot:
:::

## Required {{kib}} privileges [logs-explorer-privileges]

Viewing data in Discover logs data views requires `read` privileges for **Discover**, **Index**, and **Logs**. For more on assigning {{kib}} privileges, refer to the [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) docs.


## Find your logs [find-your-logs]

By default, the **All logs** data view shows all of your logs, according to the index patterns set in the **logs sources** advanced setting. To open **Advanced settings**, find it in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

To focus on logs from a specific source or sources, create a data view using the index patterns of those source. For more information on creating data views, refer to [Create a data view](/explore-analyze/find-and-organize/data-views.md#settings-create-pattern)

Once you have the logs you want to focus on displayed, you can drill down further to find the information you need. For more on filtering your data in Discover, refer to [Filter logs in Discover](/solutions/observability/logs/filter-aggregate-logs.md#logs-filter-discover).


## Review log data in the documents table [review-log-data-in-the-documents-table]

The documents table lets you add fields, order table columns, sort fields, and update the row height in the same way you would in Discover.

Refer to the [Discover](/explore-analyze/discover.md) documentation for more information on updating the table.


### Actions column [actions-column]

The actions column provides additional information about your logs.

**Expand:** ![The icon to expand log details](/solutions/images/observability-expand-icon.png "") Open the log details to get an in-depth look at an individual log file.

**Degraded document indicator:** ![The icon that shows ignored fields](../../images/observability-pagesSelect-icon.png "") This indicator shows if any of the document’s fields were ignored when it was indexed. Ignored fields could indicate malformed fields or other issues with your document. Use this information to investigate and determine why fields are being ignored.

**Stacktrace indicator:** ![The icon that shows if a document contains stack traces](../../images/observability-apmTrace-icon.png "") This indicator makes it easier to find documents that contain additional information in the form of stacktraces.


## View log details [view-log-details]

Click the expand icon ![icon to open log details](/solutions/images/observability-expand-icon.png "") to get an in-depth look at an individual log file.

These details provide immediate feedback and context for what’s happening and where it’s happening for each log. From here, you can quickly debug errors and investigate the services where errors have occurred.

The following actions help you filter and focus on specific fields in the log details:

* **Filter for value (![filter for value icon](../../images/observability-plusInCircle.png "")):** Show logs that contain the specific field value.
* **Filter out value (![filter out value icon](../../images/observability-minusInCircle.png "")):** Show logs that do **not** contain the specific field value.
* **Filter for field present (![filter for present icon](../../images/observability-filter.png "")):** Show logs that contain the specific field.
* **Toggle column in table (![toggle column in table icon](../../images/observability-listAdd.png "")):** Add or remove a column for the field to the main Discover table.


## View log data set details [view-log-data-set-details]

Go to **Data Sets** to view more details about your data sets and monitor their overall quality. To open the **Data Set Quality** management page, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Refer to [Data set quality](/solutions/observability/data-set-quality-monitoring.md) for more information.