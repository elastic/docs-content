---
navigation_title: "Kibana API tutorial"
description: "Learn how to create custom agents and tools using the Agent Builder APIs through a hands-on tutorial with sample book data."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
type: tutorial
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Build a custom agent with the {{agent-builder}} APIs

Learn how to work with {{agent-builder}} programmatically using the {{kib}} APIs. This tutorial walks you through creating custom tools and agents that can help users search and analyze data.

This tutorial assumes you have basic knowledge of:

- {{es}} indices and data structures
- REST APIs and JSON
- Basic {{esql}} query syntax

By the end of this tutorial, you can:

- Create and run custom {{esql}} tools tailored to specific use cases
- Build custom agents with specific instructions and tool sets
- Chat with agents programmatically using the converse API
- Manage conversations and clean up resources

## Before you begin

To build a custom agent with {{agent-builder}} APIs, you need the following:

- Access to the feature in {{kib}}. Refer to [](get-started.md)
- [Permission](permissions.md) to create indices and use {{agent-builder}}
  - A {{kib}} API key for authentication if you're using `curl`
  :::{note}
  Set the required environment variables to simplify running `curl` commands:
  ```bash
  export KIBANA_URL="your-kibana-url"
  export ELASTICSEARCH_URL="your-elasticsearch-url"
  export API_KEY="your-api-key"
  ```
  :::

## Step 0: Set up sample data

Before working with agents and tools, create a sample dataset. This tutorial uses a collection of books to demonstrate how custom tools can efficiently query specific data.

Create an index with book data:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/create-sample-index.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X PUT "${ELASTICSEARCH_URL}/kibana_sample_data_agents" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "mappings": {
         "properties": {
           "name": { "type": "text" },
           "author": { "type": "text" },
           "release_date": { "type": "date" },
           "page_count": { "type": "integer" }
         }
       }
     }'
```
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

Add sample book documents to the index:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/bulk-insert-books.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${ELASTICSEARCH_URL}/_bulk" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "Content-Type: application/x-ndjson" \
     --data-binary @- << 'EOF'
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470}
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585}
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328}
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227}
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268}
{ "index" : { "_index" : "kibana_sample_data_agents" } }
{"name": "The Handmaids Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311}
EOF
```
:::

::::

### Result

You now have a `kibana_sample_data_agents` index with six books, ready for querying with custom tools.

## Step 1: Chat with the default agent

Start by chatting with the default agent to understand how {{agent-builder}} works. The default agent has access to built-in tools that can query your data.

Send a message to the default agent:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/converse-default-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/converse" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "What books are in the kibana_sample_data_agents index?"
     }'
