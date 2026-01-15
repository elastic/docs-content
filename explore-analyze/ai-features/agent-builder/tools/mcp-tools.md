---
navigation_title: "MCP tools"
applies_to:
  stack: preview 9.3
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---



# Model Context Protocol (MCP) tools

[Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) tools provide an interface by which Agent Builder can leverage a remote [MCP server's](https://modelcontextprotocol.io/docs/learn/server-concepts) tools during chat sessions. A single Agent Builder MCP tool maps directly to a single MCP server tool. Calling an Agent Builder MCP tool will call the associated tool on the MCP server and return its result.

## Prerequisites 

To create and use MCP tools, an [MCP Kibana Stack Connector](kibana://reference/connectors-kibana/mcp-action-type.md) must first be created. This is the interface by which an Agent Builder MCP tool can communicate with a remote MCP server.

## How it works

When an agent calls an MCP tool:

1. It gets the input schema (effectively, what input parameters the tool requires to when called) from the MCP Kibana Stack Connector
2. The MCP server's tool is called with the correct parameters using the configured connector
3. The result is returned to the LLM and interpreted for the user

There is no post-processing involved between invocation and the result being passed back to the LLM.

## Configuration

MCP tools have the following configuration:

* **`MCP Server`**: The MCP Kibana Stack Connector to interface with
* **`Tool`**: The specific tool on MCP server to create an Agent Builder MCP tool for

Once a tool is selected, the `Description` field of the tool automatically populates with the description given for the tool by the MCP server.

## Monitoring tool health

MCP type tools have built-in health monitoring. Tools that are unhealthy will be indicated as such with an icon next to their IDs in the [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page.

Conditions which may cause an MCP tool to be considered "unhealthy":

* The MCP tool's associated MCP Kibana Stack Connector is unavaiable
* The MCP tool's associated tool on the MCP server no longer exists
* The MCP tool's execution failed

# Bulk import MCP tools 

Agent Builder provides an efficient way to import multiple tools from an MCP server using the `Bulk import MCP tools` feature, which can be found in the Agent Builder [Tools](/explore-analyze/ai-features/agent-builder/tools.md) landing page under the "Manage MCP" dropdown.

## Configuration for bulk tool import

Configuration for importing tools in bulk, while similar to single MCP tool creation, has some extra fields and automated behavior to consider.

* **`MCP Server`**: The MCP Kibana Stack Connector to interface with
* **`Tools to import`**: The specific tools from the MCP server to import
* **`Namespace`**: (Required) A string to prepend to the tool generated tool name to aid in searching and organization. A Namespace must start with a letter and contain only lowercase letters, numbers, and hyphens.

Clicking "Import tools" generates a series of MCP tools that map to the associated MCP server tools that were selected during the bulk import

Imported tools have their `Tool ID` generated as `Namespace.tool-name`, where `Namespace` is the user-provided namespace string, and `tool-name` is the name of the tool as provided by the MCP server. Furthermore, the `Description` field automatically populates.
