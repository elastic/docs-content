---
navigation_title: "Kibana APIs"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

# Work with {{agent-builder}} using the APIs

These APIs allow you to programmatically work with the {{agent-builder}} abstractions.

## API reference

For the full API documentation, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/).

For information on generating API keys, see [API keys](https://www.elastic.co/docs/solutions/search/search-connection-details).

## Available APIs
% TODO: we may remove this list once the API reference is live, but probably helpful in the short term

### Tools

List all tools
:   `GET kbn://api/agent_builder/tools`

Create a tool
:   `POST kbn://api/agent_builder/tools`

Get a tool by ID
:   `GET kbn://api/agent_builder/tools/{id}`

Delete a tool by ID
:   `DELETE kbn://api/agent_builder/tools/{id}`

Update a tool by ID
:   `PUT kbn://api/agent_builder/tools/{toolId}`

Execute a tool
:   `POST kbn://api/agent_builder/tools/_execute`

### Agents

List all agents
:   `GET kbn://api/agent_builder/agents`

Create an agent
:   `POST kbn://api/agent_builder/agents`

Get an agent by ID
:   `GET kbn://api/agent_builder/agents/{id}`

Update an agent by ID
:   `PUT kbn://api/agent_builder/agents/{id}`

Delete an agent by ID
:   `DELETE kbn://api/agent_builder/agents/{id}`

### Chat and Conversations

Chat with an agent
:   `POST kbn://api/agent_builder/converse`

Chat with an agent and stream events
:   `POST kbn://api/agent_builder/converse/async`

List conversations
:   `GET kbn://api/agent_builder/conversations`

Get conversation by ID
:   `GET kbn://api/agent_builder/conversations/{conversation_id}`

Delete conversation by ID
:   `DELETE kbn://api/agent_builder/conversations/{conversation_id}`

### MCP Server

Get MCP server configuration
:   `GET kbn://api/agent_builder/mcp`

Create or configure MCP server
:   `POST kbn://api/agent_builder/mcp`

Delete MCP server configuration
:   `DELETE kbn://api/agent_builder/mcp`

### A2A Protocol

Refer to [](a2a-server.md) for more information.

Get A2A agent card configuration
:   `GET kbn://api/agent_builder/a2a/{agentId}.json`

Execute A2A agent task
:   `POST kbn://api/agent_builder/a2a/{agentId}`

