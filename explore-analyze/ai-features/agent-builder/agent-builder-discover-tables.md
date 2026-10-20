---
navigation_title: "Discover tables"
description: "Show matching documents, events, or logs in an interactive Discover table in Agent Builder chat. Inspect documents, open the results in Discover, or save the table to a dashboard."
applies_to:
  stack: experimental 9.6+
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Discover tables in {{agent-builder}} chat

When you ask an agent to show matching documents, events, or logs, it can display them in an interactive **Discover** table in the conversation. Without leaving the chat, you can inspect individual documents, change the time range, open the results in **Discover**, or save the table to a dashboard.

The built-in [`discover-session`](builtin-skills-reference.md#agent-builder-discover-session-skill) skill powers this feature. Requests for charts, metrics, trends, or aggregated summaries produce a [Lens visualization](agent-builder-dashboards-and-visualizations.md) instead.

## Before you begin

- Turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional). The `discover-session` skill is hidden until you do. You don't need this setting when you [start from **Discover**](#discover-tables-from-discover).
- Use the default Elastic AI Agent, or a custom agent that has either [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) turned on or the `discover-session` skill assigned.
- To open the table in **Discover**, you need the **Read** or **All** privilege for **Discover**.
- To save the table to a dashboard, you need the **All** privilege for **Dashboard**.

## Ask for documents

Describe the documents you want to see. The agent writes an {{esql}} query and shows the results in a **Discover** table in the conversation. For example:

```text
Show me error and warning logs from logs-* for the last hour in a Discover table in this chat.
```

**Discover** tables support {{esql}} queries only, and the agent can't use aggregating queries, such as queries with `STATS` or `PROMQL`, for a table. To see aggregated results, ask for a chart instead. For example, `Chart error logs over time` produces a Lens visualization.

## Start from Discover [discover-tables-from-discover]

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` If you start the conversation from **Discover** in {{esql}} mode, the [`discover-data-analysis`](builtin-skills-reference.md#agent-builder-discover-data-analysis-skill) skill can also show the current documents in a **Discover** table, even when the `agentBuilder:experimentalFeatures` setting is off. For details on starting a conversation from **Discover**, refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai).

## Work with the table

The table works like a compact version of the **Discover** document table:

- **Context-aware columns and cells**: When your data matches a [context-aware experience](/explore-analyze/discover/discover-get-started.md#context-aware-discover), the table uses its columns, cell rendering, row indicators, and document views. The experience depends on the solution view or project type you're chatting from. For example, when you chat from an {{observability}} solution view or project, [logs data](/solutions/observability/logs/discover-logs.md) shows log-level badges, severity row indicators, the **Summary** column, and the **Log overview** document view.
- **Local time range**: The table has its own time picker. Changing it updates only this table, not the global {{kib}} time range. If you don't ask for a specific time range, the table uses the time range of the page you're chatting from. If that page has no time range, the table uses the last 24 hours.
- **Document details**: Select {icon}`maximize` **View details** on a row to open the document in a flyout over the conversation.
- **Columns**: Select **Columns** in the table toolbar to change which columns appear. Your column changes carry over when you open the table in **Discover** or save it to a dashboard.
- **Horizontal scrolling**: Scroll sideways to see more columns in the narrow chat area.

The following example shows a **Discover** table of error and warning logs in a conversation:

:::{image} images/agent-builder-discover-table-inline.png
:screenshot:
:alt: Discover table of error and warning logs in an Agent Builder conversation, with the Open in Discover button, a Last 1 hour time picker, the Columns selector, and a Summary column showing service and host badges
:::

The following example shows the document flyout for a log document:

:::{image} images/agent-builder-discover-table-flyout.png
:screenshot:
:alt: Document flyout over the conversation showing the Log overview tab with the log message, an error badge, service name, host name, and stream
:::

## Refine the table with follow-up prompts

Send a follow-up message to change the table. For example, after asking for error and warning logs from the last hour, ask for `only errors from the last 15 minutes`. The agent updates the existing table instead of creating a new one.

To keep the first table and add another, ask for a new table. If the conversation contains more than one table and your request is unclear, the agent asks which one to update.

## Open the table in Discover

Select **Open in Discover** to continue working in **Discover**. The results open in a new [**Discover** tab](/explore-analyze/discover/discover-get-started.md#run-multiple-explorations-with-tabs) with the same {{esql}} query, time range, columns, and sort order as the table.

This button appears only if you have the **Read** or **All** privilege for **Discover**.

## Save the table to a dashboard

Add the table to a new or existing dashboard as a panel. This works like [saving a table to a dashboard from Discover](/explore-analyze/discover/save-open-search.md#save-table-to-dashboard).

1. In the table toolbar, select {icon}`add_to_dashboard` **Save table to dashboard**. The **Save Discover session** dialog opens.
2. Edit the pre-filled title for the panel if needed, and optionally add a description.
3. In **Add to dashboard**, select **Existing** and then select a dashboard from the list, or select **New** to create one.
4. Select **Save and go to dashboard**. The dashboard opens in edit mode with the table added as a panel.
5. Save the dashboard to keep the panel.

The panel stores the query and your visible columns with the dashboard. It uses the dashboard's time range, not the table's. Despite the dialog title, the table isn't saved as a separate **Discover** session.

If you don't have the **All** privilege for **Dashboard**, **Save table to dashboard** is disabled.

## Limitations

**Discover** tables in chat have the following limitations:

- You can't save a table as a **Discover** session, or attach an existing **Discover** session to the conversation.
- Tables support {{esql}} only. [KQL](/explore-analyze/query-filter/languages/kql.md) queries and **Discover** sessions saved in [classic mode](/explore-analyze/discover/switch-esql-mode.md) aren't supported.
- Tables don't have a filter bar.
- The agent can't add **Discover** tables to the dashboards it creates. You can still save a table to a dashboard yourself.

## Related pages

- [Discover](/explore-analyze/discover.md)
- [Dashboards and visualizations in chat](agent-builder-dashboards-and-visualizations.md)
- [Chat with {{agent-builder}} agents](chat.md)
- [Built-in skills reference](builtin-skills-reference.md)
