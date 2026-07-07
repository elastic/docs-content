---
navigation_title: "Collect agent traces"
description: "Learn how Agent Builder collects agent execution traces into an OpenTelemetry data stream in your own Elasticsearch, how to configure collection and privacy, and how to grant access to trace data."
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

# Collect {{agent-builder}} traces

{{agent-builder}} can collect agent execution traces into your own {{es}}. Traces record how each agent round runs, including reasoning steps, tool calls, latency, and token usage, so you can monitor agent activity, debug behavior, and build dashboards on the data.

<!-- SCAFFOLD (dc#7171, branch charlotte-AB-traces-7171). Lifecycle confirmed GA in 9.5 (Stack and Serverless) via kibana#276174. Sections below are placeholders to fill in per the plan. Open questions are tracked in Task handler/dc7171-trace-collection-plan.md. -->

## How trace collection works

Agent Builder writes traces to an OpenTelemetry-compatible managed data stream in your own {{es}}.

<!-- TODO: describe the `traces-agent_builder.otel-*` data stream. It is a regular data stream, not a system index, so it works in Dashboards, Discover, Lens, and ES|QL. Traces are space-aware. Sources: search-team#14684, #14620. -->

## Enable and configure trace collection

Trace collection is on by default. You manage it in **Management > Gen AI Settings**.

<!-- TODO: confirm the settings section and toggle labels (open question 1). The sole control is `agentBuilder:tracing:enabled`, which defaults to `true`; the experimental features flag no longer gates tracing (kibana#276174). -->

### Trace privacy settings

By default, traces contain only structural metadata. Conversation content is excluded until you opt in.

<!-- TODO: reproduce the settings table from search-team#14672 with defaults (all content options OFF by default): include user prompts, include LLM responses, include system prompt, include real tool and agent names, include real conversation IDs. -->

## Grant access to trace data

To read traces, a user needs `read` and `view_index_metadata` privileges on `traces-agent_builder.otel-*`.

<!-- TODO: cross-link permissions.md (ES index privileges section). RBAC on the local trace index is still open (search-team#14100, decision TBD), including whether users can see other users' traces. Keep this precise and hedged (open questions 3 and 4). -->

## Export traces to a remote OTLP endpoint

You can send traces to a remote OTLP endpoint, such as a separate {{es}} cluster, instead of the local data stream.

<!-- TODO: document `xpack.agentBuilder.tracing.url` (and `headers`) in `kibana.yml`. Local and remote export are mutually exclusive per config. Source: search-team#14190. Confirm remote export is also GA/un-gated in 9.5 (open question 2). -->

## Build dashboards on trace data

Turning on trace collection installs an overview dashboard for monitoring agent activity and token usage.

<!-- TODO: keep this brief; the overview dashboard is owned by #7170. Note the known bug where the dashboard is not auto-installed on new space creation (search-team#15105). Do not confuse this with agent-builder-dashboards-and-visualizations.md, which is about agents building dashboards inside chat. -->

## View traces for a conversation round

In chat, you can open the trace waterfall for a single conversation round.

<!-- TODO: cross-link chat.md. The button appears only when the trace index exists, the user has access, and traces exist for that round. Source: search-team#14619. Confirm the exact button label (open question 6). -->

## Related pages

<!-- TODO: link permissions.md, monitor-usage.md, chat.md, and the sibling trace pages (#7170 dashboards, #7172 traces skill, #7173 alerting) once published. -->
