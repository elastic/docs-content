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
| **Agent Builder: Read** | `feature_agentBuilder.read` | Use agents, send chat messages, and view agents, tools, and conversations.<br>{applies_to}`stack: ga 9.4+` Also view skills.<br>On Serverless, also manage OAuth MCP clients for the [{{agent-builder}} MCP server](mcp-server.md). |
| **Agent Builder: All** | `feature_agentBuilder.all` | Everything granted by **Read**, plus all {{agent-builder}} management privileges. |
| **Agent Builder > Management: Create and edit agents** {applies_to}`stack: ga 9.4+` | `feature_agentBuilder.manage_agents` | Pair with **Read** to create, update, and delete custom agents without granting other management privileges. |
| **Agent Builder > Management: Create and edit custom tools** {applies_to}`stack: ga 9.4+` | `feature_agentBuilder.manage_tools` | Pair with **Read** to create, update, and delete custom tools without granting other management privileges. |
| **Agent Builder > Management: Create and edit skills** {applies_to}`stack: ga 9.4+` | `feature_agentBuilder.manage_skills` | Pair with **Read** to create, update, and delete custom skills without granting other management privileges. |
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

#### Read trace data [read-trace-data]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

{{agent-builder}} can [collect agent traces](collect-traces.md) into your {{es}} deployment. Trace data is stored in the `traces-agent_builder.otel-*` data stream. To read it, a role needs `read` and `view_index_metadata` on that pattern.

Access is granted at the index level. Any user who can read these data streams can read all collected traces, so trace access is not scoped per user. To control who can read traces, configure index privileges through roles in **Stack Management → Roles**.

<!-- RBAC on the local trace index is still settling (search-team#14100). In serverless Search and Observability projects the default roles may already grant broad access to these patterns. Do not document specific default-role behavior until #14100 lands. -->

### {{kib}} space scope [#space-scope]

Conversations, custom agents, and custom tools are scoped to the current {{kib}} space. Built-in agents are available in all spaces. The default Elastic AI Agent is an exception {applies_to}`stack: ga 9.4+`: it is a persisted, space-aware agent that is automatically created in each space.

In a role or API key descriptor, specify the space in the application privilege resource. For example, use `"resources": ["space:production"]` for the `production` space. Users and API keys cannot access resources in spaces outside their assigned resources.

When calling the {{agent-builder}} APIs or MCP server in a custom space, include `/s/<space-name>` before the API path. The default space does not use this prefix.

Learn more about [{{kib}} Spaces](/deploy-manage/manage-spaces.md).

## Conversation access control [conversation-access-control]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

The {{kib}} privileges described above control who can use {{agent-builder}} at all. Individual conversations have a second layer of access control on top of that, so the owner of a conversation can decide who else can read it.

Conversations are private by default. Only the user who created a conversation, its owner, can see it.

### Access modes

An owner can put a conversation into one of two access modes:

- `private`: only the owner and the users listed as members can read and continue the conversation. This is the default.
- `public`: any user who can access the conversation's agent can read and continue it. Public conversations also appear in those users' conversation lists.

Members apply to private conversations only. A public conversation cannot have members.

A conversation belongs to the {{kib}} space it was created in. Sharing does not make it visible from another space.

### The member role

Users you share a conversation with are added as members. `member` is the only available role. It grants two things:

- Read the conversation, including its full history.
- Continue the conversation by sending new messages.

Members cannot rename the conversation, delete it, or change who it is shared with.

You can share with individual users only. Granting access to an {{es}} role is not supported.

Members are identified by their {{kib}} user profile ID, not by username. A user who has never logged in to {{kib}} has no profile and cannot be added.

### Who can do what

| Action | Owner | Member | Other users |
| --- | --- | --- | --- |
| Read and continue | Yes | Yes | Only if the conversation is public |
| Rename | Yes | No | No |
| Delete | Yes | No | No |
| Change sharing | Yes | No | No |

A user with full cluster privileges, such as a superuser, can also rename or delete a `public` conversation they do not own. This does not extend to `private` conversations, even ones shared with them, and it never includes changing who a conversation is shared with.

### Sharing does not bypass privileges

Sharing a conversation grants access to that conversation only. It does not grant any privilege the user does not already have.

A member still needs:

- The `agentBuilder` {{kib}} `Read` privilege.
- Access to the agent the conversation uses.
- Access to the space the conversation belongs to.

Access to the agent is checked every time a conversation is read, and this applies to the owner as well. If anyone loses access to a conversation's agent, or the agent is deleted, the conversation stops being readable for them and disappears from their conversation list.

Managing sharing needs only the `Read` privilege plus ownership. There is no separate sharing privilege, and no write privilege is involved.

When a user cannot access a conversation, {{agent-builder}} reports it as not found rather than as a permissions error. This is deliberate, so that users cannot detect the existence of conversations they cannot read.

To share a conversation, use the [{{kib}} API](kibana-api.md#update-conversation-access-control).

## Configure access

After choosing privileges and space scope, assign them based on who or what needs access.

### Roles for users [#roles-for-users]

Use [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) to bundle the required {{kib}} feature privileges and {{es}} privileges, then assign the roles to users. In the role management UI, choose the required space and feature privileges under **Kibana privileges**, and limit index privileges to the data the users need.

:::{note}
:applies_to: elasticsearch:

When configuring roles in the {{kib}} UI, {{agent-builder}} privileges appear under **Analytics**. In {{serverless-short}} {{es}} projects, they appear under **{{es}}**.
:::

On Serverless, roles also determine what an MCP client can do when it connects to the {{agent-builder}} MCP server through OAuth. The client inherits the permissions of the user who authorizes the connection. To learn more, refer to [OAuth for MCP clients](/deploy-manage/app-connections/oauth-clients.md). {applies_to}`serverless: ga`

### API keys for programmatic clients [#api-keys-for-clients]

Use API keys for custom clients, scripts, MCP clients, and A2A clients. API key role descriptors combine the same {{kib}} application privileges, {{es}} privileges, and space scope described on this page. An API key cannot grant privileges that its owner does not have.

Refer to [Create API keys for {{agent-builder}} APIs](api-keys.md) for complete examples for read-only clients, management clients, and unrestricted development keys. To learn more about API key behavior and management, refer to [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).
