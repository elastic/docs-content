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

<!-- Source: kibana#288514 (not merged as of 2026-09-30). Re-verify UI strings, IDs, and behavior against Kibana main after merge. -->

# Show documents in a Discover table in {{agent-builder}} chat

When you ask an agent to show matching documents, events, or logs, it can display them in an interactive **Discover** table directly in the conversation. You can inspect individual documents, change the time range, open the results in **Discover**, or save the table to a dashboard without leaving the chat.

This functionality is powered by the built-in [`discover-session`](builtin-skills-reference.md#agent-builder-discover-session-skill) skill. Requests for charts, metrics, trends, or aggregated summaries still produce a [Lens visualization](agent-builder-dashboards-and-visualizations.md).

:::{note}
The `discover-session` skill is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}. This setting isn't available in {{sec-serverless}} projects.
:::

:::{tip}
If you start the conversation from **Discover** in {{esql}} mode, the [`discover-data-analysis`](builtin-skills-reference.md#agent-builder-discover-data-analysis-skill) skill can also show the current documents in a table in chat, without the experimental setting. Refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai).
:::

## Before you begin

- Turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional).
- Use the default Elastic AI Agent, or a custom agent that has [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) turned on or the `discover-session` skill assigned.
- To open the table in **Discover**, you need the `show` or `save` privilege for **Discover**.
- To save the table to a dashboard, you need write access to **Dashboards**.

## Ask for documents

Describe the documents you want to see. The agent writes an {{esql}} query and shows the results in a table in the conversation. For example:

```text
Show me error and warning logs from logs-* for the last hour in a document table in this chat.
```

To get a chart instead of a table, ask for one. For example, `Chart error logs over time` produces a Lens visualization.

The table supports {{esql}} queries only. The agent can't use aggregating queries, such as queries with `STATS`, for a table. It creates a visualization for those instead.

## Work with the table

The table works like a compact version of the **Discover** document table:

- **Context-aware columns and cells**: When your data matches a [context-aware experience](/explore-analyze/discover/discover-get-started.md#context-aware-discover), the table uses its columns, cell rendering, row indicators, and document views. The experience depends on the solution you're chatting from. For example, when you chat from an {{observability}} solution view or project, [logs data](/solutions/observability/logs/discover-logs.md) shows log-level badges, severity row indicators, a summary column, and the **Log overview** document view.
- **Local time range**: The table has its own time picker. Changing it updates only this table, not the global {{kib}} time range.
- **Document details**: Select {icon}`maximize` **View details** on a row to open the document in a flyout over the chat.
- **Columns**: Use the column selector in the table toolbar to change which columns are shown. Your column changes carry over when you open the table in **Discover** or save it to a dashboard.
- **Horizontal scrolling**: Scroll sideways to see more columns in the narrow chat area.

<!-- Screenshot to add: compact inline table with the logs profile, local time picker, and horizontal scroll, at chat width (max 768px). Images are in the kibana#288514 description. -->

## Refine the table with follow-up prompts

Send a follow-up message to change the table. For example, after asking for error and warning logs from the last hour, ask for `only errors from the last 15 minutes`. The agent updates the existing table instead of creating a new one.

To keep the first table and add another, ask for a new table. If the conversation contains more than one table, the agent asks which one to update if your request is unclear.

## Open the table in Discover

Select **Open in Discover** to continue in the full **Discover** app. **Discover** opens with the same {{esql}} query, time range, columns, and sort order as the table.

This button appears only if you have the `show` or `save` privilege for **Discover**.

## Save the table to a dashboard

Add the table to a new or existing dashboard as a panel. This works like [saving a table to a dashboard from Discover](/explore-analyze/discover/save-open-search.md#save-table-to-dashboard).

1. In the table toolbar, select {icon}`add_to_dashboard` **Save table to dashboard**.
2. Enter a title for the panel, and optionally a description.
3. In **Add to dashboard**, select **Existing** to choose a dashboard from the list, or **New** to create one.
4. Select **Save and go to dashboard**.

<!-- TODO verify in the UI after merge: whether the user must then save the dashboard to keep the panel. -->

The panel stores the query and your visible columns with the dashboard. It doesn't keep the table's time range, and uses the dashboard's time range instead. Although the dialog is titled **Save Discover session**, no **Discover** session is saved.

If you don't have write access to **Dashboards**, the button is disabled.

<!-- Screenshot to add: overlay document flyout. Available in the kibana#288514 description. -->

## Limitations

The following aren't available yet:

- Saving the table as a **Discover** session, or attaching an existing **Discover** session to the conversation.
- Classic **Discover** sessions that use KQL, and a filter bar in the table.
- Adding **Discover** tables to dashboards that the agent creates. You can still save a table to a dashboard yourself.

## Related pages

- [Discover](/explore-analyze/discover.md)
- [Dashboards and visualizations in chat](agent-builder-dashboards-and-visualizations.md)
- [Chat with {{agent-builder}} agents](chat.md)
- [Built-in skills reference](builtin-skills-reference.md)
