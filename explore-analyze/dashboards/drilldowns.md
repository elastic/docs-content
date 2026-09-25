---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/drilldowns.html
description: Add drilldowns to Kibana dashboard panels to navigate to other dashboards, external URLs, or Discover while preserving context and filters.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add drilldowns [drilldowns]

A drilldown is a navigation action on a dashboard panel. When you select a value, it opens a destination you define: another dashboard, a URL, or **Discover**.

The destination keeps the context of that selection. That includes the value you selected, the filters on the dashboard, and the time range.

Selecting a value can also filter the dashboard you have open, for example when you select a slice or drag a time range. Add a drilldown when you want that same selection to open another view.

Use this page to create a dashboard, URL, or Discover drilldown, and to carry the selected value and dashboard context to the destination.

## Drilldown types [drilldown-types]

You can add three types of drilldown:

* **Dashboard**: Open another dashboard from a panel. For example, open a host dashboard from a summary dashboard, with a filter for the host name you selected.
* **URL**: Open a website from a panel. For example, open a search page that includes the host name you selected.
* **Discover**: Open **Discover** from a visualization panel. For example, open the documents for one slice of a pie chart.

[![Drilldowns video](https://play.vidyard.com/UhGkdJGC32HRn3oS5ZYJL1.jpg)](https://videos.elastic.co/watch/UhGkdJGC32HRn3oS5ZYJL1?)

## Requirements [drilldowns-requirements]

To add a drilldown, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard with at least one panel that supports drilldowns

What else you need depends on the drilldown type:

* **Dashboard**: The destination dashboard.
* **Discover**: The panel itself. The drilldown opens **Discover** from that panel.
* **URL**: A URL template that can include variables from the dashboard and from the value you select.

A drilldown uses a value from a field in the data source. You cannot filter on a value created at query time, because that value has no field in the index. This includes a Lens formula, an aggregation result, and an {{esql}} `EVAL` or `STATS` result.

When the value comes from an {{esql}} query:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` The visualization explains that the value relies on a field created at query time, and you cannot use **Filter for** or **Filter out**. On a chart, a date value does not show those actions or the explanation. If the column only renames an index field, you can still filter and open a drilldown. [Add drilldowns to an {{esql}} visualization](../visualize/esorql.md#esql-viz-drilldowns) describes where the explanation appears.
* {applies_to}`stack: ga =9.4` The drilldown option is not available.

For more information about filter pills, refer to [Add pills by interacting with visualizations](using.md#_add_pills_by_interacting_with_visualizations).

## Create dashboard drilldowns [dashboard-drilldowns]

A dashboard drilldown opens another dashboard and can carry the time range, filters, and query with it. Use one to continue from a summary into a more specific view.

For example, a dashboard can show logs and metrics for several data centers. A drilldown can open a dashboard for the one data center or server you select.

The following panel types support dashboard drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.4` **Visualizations based on an {{esql}} query**
* **Vega** visualizations
* **Maps**
* **TSVB**
* **Aggregation-based**
* **Timelion**

### Create and set up the dashboards you want to connect [_create_and_set_up_the_dashboards_you_want_to_connect]

This example creates a dashboard and a dashboard drilldown. Follow it with the sample data, or use your own dashboard and data.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. Create a new dashboard.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In the application menu, select **Add** → **From library**.
    * {applies_to}`stack: ga 9.0-9.1` In the application menu, select **Add from library**.

3. Add the **[Logs] Visits** panel.
4. Set the [time filter](../query-filter/filtering.md) to **Last 30 days**, or to a 30-day period that contains data, depending on when you installed the sample data.
5. Save the dashboard. In the **Title** field, enter `Detailed logs`.
6. Open the **[Logs] Web Traffic** dashboard that was added with the sample data, then set a search and a filter.

    [Search](using.md#_filter_dashboards_using_the_kql_query_bar): `extension.keyword: ("gz" or "css" or "deb")`<br> [Filter](using.md#_add_pills_using_the_filter_editor): `geo.src: US`

### Create the dashboard drilldown [_create_the_dashboard_drilldown]

Create a drilldown that opens the **Detailed logs** dashboard from the **[Logs] Web Traffic** dashboard.

1. Hover over the **[Logs] Errors by host** panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
2. Select **Go to dashboard**.

    1. In **Name**, enter a name. For example, `View details`.
    2. From **Choose destination dashboard**, select **Detailed logs**.
    3. To keep the `geo.src` filter, the KQL query, and the time filter, select **Use filters and query from origin dashboard** and **Use date range from origin dashboard**.
    4. Select **Create drilldown**.

3. Save the dashboard.
4. In the data table panel, select **+** on a value, then select **View details**.

   :::{image} /explore-analyze/images/kibana-dashboard_drilldownOnPanel_8.3.png
   :alt: Drilldown on data table that navigates to another dashboard
   :screenshot:
   :::

The **Detailed logs** dashboard opens with the `geo.src` filter, the KQL query, and the time range you set.

## Create URL drilldowns [create-url-drilldowns]

A URL drilldown opens a website from a panel. The URL can change with the dashboard time range, the dashboard filters, and the value you select. You build that URL with [variables](#url-template-variable) in a [URL template](#url-templating-language).

![Drilldown on pie chart that navigates to GitHub](/explore-analyze/images/kibana-dashboard_urlDrilldownGoToGitHub_8.3.gif)

Some panels support more than one interaction. Under **Trigger**, select when the drilldown runs. The variables you can use depend on that choice. URL drilldowns support these triggers:

* **Single click**: One data point in the panel. The template can use `{{event.value}}` and `{{event.key}}`.
* **Table row click**: One row in a table. The template can use `{{event.values.[x]}}`, where `x` is the column number, starting at 0.
* **Range selection**: A range of values in the panel. The template can use `{{event.from}}` and `{{event.to}}`.

{applies_to}`serverless:` {applies_to}`stack: ga 9.4` {{esql}} visualization panels also support URL drilldowns.

### Create a URL drilldown [_create_a_url_drilldown]

If a pie chart breaks down values from a GitHub repository, a URL drilldown can open the matching GitHub search from the slice you select.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. Open the **[Logs] Web Traffic** dashboard.
3. Select **Edit**.
4. Add a pie chart.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In the application menu, select **Add** → **Visualization**.
    * {applies_to}`stack: ga 9.0-9.1` In the application menu, select **Create visualization**.

5. Set the visualization type to **Pie**.
6. From **Available fields**, drag **machine.os.keyword** to the workspace.
7. Select **Save and return**.
8. Hover over the pie chart panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
9. Select **Go to URL**.

    1. In **Name**, enter a name. For example, `Show on GitHub`.
    2. For **Trigger**, select **Single click**.
    3. To open {{kib}} issues on GitHub, enter this URL in **Enter URL**:

        ```text
        https://github.com/elastic/kibana/issues?q=is:issue+is:open+{{event.value}}
        ```

        {{kib}} replaces `{{event.value}}` with the pie slice you select.

    4. Select **Create drilldown**.

10. Save the dashboard.
11. On the pie chart panel, select a slice, then select **Show on GitHub**.

    ![URL drilldown popup](/explore-analyze/images/kibana-dashboard_urlDrilldownPopup_8.3.png)

12. In the list of {{kib}} repository issues, confirm that the slice value appears in the search.

    ![Open iOS issues in the elastic/kibana repository on GitHub](/explore-analyze/images/kibana-dashboard_urlDrilldownGithub_8.3.png)

### Pass context and table values in the URL [url-drilldown-examples]

Use variables to pass the dashboard time range, the dashboard filters, or a table cell in the URL. Select **Add variable** to insert a variable for the panel and the trigger you selected. Save the dashboard, then select a value on the panel and confirm the URL before you share the drilldown.

**Time range.** `context.panel.timeRange.from` and `context.panel.timeRange.to` are the panel time range when the panel has its own time range. Otherwise they are the dashboard time range. Format them with the `date` helper when the site expects a calendar date:

```text
https://example.com/search?from={{date context.panel.timeRange.from "YYYY-MM-DD"}}&to={{date context.panel.timeRange.to "YYYY-MM-DD"}}
```

**Dashboard filters and query.** `context.panel.filters` is the list of filters on the dashboard. Filters that exist only on the panel are not included. `context.panel.query.query` is the dashboard query, and `context.panel.query.language` is the language of that query. Use the `rison` helper when the destination stores {{kib}} state in the URL:

```text
{{rison context.panel.filters}}
```

Start internal links with `{{kibanaUrl}}`, which is the {{kib}} base URL.

**Table row.** For a **Table row click** trigger, `event.values.[0]` is the first cell in the row. `event.keys.[0]` is the field name for that column, and `event.columnNames.[0]` is the column label. This URL puts the first cell in the path:

```text
https://example.com/host/{{event.values.[0]}}
```

The [variables reference](#variables-reference) lists every variable, including `event.points` for a **Single click** that returns more than one data point.

## Create Discover drilldowns [discover-drilldowns]

A Discover drilldown opens **Discover** from a visualization panel and can carry the time range, filters, and query with it. Use one to read the documents behind a chart value.

For example, a Discover drilldown on a pie chart can open only the documents for the slice you select.

![Drilldown on bar vertical stacked chart that navigates to Discover](/explore-analyze/images/kibana-dashboard_discoverDrilldown_8.3.gif)

The following panel types support Discover drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.5` **Visualizations based on an {{esql}} query**

    On {{esql}} panels, dashboard filters and the dashboard KQL or Lucene query are translated into a `WHERE` clause in the panel's ES|QL query, so the same context applies in **Discover**. Filters that can't be expressed in ES|QL are dropped. The **Explore in Discover** panel action applies the same translation.

::::{tip}
You can [open a visualization panel in Discover](../visualize/manage-panels.md#explore-the-underlying-documents) without setting up a drilldown.
::::

### Create the Discover drilldown [_create_the_discover_drilldown]

Create a drilldown that opens **Discover** from the **[Logs] Web Traffic** dashboard. That dashboard is added when you install the [**Sample web logs**](/manage-data/ingest/sample-data.md) data.

1. Select **Edit**. Hover over the **[Logs] Bytes distribution** panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
2. Select **Open in Discover**.
3. In **Name**, enter a name. For example, `View bytes distribution in Discover`.
4. To open **Discover** in a new tab, select **Open in new tab**.
5. Select **Create drilldown**.
6. Save the dashboard.
7. On the **[Logs] Bytes distribution** bar vertical stacked chart, select a bar, then select **View bytes distribution in Discover**.

   :::{image} /explore-analyze/images/kibana-dashboard_discoverDrilldown_8.3.png
   :alt: Drilldown on bar vertical stacked chart that navigates to Discover
   :screenshot:
   :::

**Discover** opens in a new tab and shows the documents for the bar you selected.

## Manage drilldowns [manage-drilldowns]

You can edit a drilldown, copy it to another panel, or delete it.

1. Open the panel menu that includes the drilldown, then select **Manage drilldowns**.
2. On the **Manage** tab, use the following options:

    * To change a drilldown, select **Edit**, make your changes, then select **Save**.
    * To copy a drilldown, select **Copy**, enter the drilldown name, then select **Create drilldown**.
    * To delete a drilldown, select it, then select **Delete ({count})**.

## URL templating [url-templating-language]

The URL template input uses [Handlebars](https://ela.st/handlebars-docs#expressions), a templating language. A template looks like regular text with Handlebars expressions embedded in it.

```text
https://github.com/elastic/kibana/issues?q={{event.value}}
```

A Handlebars expression starts with `{{`, contains a value or helper, and ends with `}}`. When you run the drilldown, {{kib}} replaces each expression with a value from the dashboard and from the interaction.

$$$helpers$$$
In addition to [built-in](https://ela.st/handlebars-helpers) Handlebars helpers, you can use the custom helpers on this page.

Refer to the Handlebars [documentation](https://ela.st/handlebars-docs#expressions) for advanced use cases.

## Custom helpers [_custom_helpers]

**json**

Serialize variables in JSON format.

Example:

`{{json event}}`<br> `{{json event.key event.value}}`<br> `{{json filters=context.panel.filters}}`

**rison**

Serialize variables in [rison](https://github.com/w33ble/rison-node) format. Rison is a common format for {{kib}} apps for storing state in the URL.

Example:

`{{rison event}}`<br> `{{rison event.key event.value}}`<br> `{{rison filters=context.panel.filters}}`

**date**

Format dates. Supports relative date expressions (for example, `now-15d`). Refer to the [moment](https://momentjs.com/docs/#/displaying/format/) docs for formatting options.

Example:

`{{date event.from "YYYY MM DD"}}`<br> `{{date "now-15"}}`

**formatNumber**

Format numbers. Numbers can be formatted to look like currency, percentages, times or numbers with decimal places, thousands, and abbreviations. Refer to [numeral.js](http://numeraljs.com/#format) for formatting options.

Example:

`{{formatNumber event.value "0.0"}}`

**lowercase**

Convert a string to lower case.

Example:

`{{lowercase event.value}}`

**uppercase**

Convert a string to upper case.

Example:

`{{uppercase event.value}}`

**trim**

Remove leading and trailing spaces from a string.

Example:

`{{trim event.value}}`

**trimLeft**

Remove leading spaces from a string.

Example:

`{{trimLeft event.value}}`

**trimRight**

Remove trailing spaces from a string.

Example:

`{{trimRight event.value}}`

**mid**

Extract a substring from a string by start position and number of characters to extract.

Example:

`{{mid event.value 3 5}}` extracts five characters starting from the third character.

**left**

Extract a number of characters from a string, starting from the left.

Example:

`{{left event.value 3}}`

**right**

Extract a number of characters from a string, starting from the right.

Example:

`{{right event.value 3}}`

**concat**

Concatenate two or more strings.

Example:

`{{concat event.value "," event.key}}`

**replace**

Replace all substrings within a string.

Example:

`{{replace event.value "stringToReplace" "stringToReplaceWith"}}`

**split**

Split a string using a provided splitter.

Example:

`{{split event.value ","}}`

**encodeURIComponent**

Escape a string using the built-in `encodeURIComponent` function.

**encodeURIQuery**

Escape a string with the built-in `encodeURIComponent` function, but leave `@`, `:`, `$`, `,`, and `;` unchanged.

### URL template variables [url-template-variable]

The URL drilldown template has three sources for variables:

* **Global**: Static variables that do not change with the panel or the interaction. For example, `{{kibanaUrl}}`.
* **Context**: Variables from the panel on the dashboard. For example, `{{context.panel.filters}}` is the list of filters on the dashboard.
* **Event**: Variables from the trigger. {{kib}} reads them from the interaction when you run the drilldown.

Save the dashboard and test the drilldown on the panel before you rely on it. To see every variable for the current panel and the selected trigger, select **Add variable** in the URL template field.

### Variables reference [variables-reference]

| Source | Variable | Description |
| --- | --- | --- |
| **Global** | kibanaUrl | {{kib}} base URL. Use it to open another {{kib}} page. |
| **Context** | context.panel | Context from the current dashboard panel. |
|  | context.panel.id | ID of the panel. |
|  | context.panel.title | Title of the panel. |
|  | context.panel.filters | Filters on the dashboard. Filters that exist only on the panel are not included.<br>Tip: Use the [rison](#helpers) helper to pass these filters in a {{kib}} URL. |
|  | context.panel.query.query | Dashboard query string. |
|  | context.panel.query.language | Language of the dashboard query. |
|  | context.panel.timeRange.from<br>context.panel.timeRange.to | Panel time range when the panel has its own time range. Otherwise, the dashboard time range.<br>Tip: Use the [date](#helpers) helper to format the date. |
|  | context.panel.indexPatternId<br>context.panel.indexPatternIds | The {{data-source}} IDs used by the panel. |
|  | context.panel.savedObjectId | ID of the saved object behind the panel. |
| **Single click** | event.value | Value of the selected data point. |
|  | event.key | Field name of the selected data point. |
|  | event.negate | Boolean that indicates whether the selected data point resulted in a negative filter. |
|  | event.points | Some visualizations return more than one data point for the value you select. Use the list when a single value is not enough.<br><br>Example:<br>`{{json event.points}}`<br>`{{event.points.[0].key}}`<br>`{{event.points.[0].value}}`<br>`{{#each event.points}}key=value&{{/each}}`<br>Note:<br>`{{event.value}}` is a shorthand for `{{event.points.[0].value}}`<br>`{{event.key}}` is a shorthand for `{{event.points.[0].key}}` |
| **Table row click** | event.rowIndex | Number of the selected row, starting from 0. |
|  | event.values | All cell values for the selected row. To access a column value, use `{{event.values.[x]}}`, where `x` is the column number. |
|  | event.keys | Field names for each column. |
|  | event.columnNames | Column names. |
| **Range selection** | event.from<br>event.to | Start and end of the selected range, as numbers.<br>Tip: Use the [date](#helpers) helper to format a date. |
|  | event.key | Aggregation field behind the selected range, if available. |
