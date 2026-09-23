---
navigation_title: "Use Context Engine with Agent Builder"
description: Make an AI index available to an Agent Builder agent, configure source access, and test how the agent uses Knowledge Indicators.
type: how-to
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Use Context Engine with {{agent-builder}}

:::{include} _snippets/hidden-docs-notice.md
:::

When you assign an [AI index](concepts.md#ai-indices) to an {{agent-builder}} agent, the agent can retrieve [Knowledge Indicators (KIs)](concepts.md#knowledge-indicators) during a conversation. It can answer from a KI or use the KI's guidance to query source data when the question requires current details.

## Before you begin

You need:

- Context Engine enabled in the current {{kib}} space.
- An AI index that contains at least one KI. To create one, follow [Get started with Context Engine](quickstart.md).
- Access to create or edit an {{agent-builder}} agent and read the AI index.
- Access to the underlying data and an appropriate agent tool if the agent must query source data.

## Add an AI index to an agent

You can assign an AI index while [creating a custom agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-custom-agent) or by editing an existing agent:

1. In {{agent-builder}}, open **Manage components**, then select **Agents**.
2. Create an agent, or open an agent that you can edit.
3. For an existing agent, select **Edit agent settings**. For a new agent, remain on the **Settings** tab.
4. In **AI Indices**, select the AI index under **Additional indices**.
5. Save the agent.

The list contains AI indices registered in the current space that you can access. Some agent types also include default AI indices supplied by Elastic. Default AI indices apply automatically and cannot be removed from the agent.

## Understand what the assignment provides

When an agent has at least one AI index, {{agent-builder}} automatically gives it three dedicated Context Engine tools:

- `list_ai_indices` lists the accessible AI indices and their query targets.
- `describe_ai_index` returns the selected AI index's purpose, fields, KI types, tags, and example queries.
- `query_ai_indices` runs an {{esql}} query against AI indices with the current space applied automatically.

{{agent-builder}} also adds the available AI indices and retrieval guidance to the agent's system instructions. You do not need to add the three tools manually or repeat their sequence in custom instructions.

The assignment provides access to KIs, not to the original source data. If a KI contains an {{esql}} pattern for retrieving current details, the agent also needs a source-query tool such as `platform.core.execute_esql` and permission to read the source indices. For a custom agent, you can enable built-in Elastic capabilities or assign only the source tools required for its task.

## Add task-specific instructions

Use **Custom instructions** to define the agent's scope and the behavior that is specific to your use case. For example:

```text
Use the <AI index ID> AI index for questions about <subject>.
Answer from a retrieved Knowledge Indicator when it contains enough information.
For current values or detailed records, use the KI's query guidance to query the source data.
State when the available data cannot answer the question.
```

Start with concise instructions. Add more detail only when testing reveals a specific behavior that the AI index metadata, KI content, and tool descriptions do not already handle. For general guidance, refer to [Prompt engineering](/explore-analyze/ai-features/agent-builder/prompt-engineering.md).

## Test KI retrieval

Open a conversation with the agent and test the context it can use:

1. Ask a question that a KI should answer directly, such as what a dataset represents or which questions it cannot answer.
2. Confirm that the agent selects the expected AI index and retrieves a relevant KI.
3. If the agent has a source-query tool, ask for a current value or detailed record that requires the KI's query guidance.
4. Confirm that the agent queries the source instead of presenting a stored summary as current data.
5. Ask an out-of-scope question and confirm that the agent does not force an answer from an unrelated KI.

To inspect a conversation round in detail, select **View Trace** and review its model and tool calls. Refer to [View traces for a conversation round](/explore-analyze/ai-features/agent-builder/chat.md#view-traces) for trace availability and privacy settings.

## Improve the result

Use the observed behavior to decide what to change:

| Behavior | What to review |
|---|---|
| The agent does not select the AI index. | Confirm the assignment, then make the AI index name and description more specific to the questions it supports. |
| The agent retrieves the AI index but finds no useful KI. | Review the source coverage, generation strategy, automation, and KI content. |
| The agent treats stored findings as current data. | Clarify freshness and source limitations in the KI, and add a task-specific instruction when necessary. |
| The agent cannot retrieve current details. | Confirm that it has an appropriate source-query tool and permission to read the source data. |
| The agent repeatedly explores the source before answering common questions. | Add reusable findings or tested query guidance to the KIs. |

For a structured review process, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).
