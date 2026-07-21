---
navigation_title: "Overview dashboard"
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

{{agent-builder}} ships a prebuilt overview dashboard that turns your agent trace data into ready-made operational and usage metrics. Instead of building visualizations yourself, you install one managed dashboard and see how your agents behave, including how many tokens they use, how long conversations take, which agents run most often, and where tool calls fail.

Use the dashboard to:

- Track token usage and LLM request volume across models and providers.
- Spot slow conversations and long-running agent executions.
- Find tools that fail or run slowly.

The dashboard visualizes the trace data that {{agent-builder}} sends to your {{es}} deployment, giving you a view of real agent activity. First, you must configure trace collection. Then install the dashboard in each {{kib}} space where you want to view the data.

<!-- TODO(#7322): link "agent trace data" and "trace data" -> collect-traces.md once it is on main. -->

## What the dashboard shows

The overview dashboard is a single prebuilt dashboard named **[Elastic] Agent Builder Overview**. It is a managed dashboard, so it is read-only. To change or extend it, duplicate it and edit the copy, as described in Customize the dashboard.

You install the dashboard separately in each {{kib}} space, and each copy shows only that space's trace data.

The dashboard groups its panels into four areas:

- **Token Usage & Cost**: Input and output tokens by model, and LLM request counts by model and provider.
- **Conversation Volume & Latency**: How many conversation rounds ran and how long they took, including average, 95th percentile, and maximum duration.
- **Agent Execution**: How often each agent ran and how long it took, broken down by agent.
- **Tool Call Frequency & Errors**: How often tools were called, their success and error rates, average tool duration, and the most-used tools.

When trace data is flowing, the dashboard looks like this:

:::{image} images/agent-builder-overview-dashboard.png
:screenshot:
:alt: The Agent Builder Overview dashboard showing the Token Usage & Cost section with total input and output tokens, LLM request count, and token usage over time by model
:::

## Before you begin

Before you install the dashboard:

- Make sure trace collection is on for the space and the setting is saved. It is on by default. The **Install Dashboard** button appears only after trace collection is enabled and saved. For details, refer to Collect agent traces.
- Make sure you can read the trace data, otherwise the panels have no data to show. For the required privileges, refer to Read trace data.
- Make sure you can manage {{kib}} advanced settings. Installing and uninstalling the dashboard requires this privilege.
- Install the dashboard in each {{kib}} space where you want it. It is not shared across spaces.

<!-- TODO(#7322): make "Collect agent traces" a link to collect-traces.md and "Read trace data" a link to permissions.md#read-trace-data once #7322 is on main. -->

## Install the dashboard

The overview dashboard is not installed automatically. Install it once per {{kib}} space.

1. Go to **Management → GenAI Settings**.
2. In the **Agent Builder Traces** section, confirm that **Collect conversation traces** is on and saved.
3. Select **Install Dashboard**.

To open the dashboard, select **View Dashboard**, or open **Dashboards** and select **[Elastic] Agent Builder Overview**.

Repeat these steps in each space where you want the dashboard.

### Reinstall or remove the dashboard

The dashboard is not restored automatically, including in a new space or after you remove it. If it is missing, open the **Agent Builder Traces** section and select **Install Dashboard** again.

To remove it, select the arrow next to **View Dashboard**, then select **Uninstall dashboard**.

## Customize the dashboard

The overview dashboard is managed, so you cannot edit it directly. To build your own version:

1. Open the dashboard.
2. Duplicate it.
3. Edit and save the copy.

Because the original is managed, Elastic can ship improvements to it without overwriting your copy.

## Span and attribute reference

The dashboard panels are [ES|QL](elasticsearch://reference/query-languages/esql.md) queries over your trace data. To build your own visualizations in [Dashboards](/explore-analyze/dashboards.md), [Lens](/explore-analyze/visualize/lens.md), or [Discover](/explore-analyze/discover.md), query the trace data stream and filter by span type and attribute.

Traces are stored in the `traces-agent_builder.otel-*` data stream, where each document is a span. The dashboard identifies the kind of work a span represents from its `span.name`, and reads generative AI details from the span attributes.

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
| `name` | Span name. On `execute_tool` spans it is `execute_tool <tool-id>`, for example `execute_tool platform.core.list_indices`. For the bare tool id, use `attributes.gen_ai.tool.name` |
| `duration` | Span duration in nanoseconds (root field). Divide by 1,000,000,000 for seconds |
| `status.code` | Span status, for example `Error` (root field) |
| `@timestamp` | When the span started |

### Example queries

Use these as starting points, and test them on your own data. They query one space. Replace `default` in `traces-agent_builder.otel-default` with your space id. To query across all spaces at once, use the `traces-agent_builder.otel-*` wildcard, which combines data from every space.

Total input and output tokens by model and provider:

```esql
FROM traces-agent_builder.otel-default
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
FROM traces-agent_builder.otel-default
| WHERE span.name LIKE "execute_tool *"
| STATS
    calls = COUNT(*),
    errors = COUNT(*) WHERE status.code == "Error"
  BY tool = name
| SORT calls DESC
```

## Related pages

<!-- Phase 5. Wire these once targets exist on main:
     - collect-traces.md (#7171)
     - permissions.md
     - monitor-usage.md
     - chat.md
     - builtin-skills-reference.md
     - alerting how-to (#7173) once published -->
