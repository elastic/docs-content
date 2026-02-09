---
navigation_title: "Custom tools"
description: "Learn how to create and manage custom tools in Agent Builder."
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

# Create and manage custom tools

You can extend the built-in tool catalog with your own custom tool definitions. Custom tools offer flexibility in how they interact with your data. This flexibility allows you to create tools that match your specific use cases and data access patterns.

## Tool types

{{agent-builder}} supports several tool types:

- **[ES|QL tools](esql-tools.md)**: Execute pre-defined {{esql}} queries with parameterized inputs for precise, repeatable data retrieval.
- **[Index search tools](index-search-tools.md)**: Scope searches to specific indices or patterns. The LLM dynamically constructs queries based on user requests.
- **[MCP tools](mcp-tools.md)**: Connect to external Model Context Protocol servers, enabling agents to use remote tools and services.
- **[Workflow tools](workflow-tools.md)**: Call pre-defined Workflows directly from the agent chat.

## Create custom tools in the UI

You can create custom tools in the Kibana UI.

To create a custom tool in the UI:

1. Navigate to the **Tools** section on the **Agents** page in Kibana.
2. Click **New tool**.

  :::{image} ../images/new-tool-button.png
  :screenshot:
  :alt: New tool button for creating custom tools
  :width: 150px
  :::

4. Fill in the required fields:
   - **ID**: Enter a unique identifier for your tool (e.g., `get_customer_orders`). Agents use this ID to reference the tool. Refer to [Naming conventions](#naming-conventions) for recommended patterns.
   - **Name**: Enter a descriptive name for your tool.
   - **Description**: Write a clear explanation of what the tool does and when it should be used. Refer to [Writing effective tool descriptions](#writing-effective-tool-descriptions) for guidance.
   - **Type**: Choose a tool type from the list.
   - **Parameters**: For tools with {{esql}} queries, define any parameters your query needs.
   - **Labels**: (Optional) Add labels to categorize and organize your tools.
5. Choose how to save your tool:
   - Select **Save** to create the tool.
   - Select **Save and test** to create the tool and immediately open the testing interface

    :::{image} ../images/tool-save-save-and-test-buttons.png
    :screenshot:
    :alt: Save and Save and test buttons for tool creation
    :width:250px
    :::

## Create custom tools with API

You can also create and manage tools programmatically. To learn more, refer to [Tools API](../tools.md#tools-api).


## Test your tools

Before assigning tools to agents, verify they work correctly by testing them. Testing helps ensure your tool returns useful results and handles parameters correctly.

If you didn't select **Save and test** immediately:

1. Find your tool in the Tools list.
2. Click the test icon (play button) associated with your tool.

:::{image} ../images/test-icon.png
:screenshot:
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

## Assign tools to agents

To start using a custom tool, you must assign it to a [custom agent](../custom-agents.md#create-a-new-agent).
1. Navigate to the agent configuration page.
2. Select the **Tools** tab.
3. Add the desired tools to the agent.
4. Save the agent configuration.

## Best practices

Follow these guidelines to create tools that agents can use effectively.

### Naming conventions

The Tool ID is a critical identifier. Use a namespace prefix to group tools logically, which helps the LLM understand tool relationships and prevents naming collisions.

**Recommended pattern**: `domain.action_entity` or `system.function`

**Examples**:
- `finance.search_ticker`
- `support.get_ticket_details`
- `ecommerce.cancel_order`

### Writing effective tool descriptions

A strong description explains what the tool does, when to use it, and what limitations exist. Include these components:

- **Core purpose**: A high-level summary of what the tool actually does.
- **Trigger**: When should this be called?
- **Action**: What specific data does it retrieve or modify?
- **Limitations**: Are there constraints (for example, "returns max 50 rows" or "data is 24 hours old")?
- **Relationships**: How does it relate to other tools?

:::{tip}
Not sure whether logic belongs in a tool description or in the agent's custom instructions? Refer to [Custom instructions, tool descriptions, or user input](../prompt-engineering.md#custom-instructions-tool-descriptions-or-user-input).
:::

#### Example: Customer support (retrieval)

- **Tool ID**: `support.search_articles`
- **Description**: "Searches the internal Knowledge Base for technical support articles. Use this tool when a user asks about error codes, troubleshooting steps, or product configurations.
  - Input: Requires a natural language query string.
  - Limitations: Returns a maximum of 3 articles.
  - Note: If this tool returns irrelevant results, try the `support.search_tickets` tool to see how similar historical issues were resolved."

#### Example: Finance (data fetching)

- **Tool ID**: `finance.get_transaction_history`
- **Description**: "Retrieves a list of transactions for a specific user account ID.
  - Parameters: `account_id` (required), `start_date` (optional, defaults to 30 days ago).
  - Usage: Use this to analyze spending patterns or find specific charges.
  - Constraint: Data is updated nightly; do not use it for real-time balance checks (use `finance.get_realtime_balance` for that)."

### Additional tips

- **Limit scope**: Focus each tool on a specific task rather than creating overly complex tools.
- **Use meaningful parameter names**: Choose names that clearly indicate what the parameter represents.
- **Include `LIMIT` clauses in {{esql}} queries**: Prevent returning excessive results.
- **Use labels**: Add relevant labels to make tools easier to find and organize.
- **Limit tool count**: More tools are not always better. Keep each agent focused with a limited number of relevant tools.

## Related pages

- [](../prompt-engineering.md)
- [](../tools.md)
- [](builtin-tools-reference.md)
- [](../kibana-api.md#tools-apis)
