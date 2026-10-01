---
navigation_title: "Use an AI index"
description: Learn how to retrieve context from an AI index through the Context Engine APIs, tools, and supported integrations.
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

# Use an AI index

:::{include} _snippets/hidden-docs-notice.md
:::

Use an AI index to retrieve reusable context generated from source data. Applications can call the {{context-engine}} APIs directly. Agents call the same operations through tools that their integration provides, such as the built-in {{agent-builder}} tools or LangChain tools that wrap the APIs. These paths reduce repeated source data discovery and interpretation.

## Query and integration options

Use the following guides to retrieve context through an agent or application:

| Goal | Start here |
| --- | --- |
| Retrieve context directly or compare the available query modes | [Retrieve context from an AI index](retrieve-context-from-ai-index.md) |
| Configure and test an agent that uses an AI index | [Configure agents to use an AI index](use-context-engine-with-agents.md) |
| Use an AI index with an {{agent-builder}} agent | [Use {{context-engine}} with {{agent-builder}}](use-context-engine-with-agent-builder.md) |
| Query an AI index from LangChain or LangGraph | [Query AI indices from LangChain](langchain-integration.md) |

<!--
| Use an AI index from Claude Code with the {{context-engine}} skill and the `elastic` CLI | [Use {{context-engine}} with Claude Code](use-context-engine-with-claude-code.md) |
-->

## How retrieval works

Each supported access path lists the AI indices available to the caller, describes the relevant AI index, and queries it for Knowledge Indicators (KIs). This discovery-first flow provides the correct backing index, field names, and available context instead of requiring the agent or application to guess them. For the complete workflow, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md).

## Related pages

The following pages provide reference and maintenance guidance:

- [{{context-engine}} APIs](context-engine-api.md) lists the available operations and links to their complete {{kib}} API reference.
- [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md) explains how to test retrieved context and improve its automations.
