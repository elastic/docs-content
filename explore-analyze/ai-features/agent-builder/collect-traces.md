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

## Where to view traces

Traces are stored in {{es}}, but you do not have to query the data stream to read them. {{agent-builder}} gives you three ways to work with collected traces:

| To do this | Use |
|---|---|
| Debug a single agent response, step by step | The **View Trace** waterfall on a conversation round in [Agent Chat](chat.md#view-traces) |
| Monitor token usage, latency, and tool errors across all agents | The [prebuilt overview dashboard](agent-traces-dashboard.md) |
| Ask questions about trace data in natural language | The [built-in traces skill](builtin-skills-reference.md#agent-builder-traces-skill) |

You can also explore the raw spans yourself in [Discover](/explore-analyze/discover.md) or with [ES|QL](elasticsearch://reference/query-languages/esql.md), as described in [Build dashboards on trace data](#build-dashboards-on-trace-data).

## How trace collection works

When an agent runs, {{agent-builder}} records the run as OpenTelemetry (OTel) traces. Each trace covers one conversation round. A trace is made up of spans that map to the work the agent did, such as model calls and tool calls.

Trace collection is space-aware. Each {{kib}} space writes its traces to its own data stream, named with the space id, such as `traces-agent_builder.otel-default` for the `default` space. Use the `traces-agent_builder.otel-*` wildcard to work with every space's traces at once.

{{agent-builder}} ingests this data into managed OpenTelemetry data streams in your {{es}} deployment. Execution spans, such as model calls and tool calls, are stored in `traces-agent_builder.otel-*`, with their timings, token usage, model, and status.

When you opt in to capturing conversation content, that content is stored as span attributes in `traces-agent_builder.otel-*`. The `chat` spans contain the chat history, the model responses, and the system prompt, and the `execute_tool` spans contain the arguments and results of each tool call. Content is captured only when you enable it in [Trace privacy settings](#trace-privacy-settings).

These data streams are OTel-compatible and use the standard OTel index templates, so they inherit the mappings, settings, and data lifecycle that {{es}} maintains for OTel data.

These are regular data streams, not system or hidden indices. You can explore and analyze the data with the same tools you use for any other data in {{es}}, including [Discover](/explore-analyze/discover.md), [Dashboards](/explore-analyze/dashboards.md), [Lens](/explore-analyze/visualize/lens.md), and [ES|QL](elasticsearch://reference/query-languages/esql.md).

### What a trace contains

Each trace is a set of spans that follow a run from the overall conversation round down to its individual steps, including:

- Each agent execution.
- Each model call.
- Each tool call.

Spans follow [OpenTelemetry semantic conventions for generative AI](https://github.com/open-telemetry/semantic-conventions-genai) (currently experimental) and contain generative AI attributes for the model, the provider, and token usage. Use them to break down usage and latency by model, agent, or tool. For the exact fields and the prebuilt visualizations that use them, refer to [Build dashboards on trace data](#build-dashboards-on-trace-data).

By default, traces record structural metadata only. Conversation content such as prompts and responses is excluded unless an administrator opts in. For details, refer to [Trace privacy settings](#trace-privacy-settings).

## Enable and configure trace collection

Trace collection is on by default. To manage it, go to **{{stack-manage-app}}** → **GenAI Settings** and open the **Agent Builder Traces** section.

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
:alt: The expanded Advanced privacy settings, showing seven toggles for including sensitive content in traces
:::

| Setting | Setting ID | Effect when enabled |
|---|---|---|
| **Include user prompts in traces** | `agentBuilder:tracing:includeUserPrompts` | Captures user messages. |
| **Include LLM responses in traces** | `agentBuilder:tracing:includeLlmResponses` | Captures agent responses. |
| **Include tool call details in traces** | `agentBuilder:tracing:includeToolDetails` | Captures tool call arguments and results. |
| **Include system prompt in traces** | `agentBuilder:tracing:includeSystemPrompt` | Captures agent instructions. |
| **Include real tool, agent, and conversation names in traces** {applies_to}`{stack: ga 9.6+, serverless: ga}`<br>**Include real tool and agent names in traces** {applies_to}`stack: ga =9.5` | `agentBuilder:tracing:includeRealNames` | Records real tool, agent, and workflow names instead of anonymized values, and keeps the full tool definitions and descriptions.<br><br>{applies_to}`{stack: ga 9.6+, serverless: ga}` Also records the conversation title. |
| **Include real conversation and workflow IDs in traces** | `agentBuilder:tracing:includeRealIds` | Records real conversation and workflow IDs instead of anonymized values. Also controls the agent ID and the workflow execution ID, which the setting name does not mention. |
| **Include user data in traces** {applies_to}`{stack: ga 9.6+, serverless: ga}` | `agentBuilder:tracing:includeUserData` | Records the real user ID and username of the person who ran the agent, instead of a hash alone. |

:::{note}
Built-in tools and agents always appear under their real names. Anonymized names are replaced with the literal value `custom`, so every custom tool, agent, and workflow shares one value and you cannot tell them apart by name. Anonymized IDs are different: they are replaced with a stable hash, so you can still group and correlate traces by conversation or agent ID. A real conversation ID is a UUID, and an anonymized one is a 16-character hash, so you can tell at a glance which you are looking at. An anonymized custom agent ID keeps a `custom-` prefix, as in `custom-10a91bfdfac987f2`.

User data is the exception to that pattern. Every other setting anonymizes a value in place, keeping the same field. The user fields swap instead. When **Include user data in traces** is off, the username is dropped and the user ID is replaced by a stable hash in `attributes.user.hash`. When the setting is on, `attributes.user.id` and `attributes.user.name` are recorded and `attributes.user.hash` is absent. Account for that if you build dashboards that group by user.
:::

On {{ech}} and {{serverless-full}}, `attributes.user.name` holds the numeric {{ecloud}} user ID rather than a readable username, and `attributes.user.id` holds the user profile ID. To resolve a name, correlate `attributes.user.id` against the [user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-user-profile).

Changing a privacy setting affects only traces recorded after the change. Existing traces are not rewritten. {{agent-builder}} refreshes these settings every 30 seconds, so allow up to that long for a change to take effect, then run a new conversation round to see it.

Content is stored across different span types:
- **`chat` spans**: Store prompts, responses, and the system prompt in the `attributes.gen_ai.input.messages`, `attributes.gen_ai.output.messages`, and `attributes.gen_ai.system_instructions` attributes.
- **`execute_tool` spans**: Store tool call details in `attributes.gen_ai.tool.call.arguments` and `attributes.gen_ai.tool.call.result`.
- **The conversation round span** {applies_to}`{stack: ga 9.6+, serverless: ga}`: Stores the conversation title and the user identity. Only the root `invoke_agent` span carries these, one per conversation round. The nested agent, model, and tool spans do not.

To select that span, combine a span name prefix with the span kind:

```esql
FROM traces-agent_builder.otel-*
| WHERE span.name LIKE "invoke_agent *" AND attributes.elastic.inference.span.kind == "CHAIN"
```

Both conditions are needed. The name prefix on its own also matches the nested agent execution spans, and `CHAIN` on its own also matches the internal `generate_title` span, which carries neither the title nor the user fields. Anonymized names do not break the filter, because an anonymized round is still named `invoke_agent custom`.

| Attribute | Required setting |
|---|---|
| `attributes.elastic.conversation.title` | **Include real tool, agent, and conversation names in traces** |
| `attributes.user.id` | **Include user data in traces** |
| `attributes.user.name` | **Include user data in traces** |
| `attributes.user.hash` | Present only when **Include user data in traces** is off |

Two limits apply to the conversation title:

- It is recorded only for runs that create or continue a saved conversation. Chats always save, and so do runs through the conversation APIs. The [`ai.agent` workflow step](agents-and-workflows.md#use-ai-agent-workflow-step) is the exception: unless it creates a conversation or continues an existing one, nothing is saved and the run has no title attribute.
- Renaming a conversation does not update titles already recorded. Rounds recorded before the rename keep the old title, and the new one appears from the next round onward. A conversation's rounds share the same `attributes.gen_ai.conversation.id`, so to find the current title, take the title from its most recent round.

Anonymization also rewrites the span name, not just the attributes. A custom agent's round appears as `invoke_agent custom` rather than `invoke_agent <your agent name>`, and a custom tool call appears as `execute_tool custom`. Filters that match on a real name in `span.name` return nothing while the names are anonymized.

Anyone who can read the trace data stream can read this content, so review [Grant access to trace data](#grant-access-to-trace-data) before you turn these settings on. For the field-level details, refer to [Message content attributes](agent-traces-dashboard.md#message-content-attributes).

## Grant access to trace data

Trace data is stored in the `traces-agent_builder.otel-*` data stream. To read it, a role needs `read` and `view_index_metadata` on that pattern.

Access is granted at the index level. Any user who can read these data streams can read all collected traces, so trace access is not scoped per user. To control who can read traces, configure index privileges through roles in **Stack Management → Roles**.

{applies_to}`{stack: ga 9.6+, serverless: ga}` When **Include user data in traces** is on, traces identify the person who ran each agent. Anyone who can read the data stream can see which user ran which conversation, so review this section before you turn that setting on.

For the full privilege model, including {{kib}} feature and cluster privileges, refer to [Permissions and access control](permissions.md#read-trace-data).

## Build dashboards on trace data

When trace collection is on, {{agent-builder}} provides a prebuilt overview dashboard for agent activity and token usage. You install or reinstall it per space from the **Agent Builder Traces** settings section. For what each panel shows and the full span and attribute reference, refer to [Agent Builder traces overview dashboard](agent-traces-dashboard.md).

Because traces are stored in regular data streams, you can also build your own visualizations with [Dashboards](/explore-analyze/dashboards.md) and [Lens](/explore-analyze/visualize/lens.md), or query the data with [ES|QL](elasticsearch://reference/query-languages/esql.md). To explore traces in natural language, use the [built-in traces skill](builtin-skills-reference.md#agent-builder-traces-skill).

## Related pages

- [](permissions.md)
- [](monitor-usage.md)
- [](chat.md)
- [](agent-traces-dashboard.md)
- [](builtin-skills-reference.md)
