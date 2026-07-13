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

# Monitor {{agent-builder}} agents with the traces overview dashboard

<!-- STATUS: Phase 2 done (intro + What the dashboard shows drafted). Phases 3-4 still skeleton.
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

<!-- Phase 3 (how-to prerequisites).
     - Trace collection must be on. (Plain text now; TODO(#7322) link -> collect-traces.md.)
     - You need read access to the trace data streams. (TODO(#7322) link -> permissions.md#read-trace-data.)
     - Be in the Kibana space where you want the dashboard (install is per space). -->

## Install the dashboard

<!-- Phase 3 (how-to). Manual, per space, off by default. Source: kibana#276643 (+9.5 backport #277384).
     Steps (use a stepper if it reads better):
       1. Go to Management > Gen AI Settings, and open the Agent Builder Traces section.
       2. Select Install to install the overview dashboard for the current space.
       3. Open it with View, or find it in Dashboards as `agent-builder-overview-<spaceId>`.
     Notes: repeat per space; the dashboard is not auto-installed; when installed the section shows View + Delete;
     you can reinstall it after deleting. Success checkpoint: the dashboard appears in the space's Dashboards list. -->

## Customize the dashboard

<!-- Phase 3. The prebuilt dashboard is managed (read-only). To change it, duplicate it and edit the copy.
     New visualizations ship by overwriting the managed definition, so edits to a copy are safe across upgrades. -->

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