```
:::

::::

### Result

The agent responds with information about the books in your sample data. Notice the `token_usage` field in the response. To learn how to track token consumption, refer to [Monitor token usage](monitor-usage.md). You'll compare this with your custom agent later to see how specialized tools can reduce token consumption.

::::{dropdown} Example response
```json
{
  "conversation_id": "173bd57d-bb27-464c-86a3-09ecaf6bc8ef",
  "round_id": "a37100bc-3996-4be5-b874-7920a36e2ede",
  "status": "completed",
  "steps": [
    {
      "type": "reasoning",
      "reasoning": "The user is asking about books in a specific index (kibana_sample_data_agents). I'll search this index to retrieve the book information."
    },
    {
      "type": "tool_call",
      "tool_id": "platform.core.search",
      "params": {
        "query": "all books in kibana_sample_data_agents index",
        "index": "kibana_sample_data_agents"
      },
      "results": [
        {
          "type": "tabular_data",
          "data": {
            "columns": [
              { "name": "name", "type": "text" },
              { "name": "author", "type": "text" },
              { "name": "page_count", "type": "integer" },
              { "name": "release_date", "type": "date" }
            ],
            "values": [
              ["1984", "George Orwell", 328, "1985-06-01T00:00:00.000Z"],
              ["Brave New World", "Aldous Huxley", 268, "1932-06-01T00:00:00.000Z"],
              ["Fahrenheit 451", "Ray Bradbury", 227, "1953-10-15T00:00:00.000Z"],
              ["Revelation Space", "Alastair Reynolds", 585, "2000-03-15T00:00:00.000Z"],
              ["Snow Crash", "Neal Stephenson", 470, "1992-06-01T00:00:00.000Z"],
              ["The Handmaids Tale", "Margaret Atwood", 311, "1985-06-01T00:00:00.000Z"]
            ]
          }
        }
      ]
    }
  ],
  "model_usage": {
    "input_tokens": 30257,
    "output_tokens": 670
  },
  "response": {
    "message": "The **kibana_sample_data_agents** index contains 6 books:\n\n1. **1984** by George Orwell (328 pages, released June 1985)\n2. **Brave New World** by Aldous Huxley (268 pages, released June 1932)\n3. **Fahrenheit 451** by Ray Bradbury (227 pages, released October 1953)\n4. **Revelation Space** by Alastair Reynolds (585 pages, released March 2000)\n5. **Snow Crash** by Neal Stephenson (470 pages, released June 1992)\n6. **The Handmaid's Tale** by Margaret Atwood (311 pages, released June 1985)"
  }
}
```
::::

## Step 2: Explore available tools

[Tools](tools.md) are reusable functions that agents use to perform specific tasks. {{agent-builder}} includes built-in tools for common operations like searching indices and generating queries. You can also create custom tools.

List all available tools:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/list-tools.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

### Result

The response includes all available tools, including built-in platform tools like `platform.core.search`, `platform.core.generate_esql`, and others.

::::{dropdown} Example response (truncated)
```json
{
  "results": [
    {
      "id": "platform.core.search",
      "type": "builtin",
      "description": "A powerful tool for searching and analyzing data within your Elasticsearch cluster...",
      "configuration": {},
      "readonly": true
    },
    {
      "id": "platform.core.generate_esql",
      "type": "builtin",
      "description": "Generate an ES|QL query from a natural language query.",
      "configuration": {},
      "readonly": true
    },
    {
      "id": "platform.core.execute_esql",
      "type": "builtin",
      "description": "Execute an ES|QL query and return the results in a tabular format...",
      "configuration": {},
      "readonly": true
    },
    {
      "id": "platform.core.list_indices",
      "type": "builtin",
      "description": "List the indices, aliases and datastreams from the Elasticsearch cluster...",
      "configuration": {},
      "readonly": true
    }
  ]
}
```
::::

## Step 3: Run a built-in tool

Use the built-in {{esql}} generator tool to create a query for your sample data. This tool generates optimized {{esql}} queries based on natural language descriptions.

Run the {{esql}} generator tool:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/generate-esql.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/tools/_execute" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "tool_id": "platform.core.generate_esql", <1>
       "tool_params": {
         "query": "Build an ES|QL query to get the book with the most pages", <2>
         "index": "kibana_sample_data_agents" <3>
       }
     }'
```
1. ID of the built-in {{esql}} generator tool
2. Natural language description of the desired query
3. Index to query

:::

::::

### Result

The tool returns an {{esql}} query similar to: `FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1`. You'll use this query in the next step to create a custom tool.

::::{dropdown} Example response
```json
{
  "results": [
    {
      "type": "query",
      "data": {
        "esql": "FROM kibana_sample_data_agents\n| SORT page_count DESC\n| LIMIT 1"
      }
    },
    {
      "type": "other",
      "data": {
        "answer": "Here's the ES|QL query:\n\n```esql\nFROM kibana_sample_data_agents\n| SORT page_count DESC\n| LIMIT 1\n```\n\nThis query will return the book with the highest page count."
      }
    }
  ]
}
```
::::

## Step 4: Create a custom {{esql}} tool

Create a [custom {{esql}} tool](tools/esql-tools.md) using the query from the previous step. Custom tools encapsulate specific queries or operations, making them reusable and efficient.

Create a tool that finds the book with the most pages:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/create-esql-tool.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "example-books-esql-tool", <1>
       "type": "esql", <2>
       "description": "An ES|QL query tool for getting the book with the most pages", <3>
       "configuration": {
         "query": "FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1", <4>
         "params": {} <5>
       }
     }'
