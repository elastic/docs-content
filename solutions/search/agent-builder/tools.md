---
navigation_title: "Tools"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Tools in {{agent-builder}}

[Agents](agent-builder-agents.md) use tools to search, retrieve, and take meaningful steps on your behalf.

Tools can be thought of as functions: modular, reusable actions that agents can call to interact with your {{es}} data.

Each tool is defined by several key fields:

- **`id`**: The unique identifier that agents use to reference the tool (e.g., `.get_document_by_id`)
- **`type`**: Specifies whether the tool is `builtin` (pre-defined) or `esql` (custom)
- **`description`**: Natural language explanation of what the tool does, used by the AI to determine when to use it
- **`configuration`**: Contains the tool's logic - empty for built-in tools, or query and parameters for custom ESQL tools
- **`schema`**: Defines the input parameters the tool requires, written in JSON Schema format

## How agents use tools

Tools enable agents to work with {{es}} data. When an agent receives a natural language query, it does the following:

1. Analyzes the semantic intent of the request
2. Selects appropriate tools from its available toolset
3. Maps the request parameters to tool input parameters
4. Executes the tools in sequence as needed
5. Processes the structured output data

Each tool is an atomic operation with a defined signature - accepting typed parameters and returning structured results in a format the agent can parse, transform, and incorporate into its response generation.

:::{note}
Tool execution and result processing consume tokens. To understand how usage is calculated, refer to [Token usage in Elastic Agent Builder](monitor-usage.md).
:::

## Built-in tools

{{agent-builder}} ships with a comprehensive set of built-in tools that provide core capabilities for working with your {{es}} data. These tools are ready to use. They cannot be modified or deleted.

Key built-in tools include:

- `.execute_esql`: Executes an {{esql}} query and returns the results in a tabular format
- `.generate_esql`: Generates an {{esql}} query from a natural language query
- `.get_document_by_id`: Retrieves the full content of an {{es}} document based on its ID and index name
- `.get_index_mapping`: Retrieves mappings for the specified index or indices
- `.index_explorer`: Lists relevant indices and corresponding mappings based on a natural language query
- `.list_indices`: Lists the indices in the {{es}} cluster the current user has access to
- `.search`: Searches and analyzes data within a specific {{es}} index

Built-in tools serve as building blocks for more complex interactions and provide the foundation for agent capabilities.

:::{note}

Tool namespacing helps organize and identify tools by their source. Built-in tools use a consistent prefix (`platform.core`) to indicate they are built-in capabilities. This convention:

- Prevents naming conflicts between system and custom tools
- Makes it easy to identify tool sources
- Provides a consistent pattern for tool identification

:::

## Custom tools

You can extend the built-in tool catalog with your own custom tool definitions. Custom tools offer flexibility in how they interact with your data:

- **[Index search tools](tools/index-search-tools.md)**: Define tools that are scoped to a specific index or pattern, allowing the LLM to decide how to query those indices based on the user's request.
- **[ES|QL tools](tools/esql-tools.md)**: Define tools with explicit {{esql}} queries for precise, pre-defined data retrieval operations.


This flexibility allows you to create tools that match your specific use cases and data access patterns.

### Tool parameters

Parameters enable tools to be dynamic and adaptable to different queries. Each parameter has:

- A **name** that identifies it
- A **type** (such as keyword, number, boolean)
- A **description** that helps the agent understand when and how to use it

For {{esql}} tools, parameters are defined in the query using the syntax `?parameter_name` and must be configured when creating the tool.

Parameters can be:
- **Manually defined**: You explicitly define the parameters a tool needs
- **Inferred from query**: For {{esql}} tools, you can use the "Infer parameters from query" button to automatically detect parameters in your query statement

The tool's `schema` field defines these parameters using JSON Schema format, specifying:
- **`type`**: Always `"object"` for tool parameters
- **`properties`**: Dictionary defining each parameter's type and description
- **`required`**: Array listing mandatory parameters
- **`additionalProperties`**: Set to `false` to reject undefined parameters

Providing clear, descriptive parameter names and descriptions helps agents properly use your tools when answering queries.

## Create custom tools

You can create custom tools to help agents interact with your data in specific ways. This section covers how to create and test tools in the UI

