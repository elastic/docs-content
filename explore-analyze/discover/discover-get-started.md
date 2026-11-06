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

If you're new to **Discover**, the rest of this page shows what's on screen, how you select your data, and how to keep what you find. To try it hands-on, follow [Get started with {{esql}} in Discover](try-esql.md).

To open **Discover**, find it in the navigation menu or use the [global search field](../find-and-organize/find-apps-and-objects.md). You can also arrive in **Discover** with a query already set, from a [dashboard panel](../dashboards/using.md#explore-panel-data-in-discover) or from a [link that someone shared](copy-and-share-documents.md#share-your-findings).

## What you see in Discover [discover-screen]

:::{image} /explore-analyze/images/kibana-discover-overview.png
:alt: Discover in ES|QL mode with two tabs, a query on the sample web logs, the fields list, a chart of results over time, the results table with a search term highlighted, and the document flyout open
:screenshot:
:::

In **Discover**, the data, a query, and a time range make up a session. You can save a session and reopen it later. The time range is stored only if you turn on **Store time with Discover session** when you save. The screen shows the following parts. You can [customize them](document-explorer.md) to fit your work, and some change automatically for certain kinds of data. Refer to [Context-aware experiences](#context-aware-discover).

Tabs
:   {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` A single session can have several tabs, each with its own exploration, such as a different query and time range. Refer to [Run multiple explorations with tabs](work-with-tabs.md).

Query editor or search bar and time range
:   The top of **Discover** is where you define the data to explore and set the time range. In {{esql}} mode, you write your query in the editor. In classic mode, you select a data view, then search it with the search bar. Refer to the [two query modes](#query-modes).

Fields list
:   Shows the fields of your data. Select a field to see its details. In classic mode, they include the field's most frequent values.

Chart
:   Shows how the results spread over the time range, when your data has a time field. Some queries, such as ones that summarize your results, change what the chart shows.

Results table
:   Shows the results, one row for each document. In {{esql}} mode, a row is a result row, so a query that summarizes your data returns one row for each summary.

Document flyout
:   When you need to focus on one result, select {icon}`maximize` **View details** on its row. A panel opens beside the table and shows the fields of that document. In {{esql}} mode, it shows the columns that your query returned. Refer to [Look inside a document](inspect-documents.md#look-inside-a-document).

## Query modes in Discover [query-modes]

**Discover** has two ways to define the data you explore, called query modes. You can [switch between them](switch-esql-mode.md) at any time.

- [{{esql}} mode](use-esql.md): You write a query in [{{esql}}](elasticsearch://reference/query-languages/esql.md), the {{es}} query language. The query names the data to explore and can also filter it, calculate new fields, and summarize it. For example, `FROM kibana_sample_data_logs | WHERE bytes > 5000` returns the entries in the {{kib}} sample web logs that transferred more than 5,000 bytes.
- [Classic mode](use-classic-mode.md): You select a [data view](../find-and-organize/data-views.md), which is a definition of the data to query, usually saved, such as all your web logs. You then search it with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two search syntaxes, and narrow the results with filters.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Each tab keeps its own query, so one tab can run an {{esql}} query while another uses classic mode.

:::{tip} - Not sure which mode to start with? We recommend {{esql}}
{{esql}} mode lets you query your data sources directly, with optimized support for time series data through the [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) and [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) commands. You can also transform the data right from the query, for example with the [`EVAL`](elasticsearch://reference/query-languages/esql/commands/eval.md) or [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) commands. You don't need to set up a data view or a runtime field first. To try it, follow [Get started with {{esql}} in Discover](try-esql.md).
:::

## Context-aware experiences [context-aware-discover]

**Discover** adapts to the kind of data you explore. When it recognizes your data, it switches to a tailored experience, with columns, charts, and document details that suit that data. For example, log data opens with log-specific columns and details, and security alerts get color-coded row indicators. This is called a context-aware experience.

Which experiences you can get depends on where you open **Discover** from, and then on the data you query.

**In {{observability}} projects and [solution views](/deploy-manage/manage-spaces.md)**, **Discover** automatically switches to one of these experiences, depending on the data you query:

* [Logs exploration](/solutions/observability/logs/discover-logs.md): Explore log data.
* [Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md): Explore metrics data that you query in {{esql}} mode with the `TS` command.
* [Traces exploration](/solutions/observability/apm/discover-traces.md): Explore trace data.

**In Security projects and [solution views](/deploy-manage/manage-spaces.md)**, **Discover** automatically switches to one of these experiences, depending on the data you query:

* [Security data exploration](/solutions/security/investigate/discover-security.md): Explore security alerts and events.
* [Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md): Explore metrics data that you query in {{esql}} mode with the `TS` command.

{applies_to}`stack: ga 9.6+` **In spaces with the Classic [solution view](/deploy-manage/manage-spaces.md)**, the metrics, traces, and Security experiences can also apply when you query matching data. The experiences apply as long as the **Contextual profiles in Classic navigation** advanced setting is on, which it is by default. In that setting, "profiles" means context-aware experiences.

When you open **Discover** outside of these contexts, or query data without a tailored experience, you get the default **Discover** experience with all its core functionality for general-purpose data exploration.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` The active experience also shapes [AI-powered analysis](analyze-discover-data-with-ai.md): when you query logs, metrics, or traces, the AI agent receives guidance that suits that type of data. For what changes for each type, refer to [How the analysis adapts to your data](analyze-discover-data-with-ai.md#context-aware-deep-analysis).

### When you query several kinds of data [view-active-context-aware-experience]

Your query can include several kinds of data that each have a tailored experience. For example, you might query both `logs-*` and `traces-*` indices within an {{observability}} context.

In this case **Discover** provides the default experience until it detects that you're interacting with a single kind of data. For example, when you [look inside a document](inspect-documents.md#look-inside-a-document).

To check which experience is active, open the Inspector and select **Profiles** from the **View** menu. The **Profiles** view lists the solution view and the type of data that Discover detected. Together, they determine the experience. To open the Inspector, refer to [Inspect the request behind your results](inspect-documents.md#inspect-discover-request).

## Save, share, and export what you find [discover-save-share]

When a session gets you the answer, you have several ways to keep it, share it, or take it somewhere else:

- [Save the session](save-open-search.md#_save_a_discover_session) to reuse its query, filters, and view later.
- [Add the chart, the table, or the whole session to a dashboard](use-sessions-in-dashboards.md) to keep it next to your other panels.
- [Copy a link](copy-and-share-documents.md#share-your-findings) to a session or to a single document, so that others can open the same view.
- [Copy rows](copy-and-share-documents.md#copy-row-content) as text, JSON, or Markdown.
- Export the results of a session as [CSV](export-discover-session.md#export-discover-session-csv) or [JSON](export-discover-session.md#export-discover-session-json).
- [Create an alert rule](generate-alerts-from-discover.md) from your query to keep an eye on it.

## Troubleshooting

If **Discover** asks you to add data or create a data view, refer to [Discover or Dashboards asks you to add data or create a data view](/troubleshoot/kibana/discover-dashboards-no-data-screen.md). If fields show as empty when they shouldn't, refer to [Some fields show as empty in Discover](/troubleshoot/kibana/discover-empty-fields.md).

## Next steps [next-steps]

- [Get started with {{esql}} in Discover](try-esql.md): Build your first query step by step.
- [What you can do with Discover](../discover.md#what-you-can-do): Find what you want to do, from querying and shaping results to saving and sharing them.