```
1. Unique identifier for the tool
2. Tool type - `esql` for {{esql}} query tools
3. Description that helps agents understand when to use this tool
4. The {{esql}} query to run
5. Query parameters (empty for this basic example)

:::

::::

### Result

The response confirms the tool was created with its full configuration.

::::{dropdown} Example response
```json
{
  "id": "example-books-esql-tool",
  "type": "esql",
  "description": "An ES|QL query tool for getting the book with the most pages",
  "tags": [],
  "configuration": {
    "query": "FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1",
    "params": {}
  },
  "readonly": false,
  "schema": {
    "type": "object",
    "properties": {},
    "additionalProperties": false,
    "description": "Parameters needed to execute the query"
  }
}
```
::::

## Step 5: Run your custom tool

Test your new custom tool to verify it works correctly.

Run the custom tool:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/execute-tool.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/tools/_execute" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "tool_id": "example-books-esql-tool",
       "tool_params": {}
     }'
```
:::

::::

### Result

The response includes tabular data showing "Revelation Space" by Alastair Reynolds with 585 pages.

::::{dropdown} Example response
```json
{
  "results": [
    {
      "type": "query",
      "data": {
        "esql": "FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1"
      }
    },
    {
      "type": "tabular_data",
      "data": {
        "source": "esql",
        "query": "FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1",
        "columns": [
          { "name": "author", "type": "text" },
          { "name": "name", "type": "text" },
          { "name": "page_count", "type": "integer" },
          { "name": "release_date", "type": "date" }
        ],
        "values": [
          ["Alastair Reynolds", "Revelation Space", 585, "2000-03-15T00:00:00.000Z"]
        ]
      }
    }
  ]
}
```
::::

## Step 6: Get a tool by ID

Retrieve the details of a specific tool using its ID.

Get the tool you created:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/get-tool.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/tools/example-books-esql-tool" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

### Result

The response includes the full tool definition with all its configuration details.

## Step 7: Update the tool to accept parameters

Make your tool more flexible by adding parameters. This allows the same tool to handle different queries based on input values.

Update the tool to filter by year and limit results:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/create-parameterized-tool.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X PUT "${KIBANA_URL}/api/agent_builder/tools/example-books-esql-tool" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "An ES|QL query tool for finding the longest books published before a certain year",
       "configuration": {
         "query": "FROM kibana_sample_data_agents | WHERE DATE_EXTRACT(\"year\", release_date) < ?maxYear | SORT page_count DESC | LIMIT ?limit", <1>
         "params": {
           "maxYear": { <2>
             "type": "integer",
             "description": "Maximum year to filter books (exclusive)"
           },
           "limit": { <3>
             "type": "integer",
             "description": "Maximum number of results to return"
           }
         }
       }
     }'
```
1. Query with parameterized placeholders (`?maxYear`, `?limit`)
2. Integer parameter for filtering by publication year
3. Integer parameter for limiting results

:::

::::

Run the updated tool with parameters:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/execute-tool-with-params.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/tools/_execute" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "tool_id": "example-books-esql-tool",
       "tool_params": {
         "maxYear": 1960, <1>
         "limit": 2 <2>
       }
     }'
```
1. Find books published before 1960
2. Return only the top 2 results

:::

::::

### Result

The response shows "Brave New World" (268 pages, 1932) and "Fahrenheit 451" (227 pages, 1953), the two longest books published before 1960.

::::{dropdown} Example response
```json
{
  "results": [
    {
      "type": "query",
      "data": {
        "esql": "FROM kibana_sample_data_agents\n| WHERE DATE_EXTRACT(\"year\", release_date) < 1960\n| SORT page_count DESC\n| LIMIT 2"
      }
    },
    {
      "type": "tabular_data",
      "data": {
        "source": "esql",
        "query": "FROM kibana_sample_data_agents\n| WHERE DATE_EXTRACT(\"year\", release_date) < 1960\n| SORT page_count DESC\n| LIMIT 2",
        "columns": [
          { "name": "author", "type": "text" },
          { "name": "name", "type": "text" },
          { "name": "page_count", "type": "integer" },
          { "name": "release_date", "type": "date" }
        ],
        "values": [
          ["Aldous Huxley", "Brave New World", 268, "1932-06-01T00:00:00.000Z"],
          ["Ray Bradbury", "Fahrenheit 451", 227, "1953-10-15T00:00:00.000Z"]
        ]
      }
    }
  ]
}
```
::::

## Step 8: Create a custom agent

[Agents](custom-agents.md) combine instructions with specific tools to handle user conversations effectively. Create an agent specialized for searching the books collection.

List all existing agents to see what's available:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/list-agents.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/agents" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

