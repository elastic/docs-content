---
navigation_title: "Collect agent traces"
description: "Learn how Agent Builder collects agent execution traces into OpenTelemetry data streams in your Elasticsearch deployment, how to configure collection and privacy, and how to grant access."
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

{{agent-builder}} can collect agent execution traces into your {{es}} deployment. Traces record how each agent round runs, including model calls, tool calls, latency, and token usage, so you can monitor agent activity, debug behavior, and build dashboards on the data.

## How trace collection works

When an agent runs, {{agent-builder}} records the run as OpenTelemetry (OTel) traces. Each trace covers one conversation round. A trace is made up of spans that map to the work the agent did, such as model calls and tool calls.

Trace collection is space-aware. Each {{kib}} space writes its traces to its own data streams, named with the space id, such as `traces-agent_builder.otel-default` for the `default` space. Use the `traces-agent_builder.otel-*` wildcard to work with every space's traces at once.

{{agent-builder}} ingests this data into managed OpenTelemetry data streams in your {{es}} deployment. Execution spans, such as model calls and tool calls, are stored in `traces-agent_builder.otel-*`, with their timings, token usage, model, and status. Trace data is also stored in `logs-agent_builder.otel-*`, so reading all of it requires read access to both patterns.

When you opt in to capturing conversation content, that content is added to the `traces-agent_builder.otel-*` spans as attributes, such as user prompts, agent responses, system prompts, and tool call details. Content is captured only when you enable it in [Trace privacy settings](#trace-privacy-settings).

These data streams are OTel-compatible and use the standard OTel index templates, so they inherit the mappings, settings, and data lifecycle that {{es}} maintains for OTel data.

These are regular data streams, not system or hidden indices. You can explore and analyze the data with the same tools you use for any other data in {{es}}, including [Discover](/explore-analyze/discover.md), [Dashboards](/explore-analyze/dashboards.md), [Lens](/explore-analyze/visualize/lens.md), and [ES|QL](elasticsearch://reference/query-languages/esql.md).

### What a trace contains

Each trace is a set of spans that follow a run from the overall conversation round down to its individual steps, including:

- Each agent execution.
- Each model call.
- Each tool call.

Spans follow [OpenTelemetry semantic conventions for generative AI](https://github.com/open-telemetry/semantic-conventions-genai) (currently experimental) and carry generative AI attributes for the model, the provider, and token usage. Use them to break down usage and latency by model, agent, or tool. For the exact fields and the prebuilt visualizations that use them, refer to [Build dashboards on trace data](#build-dashboards-on-trace-data).

By default, traces record structural metadata only. Conversation content such as prompts and responses is excluded unless an administrator opts in. For details, refer to [Trace privacy settings](#trace-privacy-settings).

## Enable and configure trace collection

Trace collection is on by default. To manage it, go to **Management → GenAI Settings** and open the **Agent Builder Traces** section.

:::{image} images/agent-builder-traces-settings.png
:screenshot:
:alt: The Agent Builder Traces section in GenAI Settings, with trace collection enabled and the Install Dashboard button
:::

The **Collect conversation traces** setting turns collection on and off. When it is on, {{agent-builder}} collects OpenTelemetry traces for agent conversations and ingests them into {{es}}. From the same section, you can install a prebuilt overview dashboard for the current {{kib}} space.

:::{note}
Any user with index access can read trace data. To restrict access, configure index-level privileges in **Stack Management → Roles**. For details, refer to [Grant access to trace data](#grant-access-to-trace-data).
:::

### Trace privacy settings

By default, traces record structural metadata only, such as token counts, latency, and model names. Conversation content is not captured unless an administrator opts in.

To change what is captured, expand **Advanced privacy settings** in the **Agent Builder Traces** section. Each option is off by default.

:::{image} images/agent-builder-traces-privacy-settings.png
:screenshot:
:alt: The expanded Advanced privacy settings, showing six toggles for including sensitive content in traces, all turned off
:::

| Setting | Effect when enabled |
|---|---|
| **Include user prompts in traces** | Captures user messages. |
| **Include LLM responses in traces** | Captures agent responses. |
| **Include tool call details in traces** | Captures tool call arguments and results. |
| **Include system prompt in traces** | Captures agent instructions. |
| **Include real tool and agent names in traces** | Records real tool and agent names instead of anonymized values. |
| **Include real conversation and workflow IDs in traces** | Records real conversation and workflow IDs instead of anonymized values. |

:::{note}
Built-in tools and agents always appear under their real names. When a value is anonymized, {{agent-builder}} uses a stable identifier, so you can still group and correlate traces without exposing names or IDs.
:::

## Grant access to trace data

Trace data is stored in the `traces-agent_builder.otel-*` and `logs-agent_builder.otel-*` data streams. To read it, a role needs `read` and `view_index_metadata` on both patterns.

Access is granted at the index level. Any user who can read these data streams can read all collected traces, so trace access is not scoped per user. To control who can read traces, configure index privileges through roles in **Stack Management → Roles**.

For the full privilege model, including {{kib}} feature and cluster privileges, refer to [Permissions and access control](permissions.md#read-trace-data).

## Build dashboards on trace data

When trace collection is on, {{agent-builder}} provides a prebuilt overview dashboard for agent activity and token usage. You install or reinstall it per space from the **Agent Builder Traces** settings section. For what each panel shows and the full span and attribute reference, refer to [Agent Builder traces overview dashboard](agent-traces-dashboard.md).

Because traces are stored in regular data streams, you can also build your own visualizations with [Dashboards](/explore-analyze/dashboards.md) and [Lens](/explore-analyze/visualize/lens.md), or query the data with [ES|QL](elasticsearch://reference/query-languages/esql.md). To explore traces in natural language, use the [built-in traces skill](builtin-skills-reference.md).

## View traces for a conversation round

In [Agent Chat](chat.md), you can open the trace waterfall for a single conversation round. The button appears only when trace collection is enabled and the round has a trace.

## Related pages

- [](permissions.md)
- [](monitor-usage.md)
- [](chat.md)
- [](agent-traces-dashboard.md)
- [](builtin-skills-reference.md)
