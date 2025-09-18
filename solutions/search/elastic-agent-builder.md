---
navigation_title: "Agent Builder"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

# {{agent-builder}} 

{{agent-builder}} is an AI-powered conversation framework for working with {{es}} data using natural language. It features both a chat UI for synchronous interaction and extensive programmatic access through APIs, MCP and A2A servers.

## Key capabilities

- **Interactive chat interface**: Ask questions about your {{es}} data using natural language in the Agent Chat UI.
- **Agent-based architecture**: Configure AI-powered agents with customizable behaviors and tool access.
- **Modular and extensible tools**: Extend your system with tools for {{es}} data access and manipulation.
- **ES|QL integration**: Create and execute [ES|QL](elasticsearch://reference/query-languages/esql.md)-powered tools for specialized data queries.
- **MCP server**: Connect external MCP clients to access chat tools through a standardized interface.
- **A2A server**: Enable agent-to-agent communication following the A2A protocol specification.
- **Programmatic APIs**: Create, manage, and execute tools and agents through Kibana APIs.

## Key concepts

The {{agent-builder}} framework is built around several key components that work together to provide a flexible and powerful conversational experience.

### Agent Chat UI

The **Agent Chat** UI is the synchronous chat interface for interacting with agents through natural language. The chat UI enables real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents.

[**Learn more about Agent Chat**](agent-builder/chat.md)

### Agents

Agents are powered by custom LLM instructions and the ability to use tools to answer questions, take action, or support workflows. Each agent translates natural language requests into specific actions using the tools assigned to it.

[**Learn more about agents**](agent-builder/agent-builder-agents.md)

### Tools [tools-concept]

Tools are modular, reusable functions that agents use to search, retrieve, and manipulate {{es}} data. Tools are the primary mechanism for connecting agent capabilities to your data.

[**Learn more about tools**](agent-builder/tools.md)

## Programmatic interfaces

{{agent-builder}} provides APIs and LLM integration options for programmatic access and automation.
These interfaces enable you to build integrations with other applications and extend {{agent-builder}}'s capabilities to fit your specific requirements.

[**Learn more about programmatic access**](agent-builder/programmatic-access.md)

## Get started

To get started you need an Elastic deployment and you must enable the feature.

[**Get started with {{agent-builder}}**](agent-builder/get-started.md)

