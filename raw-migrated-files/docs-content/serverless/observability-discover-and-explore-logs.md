# Explore logs [observability-discover-and-explore-logs]

With **Logs Explorer**, based on Discover, you can quickly search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. You can also customize and save your searches and place them on a dashboard. Instead of having to log into different servers, change directories, and view individual files, all your logs are available in a single view.

Go to Logs Explorer by opening **Discover** from the navigation menu, and selecting the **Logs Explorer** tab.

:::{image} ../../../images/serverless-log-explorer.png
:alt: Screen capture of the Logs Explorer
:class: screenshot
:::


## Required {{kib}} privileges [observability-discover-and-explore-logs-required-kib-privileges]

Viewing data in Logs Explorer requires `read` privileges for **Discover** and **Integrations**. For more on assigning Kibana privileges, refer to the [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) docs.


## Find your logs [observability-discover-and-explore-logs-find-your-logs]

By default, Logs Explorer shows all of your logs according to the index patterns set in the **logs source** advanced setting. Update this setting by going to *Management* → *Advanced Settings* and searching for *logs source*.

If you need to focus on logs from a specific integrations, select the integration from the logs menu:

:::{image} ../../../images/serverless-log-menu.png
:alt: Screen capture of log menu
:class: screenshot
:::

Once you have the logs you want to focus on displayed, you can drill down further to find the information you need. For more on filtering your data in Logs Explorer, refer to [Filter logs in Logs Explorer](../../../solutions/observability/logs/filter-aggregate-logs.md#logs-filter-logs-explorer).


## Review log data in the documents table [observability-discover-and-explore-logs-review-log-data-in-the-documents-table]

The documents table in Logs Explorer functions similarly to the table in Discover. You can add fields, order table columns, sort fields, and update the row height in the same way you would in Discover.

Refer to the [Discover](../../../explore-analyze/discover.md) documentation for more information on updating the table.


#### Actions column [observability-discover-and-explore-logs-actions-column]

The actions column provides access to additional information about your logs.

**Expand:** (![expand icon](../../../images/serverless-expand.svg "")) Open the log details to get an in-depth look at an individual log file.

**Degraded document indicator:** (![degraded document indicator icon](../../../images/serverless-pagesSelect.svg "")) Shows if any of the document’s fields were ignored when it was indexed. Ignored fields could indicate malformed fields or other issues with your document. Use this information to investigate and determine why fields are being ignored.

**Stacktrace indicator:** (![stacktrace indicator icon](../../../images/serverless-apmTrace.svg "")) Shows if the document contains stack traces. This indicator makes it easier to navigate through your documents and know if they contain additional information in the form of stack traces.


## View log details [observability-discover-and-explore-logs-view-log-details]

Click the expand icon (![expand icon](../../../images/serverless-expand.svg "")) in the **Actions** column to get an in-depth look at an individual log file.

These details provide immediate feedback and context for what’s happening and where it’s happening for each log. From here, you can quickly debug errors and investigate the services where errors have occurred.

The following actions help you filter and focus on specific fields in the log details:

* **Filter for value (![filter for value icon](../../../images/serverless-plusInCircle.svg "")):** Show logs that contain the specific field value.
* **Filter out value (![filter out value icon](../../../images/serverless-minusInCircle.svg "")):** Show logs that do *not* contain the specific field value.
* **Filter for field present (![filter for present icon](../../../images/serverless-filter.svg "")):** Show logs that contain the specific field.
* **Toggle column in table (![toggle column in table icon](../../../images/serverless-listAdd.svg "")):** Add or remove a column for the field to the main Logs Explorer table.


## View log quality issues [observability-discover-and-explore-logs-view-log-quality-issues]

From the log details of a document with ignored fields, as shown by the degraded document indicator ![degraded document indicator icon](../../../images/serverless-pagesSelect.svg ""), expand the **Quality issues** section to see the name and value of the fields that were ignored. Select **Data set details** to open the **Data Set Quality** page. Here you can monitor your data sets and investigate any issues.

The **Data Set Details** page is also accessible from **Project settings*** → ***Management** → **Data Set Quality**. Refer to [Monitor data sets](../../../solutions/observability/data-set-quality-monitoring.md) for more information.
