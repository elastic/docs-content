---
navigation_title: "Agents and apps"
description: Learn how agents and applications retrieve Knowledge Indicators from AI indices and use them to answer questions or find current source data.
type: overview
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Use {{context-engine}} with agents and applications

:::{include} _snippets/hidden-docs-notice.md
:::

Agents use {{context-engine}} to retrieve reusable context from [AI indices](concepts.md#ai-indices) before spending time and model tokens interpreting source data. A [Knowledge Indicator (KI)](concepts.md#knowledge-indicators) can answer a question directly or give the agent tested guidance for finding current details in the source.

You can use {{context-engine}} with an {{agent-builder}} agent, an agent built with another framework, or an application that calls the [{{context-engine}} APIs](context-engine-api.md) directly.

Agents use {{context-engine}} retrieval operations to find an appropriate AI index and retrieve relevant KIs. For the common list, describe, and query workflow, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md).

A retrieved KI can answer a question directly or provide tested guidance for retrieving current details from source data.

Access to an AI index and access to its source data are separate. The integration must provide both the {{context-engine}} retrieval operations and any tools and permissions the agent needs to query the source.

## Choose an integration

Choose the integration that matches where you build and run the agent:

| Approach | Use it when | How the agent or application accesses {{context-engine}} |
|---|---|---|
| [{{agent-builder}}](use-context-engine-with-agent-builder.md) | You want to build and run the agent in {{kib}}. | Assign one or more AI indices to the agent. {{agent-builder}} adds the {{context-engine}} retrieval tools and describes the assigned indices in the agent's instructions. |
| [LangChain](langchain-integration.md) | You are building an agent with LangChain or LangGraph. | Wrap the {{context-engine}} APIs as LangChain tools in your application. |

Both approaches list and describe AI indices before querying them. The agent only discovers AI indices that its credentials can read in the current {{kib}} space.

## Define when the agent should use context

The AI index name and description help the agent decide whether its KIs are relevant. Write them around the subject and questions the AI index supports, rather than the implementation that produced it.

Agent instructions can further define when to use the context, when to query source data, and how to communicate source limitations. Keep these instructions specific to the agent's task. The retrieval tools already tell the agent how to list, describe, and query AI indices.

{{agent-builder}} also includes [{{context-engine}} skills](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-context-engine-skills) for planning AI indices, configuring sources and automations, evaluating retrieval results, and retrieving KIs. These skills support {{context-engine}} work, but they do not replace the AI index assignment or the tools required to access source data.

## Evaluate the integration

Test the agent with questions that exercise both paths:

- Ask a recurring question that a KI should answer directly.
- Ask for current or detailed information that requires the agent to follow the KI's guidance and query the source.
- Ask an out-of-scope question to confirm that the agent recognizes the AI index's limits.

Inspect the agent's tool calls to confirm that it selected the expected AI index, retrieved a relevant KI, and queried source data only when needed. If the generated context is incomplete or misleading, [evaluate and improve the KIs](evaluate-and-improve-knowledge-indicators.md) instead of compensating with increasingly detailed agent instructions.

Across a representative set of questions, compare response quality, tool calls, source queries, latency, and model token use. Repeated or related questions are especially useful because they show whether the AI index prevents agents from rediscovering the same information.

For common access and retrieval failures, refer to [Troubleshoot retrieval](retrieve-context-from-ai-index.md#troubleshoot-retrieval).
