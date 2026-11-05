---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
navigation_title: How Discover works
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: See what Discover shows by default, how you define the data to explore, and how query modes, context-aware experiences, and sharing fit in.
---

# How Discover works [discover-get-started]

When you need to look at the documents in your data, find out why something happened, or check that data arrived as expected, **Discover** is where you start. You query your data, and **Discover** shows the results as a table and, when the data allows it, as a chart.

If you're new to **Discover**, this page introduces its core concepts. When you're ready to get hands-on, check the [next steps](#next-steps) at the end of this page for a tutorial and guides for each task.

To open **Discover**, find it in the navigation menu or use the [global search field](../find-and-organize/find-apps-and-objects.md).

## What you see in Discover [discover-screen]

:::{image} /explore-analyze/images/kibana-discover-overview.png
:alt: Discover in ES|QL mode with two tabs, a query on the sample web logs, the fields list, a chart of results over time, the results table with a search term highlighted, and the document flyout open
:screenshot:
:::

Whatever you explore in **Discover** comes from three things: the data, a query, and a time range. Together they make a session, which you can save and reopen later. This is the default view, and you can [customize it](document-explorer.md) to fit your work. The elements that show can also change automatically, based on your context and the data you search. Refer to [Context-aware experiences](#context-aware-discover).

Tabs
:   {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` A single session can have several tabs, each with its own exploration, such as a different query and time range. Refer to [Run multiple explorations with tabs](work-with-tabs.md).

Search bar and query editor
:   The top of **Discover** is where you define the data to explore. You write your query there and set the time range. **Discover** offers [two query modes](#query-modes) for exploring your data.

Fields list
:   Lists the fields of your data. Select a field to see its most frequent values.

Chart
:   Shows how the results spread over the time range, when your data has a time field. Some queries, such as ones that summarize your results, change what the chart shows.

Results table
:   Lists the results, one row for each document.

Document flyout
:   When you need to focus on a specific row of the table, open it. A panel opens beside the table and shows every field of that document. Refer to [Look inside a document](inspect-documents.md#look-inside-a-document).

## Query modes in Discover [query-modes]

**Discover** has two ways to define the data you explore, called query modes. You can [switch between them](switch-esql-mode.md) at any time.

- [{{esql}} mode](use-esql.md): You write a query in [{{esql}}](elasticsearch://reference/query-languages/esql.md), the {{es}} query language. The query names the data to explore and can also filter it, calculate new fields, and summarize it. For example, `FROM kibana_sample_data_logs | WHERE bytes > 5000` returns the entries in the sample web logs that transferred more than 5,000 bytes.
- [Classic mode](use-classic-mode.md): You select a [data view](../find-and-organize/data-views.md), which is a saved definition of the data to query, such as all your web logs. You then search it with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two search syntaxes, and narrow the results with filters.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Each tab keeps its own query, so one tab can run an {{esql}} query while another uses classic mode.

## Context-aware experiences [context-aware-discover]

**Discover** provides tailored interfaces and features for the following data types when accessed from Observability or Security project types or {{kib}} solution views:

* Observability:
  * **[Logs exploration](/solutions/observability/logs/discover-logs.md)**
  * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` **[Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md)**
  * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` **[Traces exploration](/solutions/observability/apm/discover-traces.md)**
* Security:
  * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1` **[Security data exploration](/solutions/security/investigate/discover-security.md)**

This context-aware experience is determined by both your solution context and the type of data you query. When both conditions align, **Discover** provides specific capabilities useful for exploring that specific type of data, and integrates features or paths to other relevant solution applications.

When you access **Discover** outside of a specific solution context, or when working with data types that don't have specialized experiences, you get the default **Discover** interface with all its core functionality for general-purpose data exploration.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.5` The active profile also shapes [AI-powered deep analysis](analyze-discover-data-with-ai.md): when you query logs, metrics, or traces from the matching solution context, the agent receives domain-specific guidance on which fields to group by and which {{esql}} commands to use. For example, it uses the `TS` command for time series metrics.

### Context-awareness with multiple data types

Your query can include multiple data types that each have tailored experiences. For example, you might query both `logs-*` and `traces-*` indices within an Observability context.

In this case **Discover** provides the default experience until it detects that you're interacting with a single type of data. For example, when you [look inside a document](inspect-documents.md#look-inside-a-document).

To check which experience is active, refer to [Check which context-aware experience is active](inspect-documents.md#view-active-context-aware-experience).

## Save, share, and export what you find [discover-save-share]

When a session gets you the answer, you have several ways to keep it, share it, or take it somewhere else:

- [Save the session](save-open-search.md#_save_a_discover_session) to reuse its query, filters, and view later.
- [Add the chart, the table, or the whole session to a dashboard](save-open-search.md#_add_search_results_to_a_dashboard) to keep it next to your other panels.
- [Open Discover from a dashboard panel](../dashboards/create-discover-drilldown.md) with a drilldown to read the documents behind a value you select.
- [Open a field in a visualization](visualize-field.md) from the fields list, in classic mode.
- [Copy a link](copy-and-share-documents.md#share-your-findings) to a session or to a single document, so that others can open the same view.
- [Copy rows](copy-and-share-documents.md#copy-row-content) as text, JSON, or Markdown.
- Export the results of a session as [CSV](save-open-search.md#export-discover-session-csv) or [JSON](save-open-search.md#export-discover-session-json).
- [Create an alert rule](generate-alerts-from-discover.md) from your query to keep an eye on it.

## Troubleshooting

If **Discover** asks you to add data or create a data view, refer to [Discover or Dashboards asks you to add data or create a data view](/troubleshoot/kibana/discover-dashboards-no-data-screen.md). If fields show as empty when they shouldn't, refer to [Some fields show as empty in Discover](/troubleshoot/kibana/discover-empty-fields.md).

## Next steps [next-steps]

- [Get started with {{esql}} in Discover](try-esql.md): Build your first query step by step.
- [What you can do with Discover](../discover.md#what-you-can-do): Find the guide for what you want to do, from querying and shaping results to saving and sharing them.
