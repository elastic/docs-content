---
navigation_title: Create a URL drilldown
description: Create a drilldown that opens a website from a panel, using a URL template and the value you select.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
---

# Create a URL drilldown [create-url-drilldowns]

A URL drilldown opens a website from a panel. The URL can change with the dashboard time range, the dashboard filters, and the value you select. You build that URL with [variables](#url-template-variable) in a [URL template](#url-templating-language).

Refer to [Drilldowns](drilldowns.md) to choose a drilldown type and to check values created at query time.

## Before you begin [create-url-drilldown-requirements]

To create a URL drilldown, you need:

:::{include} _snippets/drilldown-access.md
:::

The following panel types support URL drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.4` **Visualizations based on an {{esql}} query**
* **Vega** visualizations
* **Maps**
* **Image**
* **Discover** sessions
* **TSVB**
* **Aggregation-based**
* **Timelion**

For a computed value, including an {{esql}} result, refer to [How a drilldown uses the selected value](drilldowns.md#drilldowns-requirements).

## Create the drilldown [_create_a_url_drilldown]

This example adds a pie chart and a URL drilldown that opens a GitHub search for the slice you select. Follow it with the sample data, or use your own dashboard and data.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. Open the **[Logs] Web Traffic** dashboard and select **Edit**.
3. From the application menu, add a new visualization to the dashboard, then set the type to **Pie**.
4. Drag **machine.os.keyword** from **Available fields** to the workspace, then select **Save and return**.
5. Hover over the pie chart panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
6. Select **Go to URL**.

    1. In **Name**, enter a name. For example, `Show on GitHub`.
    2. For **Trigger**, select **Single click**. To use another interaction, refer to [Choose a trigger](#url-drilldown-triggers).
    3. To open {{kib}} issues on GitHub, enter this URL in **Enter URL**:

        ```text
        https://github.com/elastic/kibana/issues?q=is:issue+is:open+{{event.value}}
        ```

        {{kib}} replaces `{{event.value}}` with the pie slice you select.

    4. Optional: Open **Additional options**. **Open URL in new tab** and **Encode URL** are already on. **Open URL in new tab** opens the site in a new browser tab. Turn it off to open the site in the same tab. **Encode URL** percent-encodes the URL after the template is filled in.
    5. Select **Create drilldown**.

7. Save the dashboard.
8. On the pie chart panel, select a slice, then select **Show on GitHub**.

    ![URL drilldown popup](/explore-analyze/images/kibana-dashboard_urlDrilldownPopup.png)

The GitHub issues search opens with the slice value in the query.

## Choose a trigger [url-drilldown-triggers]

**Trigger** lists only the interactions that the panel supports. If the panel supports one interaction, **Trigger** is already set and the list is hidden.

* **Single click**: Select one data point, such as a pie slice or a bar. The template can use `{{event.value}}` for the value and `{{event.key}}` for the field name. This trigger is available on visualizations that use a data view, visualizations based on an {{esql}} query, and **Maps**.
* **Table row click**: Select a row in a table visualization that uses a data view or an {{esql}} query. The template can use `{{event.values.[x]}}`, where `x` is the column number, starting at 0. `{{event.keys.[x]}}` is the field name, and `{{event.columnNames.[x]}}` is the column label.
* **Range selection**: Select a range of values on the visualization. The template can use `{{event.from}}` and `{{event.to}}`. This trigger is available on **Bar**, **Line**, **Area**, and **Heat map** visualizations, including those based on an {{esql}} query, and on **Aggregation-based**, **TSVB**, and **Timelion** panels.
* **Context menu**: The drilldown name is added to the {icon}`boxes_vertical` panel menu. The template has no value from a data point. It can still use dashboard variables, such as the time range and `{{context.panel.title}}`. This is the only URL trigger on **Vega** visualizations, **Discover** sessions, and **Gauge** visualizations.
* **Image click**: Select the image on an **Image** panel. The template has no value from the image. It can still use dashboard variables, such as `{{context.panel.title}}`.

## URL template [url-templating-language]

The URL template input uses [Handlebars](https://ela.st/handlebars-docs#expressions), a templating language. A template looks like regular text with Handlebars expressions embedded in it.

```text
https://github.com/elastic/kibana/issues?q={{event.value}}
```

A Handlebars expression starts with `{{`, contains a value or helper, and ends with `}}`. When you run the drilldown, {{kib}} replaces each expression with a value from the dashboard and from the interaction.

$$$helpers$$$
In addition to [built-in](https://ela.st/handlebars-helpers) Handlebars helpers, you can use the custom helpers on this page.

Refer to the Handlebars [documentation](https://ela.st/handlebars-docs#expressions) for advanced use cases.

### Variables [url-template-variable]

The URL drilldown template has three sources for variables:

* **Global**: Static variables that do not change with the panel or the interaction. For example, `{{kibanaUrl}}`.
* **Context**: Variables from the panel on the dashboard. For example, `{{context.panel.filters}}` is the list of filters on the dashboard.
* **Event**: Variables from the trigger. {{kib}} reads them from the interaction when you run the drilldown.

Save the dashboard and test the drilldown on the panel before you rely on it. To see every variable for the current panel and the selected trigger, select **Add variable** in the URL template field.

$$$variables-reference$$$

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

### Custom helpers [_custom_helpers]

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

### Pass context and table values in the URL [url-drilldown-examples]

You can use variables to pass the dashboard time range, the dashboard filters, or a table cell in the URL. The [variables reference](#variables-reference) lists every variable. Select **Add variable** to insert a variable for the panel and the trigger you selected. Save the dashboard, then select a value on the panel and confirm the URL before you share the drilldown.

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

A **Single click** that returns more than one data point can also use `event.points`. The [variables reference](#variables-reference) includes it with the other variables.

## Next steps [create-url-drilldown-next-steps]

* [Manage drilldowns](manage-drilldowns.md)

## Related pages [create-url-drilldown-related-pages]

* [Drilldowns](drilldowns.md)
* [Create a dashboard drilldown](create-dashboard-drilldown.md)
* [Create a Discover drilldown](create-discover-drilldown.md)
