---
navigation_title: "Tools"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

# Tools in {{agent-builder}}

Agents use tools to search, retrieve, and take meaningful steps on your behalf.

Tools can be thought of as functions: modular, reusable actions that agents can call to interact with your {{es}} data.

## How agents use tools

Tools enable agents to work with {{es}} data. When an agent receives a natural language query, it does the following:

1. Analyzes the semantic intent of the request
2. Selects appropriate tools from its available toolset
3. Maps the request parameters to tool input parameters
4. Executes the tools in sequence as needed
5. Processes the structured output data

Each tool is an atomic operation with a defined signature - accepting typed parameters and returning structured results in a format the agent can parse, transform, and incorporate into its response generation.

## Built-in tools

{{agent-builder}} ships with a comprehensive set of built-in tools that provide core capabilities for working with your {{es}} data. These tools are ready to use. They cannot be modified or deleted.

Key built-in tools include:

- **`.execute_esql`**: Executes an {{esql}} query and returns the results in a tabular format
- **`.generate_esql`**: Generates an {{esql}} query from a natural language query
- **`.get_document_by_id`**: Retrieves the full content of an {{es}} document based on its ID and index name
- **`.get_index_mapping`**: Retrieves mappings for the specified index or indices
- **`.index_explorer`**: Lists relevant indices and corresponding mappings based on a natural language query
- **`.list_indices`**: Lists the indices in the {{es}} cluster the current user has access to
- **`.search`**: A powerful tool for searching and analyzing data within a specific {{es}} index

Built-in tools serve as building blocks for more complex interactions and provide the foundation for agent capabilities.

## Custom tools

You can extend the built-in tool catalog with your own custom tool definitions. Custom tools offer flexibility in how they interact with your data:

- **Scoped tools**: Define tools that are scoped to a specific index or pattern, allowing the LLM to decide how to query those indices based on the user's request
- **Explicit query tools**: Define tools with explicit {{esql}} queries for precise, pre-defined data retrieval operations

This flexibility allows you to create tools that match your specific use cases and data access patterns.

### Find available tools

Find the list of available tools on the **Tools** landing page in the UI.

You can also use the following API call, which returns detailed information about built-in tools, including their parameters and descriptions.

```
GET kbn://api/agent_builder/tools
```

## Tool parameters

Parameters enable tools to be dynamic and adaptable to different queries. Each parameter has:

- A **name** that identifies it
- A **type** (such as keyword, number, boolean)
- A **description** that helps the agent understand when and how to use it

For tools with explicit queries, parameters are defined in the query using the syntax `?parameter_name` and must be configured when creating the tool.

Parameters can be:
- **Manually defined**: You explicitly define the parameters a tool needs
- **Inferred from query**: For tools with explicit queries, you can use the "Infer parameters from query" button to automatically detect parameters in your query statement

Providing clear, descriptive parameter names and descriptions helps agents properly use your tools when answering queries.

## Create custom tools

You can create custom tools to help agents interact with your data in specific ways. This section covers how to create and test tools through both the UI and API.

### Use the UI

1. Navigate to the Tools page in Kibana
2. Click the blue **New tool** button
3. Select the tool type you want to create
4. Fill in the required fields:
   - **Name**: Enter a descriptive name for your tool
   - **Description**: Write a clear explanation of what the tool does and when it should be used
   - Tool-specific configuration (explicit query or index settings)
   - **Parameters**: For tools with explicit queries, define any parameters your query needs
   - **Tags**: (Optional) Add labels to categorize and organize your tools
5. Click **Save** to create your tool

### Use the API

You can also create tools programmatically:

For tools with explicit {{esql}} queries:

```json
POST kbn://api/agent_builder/tools
{
  "id": "recent_orders", <1>
  "description": "Find recent orders for a specific customer. Use this tool when users ask about their recent orders or purchase history.", <2>
  "configuration": {
    "query": "FROM orders | WHERE customer_id == ?customer_id | SORT @timestamp DESC | LIMIT 5", <3>
    "params": {
      "customer_id": { <4>
        "type": "keyword",
        "description": "The unique identifier for the customer"
      }
    }
  },
  "type": "esql", <5>
  "tags": ["orders", "customers"] <6>
}
```

1. A unique identifier for your tool that will be used in API calls
2. Detailed description that helps the agent understand when to use this tool
3. {{esql}} query with parameters prefixed by `?`
4. Parameter definition including type and description
5. Tool type specifier (use "esql" for tools with explicit {{esql}} queries)
6. Optional tags for categorization

For index search tools:

```json
POST kbn://api/agent_builder/tools
{
  "id": "search_products", <1>
  "description": "Search the products catalog for specific items. Use this when users are looking for product information.", <2>
  "configuration": {
    "pattern": "products", <3>
    "fields": ["name", "description", "category", "tags"] <4>
  },
  "type": "index_search", <5>
  "tags": ["products", "catalog"] <6>
}
```

1. Unique identifier for the tool
2. Description explaining when and how to use this tool
3. The specific index pattern this tool will search against
4. Fields within the index that should be searchable
5. Tool type specifier (use `index_search` for index search tools)
6. Optional tags for organization

### Testing your tools

After creating a tool, test it before assigning it to agents:

1. Find your tool in the Tools list
2. Click the test icon associated with your tool
3. Enter test values for each parameter or search query
4. Run the test to verify the tool executes correctly and returns the expected results

Testing helps ensure your tool returns useful results and handles parameters correctly.


### Best practices

1. **Write descriptive names**: Use clear, action-oriented names
2. **Provide detailed descriptions**: Explain when and how the tool should be used
3. **Limit scope**: Focus each tool on a specific task rather than creating overly complex tools
4. **Use meaningful parameter names**: Choose names that clearly indicate what the parameter represents
5. **Add comprehensive parameter descriptions**: Help the agent understand what values to use
6. **Include `LIMIT` clauses in explicit queries**: Prevent returning excessive results
7. **Use appropriate tags**: Add relevant tags to make tools easier to find and organize
8. **Limit tool count**: More tools are not always better. Try to keep each agent focused with a limited number of relevant tools.

## Tool namespaces

Tool namespacing helps organize and identify tools by their source. Built-in tools use a consistent prefix (`platform.core`) to indicate they are built-in capabilities. This convention:

- Prevents naming conflicts between system and custom tools
- Makes it easy to identify tool sources
- Provides a consistent pattern for tool identification

## Manage tools

### List available tools

Access the complete list of available tools from the Tools page in Kibana. This view shows:
- Tool names and descriptions
- Tool types
- Associated tags
- Actions (edit, delete, test)

### Assign tools to agents

Tools must be assigned to agents before they can be used:
1. Navigate to the agent configuration page
2. Select the **Tools** tab
3. Add the desired tools to the agent
4. Save the agent configuration

### Update and delete tools

Custom tools can be modified or removed as needed:
1. From the Tools page, find the tool you want to modify
2. Click the edit icon to update the tool or the delete icon to remove it
3. For updates, modify the tool properties and save your changes

Note that built-in tools cannot be modified or deleted.