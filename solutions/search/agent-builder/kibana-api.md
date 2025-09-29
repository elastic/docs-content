---
navigation_title: "Kibana APIs"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

# Work with {{agent-builder}} using the APIs

This page provides a quick overview of the main Kibana API endpoints for {{agent-builder}}. For complete details including all available parameters, request/response schemas, and error handling, refer to the [Kibana serverless API reference](https://www.elastic.co/docs/api/doc/serverless/).

These APIs allow you to programmatically work with the {{agent-builder}} abstractions.

## Using the APIs

The examples in this documentation use Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) syntax.
```console
GET kbn://api/agent_builder/tools
```

To use these APIs with tools like `curl`, replace the `kbn://` protocol with your Kibana URL.

:::{note}
Set the required environment variables before running curl commands:
```bash
export KIBANA_URL="your-kibana-url"
export API_KEY="your-api-key"
```
:::

```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::{tip}
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
[Learn more](https://www.elastic.co/docs/solutions/search/search-connection-details).
:::

## Available APIs

% TODO: we may remove this list once the API reference is live, but probably helpful in the short term

### Tools

**Example:** List all tools
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/tools
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Create a tool
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
POST kbn://api/agent_builder/tools
{
  "id": "example-esql-tool",
  "type": "esql",
  "description": "An ES|QL query tool for analyzing financial trades with time filtering",
  "tags": ["analytics", "finance", "updated"],
  "configuration": {
    "query": "FROM financial_trades | WHERE execution_timestamp >= ?startTime | STATS trade_count=COUNT(*), avg_price=AVG(execution_price) BY symbol | SORT trade_count DESC | LIMIT ?limit",
    "params": {
      "startTime": {
        "type": "date",
        "description": "Start time for the analysis in ISO format"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return"
      }
    }
  }
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "example-esql-tool",
       "type": "esql",
       "description": "Example ES|QL query tool for analyzing financial trades with time filtering",
       "tags": ["analytics", "finance"],
       "configuration": {
         "query": "FROM financial_trades | WHERE execution_timestamp >= ?startTime | STATS trade_count=COUNT(*), avg_price=AVG(execution_price) BY symbol | SORT trade_count DESC | LIMIT ?limit",
         "params": {
           "startTime": {
             "type": "date",
             "description": "Start time for the analysis in ISO format"
           },
           "limit": {
             "type": "integer",
             "description": "Maximum number of results to return"
           }
         }
       }
     }'
```
:::

::::

