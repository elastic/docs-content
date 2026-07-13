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

<!-- STATUS: Draft body complete (Phases 1-4). Independently fact-checked 2026-07-13 against Kibana main: the span/attribute reference and the UI labels are verified verbatim. Prose corrected after that check: removed a nonexistent "slowest tools" panel and an unverified "updates automatically" claim, and made the token/request breakdown precise. Remaining: cross-links (Phase 5, after #7322 merges, still open as of 2026-07-13) and badges/build (Phase 6). Items needing a live check are marked VERIFY(cluster).
     Placeholder links: collect-traces.md (#7171) and permissions.md#read-trace-data are NOT on main yet (they land with PR #7322). Keep them as plain text + TODO until #7322 merges. -->

{{agent-builder}} ships a prebuilt overview dashboard that turns your agent trace data into ready-made operational and usage metrics. Instead of building visualizations yourself, you install one managed dashboard and see how your agents behave, including how many tokens they use, how long conversations take, which agents run most often, and where tool calls fail.

Use the dashboard to:

- Track token usage and LLM request volume across models and providers.
- Spot slow conversations and long-running agent executions.
- Find tools that fail or run slowly.

The dashboard reads the traces that {{agent-builder}} collects into your own {{es}}, so it reflects your real agent activity. You collect that trace data first, then install the dashboard in each {{kib}} space where you want it. The following sections walk through both.

<!-- TODO(#7322): link "agent trace data" and "trace data" -> collect-traces.md once it is on main. -->

## What the dashboard shows

The overview dashboard is a single prebuilt dashboard named **[Elastic] Agent Builder Overview**. It is a managed dashboard, so it is read-only. To change or extend it, duplicate it and edit the copy, as described in Customize the dashboard.

You install the dashboard separately in each {{kib}} space, and each copy shows only that space's trace data.

The dashboard groups its panels into four areas:

- **Token usage and LLM requests**: Input and output tokens by model, and LLM request counts by model and provider.
- **Conversation volume and latency**: How many conversation rounds ran and how long they took, including average, 95th percentile, and maximum duration.
- **Agent execution**: How often each agent ran and how long it took, broken down by agent.
- **Tool calls and errors**: How often tools were called, their success and error rates, average tool duration, and the most-used tools.

<!-- Notes (verified vs Kibana main; see reference_ab_overview_dashboard_fields memory):
     - On-screen section names: "Token Usage & Cost", "Conversation Volume & Latency", "Agent Execution", "Tool Call Frequency & Errors" (last one collapsed by default; the UI prefixes each with an emoji).
     - Precision (from fact-check): tokens over time are broken down by model; LLM request counts are broken down by model and by provider. The tool section has an overall average duration KPI and a Top 15 by call count, but no per-tool "slowest tools" ranking.
     - OPEN QUESTION: the dashboard's own header markdown says "token usage & cost" and "workflow performance", but no cost, cached-token, or workflow panels actually ship. The body omits them. Confirm cut vs deferred with @meghanmurphy1.
     - Field-level detail is in the Span and attribute reference section below. -->

## Before you begin

Before you install the dashboard:

- Make sure trace collection is on for the space and the setting is saved. It is on by default. The **Install Dashboard** button appears only after trace collection is enabled and saved. For details, refer to Collect agent traces.
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

<!-- VERIFY ON A TEST CLUSTER before publishing (Phase 6). The source-verifiable facts (labels, install model, four sections, span/attribute strings, ES|QL validity) were double-checked against Kibana main on 2026-07-13 and are confirmed. Still needs eyes on a live 9.5 cluster:
     - The exact management app label and casing ("Gen AI Settings").
     - That "Tool Call Frequency & Errors" is collapsed by default.
     - Screenshots: (a) Agent Builder Traces section with the Install Dashboard button; (b) the section after install (View Dashboard split button); (c) the installed dashboard.
     See also the inline VERIFY(cluster) notes for the install privilege, the duplicate control, and running the ES|QL examples. -->

## Span and attribute reference

The dashboard panels are [ES|QL](elasticsearch://reference/query-languages/esql.md) queries over your trace data. To build your own visualizations in [Dashboards](/explore-analyze/dashboards.md), [Lens](/explore-analyze/visualize/lens.md), or [Discover](/explore-analyze/discover.md), query the trace data stream and filter by span type and attribute.

Traces are stored in the `traces-agent_builder.otel-*` data stream, where each document is a span. The dashboard identifies the kind of work a span represents from its `span.name`, and reads generative AI details from the span attributes.

<!-- VERIFY(cluster): the span-name filters and attribute names below are read from the shipped dashboard definition (Kibana main). Confirm them against a live 9.5 dashboard, and re-check after the OTel schema upgrade (search-team#15270, kibana#277640). -->

### Span types

Each document is a span. Filter on the `span.name` field to select a kind of agent activity. The dashboard matches span names by prefix.

| Agent activity | Filter |
|---|---|
| LLM requests, tokens, model, and provider | `span.name LIKE "chat *"` |
| Conversation rounds (volume and latency) | `span.name LIKE "invoke_agent *"` and `attributes.elastic.inference.span.kind == "CHAIN"` |
| Agent executions | `span.name LIKE "invoke_agent *"` and `attributes.elastic.inference.span.kind == "AGENT"` |
| Tool calls | `span.name LIKE "execute_tool *"`. For failures only, add `status.code == "Error"` |

### Generative AI attributes

These fields carry the details the dashboard aggregates. Generative AI attributes use the `attributes.` prefix.

| Field | Description |
|---|---|
| `attributes.gen_ai.usage.input_tokens` | Input tokens sent to the model |
| `attributes.gen_ai.usage.output_tokens` | Output tokens generated by the model |
| `attributes.gen_ai.request.model` | Model name |
| `attributes.gen_ai.provider.name` | Model provider |
| `attributes.gen_ai.agent.id` | Agent identifier |
| `attributes.elastic.inference.span.kind` | On `invoke_agent` spans, separates conversation rounds (`CHAIN`) from agent executions (`AGENT`) |
| `name` | Tool name, on `execute_tool` spans (root field, no prefix) |
| `duration` | Span duration in nanoseconds (root field). Divide by 1,000,000,000 for seconds |
| `status.code` | Span status, for example `Error` (root field) |
| `@timestamp` | When the span started |

### Example queries

Use these as starting points, and test them on your own data. They query all spaces. To scope a query to one space, replace the wildcard with that space's data stream, for example `traces-agent_builder.otel-default`.

Total input and output tokens by model and provider:

```esql
FROM traces-agent_builder.otel-*
| WHERE span.name LIKE "chat *"
| STATS
    input_tokens = SUM(TO_LONG(attributes.gen_ai.usage.input_tokens)),
    output_tokens = SUM(TO_LONG(attributes.gen_ai.usage.output_tokens))
  BY model = attributes.gen_ai.request.model,
     provider = attributes.gen_ai.provider.name
| SORT input_tokens DESC
```

Tool calls and errors by tool:

```esql
FROM traces-agent_builder.otel-*
| WHERE span.name LIKE "execute_tool *"
| STATS
    calls = COUNT(*),
    errors = COUNT(*) WHERE status.code == "Error"
  BY tool = name
| SORT calls DESC
```

<!-- VERIFY(cluster): run both ES|QL examples on a 9.5 cluster with real trace data before publishing. Confirm the SUM(TO_LONG(...)) token pattern, the per-aggregation COUNT(*) WHERE ... syntax, and that the span-name filters return rows. These mirror the dashboard's own query patterns but were composed by hand. -->

## Related pages

<!-- Phase 5. Wire these once targets exist on main:
     - collect-traces.md (#7171)
     - permissions.md
     - monitor-usage.md
     - chat.md
     - builtin-skills-reference.md
     - alerting how-to (#7173) once published -->