Create a specialized agent for book searches:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/create-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/agents" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "books-search-agent", <1>
       "name": "Books Search Helper", <2>
       "description": "Hi! I can help you search and analyze the books in our sample data collection.", <3>
       "labels": ["books", "sample-data", "search"], <4>
       "avatar_color": "#BFDBFF", <5>
       "avatar_symbol": "📚", <6>
       "configuration": {
         "instructions": "You are a helpful agent that assists users in searching and analyzing book data from the kibana_sample_data_agents index. Help users find books by author, title, or analyze reading patterns.", <7>
         "tools": [ <8>
           {
             "tool_ids": [
               "example-books-esql-tool",
               "platform.core.search",
               "platform.core.list_indices",
               "platform.core.get_index_mapping",
               "platform.core.get_document_by_id"
             ]
           }
         ]
       }
     }'
```
1. Unique identifier for the agent
2. Display name shown in the UI
3. Greeting message users view when starting a conversation
4. Labels for organizing and filtering agents
5. Avatar background color (hex code)
6. Avatar symbol or emoji
7. System instructions that guide the agent's behavior
8. Tools the agent can use - includes your custom tool and built-in tools

:::

::::

### Result

The response confirms the agent was created with its full configuration.

::::{dropdown} Example response
```json
{
  "id": "books-search-agent",
  "type": "chat",
  "name": "Books Search Helper",
  "description": "Hi! I can help you search and analyze the books in our sample data collection.",
  "labels": ["books", "sample-data", "search"],
  "avatar_color": "#BFDBFF",
  "avatar_symbol": "📚",
  "configuration": {
    "instructions": "You are a helpful agent that assists users in searching and analyzing book data from the kibana_sample_data_agents index. Help users find books by author, title, or analyze reading patterns.",
    "tools": [
      {
        "tool_ids": [
          "example-books-esql-tool",
          "platform.core.search",
          "platform.core.list_indices",
          "platform.core.get_index_mapping",
          "platform.core.get_document_by_id"
        ]
      }
    ]
  },
  "readonly": false
}
```
::::

## Step 9: Get an agent by ID

Retrieve the details of a specific agent using its ID.

Get the agent you created:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/get-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/agents/books-search-agent" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

### Result

The response includes the full agent definition with all its configuration details.

## Step 10: Update an agent

Update your agent's configuration, such as changing its description or labels.

Update the agent's description:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/update-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X PUT "${KIBANA_URL}/api/agent_builder/agents/books-search-agent" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Books Search Helper",
       "description": "Updated - Search and analyze our sample books collection with ease!",
       "labels": ["books", "sample-data", "search", "updated"]
     }'
```
:::

::::

### Result

The response confirms the agent was updated with the new configuration.

## Step 11: Chat with your custom agent

Test your new agent by asking it questions about the book collection. The agent uses your custom tool and built-in tools to answer queries.

Start a conversation with the custom agent:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/converse-with-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/converse" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "What books do we have in our collection?",
       "agent_id": "books-search-agent" <1>
     }'
