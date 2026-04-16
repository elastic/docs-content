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

**Discover** offers a dedicated experience for exploring log data. When **Discover** recognizes data in `logs-*` indices, it enables specific features to help you investigate log events more effectively. Use this view to quickly search and filter your log data, explore field structure, and surface findings in visualizations or dashboards.

If you're just getting started with **Discover** and want to learn its main principles, you should get familiar with the [default experience](/explore-analyze/discover.md).

:::{note}
For a contextual logs experience, set the **Solution view** for your space to **{{observability}}**. Refer to [Managing spaces](/deploy-manage/manage-spaces.md) for more information.
:::

:::{image} ../../images/observability-log-explorer.png
:alt: Screen capture of Discover
:screenshot:
:::

## Required {{kib}} privileges [logs-explorer-privileges]

Viewing data in Discover logs data views requires `read` privileges for **Discover**, **Index**, and **Logs**. For more on assigning {{kib}} privileges, refer to the [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) docs.


## Load log data [load-log-data]

The logs experience is available in:

* **{{data-source-cap}} mode**: Select the `logs-*` or `All logs` {{data-source}} from the **Discover** main page. By default, **All logs** shows all of your logs according to the index patterns set in the **logs sources** advanced setting. You can navigate to the **Advanced settings** from the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    To focus on logs from a specific source, create a data view using the index patterns for that source. For more information, refer to [Create a data view](/explore-analyze/find-and-organize/data-views.md#settings-create-pattern).

* **{{esql}} mode**: Switch to **{{esql}}** mode and use the `FROM` command to query your log data:

    ```esql
    FROM logs-*-*,logs-*,filebeat-*
    ```

    You can also query a specific index:

    ```esql
    FROM logs-myservice-default
    ```

Once you have the logs you want to focus on, you can drill down further. For more on filtering, refer to [Filter logs in Discover](/solutions/observability/logs/filter-aggregate-logs.md#logs-filter-discover).


## Review log data in the documents table [review-log-data-in-the-documents-table]

The documents table lets you add fields, order table columns, sort fields, and update the row height in the same way you would in Discover.

Refer to the [Discover](/explore-analyze/discover.md) documentation for more information on updating the table.


### Actions column [actions-column]

The actions column provides additional information about your logs.

**Expand:** ![The icon to expand log details](/solutions/images/observability-expand-icon.png "") Open the log details to get an in-depth look at an individual log file.

**Degraded document indicator:** ![The icon that shows ignored fields](../../images/observability-pagesSelect-icon.png "") This indicator shows if any of the document’s fields were ignored when it was indexed. Ignored fields could indicate malformed fields or other issues with your document. Use this information to investigate and determine why fields are being ignored.

**Stacktrace indicator:** ![The icon that shows if a document contains stack traces](../../images/observability-apmTrace-icon.png "") This indicator makes it easier to find documents that contain additional information in the form of stacktraces.


## View log details [view-log-details]

Select the expand icon ![icon to open log details](/solutions/images/observability-expand-icon.png "") to get an in-depth look at an individual log file.

These details provide immediate feedback and context for what’s happening and where it’s happening for each log. From here, you can quickly debug errors and investigate the services where errors have occurred.

The following actions help you filter and focus on specific fields in the log details:

* **Filter for value (![filter for value icon](../../images/observability-plusInCircle.png "")):** Show logs that contain the specific field value.
* **Filter out value (![filter out value icon](../../images/observability-minusInCircle.png "")):** Show logs that do **not** contain the specific field value.
* **Filter for field present (![filter for present icon](../../images/observability-filter.png "")):** Show logs that contain the specific field.
* **Toggle column in table (![toggle column in table icon](../../images/observability-listAdd.png "")):** Add or remove a column for the field to the main Discover table.

### Content breakdown [discover-logs-content-breakdown]

The **Content breakdown** section gives you a view of the raw log text. For each message, the breakdown displays:

- **Field name** — the source field being parsed (for example, `message`)
- **Timestamp** — the time the log event occurred
- **Message content** — the full text of the log message

From the content breakdown, you can select **Parse content in Streams** to open the related stream and extract structured fields from the message. Use this when your logs contain unstructured data that you want to query or filter on.

### Similar errors [discover-logs-similar-errors]

The **Similar errors** section shows an occurrences chart for errors that share the same `service.name`, `error.culprit`, `message`, and `error.grouping_name` fields. Use this view to identify recurring errors and spot patterns across your services.

Select **Open in Discover** to open a filtered view of all similar errors.

### Stream [discover-logs-stream]
The **Stream** section provides a link to the related [stream](../streams/streams.md) for the selected log. From here, you can extract fields, set data retention, and route data from one place.

### Stacktrace [discover-logs-stacktrace]

The **Stacktrace** section is available for logs from instrumented applications. It shows the full stack trace leading to the error, including the culprit, error message, and individual frames. Frames from your application code are shown alongside library frames, which you can expand to see the full call stack.

When a root cause is available, a **Caused by** section appears below the main stack trace with additional context about the underlying error.

### Trace summary [discover-logs-trace-summary]

The **Trace summary** section is available for logs from instrumented applications. It shows a condensed waterfall of the trace the selected document belongs to. Each row represents a span or transaction, positioned on a timeline to show when it started and how long it took.