---
navigation_title: "Tools"
description: "Learn how Agent Builder tools enable agents to search data and perform actions in Elasticsearch. Explore built-in tools, custom tool definitions, and MCP integration."
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

# Tools in {{agent-builder}}

[Agents](agent-builder-agents.md) use tools to search, retrieve, and take actions on your behalf.

Tools can be thought of as functions: modular, reusable actions that agents can call to interact with your {{es}} data. Skills are higher-level capabilities that coordinate tools into domain-specific workflows. To learn more, refer to [Skills](skills.md).

## How agents use tools

Tools enable agents to work with {{es}} data. When an agent receives a natural language query, it does the following:

1. Analyzes the semantic intent of the request
2. Selects appropriate tools from its available toolset
3. Maps the request parameters to tool input parameters
4. Executes the tools in sequence as needed
5. Processes the structured output data

Each tool is an atomic operation with a defined signature. Tools accept typed parameters and return structured results in a format the agent can parse, transform, and incorporate into its response generation.

:::{note}
Tool execution and result processing consume tokens. To understand how usage is calculated, refer to [Token usage in Elastic Agent Builder](monitor-usage.md).
:::

## Built-in tools

{{agent-builder}} ships with a comprehensive set of built-in tools that provide core capabilities for working with your {{es}} data. These tools are ready to use. They cannot be modified or deleted.

Built-in tools serve as building blocks for more complex interactions and provide the foundation for agent capabilities.

For the complete list, refer to [Built-in tools reference](tools/builtin-tools-reference.md).

:::{note}
Some built-in skills also include inline tools that are only available while that skill is active and are not listed in the tools reference. For details, refer to [Built-in skills reference](builtin-skills-reference.md).
:::

## Custom tools

You can extend the built-in tool catalog with your own custom tool definitions. To learn how to create and manage custom tools, refer to [Custom tools](tools/custom-tools.md).

## Manage tools

You can view, organize, and manage tools from the **Tools** page in {{kib}} or programmatically using the [Tools API](kibana-api.md#tools-apis).

   :::::{applies-switch}

   ::::{applies-item} { stack: ga 9.4+, serverless: ga }

    Access the Tools page from **Manage components** at the bottom of the left sidebar, or from **Customize > Tools > Manage all tools** on an agent's page.
   ::::

   ::::{applies-item} { stack: ga =9.3 }

    Access the Tools page from the key actions menu in the Agent Chat UI.

   ::::
   
   :::::

The Tools page lists each tool by ID and description. Use the search bar or filter by labels to find specific tools. Built-in tools are marked with a lock icon (🔒).

:::{image} images/tools-overview.png
:screenshot:
:alt: Tools landing page showing the list of available tools with their descriptions and actions
:width: 600px
:::

{applies_to}`stack: ga 9.4+` The Tools page also includes a **Manage MCP** dropdown (for MCP server configuration and bulk imports) and a **Manage agents** link for quick navigation to the global agents list.

### Update and delete tools

[Custom tools](tools/custom-tools.md) can be modified or removed as needed:
1. From the Tools page, find the tool you want to modify.
2. Select the edit icon to update the tool or the delete icon to remove it.
3. For updates, modify the tool properties and save your changes.

:::{note}
Built-in tools cannot be modified or deleted.
:::

## Tools API

For a quick overview of how to work programmatically with tools, refer to [Tools API](kibana-api.md#tools-apis).

### API reference

For the complete API reference, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-tools).

## MCP server access

Tools can also be accessed through the Model Context Protocol (MCP) server, which provides a standardized interface for external clients to use Agent Builder tools.

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

On the Tools page, open the **Manage MCP** dropdown to access:

- **Copy MCP Server URL**: Copy the MCP server URL for configuring external clients.
- **Bulk import MCP tools**: Import multiple tools from an MCP server at once.
- **Documentation**: Open the MCP documentation.

:::{image} images/copy-mcp-server-url-button.png
:screenshot:
:alt: Manage MCP dropdown showing Copy MCP Server URL, Bulk import MCP tools, and Documentation options
:width: 250px
:::

::::

::::{applies-item} { stack: ga 9.2-9.3 }

The **Tools** UI provides a **Copy your MCP server URL** button for easy access.

::::

:::::

:::{important}
There is a [known issue](limitations-known-issues.md#mcp-server-url-copy-button-omits-space-name) with the copy button in 9.2.
:::

For detailed MCP server configuration, refer to [MCP server](mcp-server.md).
