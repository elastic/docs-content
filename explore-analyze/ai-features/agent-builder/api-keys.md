---
navigation_title: "Create API keys"
description: "Create API keys with the privileges required to access Agent Builder APIs, MCP clients, and A2A clients."
type: how-to
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Create API keys for {{agent-builder}}

Use an API key to authenticate applications that call {{agent-builder}} programmatically, including custom clients, scripts that use `curl`, [MCP clients](mcp-server.md), and [A2A clients](a2a-server.md).

API keys use the same {{kib}} feature privileges as roles. The role management UI displays names such as **Agent Builder: Read**, while an API key role descriptor uses the corresponding application privilege name, such as `feature_agentBuilder.read`.

## Before you begin

Before creating an API key:

- Make sure the user creating the key has the `manage_api_key` or `manage_own_api_key` cluster privilege.
- Create the key as a user, not by authenticating the request with another API key. An API key can create only a derived key with no privileges.
- Make sure the user creating the key has every privilege that you assign to the key. An API key cannot grant more privileges than its owner has.
- Identify the {{kib}} [space](/deploy-manage/manage-spaces.md) that the client will access. The examples use the default space.
- Identify the index patterns that agents and tools need to query. Replace `customer-*` in the examples with your own patterns.
- Determine whether agents use {{es}} inference endpoints, {{kib}} connectors, or workflows. These features require additional privileges.
- If you're using `curl`, set the {{es}} URL, {{kib}} URL, and username:

  ```bash
  export ELASTICSEARCH_URL="https://<elasticsearch-host>" <1>
  export KIBANA_URL="https://<kibana-host>" <2>
  export ELASTIC_USERNAME="<username>" <3>
  ```

  1. Use `ELASTICSEARCH_URL` to create API keys with the {{es}} `/_security/api_key` API. To locate it, refer to [Find your {{es}} endpoint](/solutions/elasticsearch-solution-project/search-connection-details.md).
  2. Use `KIBANA_URL` to call the {{agent-builder}} APIs under `/api/agent_builder`.
  3. `ELASTIC_USERNAME` is the username of the user creating the key. The `curl` examples prompt you for this user's password.

