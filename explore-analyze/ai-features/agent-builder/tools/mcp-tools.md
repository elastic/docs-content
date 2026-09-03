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

Once you've set up an MCP connector, click **+ New tool** on the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page and select the **MCP** tool type.

<!-- [TODO-SC] STILL OUTSTANDING -- this is the last piece of test B6 and needs a 9.6 or serverless cluster to recapture. The image was last updated 2026-01-20, six months before kibana#281896 (merged 2026-07-31) added the "Require user confirmation" select to the MCP tool Configuration panel, so it does not show the control. Re-verified at kibana HEAD 056473990ad7 on 2026-09-03: mcp_configuration_fields.tsx renders <ConfirmationPolicySelect /> at line 74, at the bottom of the panel and OUTSIDE the isCreatingTool branch (that branch only swaps McpEditableFields for McpReadOnlyFields inside the panel), so the control appears on both the create form and the tool detail view. Match the existing 800px width and crop so the page does not reflow. Do NOT recapture mcp-bulkimport-config-example.png -- the bulk import flow has no confirmation control. -->
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

Require user confirmation (Optional) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
:   Controls whether the agent asks you to approve a tool call before it runs. Select **Never** to run without a prompt, **Once** to prompt the first time the agent calls the tool in a conversation, or **Always** to prompt on every call. The default is **Never**.
:   With **Once**, your response applies to every later call to the tool in the same conversation, whether you confirmed or denied the action. This includes retries after a failed call.
:   Confirmation applies only when an agent calls the tool. Refer to [Human-in-the-loop prompts](../chat.md#human-in-the-loop-prompts).

Once you select a tool, the `Tool ID` and `Description` fields automatically populate with the tool name and description provided by the MCP server.


<!-- [TODO-CHECK] TERM STYLE, decision only -- now settled which page is wrong. Checked 2026-09-03: THIS page is the one that diverges. Its definition-list terms are bare plain text UI labels (MCP Server, Tool, Require user confirmation, Tools to import, Namespace), and style-guide/ui-writing.md:21 says "Use **bold** for component names and match the capitalization as it appears in the UI." workflow-tools.md bolds its six terms and is correct. The other two tools pages that look unbolded are NOT comparable: index-search-tools.md (`pattern`, `row_limit`) and builtin-tools-reference.md (`platform.core.*`) use code font for API identifiers and tool IDs, which is right for those. So the fix is to bold all six terms on this page -- five are pre-existing, one is new in this PR. CLAUDE.md leans towards fixing ("when content obviously diverges from the documented best practices, prefer fixing or improving it over matching the divergence"); the alternative is to leave it and raise in review. Decide before the PR. -->

### Bulk import MCP tools

To import multiple tools at once, go to the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page and select **Bulk import MCP tools** from the **Manage MCP** dropdown.

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

Bulk import does not set a confirmation policy, so each imported tool starts with **Require user confirmation** set to **Never**. To require confirmation for an imported tool, edit the tool after import. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`


## How MCP tool calls work

When an agent calls an MCP tool:

1. Agent Builder retrieves the tool's input schema from the MCP connector.
2. Agent Builder calls the MCP server tool with the required parameters.
3. The MCP server returns the result directly to the LLM with no post-processing.
4. The LLM interprets the result for the user.

## Monitoring tool health

MCP tools have built-in health monitoring. Tools that are unhealthy display an icon next to their IDs on the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) page.

An MCP tool is marked "unhealthy" when:

* The MCP tool's associated MCP connector is unavailable.

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
