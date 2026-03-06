---
navigation_title: "Learn data exploration and visualization"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/get-started.html
description: Learn Kibana's core analyst features, including Discover, ES|QL, Lens, and Dashboards, by exploring data, building visualizations, and sharing a dashboard.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: tutorial
---

# Learn data exploration and visualization with {{kib}} [kibana-get-started]

{{kib}} provides powerful tools for exploring and visualizing data stored in {{es}}. **Discover** lets you search and filter documents with Elasticsearch Query Language ({{esql}}), **Lens** transforms query results into charts, and **Dashboards** combine visualizations into shareable, interactive views. This tutorial teaches you how these core features work together by walking through a complete workflow, from querying data to sharing a finished dashboard.

You'll use {{kib}}'s built-in sample web logs dataset so you can focus on learning the tools without needing to set up data ingestion. Basic familiarity with {{es}} concepts (indices, documents, fields) is helpful but not required.

These features are available across all Elastic solutions and project types, so what you learn here applies regardless of your use case.

By the end of this tutorial, you'll know how to:

* Search and filter data in **Discover** using {{esql}}
* Create visualizations with **Lens**
* Combine panels into a **Dashboard** and customize the layout
* Navigate between **Discover**, **Lens**, and **Dashboards** to iterate on your analysis
* Share a dashboard with your team

## Before you begin [visualize-explore-prerequisites]

* An {{stack}} deployment or {{serverless-full}} project with {{es}} and {{kib}}. Don't have one yet? [Start a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body). 
* The required privileges to complete the tutorial. Specifically:
  - **{{kib}} privileges**: `All` on **Discover** and **Dashboard** (to explore data and create dashboards).
  - **{{es}} index privileges**: `read` and `view_index_metadata` on the `kibana_sample_data_logs` index (to query the sample data in Discover).

  :::{note}
  If you created a trial account, you are the admin of your deployment and already have all the required privileges.
  :::

## Step 1: Load sample data [get-your-data-in]

Before you can explore and visualize, you need data in {{es}}. In this tutorial you use {{kib}}'s built-in sample web logs dataset, which you can load in a few clicks. No agents or integrations required.

1. Open the **Integrations** page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the list of integrations, select **Sample Data**.
3. On the page that opens, select **Other sample data sets**.
4. On the **Sample web logs** card, select **Add data**.

The sample data is loaded into the `kibana_sample_data_logs` index. It includes web server access logs with fields like `@timestamp`, `clientip`, `response`, `bytes`, `url`, `extension`, and `geo.src`.

:::{tip}
When you're ready to explore your own data, refer to [Ingest data](/manage-data/ingest.md) for an overview of ingestion options, including {{agent}}, Beats, and direct API uploads. Many [integrations](/reference/fleet/manage-integrations.md) also ship with pre-built dashboards, visualizations, {{anomaly-jobs}}, and alerting rules, so you can start analyzing your data as soon as it's ingested.
:::

## Step 2: Explore data in Discover with {{esql}} [explore-data-in-discover]

**Discover** is the starting point for data exploration. You can search, filter, and visualize your data interactively.

Discover supports two exploration modes. This tutorial uses **{{esql}}** (Elasticsearch Query Language), a piped query language that lets you chain operations like filtering, aggregating, and sorting in a single query. Unlike the default classic, KQL-based mode, {{esql}} doesn't require you to set up a {{data-source}} first: you query indices directly by name, so you can start exploring right away.

::::::{stepper}

:::::{step} Open Discover and switch to {{esql}}

1. From the navigation menu, go to **Discover**.
2. Select {icon}`editorCodeBlock` **{{esql}}** from the application menu.

**Result:** The query bar changes to an {{esql}} editor where you can write piped queries.
:::::

:::::{step} Run your first query

Enter the following query, then select {icon}`playFilled` **Run** or **Search**. If you choose to type your own query, the editor helps you with relevant autocomplete suggestions for commands, fields, and values.

```esql
FROM kibana_sample_data_logs <1>
| KEEP @timestamp, clientip, response, message <2>
| SORT @timestamp DESC <3>
| LIMIT 50 <4>
```

1. Reads from the sample web logs index.
2. Retains only these four fields in the output, discarding everything else.
3. Orders results by timestamp, most recent first.
4. Returns only the first 50 rows. Without `LIMIT`, {{esql}} returns up to 1,000 rows by default. A smaller limit keeps the result set focused and the response fast while you explore. 

For a complete list of commands and functions, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

**Result:** The results table displays the most recent web log entries with only the fields you selected. To discover which fields are available, browse the field list in the sidebar.

:::{image} /explore-analyze/images/kibana-learning-tutorial-esql-first-query.png
:alt: Discover showing an ES|QL query with results table and histogram
:screenshot:
:::

