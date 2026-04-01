---
applies_to:
  stack: preview 9.4
navigation_title: Query activity
description: Monitor and manage long-running queries in your Elasticsearch cluster using the Query activity page in Kibana.
products:
  - id: kibana
  - id: elasticsearch
---

# Query activity

The **Query activity** page in {{kib}} provides real-time visibility into queries currently running in your {{es}} cluster.
Use it to identify long-running or resource-intensive queries, inspect their details, trace them back to their source, and cancel them when needed.

Query activity surfaces search tasks from all query languages, including ES|QL, DSL, EQL, SQL, and multi-search requests.

:::{image} /deploy-manage/images/query-activity.png
:alt: The Query activity page showing a list of running queries with their task ID, query type, source, start time, and run time
:screenshot:
:::

## Prerequisites

To use the **Query activity** page, you need the following privileges:

| Action | Required {{es}} cluster privilege | Required {{kib}} privilege |
| --- | --- | --- |
| View running queries | `monitor` | **Query activity** read access |
| Cancel a query | `manage` | **Query activity** all access |

If you don't have the required privileges, the page displays a message asking you to contact your administrator.

## Access query activity

To open **Query activity**, go to **{{stack-manage-app}} → Cluster performance → Query activity**.

## View running queries

The **Query activity** page lists all in-flight search tasks in your cluster.
The list does not auto-refresh. Select **Refresh** to update the data. The time of the last refresh is displayed next to the button.

The table displays the following columns:

**Task ID**
:   The unique identifier for the {{es}} task. Select the task ID to open the [query details flyout](#inspect-query-details).

**Query type**
:   The query language used: ES|QL, DSL, EQL, SQL, MSearch, Async search, or Other.

**Source**
:   The {{kib}} saved object that originated the query, such as a dashboard or a Discover session.
    Select the source link to open the originating saved object in a new tab.
    If the source can't be determined, *Not available* is displayed.
    For more information about tracing queries, refer to [Trace an Elasticsearch query to its origin in Kibana](docs-content://troubleshoot/kibana/trace-elasticsearch-query-to-the-origin-in-kibana.md).

**Start time**
:   The timestamp when the query started running.

**Run time**
:   How long the query has been running.

**Actions**
:   A cancel button to request cancellation of the query. This button is only available if you have the required privileges.

### Filter the query list

You can narrow down the list of running queries using several filters:

- **Search bar**: Enter any text to match against table contents, including task IDs.
- **Run time**: Set a minimum run time threshold to surface only queries that have been running longer than a specific duration.
- **Query type**: Filter by one or more query languages (ES|QL, DSL, EQL, SQL, and others).
- **Source**: Filter by one or more originating {{kib}} applications (Discover, Dashboard, and others).

## Inspect query details

Select a task ID from the table to open the **Query details** flyout.
The flyout provides detailed information about the selected query:

% TODO: replace with a final screenshot before GA
:::{image} /deploy-manage/images/query-activity-flyout.png
:alt: The query details flyout showing the task ID, query type, start time, runtime, indices count, trace ID, source, and full query text
:screenshot:
:width: 66%
:::

- **Task ID** and **query type** badge
- **Start time** and **Run time**
- **Indices**: the number of indices the query targets
- **Trace ID**: when available, a link that opens Discover with the `trace.id` pre-filtered around the query start time
- **Source**: a link to the originating {{kib}} saved object
- **Query**: the full query text, displayed in a syntax-highlighted code block
- **Opaque ID**: the `X-Opaque-Id` header value, when present

Use the navigation controls at the top of the flyout to browse through queries without returning to the list.

## Cancel a query

You can cancel a running query from the table or from the query details flyout.

1. Select the cancel icon in the **Actions** column, or select **Cancel query** in the flyout footer.
2. In the confirmation dialog, select **Confirm** to proceed.

    :::{warning}
    Canceling a query is irreversible. The query stops running and any partial results are discarded.
    :::

3. After confirmation, the UI displays a "Cancelling the query..." status until {{es}} confirms the task has stopped.

A toast notification confirms when the cancel request has been submitted.

## Configure the minimum running time

By default, the **Query activity** page only displays queries that have been running for longer than 100 milliseconds.
This filters out fast-completing queries so you can focus on the ones that are most likely to affect cluster performance.

To change this threshold:

1. Go to **{{stack-manage-app}} → Advanced Settings**.
2. Search for `running_queries:minRunningTime`.
3. Enter a new value in milliseconds.
4. Select **Save changes**.
