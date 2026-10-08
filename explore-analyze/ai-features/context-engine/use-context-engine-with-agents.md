---
navigation_title: "Configure agents"
description: Configure source access, instructions, and testing for an agent that retrieves context from AI indices.
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

# Configure agents to use an AI index

:::{include} _snippets/hidden-docs-notice.md
:::

An agent that retrieves context from an AI index might also need tools and permissions to query source data when a [Knowledge Indicator (KI)](concepts.md#knowledge-indicators) points to current details. This page explains how to provide that access, tell the agent when to use the AI index, and test the integration. For the list, describe, and query sequence itself, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md).

For implementation steps, follow the guide for [{{agent-builder}}](use-context-engine-with-agent-builder.md) or [LangChain and LangGraph](langchain-integration.md).

## Provide access to context and source data

Access to an AI index and access to its source data are separate. Provide the agent with both the {{context-engine}} retrieval operations and any tools and permissions it needs to query the source.

The agent only discovers AI indices that its credentials can read in the current {{kib}} space. A retrieved KI can answer a question directly or provide tested guidance for retrieving current details from source data.

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