```
1. Specify your custom agent ID

:::

::::

### Result

The agent responds with information about your book collection. Note the `conversation_id` in the response - you'll use this to continue the conversation.

::::{dropdown} Example response (truncated)
```json
{
  "conversation_id": "e5b4e3ff-f5c9-4f52-9001-87b403df1a6a",
  "round_id": "145aeacf-fa04-4d3d-a93c-141b5c2463fe",
  "status": "completed",
  "steps": [
    {
      "type": "reasoning",
      "reasoning": "The user is asking about books in the collection. I should search the kibana_sample_data_agents index."
    },
    {
      "type": "tool_call",
      "tool_id": "platform.core.search",
      "params": {
        "query": "list all books in kibana_sample_data_agents index",
        "index": "kibana_sample_data_agents"
      },
      "results": [
        {
          "type": "tabular_data",
          "data": {
            "columns": [
              { "name": "name", "type": "text" },
              { "name": "author", "type": "text" },
              { "name": "page_count", "type": "integer" },
              { "name": "release_date", "type": "date" }
            ],
            "values": [
              ["1984", "George Orwell", 328, "1985-06-01T00:00:00.000Z"],
              ["Brave New World", "Aldous Huxley", 268, "1932-06-01T00:00:00.000Z"],
              ["Fahrenheit 451", "Ray Bradbury", 227, "1953-10-15T00:00:00.000Z"],
              ["Revelation Space", "Alastair Reynolds", 585, "2000-03-15T00:00:00.000Z"],
              ["Snow Crash", "Neal Stephenson", 470, "1992-06-01T00:00:00.000Z"],
              ["The Handmaids Tale", "Margaret Atwood", 311, "1985-06-01T00:00:00.000Z"]
            ]
          }
        }
      ]
    }
  ],
  "model_usage": {
    "input_tokens": 30345,
    "output_tokens": 704
  },
  "response": {
    "message": "Your collection contains **6 books**:\n\n1. **1984** by George Orwell (328 pages, released June 1985)\n2. **Brave New World** by Aldous Huxley (268 pages, released June 1932)\n3. **Fahrenheit 451** by Ray Bradbury (227 pages, released October 1953)\n4. **Revelation Space** by Alastair Reynolds (585 pages, released March 2000)\n5. **Snow Crash** by Neal Stephenson (470 pages, released June 1992)\n6. **The Handmaid's Tale** by Margaret Atwood (311 pages, released June 1985)"
  }
}
```
::::

Continue the conversation using the custom tool:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/converse-continue-conversation.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/agent_builder/converse" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "Can you find the longest book published before 1960?",
       "agent_id": "books-search-agent",
       "conversation_id": "<CONVERSATION_ID>" <1>
     }'
```
1. Use the conversation ID from the previous response to maintain context

:::

::::

### Result

The agent uses your custom `example-books-esql-tool` to efficiently answer the query in a single step. Compare the `token_usage` in this response with Step 1. Custom tools optimized for specific use cases typically consume fewer tokens than general-purpose agents. To learn more about token consumption, refer to [Monitor token usage](monitor-usage.md).

:::{tip}
For real-time chat responses, use the [streaming converse API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-converse-async) instead.
:::

## Step 12: Manage conversations

View and manage your conversation history with agents.

List all conversations:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/list-conversations.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/conversations" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

Get the full history of a specific conversation:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/get-conversation.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/agent_builder/conversations/<CONVERSATION_ID>" \ <1>
     -H "Authorization: ApiKey ${API_KEY}"
```
1. Replace with an actual conversation ID from the previous step

:::

::::

### Result

The response includes the complete conversation history with all messages, tool calls, and responses.

## Step 13: Clean up resources (optional)

Remove the resources created in this tutorial when you no longer need them.

Delete the conversation:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/delete-conversation.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "${KIBANA_URL}/api/agent_builder/conversations/<CONVERSATION_ID>" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

Delete the custom agent:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/delete-agent.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "${KIBANA_URL}/api/agent_builder/agents/books-search-agent" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

Delete the custom tool:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/delete-tool.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "${KIBANA_URL}/api/agent_builder/tools/example-books-esql-tool" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

Delete the sample index:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
:::{include} _snippets/api-tutorial/delete-sample-index.md
:::
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "${ELASTICSEARCH_URL}/kibana_sample_data_agents" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

### Result

All resources created during this tutorial are now removed.

## Summary

In this tutorial, you learned how to:

- Create custom {{esql}} tools with and without parameters
- Run tools directly using the tools API
- Build custom agents with specific instructions and tool sets
- Chat with agents programmatically using the converse API
- Manage conversation history

Custom tools optimized for specific use cases can significantly reduce token consumption and improve response accuracy compared to general-purpose agents with many tools. By tailoring agents and tools to your specific data and workflows, you create more efficient and effective AI-powered experiences.

## Next steps

- Explore [streaming responses](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-converse-async) for real-time chat experiences
- Learn about [other tool types](tools.md) beyond {{esql}}, including [index search tools](tools/index-search-tools.md), [MCP tools](tools/mcp-tools.md), and [workflow tools](tools/workflow-tools.md)
- Try the [MCP server](mcp-server.md) to connect external AI clients like Claude Desktop to your agents
- Review [best practices for prompt engineering](prompt-engineering.md) to optimize your agents

## Related pages

- [{{agent-builder}} Kibana APIs overview](kibana-api.md)
- [{{kib}} API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder)
- [Custom agents](custom-agents.md)
- [Tools reference](tools.md)
