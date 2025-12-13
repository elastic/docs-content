---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/timelines-ui.html
  - https://www.elastic.co/guide/en/serverless/current/security-timelines-ui.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Timeline [security-timelines-ui]

Use Timeline as your workspace for investigations and threat hunting. You can add alerts from multiple indices to a Timeline to facilitate advanced investigations.

You can drag or send fields of interest to a Timeline to create the desired query. For example, you can add fields from tables and histograms on the **Overview**, **Alerts**, **Hosts**, and **Network** pages, as well as from other Timelines. Alternatively, you can add a query directly in Timeline by expanding the [query builder](/solutions/security/investigate/timeline.md#narrow-expand) and clicking **+ Add field**.

:::{image} /solutions/images/security-timeline-ui-updated.png
:alt: example Timeline with several events
:screenshot:
:::

In addition to Timelines, you can create and attach Timeline templates to [detection rules](/solutions/security/detect-and-alert.md). Timeline templates allow you to define the source event fields used when you investigate alerts in Timeline. You can select whether the fields use predefined values or values retrieved from the alert. For more information, refer to [Timeline templates](/solutions/security/investigate/timeline-templates.md).


## Grant access to Timeline [timeline-privileges]

You can control access to Timeline by setting the [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) for the **Timeline** feature under **Security**. 

::::{note}
Refer to [Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md) to learn about other available SIEM features and how to give your role access to them.


## Create new or open existing Timeline [open-create-timeline]

To make a new Timeline, choose one of the following:

* Find **Timelines** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new Timeline**.
* Go to the Timeline bar (which is at the bottom of most pages), click the ![Add new button](/solutions/images/security-add-new-timeline-button.png "title =20x20") button, then click **Create new Timeline template**.
* From an open Timeline or Timeline template, click **New** → **New Timeline**.

To open an existing Timeline, choose one of the following:

* Go to the Timelines page, then click a Timeline’s title.
* Go to the Timeline bar, click the ![Add new button](/solutions/images/security-add-new-timeline-button.png "title =20x20") button, then click **Open Timeline**.
* From an open Timeline or Timeline template, click **Open**, then select the appropriate Timeline.

To avoid losing your changes, you must save the Timeline before moving to a different {{security-app}} page. If you change an existing Timeline, you can use the **Save as new timeline** toggle to make a new copy of the Timeline without overwriting the original one.

::::{tip}
Click the star icon (![Favorite icon](/solutions/images/security-favorite-icon.png "title =20x20")) to favorite your Timeline and quickly find it later.
::::



## View and refine Timeline results [refine-timeline-results]

You can select whether Timeline displays detection alerts and other raw events, or just alerts. By default, Timeline displays both raw events and alerts. To hide raw events and display alerts only:
* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` Select the `Security solution alerts` data view.
* {applies_to}`stack: ga 9.0` Click **Data view** to the left of the KQL query bar, then select **Show only detection alerts**.


## Inspect an event or alert [timeline-inspect-events-alerts]

To further inspect an event or detection alert, click the **View details** button. A flyout with event or [alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md) appears.


## Configure Timeline event context and display [conf-timeline-display]

Many types of events automatically appear in preconfigured views that provide relevant contextual information, called **Event renderers**. All event renderers are turned off by default. To turn them on, use the **Event renderers** toggle at the top of the results pane. To only turn on specific event renderers, click the gear (![Customize event renderer button](/solutions/images/security-customize-event-renderers.png "title =20x20")) icon next to the toggle, and select the ones you want enabled. Close the **Customize event renderers** pane when you’re done. Your changes are automatically applied to Timeline.

:::{image} /solutions/images/security-timeline-ui-renderer.png
:alt: example timeline with the event renderer highlighted
:screenshot:
:::

The example above displays the Flow event renderer, which highlights the movement of data between its source and destination. If you see a particular part of the rendered event that interests you, you can drag it up to the drop zone below the query bar for further investigation.

You can also modify a Timeline’s display in other ways:

* [Add and remove fields](/solutions/security/investigate/timeline.md#add-remove-timeline-fields) from Timeline
* Create [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) and display them in the Timeline
* Reorder and resize columns
* Copy a column name or values to a clipboard
* Change how the name, value, or description of a field are displayed in Timeline
* View the Timeline in full screen mode
* Add or delete [notes](/solutions/security/investigate/notes.md) attached to alerts, events, or Timeline
* Pin interesting events to the Timeline


## Add and remove fields from Timeline [add-remove-timeline-fields]

The Timeline table shows fields that are available for alerts and events in the selected data view. You can modify the table to display fields that interest you. Use the sidebar to search for specific fields or scroll through it to find fields of interest. Fields that you select display as columns in the table.

To add a field from the sidebar, hover over it, and click the **Add field as a column** button (![Add a field as a column button](/solutions/images/security-add-field-button.png "title =20x20")), or drag and drop the field into the table. To remove a field, hover over it, and click the **Remove field as a column** button (![Remove a field as a column button](/solutions/images/security-remove-field-button.png "title =20x20")).

:::{image} /solutions/images/security-timeline-sidebar.png
:alt: Shows the sidebar that allows you to configure the columns that display in Timeline
:screenshot:
:::


## Use the Timeline query builder [narrow-expand]

Expand the query builder by clicking the query builder button (![Query builder button](/solutions/images/security-query-builder-button.png "title =20x20")) to the right of the KQL query bar. Drop in fields to build a query that filters Timeline results. The fields' relative placement specifies their logical relationships: horizontally adjacent filters use `AND`, while vertically adjacent filters use `OR`.

::::{tip}
Collapse the query builder and provide more space for Timeline results by clicking the query builder button (![Query builder button](/solutions/images/security-query-builder-button.png "title =20x20")).
::::



## Edit existing filters [pivot]

% Consider changing the anchor text for this section. It's not very descriptive atm.

Click a filter to access additional operations such as **Add filter**, **Clear all**, **Load saved query**, and more:

:::{image} /solutions/images/security-timeline-ui-filter-options.png
:alt: timeline ui filter options
:screenshot:
:::

Here are examples of various types of filters:

Field with value
:   Filters for events with the specified field value:

    :::{image} /solutions/images/security-timeline-filter-value.png
    :alt: timeline filter value
    :screenshot:
    :::


Field exists
:   Filters for events containing the specified field:

    :::{image} /solutions/images/security-timeline-field-exists.png
    :alt: timeline field exists
    :screenshot:
    :::


Exclude results
:   Filters for events that do not contain the specified field value (`field with value` filter) or the specified field (`field exists` filter):

    :::{image} /solutions/images/security-timeline-filter-exclude.png
    :alt: timeline filter exclude
    :screenshot:
    :::


Temporarily disable
:   The filter is not used in the query until it is enabled again:

    :::{image} /solutions/images/security-timeline-disable-filter.png
    :alt: timeline disable filter
    :screenshot:
    :::


Filter for field present
:   Converts a `field with value` filter to a `field exists` filter.

::::{note}
When you convert a [Timeline template](/solutions/security/investigate/timeline-templates.md) to a Timeline, some fields may be disabled. For more information, refer to [Timeline template legend](/solutions/security/investigate/timeline-templates.md#template-legend-ui).
::::



## Attach Timeline to a case [timeline-to-cases-ui]

To attach a Timeline to a new or existing case, open it, click **Attach to case** in the upper right corner, then select either **Attach to new case** or **Attach to existing case**.

To learn more about cases, refer to [Cases](/solutions/security/investigate/cases.md).


## Manage existing Timelines [manage-timelines-ui]

You can view, duplicate, export, delete, and create templates from existing Timelines:

1. Find **Timelines** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click the **All actions** menu in the desired row, then select an action:

    * **Create template from timeline** (refer to [Timeline templates](/solutions/security/investigate/timeline-templates.md))
    * **Duplicate timeline**
    * **Export selected** (refer to [Export and import Timelines](/solutions/security/investigate/timeline.md#import-export-timelines))
    * **Delete selected**
    * **Create query rule from timeline** (only available if the Timeline contains a KQL query)
    * **Create EQL rule from timeline** (only available if the Timeline contains an EQL query)


::::{tip}
To perform an action on multiple Timelines, first select the Timelines, then select an action from the **Bulk actions** menu.
::::



## Export and import Timelines [import-export-timelines]

You can export and import Timelines, which enables you to share Timelines from one space or {{elastic-sec}} instance to another. Exported Timelines are saved as `.ndjson` files.

To export Timelines:

* Find **Timelines** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Either click the **All actions** menu in the relevant row and select **Export selected**, or select multiple Timelines and then click **Bulk actions** → **Export selected**.

To import Timelines:

* Click **Import**, then select or drag and drop the relevant `.ndjson` file.

    ::::{note}
    Multiple Timeline objects are delimited with newlines.
    ::::



## Filter Timeline results with EQL [filter-with-eql]

Use the **Correlation** tab to investigate Timeline results with [EQL queries](/explore-analyze/query-filter/languages/eql.md).

When forming EQL queries, you can write a basic query to return a list of events and alerts. Or, you can create sequences of EQL queries to view matched, ordered events across multiple event categories. Sequence queries are useful for identifying and predicting related events. They can also provide a more complete picture of potential adversary behavior in your environment, which you can use to create or update rules and detection alerts.

The following image shows what matched ordered events look like in the Timeline table. Events that belong to the same sequence are matched together in groups and shaded red or blue. Matched events are also ordered from oldest to newest in each sequence.

:::{image} /solutions/images/security-correlation-tab-eql-query.png
:alt: a Timeline's correlation tab
:screenshot:
:::

From the **Correlation** tab, you can also do the following:

* Specify the date and time range that you want to investigate.
* Reorder the columns and choose which fields to display.
* Choose a data view and whether to show detection alerts only.


## Use {{esql}} to investigate events [esql-in-timeline]

::::{note}
{{esql}} is enabled by default in {{kib}}. It can be disabled using the `enableESQL` setting from the [Advanced Settings](kibana://reference/advanced-settings.md). This will hide the {{esql}} user interface from various applications. However, users will be able to access existing {{esql}} artifacts like saved searches and visualizations.
::::


The [Elasticsearch Query Language ({{esql}})](elasticsearch://reference/query-languages/esql.md) provides a powerful way to filter, transform, and analyze event data stored in {{es}}. {{esql}} queries use "pipes" to manipulate and transform data in a step-by-step fashion. This approach allows you to compose a series of operations, where the output of one operation becomes the input for the next, enabling complex data transformations and analysis.

You can use {{esql}} in Timeline by opening the **{{esql}}** tab. From there, you can:

* Write an {{esql}} query to explore your events. For example, start with the following query, then iterate on it to tailor your results:

    ```esql
    FROM .alerts-security.alerts-default,apm-*-transaction*,auditbeat-*,endgame-*,filebeat-*,logs-*,packetbeat-*,traces-apm*,winlogbeat-*,-*elastic-cloud-logs-*
    | LIMIT 10
    | KEEP @timestamp, message, event.category, event.action, host.name, source.ip, destination.ip, user.name
    ```

    This query does the following:

    * It starts by querying documents within the Security alert index (`.alerts-security.alerts-default`) and indices specified in the [Security data view](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices).
    * Then, the query limits the output to the top 10 results.
    * Finally, it keeps the default Timeline fields (`@timestamp`, `message`, `event.category`, `event.action`, `host.name`, `source.ip`, `destination.ip`, and `user.name`) in the output.

        ::::{tip}
        When querying indices that tend to be large (for example, `logs-*`), performance can be impacted by the number of fields returned in the output. To optimize performance, we recommend using the [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) command to specify fields that you want returned. For example, add the clause `KEEP @timestamp, user.name` to the end of your query to specify that you only want the `@timestamp` and `user.name` fields returned.
        ::::


::::{note}
* An error message displays when the query bar is empty.
* When specifying data sources for an {{esql}} query, autocomplete doesn’t suggest hidden indices, such as `.alerts-*`. You must manually enter the index name or pattern.

::::


* Click the help icon (![ES|QL reference button](/solutions/images/security-esql-help-ref-button.png "title =20x20")) on the far right side of the query editor to open the in-product reference documentation for all {{esql}} commands and functions.
* Visualize query results using [Discover](/explore-analyze/discover.md) functionality.

:::{image} /solutions/images/security-esql-tab.png
:alt: Example of the ES|QL tab in Timeline
:screenshot:
:::


### Additional {{esql}} resources [esql-in-timeline-resources]

To get started using {{esql}}, read the tutorial for [using {{esql}} in {{kib}}](/explore-analyze/query-filter/languages/esql-kibana.md). Much of the functionality available in {{kib}} is also available in Timeline.

To find examples of using {{esql}} for threat hunting, check out [our blog](https://www.elastic.co/blog/introduction-to-esql-new-query-language-flexible-iterative-analytics).