:::{tip}
**No results?** The time range filter defaults to the last 15 minutes. Sample data timestamps are relative to when you loaded the dataset, so you may need to select a wider range, such as **Last 90 days**, or more, to see results.
:::
:::::

:::::{step} Inspect individual results and documents

The results table gives you an overview, but sometimes you need the full details of a single event. To inspect a document:

1. Select the expand icon ({icon}`expand`) on any row in the results table. A flyout opens.
2. The flyout shows the fields returned by your query in a detailed view. Use the **Table** tab to see field names and values, or the **JSON** tab to see the raw document.
3. Use the navigation arrows at the top of the flyout to move between documents without closing it. This is useful when you need to compare consecutive events or trace a sequence.

:::{image} /explore-analyze/images/kibana-learning-tutorial-document-viewer.png
:alt: Document viewer flyout showing all fields for a single web log entry
:screenshot:
:::
:::::

:::::{step} Filter and aggregate

Browsing individual events is useful, but you can also summarize data directly in {{esql}}. In this step, you check which HTTP response codes appear in the logs and how frequently. Use `WHERE` to filter out rows with missing values and `STATS` to count events per response code:

```esql
FROM kibana_sample_data_logs
| WHERE response IS NOT NULL <1>
| STATS event_count = COUNT(*) BY response <2>
| SORT event_count DESC <3>
| LIMIT 50
```

1. Excludes rows where the HTTP response code is missing.
2. Groups rows by response code and counts events in each group.
3. Puts the most frequent response codes at the top.

**Result:** The table shows the HTTP response codes ranked by frequency. A chart appears above the table to visualize the aggregation, so you can see at a glance how traffic breaks down by status (200, 404, 503, and so on). A four-line query turned thousands of raw log entries into a ranked breakdown with a chart. Notice that the field list in the sidebar now only shows the fields produced by the query (`event_count` and `response`), reflecting the narrower result set.

:::{image} /explore-analyze/images/kibana-learning-tutorial-esql-aggregation.png
:alt: Discover showing a STATS aggregation with HTTP response codes ranked by event count
:screenshot:
:::
:::::

:::::{step} Save the visualization to a dashboard

The aggregation query produced a chart showing event counts by response code. You can save this chart directly to a dashboard:

1. Select {icon}`save` **Save visualization** above the chart. You can also select {icon}`pencil` **Edit visualization** to open the Lens editor inline and customize the chart before saving it.
2. Enter a title, for example `Events by response code`.
3. Under **Add to dashboard**, select **New**.
4. Select **Save and go to dashboard**.

:::{image} /explore-analyze/images/kibana-learning-tutorial-save-to-dashboard.png
:alt: Save visualization dialog with "Add to dashboard" set to New
:screenshot:
:::

**Result:** {{kib}} opens a new, unsaved dashboard with your response code chart already on it.

:::{tip}
Want to show the results table on a dashboard instead of the chart? Save your Discover session (select **Save** in the toolbar), then from your dashboard, import it from the library as a new panel. This embeds the table view, including the query and any filters you applied.
:::
:::::

::::::

