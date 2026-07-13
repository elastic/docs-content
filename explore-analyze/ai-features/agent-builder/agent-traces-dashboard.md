---
navigation_title: "Agent traces dashboard"
description: "Install and use the prebuilt Agent Builder overview dashboard to monitor agent activity, token usage, latency, and tool calls from trace data."
applies_to:
  stack: ga 9.5+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} traces overview dashboard

<!-- STATUS: Phase 3 done (overview + install how-to drafted). Phase 4 reference still skeleton. Items needing a live check are marked VERIFY(cluster) and collected in the checklist near the end.
     Lifecycle: GA 9.5 (Stack + Serverless), confirmed. Badge matches collect-traces.md.
     Placeholder links: collect-traces.md (#7171) and permissions.md#read-trace-data are NOT on main yet
     (they land with PR #7322). Keep those links as plain text + TODO until #7322 merges, then wire them live. -->

{{agent-builder}} ships a prebuilt overview dashboard that turns your agent trace data into ready-made operational and usage metrics. Instead of building visualizations yourself, you install one managed dashboard and see how your agents behave, including how many tokens they use, how long conversations take, which agents run most often, and where tool calls fail.

Use the dashboard to:

- Track token usage and LLM request volume across models and providers.
- Spot slow conversations and long-running agent executions.
- Find tools that fail or run slowly.

The dashboard reads the traces that {{agent-builder}} collects into your own {{es}}, so it reflects your real agent activity. You collect that trace data first, then install the dashboard in each {{kib}} space where you want it. The following sections walk through both.

<!-- TODO(#7322): link "agent trace data" and "trace data" -> collect-traces.md once it is on main. -->

## What the dashboard shows

The overview dashboard is a single prebuilt dashboard named **[Elastic] Agent Builder Overview**. It is a managed dashboard, which means it is read-only and updates automatically when Elastic improves it. To change or extend it, duplicate it and edit the copy, as described in Customize the dashboard.

Every {{kib}} space has its own copy of the dashboard, built from the trace data collected in that space.

The dashboard groups its panels into four areas:

- **Token usage and LLM requests**: Input and output tokens, and the number of LLM requests, broken down by model and provider.
- **Conversation volume and latency**: How many conversation rounds ran and how long they took, including average, 95th percentile, and maximum duration.
- **Agent execution**: How often each agent ran and how long it took, broken down by agent.
- **Tool calls and errors**: How often tools were called, their success and error rates, and the most-used and slowest tools.

<!-- Phase 2 notes (verified vs Kibana main; see reference_ab_overview_dashboard_fields memory):
     - On-screen section names: "Token Usage & Cost", "Conversation Volume & Latency", "Agent Execution", "Tool Call Frequency & Errors" (last one collapsed by default; the UI prefixes each with an emoji).
     - OPEN QUESTION: section 1 is labeled "...& Cost" but no cost metric ships, and there is no cached-tokens or workflow panel. Body intentionally omits cost, cached tokens, and workflow. Do not add them until @meghanmurphy1 confirms cut vs deferred.
     - Anchor link to Customize the dashboard can be added in Phase 6 once anchors are finalized.
     - Field-level detail is in the Span and attribute reference section below. -->

## Before you begin

Before you install the dashboard:

- Turn on trace collection for the space and save the change. The **Install Dashboard** button appears only after trace collection is enabled and saved. For details, refer to Collect agent traces.
- Make sure you can read the trace data streams, otherwise the panels have no data to show. For the required privileges, refer to Read trace data.
- Install the dashboard in each {{kib}} space where you want it. It is not shared across spaces.

<!-- TODO(#7322): make "Collect agent traces" a link to collect-traces.md and "Read trace data" a link to permissions.md#read-trace-data once #7322 is on main. -->
<!-- VERIFY(cluster): which privilege lets a user open Management > Gen AI Settings and install or uninstall the dashboard (for example advanced settings save, or a management privilege). Not determinable from source. -->

## Install the dashboard

The overview dashboard is not installed automatically. Install it once per {{kib}} space.

1. Go to **Management > Gen AI Settings**.
2. In the **Agent Builder Traces** section, confirm that **Collect conversation traces** is on and saved.
3. Select **Install Dashboard**.

To open the dashboard, select **View Dashboard**, or open **Dashboards** and select **[Elastic] Agent Builder Overview**.

Repeat these steps in each space where you want the dashboard.

### Reinstall or remove the dashboard

The dashboard is not restored automatically, including in a new space or after you remove it. If it is missing, open the **Agent Builder Traces** section and select **Install Dashboard** again.

To remove it, select the arrow next to **View Dashboard**, then select **Uninstall dashboard**.

<!-- Source-verified labels (Kibana main, agent_builder_tracing_section.tsx): section "Agent Builder Traces"; "Install Dashboard" when not installed; "View Dashboard" split button with an "Uninstall dashboard" menu item when installed. The button renders only after tracing is enabled and saved. View opens dashboards at #/view/agent-builder-overview-<spaceId>; the saved-object title is "[Elastic] Agent Builder Overview". Install and remove call POST /internal/gen_ai_settings/agent_builder/tracing_dashboard with {enabled}. -->

## Customize the dashboard

The overview dashboard is managed, so you cannot edit it directly. To build your own version:

1. Open the dashboard.
2. Duplicate it.
3. Edit and save the copy.

Because the original is managed, Elastic can ship improvements to it without overwriting your copy.

<!-- VERIFY(cluster): confirm the exact control to duplicate a managed, read-only dashboard (for example a "Duplicate" action in the Dashboards list, or "Save as" from the open dashboard). Not determinable from source. -->

<!-- ============================================================
     VERIFY ON A TEST CLUSTER before publishing (Phase 6).
     Charlotte to check on a 9.5 test cluster and capture screenshots.
     1. Nav path and casing: Management > Gen AI Settings, section titled "Agent Builder Traces".
     2. The "Install Dashboard" button appears only after "Collect conversation traces" is enabled AND saved.
     3. Exact labels: "Install Dashboard"; when installed, "View Dashboard" split button + "Uninstall dashboard" (via the arrow / More dashboard options).
     4. After install, the dashboard shows in Dashboards as "[Elastic] Agent Builder Overview" (id agent-builder-overview-<spaceId>).
     5. New-space and post-uninstall behavior: the dashboard is absent until reinstalled from the section.
     6. Customize: the exact control to duplicate the managed dashboard.
     7. Privilege required to open Gen AI Settings and to install/uninstall the dashboard.
     8. The four sections render, and "Tool Call Frequency & Errors" is collapsed by default.
     Screenshots to capture: (a) Agent Builder Traces section with the Install Dashboard button; (b) the section after install (View Dashboard split button); (c) the installed dashboard.
     ============================================================ -->

## Span and attribute reference

<!-- Phase 4. This page OWNS the reference that collect-traces.md (#7171) defers here.
     Framing: to build your own visualizations with Dashboards, Lens, or ES|QL, use these span types and attributes.
     Data source: FROM traces-agent_builder.otel-* for the current space.
     ACCURACY: re-verify all strings against source right before publishing (OTel schema upgrade search-team#15270 / kibana#277640). -->

### Span types

<!-- Phase 4 table. What it covers | Matched on span.name
     - LLM requests, tokens, model, provider | span.name LIKE "chat *"
     - Conversation volume and latency        | span.name LIKE "invoke_agent *" AND attributes.elastic.inference.span.kind == "CHAIN"
     - Agent execution                         | span.name LIKE "invoke_agent *" AND attributes.elastic.inference.span.kind == "AGENT"
     - Tool calls and errors                   | span.name LIKE "execute_tool *"  (errors add status.code == "Error") -->

### Generative AI attributes

<!-- Phase 4 table. Purpose | Field (all carry the attributes. prefix unless noted)
     - Input tokens  | attributes.gen_ai.usage.input_tokens
     - Output tokens | attributes.gen_ai.usage.output_tokens
     - Model         | attributes.gen_ai.request.model
     - Provider      | attributes.gen_ai.provider.name
     - Agent id      | attributes.gen_ai.agent.id
     - Tool name     | name  (bare root field)
     - Duration      | duration  (root field, nanoseconds)
     - Status        | status.code -->

## Related pages

<!-- Phase 5. Wire these once targets exist on main:
     - collect-traces.md (#7171)
     - permissions.md
     - monitor-usage.md
     - chat.md
     - builtin-skills-reference.md
     - alerting how-to (#7173) once published -->
