---
navigation_title: "Kibana APIs"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Work with {{agent-builder}} using the APIs

This page provides a quick overview of the main {{kib}} API endpoints for {{agent-builder}}. For complete details including all available parameters, request/response schemas, and error handling, refer to the [{{kib}} API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder).

These APIs allow you to programmatically work with the {{agent-builder}} abstractions.

## Using the APIs

The examples in this documentation use Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) syntax.
```console
GET kbn://api/agent_builder/tools
```

To use these APIs with tools like `curl`, replace the `kbn://` protocol with your {{kib}} URL.

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

### Working with Spaces

To run APIs in non-default [spaces](/deploy-manage/manage-spaces.md), you must include the space identifier in the URL when making API calls with `curl` or other external tools. Insert `/s/<space_name>` before `/api/agent_builder` in your requests.

For example, to list tools in a space named `my-space`:

```bash
curl -X GET "https://${KIBANA_URL}/s/my-space/api/agent_builder/tools" \
     -H "Authorization: ApiKey ${API_KEY}"
```

The default space does not require the `/s/default` prefix.

Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) automatically uses your current space context and does not require the `/s/<space_name>` prefix.

## Available APIs

% TODO: we may remove this list once the API reference is live, but probably helpful in the short term

### Tools

**Example:** List all tools

This example uses the [list tools API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-tools).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Create a tool

This example uses the [create a tool API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-tools).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Get a tool by ID

This example uses the [get a tool by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-tools-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Delete a tool by ID

This example uses the [delete a tool by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-agent-builder-tools-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Update a tool by ID

This example uses the [update a tool API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-agent-builder-tools-toolid).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Run a tool

This example uses the [execute a tool API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-tools-execute).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

### Agents

**Example:** List all agents

This example uses the [list agents API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-agents).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Create an agent

This example uses the [create an agent API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-agents).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Get an agent by ID

This example uses the [get an agent by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-agents-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Update an agent by ID

This example uses the [update an agent API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-agent-builder-agents-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Delete an agent by ID

This example uses the [delete an agent by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-agent-builder-agents-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

### Chat and conversations

**Example:** Chat with an agent

This example uses the [send chat message API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-converse).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Chat with an agent and stream events

This example uses the [send chat message (streaming) API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-converse-async).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** List conversations

This example uses the [list conversations API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-conversations).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Get conversation by ID

This example uses the [get conversation by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-conversations-conversation-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

**Example:** Delete conversation by ID

This example uses the [delete conversation by ID API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-agent-builder-conversations-conversation-id).

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::

### Get A2A agent card configuration

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
:::{include} _snippets/spaces-api-note.md
:::
:::

::::





## API reference

For the full API documentation, refer to the [{{kib}} API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder).
