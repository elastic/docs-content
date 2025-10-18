---
navigation_title: "Agent Builder"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.
:::

# {{agent-builder}} 

{{agent-builder}} is a set of AI-powered capabilities for developing and interacting with agents that work with your {{es}} data. Agent Builder simplifies building data-driven agents with intuitive UI and programmatic interfaces, so you don't have to compose the different pieces separately.

You can use the built-in agent for natural language conversations with any {{es}} data or instance, or work programmatically with tools, agents, and conversations using Elastic APIs, MCP, and A2A.

## Key capabilities

- **Interactive chat interface**: Ask questions about your {{es}} data using natural language in the Agent Chat UI.
- **Agent-based architecture**: Configure AI-powered agents with customizable behaviors and tool access.
- **Modular and extensible tools**: Extend your system with tools for {{es}} data access and manipulation.
- **ES|QL integration**: Create and run [ES|QL](elasticsearch://reference/query-languages/esql.md)-powered tools for specialized data queries.
- **MCP server**: Connect external MCP clients to access chat tools through a standardized interface.
- **A2A server**: Enable agent-to-agent communication following the A2A protocol specification.
- **Programmatic APIs**: Create, manage, and execute tools and agents through Kibana APIs.

## Key concepts

The {{agent-builder}} framework consists of three key components: Agent Chat, Agents, and Tools.

### Agent Chat

**Agent Chat** is the synchronous chat interface for interacting with agents through natural language. The chat UI enables real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents.

[**Learn more about Agent Chat**](agent-builder/chat.md)

### Agents

Agents are powered by custom LLM instructions and the ability to use tools to answer questions, take action, or support workflows. Each agent translates natural language requests into specific actions using the tools assigned to it.

[**Learn more about agents**](agent-builder/agent-builder-agents.md)

### Tools [tools-concept]

Tools are modular, reusable functions that agents use to search, retrieve, and manipulate {{es}} data. Tools are the primary mechanism for connecting agent capabilities to your data.

[**Learn more about tools**](agent-builder/tools.md)

## Get started

To get started you need an Elastic deployment and you must enable the feature.

[**Get started with {{agent-builder}}**](agent-builder/get-started.md)

## Model selection

By default, agents use the Elastic Managed LLM, but you can configure other model providers using connectors, including local LLMs deployed on your infrastructure.

[**Learn more about model selection**](agent-builder/models.md)


## Programmatic interfaces

{{agent-builder}} provides APIs and LLM integration options for programmatic access and automation.
These interfaces enable you to build integrations with other applications and extend {{agent-builder}}'s capabilities to fit your specific requirements.

[**Learn more about programmatic access**](agent-builder/programmatic-access.md)

## Limitations and known issues

{{agent-builder}} is in technical preview.

[**Learn more about limitations and known issues**](agent-builder/limitations-known-issues.md)

