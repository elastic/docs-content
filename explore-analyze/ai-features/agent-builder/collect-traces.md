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

When an agent runs, {{agent-builder}} records the run as OpenTelemetry (OTel) traces. Each trace covers one conversation round. A trace is made up of spans that map to the work the agent did, such as model calls, tool calls, and any workflows it triggered.

{{agent-builder}} ingests these traces into a managed data stream in your own {{es}}, named `traces-agent_builder.otel-*`. The data stream is OTel-compatible and uses the standard OTel index template, so it inherits the mappings, settings, and data lifecycle that {{es}} maintains for OTel data.

The trace data stream is a regular data stream, not a system or hidden index. You can explore and analyze traces with the same tools you use for any other data in {{es}}, including Discover, Dashboards, Lens, and ES|QL.

<!-- TODO (step 9, cross-links): link Discover, Dashboards, Lens, and ES|QL. -->

Trace collection is space-aware. Each {{kib}} space collects its own traces, and turning on collection installs an overview dashboard in that space.

### What a trace contains

Spans in a trace mirror how the agent ran. Common span types include:

- `Converse`: the full conversation round.
- `ExecuteAgent`: a single agent execution, identified by `elastic.agent.id`.
- `Tool: <name>`: an individual tool call, identified by `gen_ai.tool.name`.
- `Workflow: <name>`: a workflow the agent triggered.
- `ChatComplete`: a single model call.

Spans carry standard OTel generative AI attributes, such as the model (`gen_ai.request.model`), the model provider (`gen_ai.system`), and token cost (`gen_ai.usage.cost`). Use these to break down usage and latency by model, agent, or tool.

By default, traces record structural metadata only. Conversation content such as prompts and responses is excluded unless an administrator opts in. For details, see the trace privacy settings later on this page.

<!-- Span types and attributes are from #7170 research (search-team#14180). Verify exact span names against the shipped feature before publishing, and keep the full attribute list on the dashboards page (#7170). -->

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
