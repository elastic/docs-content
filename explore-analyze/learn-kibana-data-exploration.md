---
navigation_title: "Learn data exploration and visualization"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/get-started.html
description: Learn Kibana's core analyst features — Discover, Lens, and Dashboards — by exploring your system logs, building visualizations, and sharing dashboards.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Learn data exploration and visualization with {{kib}} [kibana-get-started]

This tutorial introduces {{kib}}'s core analyst features — **Discover**, **Lens**, and **Dashboards** — through a hands-on scenario that mirrors a real-world workflow. You ingest your own system logs, explore them with {{esql}}, create visualizations, assemble a dashboard, and share it with your team.

This tutorial is intended for users who are new to {{kib}} or want to learn the end-to-end data exploration and visualization workflow. Basic familiarity with {{es}} concepts (indices, documents, fields) is helpful but not required. If you prefer not to install an agent, you can follow along using the [sample web logs data](index.md#gs-get-data-into-kibana) and adapt the queries.

Discover, Lens, and Dashboards are core {{kib}} features available in every solution context — Observability, Security, Search, and Elasticsearch projects — so this tutorial applies regardless of your use case.

By the end of this tutorial, you'll know how to:

* Ingest system logs from your machine into {{es}} using {{agent}}
* Explore and query data in **Discover** using {{esql}}
* Build a dashboard with multiple Lens visualizations
* Navigate between **Discover**, **Lens**, and **Dashboards** to iterate on your analysis
* Share a dashboard with your team

## Before you begin [visualize-explore-prerequisites]

* An {{stack}} deployment or {{serverless-full}} project with {{es}} and {{kib}}. Don't have one yet? [Start a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* The required privileges to complete the tutorial. Specifically:
  - **{{kib}} privileges**: `All` on **Fleet** and **Integrations** (to install the System integration — must be assigned in all spaces), and `All` on **Discover** and **Dashboard** (to explore data and create dashboards).
  - **{{es}} index privileges**: `read` and `view_index_metadata` on the `logs-system.*` indices (to query system log data in Discover).

  :::{note}
  If you just created a trial account, you are the admin of your deployment and already have all the required privileges.
  :::

## Step 1: Get your data in [get-your-data-in]

Before you can explore and visualize, you need data in {{es}}. The quickest way to collect your machine's system logs is with {{agent}} and the **System** integration, which captures syslog events, authentication logs, and system metrics out of the box.

Follow the steps in [Get started with system logs](/solutions/observability/logs/get-started-with-system-logs.md) to install {{agent}} and start collecting data.

Once the agent is running, your logs are indexed into `logs-system.syslog-*` (and related data streams like `logs-system.auth-*`). Give it a few minutes to accumulate some data before moving on.

:::{tip}
If you don't want to install an agent right now, [add the sample web logs data](index.md#gs-get-data-into-kibana) instead. Replace the `FROM logs-system.syslog*` queries in this tutorial with `FROM kibana_sample_data_logs` and adjust field names accordingly.
:::

## Step 2: Explore data in Discover with {{esql}} [explore-data-in-discover]

**Discover** is the starting point for data exploration. You can search, filter, and visualize your data interactively. In this tutorial, you use {{esql}}, Elastic's piped query language, which lets you query data directly without needing a {{data-source}}.

::::::{stepper}

:::::{step} Open Discover and switch to {{esql}}

1. From the navigation menu, go to **Discover**.
2. Select {icon}`editorCodeBlock` **{{esql}}** from the application menu.

**Result:** The query bar changes to an {{esql}} editor where you can write piped queries.
:::::

:::::{step} Run your first query

Enter the following query, then select {icon}`playFilled` **Run**:

```esql
FROM logs-system.syslog* <1>
| KEEP @timestamp, host.hostname, process.name, message <2>
| SORT @timestamp DESC <3>
| LIMIT 50 <4>
```

1. Reads from all syslog data streams matching this pattern.
2. Retains only these four fields in the output, discarding everything else.
3. Orders results by timestamp, most recent first.
4. Returns only the first 50 rows.

**Result:** The results table displays the most recent syslog entries with only the fields you selected. The histogram above the table updates automatically to show the distribution of events over time.

<!-- TODO: Screenshot of Discover in ES|QL mode showing the query, results table with the four fields, and the histogram above. This is the first checkpoint — helps users confirm they're in the right place. -->
:::{image} /explore-analyze/images/tutorial-esql-first-query.png
:alt: Discover showing an ES|QL query with results table and histogram
:screenshot:
:::

:::{tip}
Not sure which fields are available? Start with `FROM logs-system.syslog* | LIMIT 10` and look at the field list in the sidebar.
:::
:::::

:::::{step} Filter and aggregate

Refine your exploration with `WHERE` to filter and `STATS` to aggregate:

```esql
FROM logs-system.syslog*
| WHERE process.name IS NOT NULL <1>
| STATS event_count = COUNT(*) BY process.name <2>
| SORT event_count DESC <3>
| LIMIT 15
```

1. Excludes rows where the process name is missing.
2. Groups rows by process name and counts events in each group.
3. Puts the most active processes at the top.

**Result:** The table shows the top 15 processes generating syslog events. The visualization updates to reflect the aggregation, so you can see at a glance which processes are the most active.

<!-- TODO: Screenshot of Discover showing the STATS aggregation result — the table with process names and counts, and the bar chart visualization above. Shows the value of ES|QL aggregation at a glance. -->
:::{image} /explore-analyze/images/tutorial-esql-aggregation.png
:alt: Discover showing a STATS aggregation with process names ranked by event count
:screenshot:
:::
:::::

:::::{step} Save a visualization to a dashboard

The histogram at the top of Discover is a Lens visualization that you can save directly to a dashboard:

1. Select {icon}`save` **Save visualization** above the chart.
2. Enter a title, for example `Syslog volume over time`.
3. Under **Add to dashboard**, select **New**.
4. Select **Save and go to dashboard**.

<!-- TODO: Screenshot or GIF of the "Save visualization" dialog, showing the title field, the "Add to dashboard" dropdown set to "New", and the "Save and go to dashboard" button. Key navigation moment — shows how Discover flows into Dashboards. -->
:::{image} /explore-analyze/images/tutorial-save-to-dashboard.png
:alt: Save visualization dialog with "Add to dashboard" set to New
:screenshot:
:::

**Result:** {{kib}} opens a new, unsaved dashboard with your visualization already on it.

:::{note}
You can also select {icon}`pencil` **Edit visualization** to open the Lens editor inline and customize the chart before saving it.
:::
:::::

::::::

## Step 3: Build your dashboard [build-your-dashboard]

Now that you have a dashboard with your first panel, add more visualizations to tell a complete story about your system activity.

::::::{stepper}

:::::{step} Save the dashboard

Before adding more panels, save your dashboard so you don't lose your work:

1. In the toolbar, select **Save**.
2. Enter a title, for example `System logs overview`.
3. Select **Save**.
:::::

:::::{step} Add a metric panel for total log count

1. {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.

   {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. In the Lens editor, open the **Visualization type** dropdown and select **Metric**.
3. From the **Available fields** list on the left, drag **Records** to the **Primary metric** area.
4. Select **Primary metric**, go to **Appearance**, and in the **Name** field, enter `Total log events`. Select **Close**.
5. Select **Save and return**.

**Result:** A metric panel showing the total number of log events appears on the dashboard.
:::::

:::::{step} Add a bar chart of events by process

1. {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.

   {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. Make sure the correct {{data-source}} is selected (for example, `logs-*`).
3. From the **Available fields** list, drag **process.name** to the workspace.

   The editor creates a bar chart showing the **Top values of process.name** by **Count of records**.

4. Select **Save and return**.

Add a panel title:

1. Hover over the panel and select {icon}`gear` **Settings**. The **Settings** flyout appears.
2. In the **Title** field, enter `Events by process`, then select **Apply**.
:::::

:::::{step} Add a line chart of log volume over time

1. {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **Visualization** in the toolbar.

   {applies_to}`stack: ga 9.0-9.1` Select **Create visualization**.

2. From the **Available fields** list, drag **Records** to the workspace.

   The editor creates a bar chart with **@timestamp** on the horizontal axis and **Count of Records** on the vertical axis.

3. In the layer pane, open the **Layer visualization type** menu and select **Line**.
4. Select **Save and return**.

Add a panel title:

1. Hover over the panel and select {icon}`gear` **Settings**.
2. In the **Title** field, enter `Log volume over time`, then select **Apply**.

**Result:** Your dashboard now has three panels: a metric, a bar chart, and a line chart.

<!-- TODO: Screenshot of the dashboard with all three panels visible — metric at the top, bar chart and line chart below. This is the main payoff of the tutorial and helps users confirm their layout is on track. -->
:::{image} /explore-analyze/images/tutorial-dashboard-three-panels.png
:alt: Dashboard with a metric panel, a bar chart of events by process, and a line chart of log volume over time
:screenshot:
:::
:::::

:::::{step} Customize a panel with inline editing

You can fine-tune any Lens panel without leaving the dashboard:

1. Hover over the **Events by process** panel and select {icon}`pencil` **Edit**.
2. A **Configuration** flyout opens on the right side of the panel. Use it to adjust the chart type, axes, breakdown, and colors.
3. When you finish making changes, select **Apply and close**.

<!-- TODO: Screenshot or GIF of the inline editing flyout open on a panel, showing the Configuration options on the right. Helps users recognize the flyout and discover what can be changed without leaving the dashboard. -->
:::{image} /explore-analyze/images/tutorial-inline-editing.png
:alt: Dashboard panel with the inline Configuration flyout open on the right
:screenshot:
:::

:::{tip}
For more advanced editing, select **Edit in Lens** in the flyout to open the full Lens editor. When you are done, select **Save and return** to go back to the dashboard.
:::
:::::

:::::{step} Arrange and save

Resize and reposition the panels to create a clear layout. Place the metric panel at the top, and arrange the charts below it.

When you are happy with the layout, select **Save** in the toolbar.
:::::

::::::

## Step 4: Share the dashboard [share-the-dashboard]

Once your dashboard is ready, share it with your team:

1. In the toolbar, select {icon}`share` **Share**.
2. Select a sharing option:
   * **Link**: Copy a short or snapshot URL to share with colleagues who have access to {{kib}}.
   * **Embed**: Generate an iframe code to embed the dashboard in a web page or wiki.
   * **Export**: Download the dashboard as an NDJSON file to import into another {{kib}} environment.

For more details on sharing options, access control, and managing dashboard ownership, refer to [Sharing dashboards](dashboards/sharing.md).

## Navigate between Discover and dashboards [navigate-between-apps]

One of {{kib}}'s strengths is how you can move between exploring raw data and visualizing it. Here are the key navigation paths:

**From Discover to a dashboard**
: In Discover, select {icon}`save` **Save visualization** above the histogram chart, then select **Add to dashboard** to send the chart to an existing or new dashboard.

**From a dashboard panel back to Discover**
: Open the context menu on any Lens panel and select **Explore in Discover**. {{kib}} opens Discover with the underlying data and filters of that panel already applied, so you can drill into the details.

**Inline and full Lens editing from a dashboard**
: Select {icon}`pencil` on any panel to open the inline **Configuration** flyout. For deeper changes, select **Edit in Lens** to switch to the full editor, then **Save and return** to go back to the dashboard.

:::{tip}
This back-and-forth workflow is especially powerful when investigating anomalies: spot something unusual on a dashboard, jump to Discover to examine the raw events, refine your query, then save an updated visualization back to the dashboard.
:::

## Next steps [next-steps]

You've completed the core workflow — from raw data to a shareable dashboard. Here are some directions to explore next:

**Deepen your {{esql}} skills**
: {{esql}} supports advanced operations like `ENRICH`, `LOOKUP JOIN`, `DISSECT`, and `GROK` to transform your data on the fly. Refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md) and [Use {{esql}} in {{kib}}](query-filter/languages/esql-kibana.md).

**Explore different types of data**
: The same workflow applies to any data in {{es}}. Depending on what you monitor, you can use specialized tools:
  * **Logs**: [Explore logs in Discover](/solutions/observability/logs/explore-logs.md) with field-level filtering and log parsing.
  * **Metrics**: [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md) and the {{infrastructure-app}}.
  * **Traces**: [Get started with {{product.apm}}](/solutions/observability/apm/get-started.md) to trace requests across distributed services.

**Try more visualization techniques**
: Build richer dashboards with the step-by-step tutorials:
  * [Dashboard with web server data](dashboards/create-dashboard-of-panels-with-web-server-data.md)
  * [Dashboard with time series eCommerce data](dashboards/create-dashboard-of-panels-with-ecommerce-data.md)

**Add geographic context**
: If your data includes location fields, [Maps](visualize/maps.md) lets you visualize data on interactive maps and add them to dashboards.

**Set up alerts**
: Don't wait for problems to show up on a dashboard — [create alerting rules](alerting/alerts/alerting-getting-started.md) to get notified when your data crosses a threshold.

## Related pages [related-pages]

* [Discover](discover.md)
* [Dashboards](dashboards.md)
* [Panels and visualizations](visualize.md)
* [Lens](visualize/lens.md)
* [{{esql}} in {{kib}}](query-filter/languages/esql-kibana.md)
* [Sharing dashboards](dashboards/sharing.md)
