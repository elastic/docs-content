---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
navigation_title: Introduction
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Understand how Discover works, from what a session combines and what each part of the screen does to query modes, tabs, and context-aware experiences.
---

# Introduction to Discover [discover-get-started]

When you need to look at the documents in your data, find out why something happened, or check that data arrived as expected, **Discover** is where you start. This page explains how **Discover** works, so that the guides for individual tasks make sense whether you're new to **Discover** or you've landed in a mode you didn't expect. To learn by running a first query, follow [Get started with {{esql}} in Discover](try-esql.md). To go straight to the guide for a task, refer to [What you can do with Discover](../discover.md#what-you-can-do).

To open **Discover**, find it in the navigation menu or use the [global search field](../find-and-organize/find-apps-and-objects.md).

## What you see in Discover [discover-screen]

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: Discover in ES|QL mode, with a query on the sample web logs, a chart of the results over time, the fields list, and the results table
:screenshot:
:::

A **Discover** session combines data, a query, and a time range. The chart and the table show what that combination returns, and you can refine each part as you explore.

Query bar or editor
:   Where you write the query. In {{esql}} mode, it is an editor, and the query defines the data. In classic mode, you select a data view and write a Kibana Query Language (KQL) or Lucene query.

Time filter
:   Keeps only the results in the time range you select.

Fields list
:   Lists the fields of your data. Select a field to see its most frequent values.

Chart
:   By default, shows how the results spread over the time range.

Results table
:   Lists the results. The table is named **Results** in {{esql}} mode and **Documents** in classic mode.

## Two query modes [query-modes]

**Discover** has two query modes, and you can [switch between them](switch-esql-mode.md) at any time:

- {{esql}} mode: You write a query that defines the data, so you don't need a data view. The query can also filter, transform, and group results.
- Classic mode: You select a [data view](../find-and-organize/data-views.md), search with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), and add filters.

The mode that **Discover** opens in by default depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Discover** opens in {{esql}} mode.
- {applies_to}`stack: ga 9.0-9.5` **Discover** opens in classic mode.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` After you switch modes, **Discover** remembers the last mode you used in your browser and opens new tabs and sessions in that mode.

The steps for a task can differ between the two modes, and a few tasks work in only one. The guide for each task says which mode it covers. For the tasks that belong to a mode, refer to [Use Discover with {{esql}}](use-esql.md) and [Use Discover in classic mode](use-classic-mode.md). To see what happens to your query when you switch, refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md).

## Several explorations at once [discover-tabs]

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Tabs let you follow one line of investigation without losing another. Each tab keeps its own query, time range, filters, and columns. To open, duplicate, and reorder tabs, refer to [Run multiple explorations with tabs](work-with-tabs.md).

## Keeping and sharing what you find [discover-save-share]

When a session gets you the answer, you can [save it](save-open-search.md) to reuse its query, filters, and view later, including on a dashboard. You can also [copy results or send a link](copy-and-share-documents.md) to share what you found, or [create an alert rule](generate-alerts-from-discover.md) from your query to keep an eye on it.

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

## Troubleshooting

If **Discover** asks you to add data or create a data view, refer to [Discover or Dashboards asks you to add data or create a data view](/troubleshoot/kibana/discover-dashboards-no-data-screen.md). If fields show as empty when they shouldn't, refer to [Some fields show as empty in Discover](/troubleshoot/kibana/discover-empty-fields.md).
