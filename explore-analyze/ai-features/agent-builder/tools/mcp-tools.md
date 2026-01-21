---
navigation_title: "MCP tools"
applies_to:
  stack: preview 9.3+
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Model Context Protocol (MCP) tools

Agent Builder MCP tools enable calling a remote [MCP server's](https://modelcontextprotocol.io/docs/learn/server-concepts) tools in your agent [chat](../chat.md). When your agent calls an MCP tool, it executes the associated tool on the MCP server and returns its result.

## Prerequisites

To use external MCP tools, you first need to set up an [MCP connector](kibana://reference/connectors-kibana/mcp-action-type.md). This interface enables Agent Builder MCP tools to communicate with a remote MCP server.

## Adding MCP tools

You can import MCP tools individually or in bulk.

### Add a single tool

Once you've set up an MCP connector, click "New tool" on the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page and select the `MCP` tool type.

:::{image} ../images/mcp-createnewtool-config-example.png
:screenshot:
:alt: Example configuration for a new MCP tool with the Context7 MCP server.
:width: 800px
:::

#### Configuration

Individual MCP tools have the following configuration settings:

MCP Server
:   The MCP connector to interface with.

Tool
:   The specific tool on MCP server to create an Agent Builder MCP tool for.

Once a tool is selected, the `Tool ID` and `Description` fields automatically populate with the tool name and description provided by the MCP server.

### Bulk import MCP tools

To import multiple tools at once, go to the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page and select **Bulk import MCP tools** from the "Manage MCP" dropdown.

:::{image} ../images/mcp-bulkimport-location.png
:screenshot:
:alt: How to bulk import MCP tools from an MCP server.
:width: 500px
:::

Configure the following fields:

MCP Server
:   The MCP connector to interface with.

Tools to import
:   The specific tools from the MCP server to import.

Namespace
:   A string to prepend to the tool name to aid in searching and organization. A namespace must start with a letter and contain only lowercase letters, numbers, and hyphens.

:::{image} ../images/mcp-bulkimport-config-example.png
:screenshot:
:alt: Example configuration for bulk importing MCP tools from the Context7 MCP server.
:width: 800px
:::

After clicking **Import tools**, Agent Builder creates an MCP tool for each selection.

Each tool's ID is generated as `namespace.tool-name` (for example, `context7.resolve-library-id`), and descriptions are populated automatically from the MCP server.

## How MCP tool calls work

When an agent calls an MCP tool:

1. Agent Builder retrieves the tool's input schema from the MCP connector.
2. Agent Builder calls the MCP server tool with the required parameters.
3. The MCP server returns the result directly to the LLM with no post-processing.
4. The LLM interprets the result for the user.

## Monitoring tool health

MCP tools have built-in health monitoring. Tools that are unhealthy display an icon next to their IDs in the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page.

An MCP tool is marked "unhealthy" when:

* The MCP tool's associated MCP connector is unavaiable.

    :::{image} ../images/mcp-connector-unavailable.png
    :screenshot:
    :alt: Connector unavailable icon.
    :width: 100px
    :::

* The MCP tool's associated tool on the MCP server no longer exists.

    :::{image} ../images/mcp-tool-not-found.png
    :screenshot:
    :alt: Tool not found icon.
    :width: 100px
    :::

* The MCP tool's execution failed.

    :::{image} ../images/mcp-tool-execution-failed.png
    :screenshot:
    :alt: Tool execution failed icon.
    :width: 100px
    :::

## Related pages

* [Tools](/explore-analyze/ai-features/agent-builder/tools.md)
* [ES|QL tools](/explore-analyze/ai-features/agent-builder/tools/esql-tools.md)
* [Index search tools](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md)