Refer to the [privilege reference](permissions.md#privilege-reference) for the exact privilege names to use in a role descriptor.

## Create a read-only client key

The following example creates a key for a client that can use agents and view {{agent-builder}} components, but cannot create, update, or delete them. The key can read data only from indices matching `customer-*`.

::::{tab-set}

:::{tab-item} Console

Run the following request in [Console](/explore-analyze/query-filter/tools/console.md). The key is owned by the user who is signed in to {{kib}}:

```console
POST /_security/api_key
{
  "name": "agent-builder-read-only",
  "expiration": "30d",
  "role_descriptors": {
    "agent-builder-read-only": {
      "cluster": ["monitor_inference"], <1>
      "indices": [
        {
          "names": ["customer-*"], <2>
          "privileges": ["read", "view_index_metadata"]
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana", <3>
          "privileges": [
            "feature_agentBuilder.read", <4>
            "feature_actions.read",
            "feature_workflowsManagement.read"
          ],
          "resources": ["space:default"] <5>
        }
      ]
    }
  }
}
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.read` provides read-only access to {{agent-builder}}. The other two privileges provide read-only access to connectors and workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

:::{tab-item} curl

```bash
curl --user "${ELASTIC_USERNAME}" \
  -X POST "${ELASTICSEARCH_URL}/_security/api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agent-builder-read-only",
    "expiration": "30d",
    "role_descriptors": {
      "agent-builder-read-only": {
        "cluster": ["monitor_inference"], <1>
        "indices": [
          {
            "names": ["customer-*"], <2>
            "privileges": ["read", "view_index_metadata"]
          }
        ],
        "applications": [
          {
            "application": "kibana-.kibana", <3>
            "privileges": [
              "feature_agentBuilder.read", <4>
              "feature_actions.read",
              "feature_workflowsManagement.read"
            ],
            "resources": ["space:default"] <5>
          }
        ]
      }
    }
  }'
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.read` provides read-only access to {{agent-builder}}. The other two privileges provide read-only access to connectors and workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

:::{tab-item} API keys UI

1. Open the **API keys** management page and select **Create API key**.
2. Enter a name and expiration for the key.
3. Enable **Control security privileges**.
4. Paste the following role descriptor into the editor, then create the key:

```json
{
  "agent-builder-read-only": {
    "cluster": ["monitor_inference"], <1>
    "indices": [
      {
        "names": ["customer-*"], <2>
        "privileges": ["read", "view_index_metadata"]
      }
    ],
    "applications": [
      {
        "application": "kibana-.kibana", <3>
        "privileges": [
          "feature_agentBuilder.read", <4>
          "feature_actions.read",
          "feature_workflowsManagement.read"
        ],
        "resources": ["space:default"] <5>
      }
    ]
  }
}
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.read` provides read-only access to {{agent-builder}}. The other two privileges provide read-only access to connectors and workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

::::

Remove privileges that the client does not need:

- Remove `feature_actions.read` if agents do not use {{kib}} connectors.
- Remove `feature_workflowsManagement.read` if agents do not interact with workflows.
- Remove `monitor_inference` if agents and tools do not call the {{es}} Inference API.

## Create a key that can manage agents, tools, skills, and workflows

The following example allows a client to manage {{agent-builder}} components and workflows while keeping the underlying index access read-only.

::::{tab-set}

:::{tab-item} Console

```console
POST /_security/api_key
{
  "name": "agent-builder-management",
  "expiration": "30d",
  "role_descriptors": {
    "agent-builder-management": {
      "cluster": ["monitor_inference"], <1>
      "indices": [
        {
          "names": ["customer-*"], <2>
          "privileges": ["read", "view_index_metadata"]
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana", <3>
          "privileges": [
            "feature_agentBuilder.all", <4>
            "feature_actions.read",
            "feature_workflowsManagement.all"
          ],
          "resources": ["space:default"] <5>
        }
      ]
    }
  }
}
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.all` allows the client to manage {{agent-builder}} components. `feature_actions.read` allows it to use connectors, and `feature_workflowsManagement.all` allows it to manage workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

:::{tab-item} curl

```bash
curl --user "${ELASTIC_USERNAME}" \
  -X POST "${ELASTICSEARCH_URL}/_security/api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agent-builder-management",
    "expiration": "30d",
    "role_descriptors": {
      "agent-builder-management": {
        "cluster": ["monitor_inference"], <1>
        "indices": [
          {
            "names": ["customer-*"], <2>
            "privileges": ["read", "view_index_metadata"]
          }
        ],
        "applications": [
          {
            "application": "kibana-.kibana", <3>
            "privileges": [
              "feature_agentBuilder.all", <4>
              "feature_actions.read",
              "feature_workflowsManagement.all"
            ],
            "resources": ["space:default"] <5>
          }
        ]
      }
    }
  }'
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.all` allows the client to manage {{agent-builder}} components. `feature_actions.read` allows it to use connectors, and `feature_workflowsManagement.all` allows it to manage workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

:::{tab-item} API keys UI

Enable **Control security privileges** and paste the following role descriptor into the editor:

```json
{
  "agent-builder-management": {
    "cluster": ["monitor_inference"], <1>
    "indices": [
      {
        "names": ["customer-*"], <2>
        "privileges": ["read", "view_index_metadata"]
      }
    ],
    "applications": [
      {
        "application": "kibana-.kibana", <3>
        "privileges": [
          "feature_agentBuilder.all", <4>
          "feature_actions.read",
          "feature_workflowsManagement.all"
        ],
        "resources": ["space:default"] <5>
      }
    ]
  }
}
```

1. `monitor_inference` is required when agents or tools call the {{es}} Inference API. Remove it if they do not.
2. Replace `customer-*` with the index patterns that the client needs. The assigned index privileges allow reads and access to index mappings, but not writes.
3. Use `kibana-.kibana` as the application name for {{kib}} feature privileges.
4. `feature_agentBuilder.all` allows the client to manage {{agent-builder}} components. `feature_actions.read` allows it to use connectors, and `feature_workflowsManagement.all` allows it to manage workflows.
5. Replace `space:default` if the client uses a different {{kib}} space.

:::

::::

The `feature_agentBuilder.all` application privilege does not grant write access to indices. Tools continue to run with only the `read` and `view_index_metadata` index privileges assigned to the key.

## Create an unrestricted development key

:::{warning}
An unrestricted key can access everything its owner can access. Use this approach only for development or trusted administrative automation. Before using a key in production, replace it with a restricted key that grants only the required spaces, indices, and features.
:::

For short-lived development or administrative automation, you can create a key without role descriptors:

::::{tab-set}

:::{tab-item} Console

```console
POST /_security/api_key
{
  "name": "agent-builder-development",
  "expiration": "1d"
}
```

:::

:::{tab-item} curl

```bash
curl --user "${ELASTIC_USERNAME}" \
  -X POST "${ELASTICSEARCH_URL}/_security/api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agent-builder-development",
    "expiration": "1d"
  }'
```

:::

:::{tab-item} API keys UI

Enter a name and expiration for the key, leave **Control security privileges** disabled, and create the key.

:::

::::

The key inherits a point-in-time snapshot of the privileges of the user who creates it. It is an administrator key only when the owner has administrator privileges.

## Use the API key

The create API returns an `encoded` value. Store that value securely and send it in the `Authorization` header:

```bash
export API_KEY="<encoded-api-key>" <1>

curl -X GET "${KIBANA_URL}/api/agent_builder/tools" \
  -H "Authorization: ApiKey ${API_KEY}"
```

1. Use the `encoded` value returned by the create API, not the separate `id` or `api_key` values.

For a non-default space, include the space in the request URL and make sure it matches the application privilege resource:

```bash
curl -X GET "${KIBANA_URL}/s/production/api/agent_builder/tools" \ <1>
  -H "Authorization: ApiKey ${API_KEY}"
```

1. The space identifier in the URL must match the role descriptor resource. In this example, the role descriptor must use `"resources": ["space:production"]`.

## Troubleshoot API keys

The following list pairs common API key symptoms with checks or changes that can resolve them.

`401 Unauthorized`
:   Make sure the header uses the `encoded` value returned by the create API, not the separate `id` or `api_key` fields.

`403 Forbidden`
:   Check that the key has the required {{kib}} application privilege and that the space in the URL matches the `resources` value. Also make sure the key owner had the privilege when the key was created.

An agent or tool cannot find data
:   Check the index patterns and make sure the key has both `read` and `view_index_metadata` for the required indices.

Connector or model requests fail
:   Add `feature_actions.read` for {{kib}} connectors. Add `monitor_inference` for {{es}} inference endpoints and tools that use the {{es}} Inference API.

Workflow requests fail
:   Add `feature_workflowsManagement.read` to read workflows, `feature_workflowsManagement.workflow_execute` to run them, or `feature_workflowsManagement.all` to manage them.

The create API rejects the role descriptor for a derived key
:   Authenticate the create request as a user. When the request is authenticated with an API key, {{es}} requires an explicit role descriptor with no privileges.

Learn more about [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md) and [{{agent-builder}} permissions](permissions.md).
