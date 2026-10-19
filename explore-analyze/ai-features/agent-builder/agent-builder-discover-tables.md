---
navigation_title: "Discover tables"
description: "Ask an Agent Builder agent to show matching documents, events, or logs in an interactive Discover table directly in the chat."
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

When you ask an agent to show matching documents, events, or logs, it can display them in an interactive **Discover** table directly in the conversation. You can inspect individual documents, change the time range, open the results in **Discover**, or save the table to a dashboard without leaving the chat.

This functionality is powered by the built-in [`discover-session`](builtin-skills-reference.md#agent-builder-discover-session-skill) skill. Requests for charts, metrics, trends, or aggregated summaries produce a [Lens visualization](agent-builder-dashboards-and-visualizations.md).

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` If you start the conversation from **Discover** in {{esql}} mode, the [`discover-data-analysis`](builtin-skills-reference.md#agent-builder-discover-data-analysis-skill) skill can also show the current documents in a **Discover** table in chat, without the experimental setting. To get the table, ask for a **Discover** table explicitly. Otherwise, the agent might answer with a plain text table. Refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai).

## Before you begin

- Turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional). The `discover-session` skill is hidden until you do.
- Use the default Elastic AI Agent, or a custom agent that has [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) turned on or the `discover-session` skill assigned.
- To open the table in **Discover**, you need the **Read** or **All** privilege for **Discover**.
- To save the table to a dashboard, you need the **All** privilege for **Dashboard**.

## Ask for documents

Describe the documents you want to see. The agent writes an {{esql}} query and shows the results in a table in the conversation. For example:

```text
Show me error and warning logs from logs-* for the last hour in a document table in this chat.
```

To get a chart instead of a table, ask for one. For example, `Chart error logs over time` produces a Lens visualization.

The table supports {{esql}} queries only. The agent can't use aggregating queries, such as queries with `STATS` or `PROMQL`, for a table. Ask for a chart instead.

## Work with the table

The table works like a compact version of the **Discover** document table:

- **Context-aware columns and cells**: When your data matches a [context-aware experience](/explore-analyze/discover/discover-get-started.md#context-aware-discover), the table uses its columns, cell rendering, row indicators, and document views. The experience depends on the solution you're chatting from. For example, when you chat from an {{observability}} solution view or project, [logs data](/solutions/observability/logs/discover-logs.md) shows log-level badges, severity row indicators, the **Summary** column, and the **Log overview** document view.
- **Local time range**: The table has its own time picker. Changing it updates only this table, not the global {{kib}} time range. If you don't ask for a specific time range, the table uses the time range of the page you're chatting from, or the last 24 hours.
- **Document details**: Select {icon}`maximize` **View details** on a row to open the document in a flyout over the chat.
- **Columns**: Use the column selector in the table toolbar to change which columns are shown. Your column changes carry over when you open the table in **Discover** or save it to a dashboard.
- **Horizontal scrolling**: Scroll sideways to see more columns in the narrow chat area.

:::{image} images/agent-builder-discover-table-inline.png
:screenshot:
:alt: Discover table of error and warning logs in an Agent Builder conversation, with the Open in Discover button, a Last 1 hour time picker, the Columns selector, and a Summary column showing service and host badges
:::

When you select **View details**, the document opens in a flyout over the conversation:

:::{image} images/agent-builder-discover-table-flyout.png
:screenshot:
:alt: Document flyout over the conversation showing the Log overview tab with the log message, an error badge, service name, host name, and stream
:::

## Refine the table with follow-up prompts

Send a follow-up message to change the table. For example, after asking for error and warning logs from the last hour, ask for `only errors from the last 15 minutes`. The agent updates the existing table instead of creating a new one.

To keep the first table and add another, ask for a new table. If the conversation contains more than one table, the agent asks which one to update if your request is unclear.

## Open the table in Discover

Select **Open in Discover** to continue in the full **Discover** app. **Discover** opens in a new **Discover** tab with the same {{esql}} query, time range, columns, and sort order as the table.

This button appears only if you have the **Read** or **All** privilege for **Discover**.

## Save the table to a dashboard

Add the table to a new or existing dashboard as a panel. This works like [saving a table to a dashboard from Discover](/explore-analyze/discover/save-open-search.md#save-table-to-dashboard).

1. In the table toolbar, select {icon}`add_to_dashboard` **Save table to dashboard**.
2. Enter or edit the title for the panel, and optionally add a description.
3. In **Add to dashboard**, select **Existing** to choose a dashboard from the list, or **New** to create one.
4. Select **Save and go to dashboard**. The dashboard opens in edit mode with the table added as a panel.
5. Save the dashboard to keep the panel.

The panel stores the query and your visible columns with the dashboard. It doesn't keep the table's time range. It uses the dashboard's time range instead. Although the dialog is titled **Save Discover session**, the table isn't saved as a **Discover** session in the library.

If you don't have the **All** privilege for **Dashboard**, the button is disabled.

## Limitations

The table doesn't support:

- Saving the table as a **Discover** session, or attaching an existing **Discover** session to the conversation.
- KQL queries or classic **Discover** sessions.
- A filter bar.
- Adding **Discover** tables to dashboards that the agent creates. You can still save a table to a dashboard yourself.

## Related pages

- [Discover](/explore-analyze/discover.md)
- [Dashboards and visualizations in chat](agent-builder-dashboards-and-visualizations.md)
- [Chat with {{agent-builder}} agents](chat.md)
- [Built-in skills reference](builtin-skills-reference.md)
