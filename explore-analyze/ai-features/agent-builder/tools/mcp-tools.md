---
navigation_title: "MCP tools"
description: "Connect to external MCP servers to enable agents to use remote tools and services."
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

# Model Context Protocol (MCP) tools in {{agent-builder}}

Agent Builder MCP tools enable calling a remote [MCP server's](https://modelcontextprotocol.io/docs/learn/server-concepts) tools in your agent [chat](../chat.md). For example, you can import a documentation-lookup tool from an external service so your agent can fetch current library docs during a conversation. When your agent calls an MCP tool, it executes the associated tool on the MCP server and returns its result.

:::{note}
On this page, {{agent-builder}} acts as the MCP client: your agents connect to an external MCP server to use its tools. To instead let external MCP hosts use your {{agent-builder}} tools, refer to [](../mcp-server.md).
:::

## Prerequisites

To use external MCP tools, you first need to set up an [MCP connector](kibana://reference/connectors-kibana/mcp-action-type.md). This interface enables Agent Builder MCP tools to communicate with a remote MCP server.

## Adding MCP tools

You can import MCP tools individually or in bulk.

### Add a single tool

After you set up an MCP connector, click **+ New tool** on the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page and select the **MCP** tool type. The following screenshot shows an example configuration:

:::{image} ../images/mcp-createnewtool-config-example.png
:screenshot:
:alt: Example configuration for a new MCP tool with the Context7 MCP server, including the Require user confirmation policy set to Never.
:width: 800px
:::

#### Configuration

Individual MCP tools have the following configuration settings:

**MCP Server**
:   The MCP connector to interface with.

**Tool**
:   The specific tool on MCP server to create an Agent Builder MCP tool for.
:   After you select a tool, the **Tool ID** and **Description** fields automatically populate with the tool name and description provided by the MCP server.

**Require user confirmation** {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`
:   Controls whether the agent asks you to approve a call to this tool before it runs. Select **Never** (default) to run without a prompt, **Once** to prompt the first time the agent calls the tool in a conversation, or **Always** to prompt on every call. For details, refer to [Require confirmation before a tool runs](custom-tools.md#require-confirmation-before-a-tool-runs).

### Bulk import MCP tools

To import multiple tools at once, go to the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page and select **Bulk import MCP tools** from the **Manage MCP** dropdown. The following screenshot shows where to find this option:

:::{image} ../images/mcp-bulkimport-location.png
:screenshot:
:alt: How to bulk import MCP tools from an MCP server.
:width: 500px
:::

Configure the following fields:

**MCP Server**
:   The MCP connector to interface with.

**Tools to import**
:   The specific tools from the MCP server to import.

**Namespace**
:   A string to prepend to the tool name to aid in searching and organization. A namespace must start with a letter and contain only lowercase letters, numbers, and hyphens.

The following screenshot shows an example bulk import from the Context7 MCP server:

:::{image} ../images/mcp-bulkimport-config-example.png
:screenshot:
:alt: Example configuration for bulk importing MCP tools from the Context7 MCP server.
:width: 800px
:::

After you click **Import tools**, Agent Builder creates an MCP tool for each selection.

Each tool's ID is generated as `namespace.tool-name` (for example, `context7.resolve-library-id`), and descriptions are populated automatically from the MCP server.

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Bulk import doesn't configure confirmation, so each imported tool starts with **Require user confirmation** set to **Never**. To require confirmation for an imported tool, edit it after import.

## How MCP tool calls work

When an agent calls an MCP tool:

1. Agent Builder retrieves the tool's input schema from the MCP connector.
2. Agent Builder calls the MCP server tool with the required parameters.
3. The MCP server returns the result directly to the LLM with no post-processing.
4. The LLM interprets the result for the user.

## Monitoring tool health

MCP tools have built-in health monitoring. Tools that are unhealthy display an icon next to their IDs on the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page.

An MCP tool is marked "unhealthy" when:

* The MCP tool's associated MCP connector is unavailable. The tool shows this icon:

    :::{image} ../images/mcp-connector-unavailable.png
    :screenshot:
    :alt: Connector unavailable icon.
    :width: 100px
    :::

* The MCP tool's associated tool on the MCP server no longer exists. The tool shows this icon:

    :::{image} ../images/mcp-tool-not-found.png
    :screenshot:
    :alt: Tool not found icon.
    :width: 100px
    :::

* The MCP tool's execution failed. The tool shows this icon:

    :::{image} ../images/mcp-tool-execution-failed.png
    :screenshot:
    :alt: Tool execution failed icon.
    :width: 100px
    :::

## Related pages

* [Tools](/explore-analyze/ai-features/agent-builder/tools.md)
* [ES|QL tools](/explore-analyze/ai-features/agent-builder/tools/esql-tools.md)
* [Index search tools](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md)
