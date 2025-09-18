---
navigation_title: "Kibana APIs"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

# Work with {{agent-builder}} using the APIs

These APIs allow you to programmatically work with the {{agent-builder}} abstractions.

## API reference

For the full API documentation, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/).

## Using the APIs

The examples in this documentation use Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) syntax.
```console
GET kbn://api/agent_builder/tools
```

To use these APIs with tools like `curl`, replace the `kbn://` protocol with your Kibana URL.

 
```bash
curl -X GET "https://<KIBANA_URL>/api/agent_builder/tools" \
     -H "Authorization: ApiKey <API_KEY>"
```
:::{tip}
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
[Learn more](https://www.elastic.co/docs/solutions/search/search-connection-details).
:::

## Available APIs
% TODO: we may remove this list once the API reference is live, but probably helpful in the short term

### Tools

List all tools
:   ```console
    GET kbn://api/agent_builder/tools
    ```

Create a tool
:   ```console
    POST kbn://api/agent_builder/tools
    ```

Get a tool by ID
:   ```console
    GET kbn://api/agent_builder/tools/{id}
    ```

Delete a tool by ID
:   ```console
    DELETE kbn://api/agent_builder/tools/{id}
    ```

Update a tool by ID
:   ```console
    PUT kbn://api/agent_builder/tools/{toolId}
    ```

Execute a tool
:   ```console
    POST kbn://api/agent_builder/tools/_execute
    ```

### Agents

List all agents
:   ```console
    GET kbn://api/agent_builder/agents
    ```

Create an agent
:   ```console
    POST kbn://api/agent_builder/agents
    ```

Get an agent by ID
:   ```console
    GET kbn://api/agent_builder/agents/{id}
    ```

Update an agent by ID
:   ```console
    PUT kbn://api/agent_builder/agents/{id}
    ```

Delete an agent by ID
:   ```console
    DELETE kbn://api/agent_builder/agents/{id}
    ```

### Chat and Conversations

Chat with an agent
:   ```console
    POST kbn://api/agent_builder/converse
    ```

Chat with an agent and stream events
:   ```console
    POST kbn://api/agent_builder/converse/async
    ```

List conversations
:   ```console
    GET kbn://api/agent_builder/conversations
    ```

Get conversation by ID
:   ```console
    GET kbn://api/agent_builder/conversations/{conversation_id}
    ```

Delete conversation by ID
:   ```console
    DELETE kbn://api/agent_builder/conversations/{conversation_id}
    ```

### MCP Server

Get MCP server configuration
:   ```console
    GET kbn://api/agent_builder/mcp
    ```

Create or configure MCP server
:   ```console
    POST kbn://api/agent_builder/mcp
    ```

Delete MCP server configuration
:   ```console
    DELETE kbn://api/agent_builder/mcp
    ```

### A2A Protocol

Refer to [](a2a-server.md) for more information.

Get A2A agent card configuration
:   ```console
    GET kbn://api/agent_builder/a2a/{agentId}.json
    ```

Execute A2A agent task
:   ```console
    POST kbn://api/agent_builder/a2a/{agentId}
    ```

