---
navigation_title: "MCP tools"
applies_to:
  stack: preview 9.3
  serverless: preview
---



# Model Context Protocol (MCP) tools

Agent Builder MCP tools enable calling a remote [MCP server's](https://modelcontextprotocol.io/docs/learn/server-concepts) tools in your agent [chat](../chat.md). When you call an Agent Builder MCP tool, it calls the associated tool on the MCP server and returns its result.

## Prerequisites

To use external MCP tools, you first need to set up an [MCP Kibana Stack Connector](kibana://reference/connectors-kibana/mcp-action-type.md). This interface enables Agent Builder MCP tools to communicate with a remote MCP server.

## How it works

When an agent calls an MCP tool:

1. Agent Builder retrieves the tool's input schema from the MCP Kibana Stack Connector.
2. Agent Builder calls the MCP server tool with the required parameters.
3. The MCP server returns the result directly to the LLM with no post-processing.
4. The LLM interprets the result for the user.

## Configuration

:::{image} ../images/mcp-createnewtool-config-example.png
:screenshot:
:alt: Example configuration for a new MCP tool with the Context7 MCP server.
:width: 800px
:::

MCP tools have the following configuration:

MCP Server
:   The MCP Kibana Stack Connector to interface with.

Tool
:   The specific tool on MCP server to create an Agent Builder MCP tool for.

Once a tool is selected, the `Description` field of the tool automatically populates with the description provided by the MCP server.

## Monitoring tool health

MCP type tools have built-in health monitoring. Tools that are unhealthy display an icon next to their IDs in the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page.

An MCP tool is marked "unhealthy" when:

* The MCP tool's associated MCP Kibana Stack Connector is unavaiable
* The MCP tool's associated tool on the MCP server no longer exists
* The MCP tool's execution failed

## Bulk import MCP tools

:::{image} ../images/mcp-bulkimport-location.png
:screenshot:
:alt: How to bulk import MCP tools from an MCP server.
:width: 500px
:::

Agent Builder provides an efficient way to import multiple tools from an MCP server using the `Bulk import MCP tools` feature, which can be found in the Agent Builder [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page under the "Manage MCP" dropdown.

## Configuration for bulk tool import

:::{image} ../images/mcp-bulkimport-config-example.png
:screenshot:
:alt: Example configuration for bulk importing MCP tools from the Context7 MCP server.
:width: 800px
:::

Configuration for importing tools in bulk, while similar to single MCP tool creation, has some extra fields and automated behavior to consider.

MCP Server
:   The MCP Kibana Stack Connector to interface with.

Tools to import
:   The specific tools from the MCP server to import.

Namespace
:   A string to prepend to the tool name to aid in searching and organization. A namespace must start with a letter and contain only lowercase letters, numbers, and hyphens.

Clicking "Import tools" generates a series of MCP tools that map to the associated MCP server tools that were selected.

Imported tools have their `Tool ID` generated as `ramespace.tool-name`, where `namespace` is the user-provided namespace string, and `tool-name` is the name of the tool as provided by the MCP server. Furthermore, the `Description` field automatically populates.