1. Navigate to the **Tools** section on the **Agents** page in Kibana.
2. Click **New tool**.

  :::{image} images/new-tool-button.png
  :alt: New tool button for creating custom tools
  :width: 150px
  :::

4. Fill in the required fields:
   - **Name**: Enter a descriptive name for your tool.
   - **Description**: Write a clear explanation of what the tool does and when it should be used.
   - **Tool type**: Choose either **[{{esql}}](tools/esql-tools.md)** or **[Index search](tools/index-search-tools.md).**
   - **Parameters**: For tools with {{esql}} queries, define any parameters your query needs.
   - **Tags**: (Optional) Add labels to categorize and organize your tools.
5. Choose how to save your tool:
   - Select **Save** to create the tool.
   - Select **Save and test** to create the tool and immediately open the testing interface

    :::{image} images/tool-save-save-and-test-buttons.png
    :alt: Save and Save and test buttons for tool creation
    :width:250px
    :::

### Testing your tools

Before assigning tools to agents, verify they work correctly by testing them. Testing helps ensure your tool returns useful results and handles parameters correctly.

If you didn't select **Save and test** immediately:

1. Find your tool in the Tools list.
2. Click the test icon (play button) associated with your tool.

:::{image} images/test-icon.png
:alt: Test icon (play button) for running tool tests
:width: 150px
:::
3. Enter test data based on your tool type:
   - **For {{esql}} tools with parameters**: Enter realistic test values for each parameter in the **Inputs** section.
   - **For Index search tools**: Enter a sample search query to test the search functionality.
4. Select **Submit** to run the test.
5. Review the Response section to verify:
   - The tool executes without errors.
   - Results are returned in the expected format.
   - The data matches your expectations.
6. Now you can [assign the tool to an agent](#assign-tools-to-agents).

### Best practices

1. **Write descriptive names**: Use clear, action-oriented names.
2. **Provide detailed descriptions**: Explain when and how the tool should be used.
3. **Limit scope**: Focus each tool on a specific task rather than creating overly complex tools.
4. **Use meaningful parameter names**: Choose names that clearly indicate what the parameter represents.
5. **Add comprehensive parameter descriptions**: Help the agent understand what values to use.
6. **Include `LIMIT` clauses in {{esql}} queries**: Prevent returning excessive results.
7. **Use appropriate tags**: Add relevant tags to make tools easier to find and organize.
8. **Limit tool count**: More tools are not always better. Try to keep each agent focused with a limited number of relevant tools.

## Manage tools

### Find available tools

Find the list of available tools on the **Tools** landing page in the UI, or use [Tools API](kibana-api.md#tools).

:::{image} images/tools-overview.png
:alt: Tools landing page showing the list of available tools with their descriptions and actions
:width:800px
:::

### List available tools

Access the complete list of available tools from the **Tools** page in Kibana. This view shows:
- Tool names and descriptions
- Tool types
- Associated tags
- Actions (edit, delete, test)

### Assign tools to agents

Tools must be assigned to agents before they can be used:
1. Navigate to the agent configuration page.
2. Select the **Tools** tab.
3. Add the desired tools to the agent.
4. Save the agent configuration.

### Update and delete tools

Custom tools can be modified or removed as needed:
1. From the Tools page, find the tool you want to modify.
2. Select the edit icon to update the tool or the delete icon to remove it.
3. For updates, modify the tool properties and save your changes.

Note that built-in tools cannot be modified or deleted.

## Tools API

For a quick overview of how to work programmatically with tools, refer to [Tools API](kibana-api.md#tools).

### API reference

For the complete API reference, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-tools).

## Copy your MCP server URL

Tools can also be accessed through the Model Context Protocol (MCP) server, which provides a standardized interface for external clients to use Agent Builder tools.

The **Tools** UI provides a **Copy your MCP server URL** button for easy access.

:::{image} images/copy-mcp-server-url-button.png
:alt: Copy MCP server URL button for easy configuration of external clients
:width: 250px
:::

:::{important}
There is a [known issue](limitations-known-issues.md#mcp-server-url-copy-button-omits-space-name) with the copy button in 9.2.
:::

For detailed MCP server configuration, refer to [MCP server](mcp-server.md).
