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

{{agent-builder}} ingests this data into managed data streams in your own {{es}}. It uses two OpenTelemetry data streams, `traces-agent_builder.otel-*` and `logs-agent_builder.otel-*`. They are OTel-compatible and use the standard OTel index templates, so they inherit the mappings, settings, and data lifecycle that {{es}} maintains for OTel data.

These are regular data streams, not system or hidden indices. You can explore and analyze the data with the same tools you use for any other data in {{es}}, including [Discover](/explore-analyze/discover.md), [Dashboards](/explore-analyze/dashboards.md), [Lens](/explore-analyze/visualize/lens.md), and [ES|QL](elasticsearch://reference/query-languages/esql.md).

<!-- Both `traces-agent_builder.otel-*` and `logs-agent_builder.otel-*` are named in the Kibana Gen AI Settings source. Confirm what each stream carries (spans vs. log records) before publishing. -->

Trace collection is space-aware. Each {{kib}} space collects its own traces, and turning on collection installs an overview dashboard in that space.

### What a trace contains

Spans in a trace mirror how the agent ran. Common span types include:

- `Converse`: the full conversation round.
- `ExecuteAgent`: a single agent execution, identified by `elastic.agent.id`.
- `Tool: <name>`: an individual tool call, identified by `gen_ai.tool.name`.
- `Workflow: <name>`: a workflow the agent triggered.
- `ChatComplete`: a single model call.

Spans carry standard OTel generative AI attributes, such as the model (`gen_ai.request.model`), the model provider (`gen_ai.system`), and token cost (`gen_ai.usage.cost`). Use these to break down usage and latency by model, agent, or tool.

By default, traces record structural metadata only. Conversation content such as prompts and responses is excluded unless an administrator opts in. For details, see [Trace privacy settings](#trace-privacy-settings).

<!-- Span types and attributes are from #7170 research (search-team#14180). Verify exact span names against the shipped feature before publishing, and keep the full attribute list on the dashboards page (#7170). -->

## Enable and configure trace collection

Trace collection is on by default. To manage it, go to **Management > Gen AI Settings** and open the **Agent Builder Traces** section.

The **Collect conversation traces** setting turns collection on and off. When it is on, {{agent-builder}} collects OpenTelemetry traces for agent conversations and ingests them into {{es}}. From the same section, you can install a prebuilt overview dashboard for the current {{kib}} space.

:::{note}
Any user with index access can read trace data. To restrict access, configure index-level privileges in **Stack Management > Roles**. For details, see [Grant access to trace data](#grant-access-to-trace-data).
:::

### Trace privacy settings

By default, traces record structural metadata only, such as token counts, latency, and model names. Conversation content is not captured unless an administrator opts in.

To change what is captured, expand **Advanced privacy settings** in the **Agent Builder Traces** section. Each option is off by default.

| Setting | Effect when enabled |
|---|---|
| **Include user prompts in traces** | Captures user messages. |
| **Include system prompt in traces** | Captures agent instructions. |
| **Include LLM responses in traces** | Captures agent responses. |
| **Include tool call details in traces** | Captures tool call arguments and results. |
| **Include real tool and agent names in traces** | Records real tool and agent names instead of anonymized values. |
| **Include real conversation and workflow IDs in traces** | Records real conversation and workflow IDs instead of anonymized values. |

:::{note}
Built-in tools and agents always appear under their real names. When a value is anonymized, {{agent-builder}} uses a stable identifier, so you can still group and correlate traces without exposing names or IDs.
:::

<!-- Labels, defaults, and the access note are from Kibana source (ui_settings.ts and agent_builder_tracing_section.tsx, main, 2026-07-10). Real screenshots still needed for the settings section. -->

## Grant access to trace data

Trace data is stored in the `traces-agent_builder.otel-*` and `logs-agent_builder.otel-*` data streams. To read it, a role needs `read` and `view_index_metadata` on both patterns.

Access is granted at the index level. Any user who can read these data streams can read all collected traces, so trace access is not scoped per user. To control who can read traces, configure index privileges through roles in **Stack Management > Roles**.

For the full privilege model, including {{kib}} feature and cluster privileges, see [Permissions and access control](permissions.md#read-trace-data).

<!-- RBAC on the local trace index is still settling (search-team#14100). Keep this hedged until the decision lands. -->

## Export traces to a remote OTLP endpoint

By default, {{agent-builder}} exports traces to the local data streams in your {{es}}. You can also forward traces to one or more remote OpenTelemetry Protocol (OTLP) endpoints, such as a dedicated observability cluster.

Configure remote endpoints with `xpack.agentBuilder.tracing.exporters` in `kibana.yml`. Each entry takes a `url` and optional `headers` for authentication:

```yaml
xpack.agentBuilder.tracing:
  exporters:
    - url: "https://remote-cluster:9200/_otlp/v1/traces"
      headers:
        Authorization: "ApiKey <encoded-key>"
```

Remote export is additive. Traces still go to the local `traces-agent_builder.otel-*` and `logs-agent_builder.otel-*` data streams, and a copy is sent to each configured endpoint. The [trace privacy settings](#trace-privacy-settings) apply to every destination, so content that is excluded locally is also excluded from remote export.

:::{note}
These are `kibana.yml` settings, so remote export is available on deployments where you can edit the {{kib}} configuration.
:::

<!-- Source: kibana `main` config.ts + register_tracing.ts (2026-07-10). The local ES exporter is always registered and `exporters` entries are added on top, so local and remote export are additive, not mutually exclusive. This supersedes search-team#14190, which described a single `tracing.url` that replaced local export. Not gated by the experimental flag. `scheduledDelay` (batch flush) and `opik_distributed_tracing` also exist under `tracing` but are tuning/internal options, omitted here. Confirm whether serverless permits these kibana.yml settings. -->

## Build dashboards on trace data

When trace collection is on, {{agent-builder}} provides a prebuilt overview dashboard for agent activity and token usage. You install or reinstall it per space from the **Agent Builder Traces** settings section.

Because traces are stored in regular data streams, you can also build your own visualizations with [Dashboards](/explore-analyze/dashboards.md) and [Lens](/explore-analyze/visualize/lens.md), or query the data with [ES|QL](elasticsearch://reference/query-languages/esql.md). To explore traces in natural language, use the built-in traces skill described in the [built-in skills reference](builtin-skills-reference.md).

<!-- The out-of-the-box overview dashboard is owned by #7170. Link its page once published and keep this section brief. Known bug: dashboard not auto-installed on new space creation (search-team#15105). Confirm status (open question 5) before documenting a workaround. Do not confuse with agent-builder-dashboards-and-visualizations.md (agents building dashboards in chat). Tighten the skills link to the traces-skill anchor once PR #7255 merges. -->

## View traces for a conversation round

In [Agent Chat](chat.md), you can open the trace waterfall for a single conversation round. The button appears only when the trace data stream exists, you have access to it, and traces exist for that round.

<!-- Step 8 adds the detailed button subsection to chat.md, coordinated with PR #7290. Confirm the exact button label (open question 6). Source: search-team#14619. -->

## Related pages

- [](permissions.md)
- [](monitor-usage.md)
- [](chat.md)
- [](builtin-skills-reference.md)

<!-- Add the dashboards page (#7170) and alerting page (#7173) here once published. -->
