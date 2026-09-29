---
navigation_title: "Use Context Engine with agents"
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

You can use {{context-engine}} with an {{agent-builder}} agent, an agent built with another framework, or an application that calls the APIs directly.

## How retrieval works

An agent retrieves context from an AI index in three stages:

1. List the AI indices it can access and select one whose name and description match the question.
2. Describe the selected AI index to learn what it contains, which KI types and fields are available, and how to query it.
3. Query the AI index for relevant KIs.

The agent can answer from the retrieved KI when it contains enough information. If the question requires current or more detailed data, the KI can provide a verified query pattern or other guidance for reaching the source.

Access to an AI index and access to its source data are separate. The integration must provide both the {{context-engine}} retrieval operations and any tools and permissions the agent needs to query the source.

## Choose an integration

Choose the integration that matches where you build and run the agent:

| Approach | Use it when | How the agent or application accesses {{context-engine}} |
|---|---|---|
| [{{agent-builder}}](use-context-engine-with-agent-builder.md) | You want to build and run the agent in {{kib}}. | Assign one or more AI indices to the agent. {{agent-builder}} adds the {{context-engine}} retrieval tools and describes the assigned indices in the agent's instructions. |
| [LangChain](langchain-integration.md) | You are building an agent with LangChain or LangGraph. | Load the {{context-engine}} tools through the {{agent-builder}} MCP server, or wrap the {{context-engine}} APIs as LangChain tools. |

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

## Troubleshoot {{context-engine}} retrieval [troubleshoot-context-engine-retrieval]

Use the following table to resolve common retrieval problems across agent integrations:

| Symptom | Cause | Resolution |
|---|---|---|
| Every {{context-engine}} operation returns `403`. | The credential lacks the Kibana **{{context-engine}}** feature privilege. | Add the privilege in the space that contains the AI index. Elasticsearch index privileges alone are not enough. |
| Query or describe operations return `403`. | The credential lacks Elasticsearch privileges on the backing indices. | Grant `read` and `view_index_metadata` on the relevant `ai-index-*` indices. |
| Every {{context-engine}} operation returns `404`. | `contextEngine:enabled` is turned off in the space targeted by the request. | Turn on {{context-engine}} in that space's advanced settings. |
| An expected AI index is not listed. | The credential cannot read its backing index, or its documents belong to another space. | Check the credential's index privileges and the space targeted by the request. |
| A query returns `Unknown index` for an AI index that was listed. | The AI index is registered, but its backing index does not exist yet. | Select an AI index that contains data. |
| A query returns no rows even though the AI index contains data. | The request targets the wrong space, or the query contains its own space condition. | Target the correct space and remove any space condition from the query. |
| The describe operation omits Knowledge Indicator types or tags. | The credential cannot read the backing indices, or `type` and `tags` are not mapped as aggregatable keywords. | Check the index privileges and mappings. Other describe output remains available. |
| The response is too large. | The result exceeds the 20 MB response limit. | Use `KEEP` to return only the required fields, lower the result limit, or aggregate the data with `STATS`. |
