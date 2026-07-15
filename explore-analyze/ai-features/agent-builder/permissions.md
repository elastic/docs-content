---
navigation_title: "Permissions"
description: "Understand how Kibana feature privileges, Elasticsearch privileges, and spaces control access to Agent Builder."
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

# Permissions and access control in {{agent-builder}}

Use this page to understand the {{agent-builder}} permission model and choose least-privilege access for users and programmatic clients. After choosing the required privileges, assign them to users with roles or to clients with API keys.

::::{admonition}
This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

## How permissions work

An {{agent-builder}} request is allowed only when the user or client has access at every relevant layer:

- **{{kib}} feature privileges** control which {{agent-builder}}, connector, and workflow operations the user or client can perform.
- **{{es}} cluster and index privileges** control whether agents and tools can use inference endpoints, query data, and inspect mappings.
- **{{kib}} space scope** controls which space-specific {{agent-builder}} resources the user or client can access.

Not every operation requires every privilege. For example, a tool that queries an index requires index privileges, while `monitor_inference` is required only when an agent or tool calls the {{es}} Inference API.

## Privilege reference [#privilege-reference]

Use the following tables to identify the {{kib}} feature privileges and {{es}} privileges required for each {{agent-builder}} use case.

### {{kib}} feature privileges [#kib-privileges]

In the role management UI, {{kib}} displays human-readable privilege names. Role descriptors and API keys use the corresponding application privilege identifiers. For these privileges, use `kibana-.kibana` as the application name and scope the application resource to the required space.

| Feature and UI privilege | Role and API key privilege | Grants |
| --- | --- | --- |
| **Agent Builder: Read** | `feature_agentBuilder.read` | Use agents, send chat messages, and view agents, tools, skills, and conversations. |
| **Agent Builder: All** | `feature_agentBuilder.all` | Everything granted by **Read**, plus all {{agent-builder}} management privileges. |
| **Agent Builder > Management: Create and edit agents** | `feature_agentBuilder.manage_agents` | Pair with **Read** to create, update, and delete custom agents without granting other management privileges. |
| **Agent Builder > Management: Create and edit custom tools** | `feature_agentBuilder.manage_tools` | Pair with **Read** to create, update, and delete custom tools without granting other management privileges. |
| **Agent Builder > Management: Create and edit skills** | `feature_agentBuilder.manage_skills` | Pair with **Read** to create, update, and delete custom skills without granting other management privileges. |
| **Actions and Connectors: Read** | `feature_actions.read` | Use agents that access {{kib}} connectors. |
| **Workflows: Read** | `feature_workflowsManagement.read` | Read workflows and workflow execution information. |
| **Workflows > Workflows Actions: Execute** | `feature_workflowsManagement.workflow_execute` | Run workflows. Also include **Workflows: Read** when the user or client must inspect workflows. |
| **Workflows: All** | `feature_workflowsManagement.all` | Create, update, delete, run, and read workflows and their executions. |

Learn more about [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

### {{es}} privileges [#es-privileges]

Tools execute {{es}} requests with the privileges of the current user or API key. Assign only the cluster and index privileges required by the tools the principal can access.

| Scope | Privilege | When to use it |
| --- | --- | --- |
| Cluster | `monitor_inference` | Required when an agent uses an AI connector that calls the {{es}} Inference API, including the Elastic default LLM, or when a tool uses the Inference API to generate queries from natural language. The built-in `search` and `generate_esql` tools and [index search tools](tools/index-search-tools.md) use this API. This privilege is not required for other {{kib}} GenAI connectors. |
| Indices | `read` | Required for tools that query index data. Limit the assigned index patterns to the data the user or client needs. |
| Indices | `view_index_metadata` | Required for tools that inspect index mappings. The built-in `search` tool and index search tools might use this capability internally. |

Learn more about [cluster privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-cluster) and [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).

### {{kib}} space scope [#space-scope]

Conversations, custom agents, and custom tools are scoped to the current {{kib}} space. Built-in agents are available in all spaces. The default Elastic AI Agent is an exception {applies_to}`stack: ga 9.4+`: it is a persisted, space-aware agent that is automatically created in each space.

In a role or API key descriptor, specify the space in the application privilege resource. For example, use `"resources": ["space:production"]` for the `production` space. Users and API keys cannot access resources in spaces outside their assigned resources.

When calling the {{agent-builder}} APIs or MCP server in a custom space, include `/s/<space-name>` before the API path. The default space does not use this prefix.

Learn more about [{{kib}} Spaces](/deploy-manage/manage-spaces.md).

## Configure access

After choosing privileges and space scope, assign them based on who or what needs access.

### Roles for users [#roles-for-users]

Use [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) to bundle the required {{kib}} feature privileges and {{es}} privileges, then assign the roles to users. In the role management UI, choose the required space and feature privileges under **Kibana privileges**, and limit index privileges to the data the users need.

:::{note}
When configuring roles in the {{kib}} UI, {{agent-builder}} privileges are currently located under the **Analytics** section, not the {{es}} section.
:::

### API keys for programmatic clients [#api-keys-for-clients]

Use API keys for custom clients, scripts, MCP clients, and A2A clients. API key role descriptors combine the same {{kib}} application privileges, {{es}} privileges, and space scope described on this page. An API key cannot grant privileges that its owner does not have.

Refer to [Create API keys for {{agent-builder}} APIs](api-keys.md) for complete examples for read-only clients, management clients, and unrestricted development keys. To learn more about API key behavior and management, refer to [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).