**Example:** Get a tool by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/tools/{id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/tools/{id}" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Delete a tool by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
DELETE kbn://api/agent_builder/tools/{id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "https://${KIBANA_URL}/api/agent_builder/tools/{id}" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

**Example:** Update a tool by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
PUT kbn://api/agent_builder/tools/{toolId}
{
  "description": "Updated ES|QL query tool for analyzing financial trades with time filtering",
  "tags": ["analytics", "finance", "updated"],
  "configuration": {
    "query": "FROM financial_trades | WHERE execution_timestamp >= ?startTime | STATS trade_count=COUNT(*), avg_price=AVG(execution_price) BY symbol | SORT trade_count DESC | LIMIT ?limit",
    "params": {
      "startTime": {
        "type": "date",
        "description": "Start time for the analysis in ISO format"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return"
      }
    }
  }
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X PUT "https://${KIBANA_URL}/api/agent_builder/tools/{toolId}" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "Updated ES|QL query tool for analyzing financial trades with time filtering",
       "tags": ["analytics", "finance", "updated"],
       "configuration": {
         "query": "FROM financial_trades | WHERE execution_timestamp >= ?startTime | STATS trade_count=COUNT(*), avg_price=AVG(execution_price) BY symbol | SORT trade_count DESC | LIMIT ?limit",
         "params": {
           "startTime": {
             "type": "date",
             "description": "Start time for the analysis in ISO format"
           },
           "limit": {
             "type": "integer",
             "description": "Maximum number of results to return"
           }
         }
       }
     }'
```
:::

::::

**Example:** Execute a tool
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
POST kbn://api/agent_builder/tools/_execute
{
  "tool_id": "platform.core.search",
  "tool_params": {
    "query": "can you find john doe's email from the employee index?"
  }
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/tools/_execute" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "tool_id": "platform.core.search",
       "tool_params": {
         "query": "can you find john doe's email from the employee index?"}
       }
     }'
```
:::

::::

### Agents

**Example:** List all agents
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/agents
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/agents" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Create an agent
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
POST kbn://api/agent_builder/agents
{
  "id": "new-agent-id",
  "name": "Search Index Helper",
  "description": "Hi! I can help you search the data within the indices starting with \"content-\" prefix.",
  "labels": ["custom-indices", "department-search"],
  "avatar_color": "#BFDBFF",
  "avatar_symbol": "SI",
  "configuration": {
    "instructions": "You are a custom agent that wants to help searching data using all indices starting with prefix \"content-\".",
    "tools": [
      {
        "tool_ids": [
          "platform.core.search",
          "platform.core.list_indices",
          "platform.core.get_index_mapping",
          "platform.core.get_document_by_id"
        ]
      }
    ]
  }
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/agents" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "new-agent-id",
       "name": "Search Index Helper",
       "description": "Hi! I can help you search the data within the indices starting with \"content-\" prefix.",
       "labels": ["custom-indices", "department-search"],
       "avatar_color": "#BFDBFF",
       "avatar_symbol": "SI",
       "configuration": {
         "instructions": "You are a custom agent that wants to help searching data using all indices starting with prefix \"content-\".",
         "tools": [
           {
             "tool_ids": [
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
:::

::::

**Example:** Get an agent by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/agents/{id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/agents/{id}" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Update an agent by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
PUT kbn://api/agent_builder/agents/{id}
{
  "name": "Search Index Helper",
  "description": "Updated description - Search for anything in \"content-*\" indices!",
  "labels": ["custom-indices", "department-search", "elastic-employees"],
  "avatar_color": "#BFDBFF",
  "avatar_symbol": "SI",
  "configuration": {
    "instructions": "You are a custom agent that wants to help searching data using all indices starting with prefix \"content-\".",
    "tools": [{
      "tool_ids": [
        "platform.core.search",
        "platform.core.list_indices",
        "platform.core.get_index_mapping",
        "platform.core.get_document_by_id"
      ]
    }]
  }
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X PUT "https://${KIBANA_URL}/api/agent_builder/agents/{id}" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Search Index Helper",
       "description": "Updated description - Search for anything in \"content-*\" indices!",
       "labels": ["custom-indices", "department-search", "elastic-employees"],
       "avatar_color": "#BFDBFF",
       "avatar_symbol": "SI",
       "configuration": {
         "instructions": "You are a custom agent that wants to help searching data using all indices starting with prefix \"content-\".",
         "tools": [{
           "tool_ids": [
             "platform.core.search",
             "platform.core.list_indices",
             "platform.core.get_index_mapping",
             "platform.core.get_document_by_id"
           ]
         }]
       }
     }'
```
:::

::::

**Example:** Delete an agent by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
DELETE kbn://api/agent_builder/agents/{id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "https://${KIBANA_URL}/api/agent_builder/agents/{id}" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

### Chat and conversations

**Example:** Chat with an agent
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
POST kbn://api/agent_builder/converse
{
  "input": "What is Elasticsearch?",
  "agent_id": "elastic-ai-agent"
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/converse" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "What is Elasticsearch?",
       "agent_id": "elastic-ai-agent"}'
```
:::

::::

**Example:** Chat with an agent and stream events
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
POST kbn://api/agent_builder/converse/async
{
  "input": "Hello again let's have an async chat",
  "agent_id": "elastic-ai-agent",
  "conversation_id": "<CONVERSATION_ID>"
}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/converse/async" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "Hello again let us have an async chat",
       "agent_id": "elastic-ai-agent",
       "conversation_id": "<CONVERSATION_ID>"
     }'
```
:::

::::

**Example:** List conversations
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/conversations
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/conversations" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Get conversation by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/conversations/{conversation_id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/conversations/{conversation_id}" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::

**Example:** Delete conversation by ID
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
DELETE kbn://api/agent_builder/conversations/{conversation_id}
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X DELETE "https://${KIBANA_URL}/api/agent_builder/conversations/{conversation_id}" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -H "kbn-xsrf: true"
```
:::

::::

### MCP server API

Refer to [](mcp-server.md) for more information.


Communicate with the MCP server via JSON-RPC 2.0.

```bash
curl -X POST "https://${KIBANA_URL}/api/agent_builder/mcp" \
    -H "Authorization: ApiKey ${API_KEY}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "kbn-xsrf: true" \
    -d '{
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }'
```

:::{note}
This endpoint uses the JSON-RPC protocol. The MCP server is designed for AI clients like Claude Desktop, Cursor, and VS Code extensions to access your Elastic tools. Use this endpoint for testing MCP connectivity or debugging protocol communication. This endpoint requires JSON-RPC formatting and will not work from the Dev Tools Console.
:::

### A2A Protocol

Refer to [](a2a-server.md) for more information.

**Example:** Get A2A agent card configuration
::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console
```console
GET kbn://api/agent_builder/a2a/{agentId}.json
```
:::

:::{tab-item} curl
:sync: curl
```bash
curl -X GET "https://${KIBANA_URL}/api/agent_builder/a2a/{agentId}.json" \
     -H "Authorization: ApiKey ${API_KEY}"
```
:::

::::


% TODO: Execute A2A agent task section - commented out until ready
% Execute A2A agent task
% ::::{tab-set}
% :group: api-examples
% 
% :::{tab-item} Console
% :sync: console
% :::{note}
% This endpoint uses the JSON-RPC protocol, which cannot be executed in the Dev Tools Console.
% Use curl or another HTTP client.
% :::
% 
% :::{tab-item} curl
% :sync: curl
% ```bash
% curl -X POST "https://${KIBANA_URL}/api/agent_builder/a2a/{agentId}" \
%      -H "Authorization: ApiKey ${API_KEY}" \
%      -H "kbn-xsrf: true" \
%      -H "Content-Type: application/json" \
%      -d '{
%        "jsonrpc": "2.0",
%        "method": "complete",
%        "params": {
%          "messages": [
%            {
%              "role": "user",
%              "content": "Hello from A2A protocol"
%            }
%          ]
%        },
%        "id": "task-123"
%      }'
% ```
% :::
% 
% ::::





## API reference

For the full API documentation, refer to the [Kibana serverless API reference](https://www.elastic.co/docs/api/doc/serverless/).
% TODO: Update link once page is live