---
navigation_title: "Agent Builder"
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}}

{{agent-builder}} combines large language models with Elastic-native features for prompt engineering, context engineering, and automation. Key use cases enabled by Agent Builder include:

- **Chat with your {{es}} data immediately** using the chat interface, preconfigured agents, and built-in tools available out of the box.
- **Build custom agents and tools** tailored to your specific use cases using the UI or APIs.
- **Import tools from external MCP servers** to give your agents additional capabilities.
- **Expose tools and agents to external systems** like Claude Desktop, Cursor, and LangChain apps through the MCP server, A2A server, and REST APIs.

**[Learn more in key capabilities](#key-capabilities)**

## Get started

To get started you need an Elastic deployment and you might need to enable the feature.

[**Get started with {{agent-builder}}**](agent-builder/get-started.md)

This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).


## Key capabilities

- **{{es}} relevance and security**: Leverage {{es}}'s search capabilities for precise context retrieval, with [secure data access controls](agent-builder/permissions.md).
- **Built-in agents and tools**: Get started immediately with pre-configured [agents](agent-builder/builtin-agents-reference.md) and [tools](agent-builder/tools/builtin-tools-reference.md) available out of the box.
- **Chat UI**: [Chat with agents](agent-builder/chat.md) in real time using natural language.
- **Custom and external tools**: Build targeted [custom tools](agent-builder/tools/custom-tools.md) to deliver precise context, or import external tools through the [Model Context Protocol](agent-builder/tools/mcp-tools.md).
- **Custom agents**: Create [agents with tailored instructions](agent-builder/custom-agents.md) and toolsets for specific use cases.
- **MCP and A2A servers**: Expose tools and agents to external clients through the [MCP server](agent-builder/mcp-server.md) and [A2A server](agent-builder/a2a-server.md).
- **Kibana REST APIs**: Work with Agent Builder functionalities [programmatically](agent-builder/kibana-api.md), including agents, tools, and conversations.
- **[Elastic Workflows](/explore-analyze/workflows.md) integration**: Automate complex processes within your deployment using the Elastic-native automation engine. Your agents can [trigger workflows](agent-builder/agents-and-workflows.md) and [workflows can invoke agents](agent-builder/agents-and-workflows.md) in their steps.

## Key concepts

The {{agent-builder}} framework consists of three key components: Agent Chat, Agents, and Tools.

### Agent Chat

**Agent Chat** is the synchronous chat interface for interacting with agents through natural language. The chat UI enables real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents. You can also chat with agents programmatically.

[**Learn more about Agent Chat**](agent-builder/chat.md)

### Agents

Agents are powered by custom LLM instructions and the ability to use tools to answer questions, take action, or support workflows. Each agent translates natural language requests into specific actions using the tools assigned to it. Choose from a set of built-in agents, or create your own.

[**Learn more about agents**](agent-builder/agent-builder-agents.md)

### Tools [tools-concept]

Tools are modular, reusable functions that agents use to search, retrieve, and manipulate {{es}} data. Tools are the primary mechanism for connecting agent capabilities to your data. Choose from a set of built-in tools, or create your own and assign them to your custom agents.

[**Learn more about tools**](agent-builder/tools.md)

## Model selection

On {{ech}} and {{serverless-full}}, {{agent-builder}} comes with preconfigured models ready to use. You can also configure other model providers using connectors, including local LLMs deployed on your infrastructure.

[**Learn more about model selection**](agent-builder/models.md)


## Programmatic interfaces

{{agent-builder}} provides APIs and LLM integration options for programmatic access and automation.
These interfaces enable you to build integrations with other applications and extend {{agent-builder}}'s capabilities to fit your specific requirements.

[**Learn more about programmatic access**](agent-builder/programmatic-access.md)

## Permissions and access control

Configure security roles and API keys to control who can use agents, which tools they can access, and what data they can query.

[**Learn more about permissions and access control**](agent-builder/permissions.md)

## Monitor usage

Understand how tokens are calculated and accumulated during agent execution to predict the impact on your usage and costs.

[**Learn more about token usage**](agent-builder/monitor-usage.md)

## Troubleshooting

Find solutions to common problems when working with {{agent-builder}}.

[**Learn more about troubleshooting**](agent-builder/troubleshooting.md)

## Limitations and known issues

Understand current limitations and known issues with {{agent-builder}}.

[**Learn more about limitations and known issues**](agent-builder/limitations-known-issues.md)