You've queried, filtered, aggregated, and inspected data, all within Discover using {{esql}}. You also saved a visualization to a new dashboard, which is where you're headed next. When you work with specific types of data, Discover adapts its interface accordingly. For example, it provides [specialized log exploration tools](/solutions/observability/logs/explore-logs.md) with built-in parsing and categorization when it detects log data. To learn more about Discover, refer to [Discover](discover.md). For the full {{esql}} language reference, refer to [{{esql}}](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

## Step 3: Build your dashboard [build-your-dashboard]

Now that you have a dashboard with your first panel, add more visualizations to tell a complete story about your web traffic.

::::::{stepper}

:::::{step} Save the dashboard

Before adding more panels, save your dashboard so you don't lose your work:

1. In the toolbar, select **Save**.
2. Enter a title, for example `Web logs overview`.
3. Select **Save**.
:::::

:::::{step} Add a metric panel for median response size

1. Create the visualization:

   - {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.
   - {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. Once in the Lens editor, switch the visualization type to **Metric**.
3. From the **Available fields** list on the left, drag **bytes** to the **Primary metric** area. Lens selects the **Median** aggregation automatically.
4. Select the "Median of bytes" **Primary metric** that we just added, then go to the **Appearance** section and configure the following:
   - **Name**: `Median response size`
   - **Value format**: `Bytes (1024)`
   - **Background chart** (or **Supporting visualization**): `Line`. A sparkline appears behind the number, showing how the median changes over the selected time range.
   - **Color by value** (or **Color mode**): `Dynamic`. Set three color stops: green at `0`, yellow at `6000`, and red at `10000`. With these thresholds, the panel color reflects whether the median response size is small (under 6 KB), moderate, or large (over 10 KB).

:::{image} /explore-analyze/images/kibana-learning-tutorial-metric-lens.png
:alt: Lens editor showing a metric panel with median response size, background sparkline, and dynamic coloring
:screenshot:
:::

5. Select **Close**, then select **Save and return**.


**Result:** A metric panel appears on the dashboard showing the median response size in a human-readable format (for example, 5.6 KB instead of 5,748), with a background sparkline for context.

:::::

:::::{step} Add a bar chart of requests by file extension

1. Create the visualization:

   - {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.
   - {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. Make sure the correct {{data-source}} is selected (for example, `kibana_sample_data_logs`).
3. From the **Available fields** list, drag **extension.keyword** to the workspace.

   Lens detects that this is a categorical field and creates a bar chart of its top values by count. It picks the chart type and axis configuration automatically.

:::{image} /explore-analyze/images/kibana-learning-tutorial-bar-chart-lens.png
:alt: Lens editor showing a bar chart of top values of extension.keyword by count of records
:screenshot:
:::

4. Select **Save and return**.

Add a panel title:

1. Hover over the panel and select {icon}`gear` **Settings**. The **Settings** flyout appears.
2. In the **Title** field, enter `Requests by file extension`, then select **Apply**.
:::::

:::::{step} Add a line chart of log volume over time

1. Create the visualization:

   - {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.
   - {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. Once in the Lens editor, switch the visualization type to **Line**.

3. From the **Available fields** list, drag **Records** to the workspace.

   Because the data contains a time field, Lens places **@timestamp** on the horizontal axis and **Count of Records** on the vertical axis automatically.

4. Add a reference line to give the chart visual context:
   1. Select the **Add layer** icon {icon}`plus_in_square`, then select **Reference lines**.
   2. Select the reference line value and enter `150`. This marks a "high traffic" threshold on the chart.
   3. Set the color to red, then under **Text decoration**, enter a label such as `High traffic` and select **Fill below** to shade the area under the line.
:::{image} /explore-analyze/images/kibana-learning-tutorial-line-chart-lens.png
:alt: Lens editor showing a line chart of count of records over time with a reference line
:screenshot:
:::

5. Select **Save and return**.

Add a panel title:

1. Hover over the panel and select {icon}`gear` **Settings**.
2. In the **Title** field, enter `Log volume over time`, then select **Apply**.

**Result:** Your dashboard now has four panels: the response code chart from Discover, the metric, the bar chart, and the line chart.

:::{image} /explore-analyze/images/kibana-learning-tutorial-dashboard-four-panels.png
:alt: Dashboard with a response code chart, a metric panel, a bar chart of requests by file extension, and a line chart of log volume over time
:screenshot:
:::
:::::

:::::{step} Customize a panel with inline editing

You can fine-tune any Lens panel without leaving the dashboard. Try it on the **Requests by file extension** panel:

1. Hover over the panel and select {icon}`pencil` **Edit visualization configuration**. A **Configuration** flyout opens on the right side of the panel.
2. In the flyout, select the **Horizontal axis** configuration.
3. Expand **Advanced**, then in the **Include values** field, enter `.+` and select **Use regular expression**. This regular expression matches any non-empty string, which filters out documents where the extension field is blank. The panel updates immediately to reflect the change.
4. Select **Back**, then **Apply and close**.

:::{image} /explore-analyze/images/kibana-learning-tutorial-inline-editing.png
:alt: Dashboard panel with the inline Configuration flyout open on the right
:screenshot:
:::

:::{tip}
For more advanced editing, select **Edit in Lens** in the inline editing flyout to open the full Lens editor. When you are done, select **Save and return** to go back to the dashboard.
:::
:::::

:::::{step} Try interactive filtering

Dashboard panels are interactive. Try selecting the `404` bar in the **Events by response code** chart. {{kib}} adds a filter for that value, and the other panels update to show only the matching log events. The metric, bar chart, and line chart now reflect only the 404 traffic.

To remove the filter, select the {icon}`cross` next to it in the dashboard's filter bar.

:::{tip}
If you know which dimensions your viewers will want to filter by, you can add [controls](dashboards/add-controls.md) (dropdown menus, range sliders) directly to the dashboard so they don't have to build those filters themselves.
:::
:::::

:::::{step} Arrange and save

Resize and reposition the panels to create a clear layout. Place the metric panel at the top, and arrange the charts below it. For larger dashboards, you can also group panels into [collapsible sections](dashboards/arrange-panels.md) to keep things organized.

When you are happy with the layout, select **Save** in the toolbar.
:::::

::::::

Your dashboard now combines multiple panel types (metric, bar chart, line chart) built with Lens, and you've seen how inline editing and interactive filtering make the dashboard both customizable and explorable. To learn more, refer to [Dashboards](dashboards.md), [Lens](visualize/lens.md), and [Panels and visualizations](visualize.md).

## Step 4: Share the dashboard [share-the-dashboard]

Once your dashboard is ready, share it with your team:

1. In the toolbar, select {icon}`share` **Share**.
2. [Copy the link](report-and-share.md#share-a-direct-link) and share it with your team.

Users who receive the link need to authenticate and have the appropriate privileges to access the underlying data. 

{applies_to}`serverless:` {applies_to}`stack: ga 9.3+` From the same **Share** menu, you can also set whether other users in the space can edit or only view the dashboard. Users with view-only access can still duplicate it to create their own version.

For more details on sharing options, access control, and managing dashboard ownership, refer to [Sharing dashboards](dashboards/sharing.md).

## Navigate between Discover and dashboards [navigate-between-apps]

One of {{kib}}'s strengths is how you can move between exploring raw data and visualizing it. Here are the key navigation paths:

**From Discover to a dashboard**
:   When a classic search or an {{esql}} aggregation produces a chart in Discover, select {icon}`save` **Save visualization** above the chart, then choose **Add to dashboard** to send it to an existing or new dashboard. You can also save the entire Discover session (query, filters, and selected fields) and add it to a dashboard as a table panel.

**From a dashboard panel back to Discover**
:   Open the context menu on any Lens panel and select **Explore in Discover**. {{kib}} opens Discover with the panel's query and filters already applied, so you can drill into the underlying data.

**Inline and full Lens editing from a dashboard**
:   Select {icon}`pencil` on any panel to open the inline **Configuration** flyout. For deeper changes, select **Edit in Lens** in the flyout to switch to the full editor, then **Save and return** to go back to the dashboard.

**Add a new visualization directly from a dashboard**
:   From a dashboard, select **Add** > **Visualization** to open the Lens editor, or **Add** > **ES|QL** to create a chart from an {{esql}} query without going through Discover first.

:::{tip}
This back-and-forth workflow is especially useful when investigating anomalies: spot something unusual on a dashboard, jump to Discover to examine the raw events, refine your query, then save an updated visualization back to the dashboard.
:::

## Next steps [next-steps]

You've completed the core workflow, from sample data to a shareable dashboard. Here are some directions to explore next:

**Bring in your own data**
: The same workflow applies to any data in {{es}}. Use [{{agent}}](/reference/fleet/install-elastic-agents.md) or [Beats](/reference/beats.md) to ingest your own logs, metrics, or traces. Refer to [Ingest data](/manage-data/ingest.md) for an overview of all ingestion options.

**Deepen your {{esql}} knowledge**
: {{esql}} supports advanced operations like `ENRICH`, `LOOKUP JOIN`, `DISSECT`, and `GROK`, and more to transform your data on the fly. Refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md) and [Use {{esql}} in {{kib}}](query-filter/languages/esql-kibana.md).

**Explore different types of data**
: Depending on what you monitor, you can use specialized tools:
  * **Logs**: [Explore logs in Discover](/solutions/observability/logs/explore-logs.md) with field-level filtering and log parsing.
  * **Metrics**: [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md) and the {{infrastructure-app}}.
  * **Traces**: [Get started with {{product.apm}}](/solutions/observability/apm/get-started.md) to trace requests across distributed services.

**Try more visualization techniques**
: Build richer dashboards with the following step-by-step tutorials:
  * [Dashboard with web server data](dashboards/create-dashboard-of-panels-with-web-server-data.md)
  * [Dashboard with time series eCommerce data](dashboards/create-dashboard-of-panels-with-ecommerce-data.md)

**Add geographic context**
: The sample web logs data includes `geo.src` and `geo.dest` fields. [Maps](visualize/maps.md) lets you visualize this data on interactive maps and add them to dashboards.

**Set up alerts**
: Don't wait for problems to show up on a dashboard. [Create alerting rules](alerting/alerts/alerting-getting-started.md) to get notified when your data crosses a threshold.

**Try machine learning**
: Use {{ml}} to [detect anomalies](/explore-analyze/machine-learning/anomaly-detection/ml-getting-started.md) in time-series data, forecast trends, or categorize log messages. The sample data sets include pre-configured {{anomaly-jobs}} you can experiment with.

## Related pages [related-pages]

* [Discover](discover.md)
* [Dashboards](dashboards.md)
* [Panels and visualizations](visualize.md)
* [Lens](visualize/lens.md)
* [{{esql}} in {{kib}}](query-filter/languages/esql-kibana.md)
* [Sharing dashboards](dashboards/sharing.md)
