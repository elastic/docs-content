---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/service-accounts.html
applies_to:
  stack: all
  serverless: unavailable
description: Learn how built-in and user-managed service accounts provide non-human identities for Elastic services and workloads.
products:
  - id: elasticsearch
  - id: kibana
---

# Service accounts [service-accounts]

A service account is a non-human identity for a service or workload. Unlike a user, a service account isn't associated with a person and can't log in to the {{kib}} UI.

Service accounts authenticate with service tokens. The account defines the identity and privileges, while the token is a credential for that identity. For example, {{fleet}} server uses a service token to authenticate with {{es}} and manage its own API keys.

You can create multiple service tokens for the same service account. This lets multiple instances of a service use the same identity without sharing credentials.

::::{important}
Don't use service accounts to authenticate individual users. Service tokens are credentials for software and workloads, not people.
::::

$$$service-accounts-explanation$$$

Each service account has a unique identifier, called a principal, in the form `<namespace>/<service>`. The `namespace` groups related accounts, and the `service` name must be unique within that namespace.

Service accounts are not included in the response of the [get users API]({{es-apis}}operation/operation-security-get-user). To retrieve a service account, use the [get service accounts API]({{es-apis}}operation/operation-security-get-service-accounts). Use the [get service account credentials API]({{es-apis}}operation/operation-security-get-service-credentials) to retrieve all service credentials for a service account.

## Service account types [service-account-types]

Service accounts can be built-in, with privileges defined by Elastic, or user-managed, with privileges determined by the roles you assign.

### Built-in service accounts [built-in-service-accounts]

Built-in service accounts are predefined in code, always enabled, and have fixed privileges.

A built-in service account corresponds to a specific service.

The following built-in accounts are available:

`elastic/fleet-server`
:   The service account used by the {{fleet}} server to communicate with {{es}}.

`elastic/kibana`
:   The service account used by {{kib}} to communicate with {{es}}.

The `elastic` namespace is reserved for built-in accounts.

You can create and delete service tokens for these accounts, but you can't change their predefined privileges.

### User-managed service accounts [user-managed-service-accounts]
```{applies_to}
stack: ga 9.6+
```

You create these accounts and assign roles to control their privileges. Accounts created in {{kib}} have IDs such as `kibana/order-processing`.

Use a user-managed service account when your application needs its own identity to access {{es}} or {{kib}} APIs. Assign the roles required by the application, and authenticate its requests with a [service account token](#service-accounts-tokens).

In {{stack}} 9.6, [Workflows](/explore-analyze/workflows.md) is the only {{kib}} application that supports directly assigning a service account as the execution identity of a workload. {{kib}} manages the credential used for this integration.

To manage service accounts and use them in your own applications:

- [Create and manage service accounts in {{kib}}](manage-service-accounts-in-kibana.md).
- [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).

To use service accounts with {{kib}} Workflows, refer to [Run a workflow as a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md).

The {{es}} API reference also documents these operations:

- [Create or replace an account]({{es-apis}}operation/operation-security-put-user-managed-service-account).
- [Delete an account]({{es-apis}}operation/operation-security-delete-user-managed-service-account).

% TBD: Add the query service accounts API link when elasticsearch-specification includes the endpoint from elastic/elasticsearch#159406.
% Serverless follow-up: publish only after availability is confirmed. Reuse these pages with deployment-specific sections for the 50-role limit, creator privilege ceiling, user-only management, and cross-project role resolution.
% Serverless follow-up: omit the encryption-key prerequisite and direct service-token API instructions. Document deletion and token expiry instead of disabling an account. Confirm mixed-project-type restrictions before documenting them.

## Service account tokens [service-accounts-tokens]

A service account token, or service token, is a unique string that a service uses to authenticate with {{es}}. For a given service account, each token must have a unique name. Because tokens include access credentials, they should always be kept secret by whichever client is using them.

:::{note}
:applies_to: {"stack": "ga 9.6+", "serverless": "unavailable"}
When you create a user-managed service account in {{kib}}, {{kib}} creates and stores a service token so applications such as Workflows can run on behalf of the account. This token isn't displayed. To authenticate requests from your own application, create an additional service token with the API.
:::

You can create a service token using either:

* The [create service account token API]({{es-apis}}operation/operation-security-create-service-token) (recommended). The API stores the token in the `.security` index and returns the bearer token in the HTTP response. Tokens are available for authentication on all nodes and are included in cluster snapshots.
* The [elasticsearch-service-tokens](elasticsearch://reference/elasticsearch/command-line-tools/service-tokens-command.md) CLI tool, for built-in accounts on self-managed and {{eck}} deployments. The tool stores the token in the [`$ES_HOME/config/service_tokens` file](elasticsearch://reference/elasticsearch/command-line-tools/service-tokens-command.md) and outputs the bearer token to your terminal. This method is intended for environments where an external orchestration process, such as [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) or [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), manages and distributes the file.

Both the API and CLI generate service tokens with a 22-character secret. {{es}} requires a secret of at least 10 characters and rejects shorter secrets without checking their value.

Service tokens never expire. You must actively [delete]({{es-apis}}operation/operation-security-delete-service-token) them if they are no longer needed.

For an overview of how service tokens, access tokens, and API keys are used for authentication, refer to [Token-based authentication services](token-based-authentication-services.md).


### Authenticate with service tokens [authenticate-with-service-account-token]

To authenticate requests to {{es}}, include the service token in the `Authorization: Bearer` header of each request. Service accounts don't support basic authentication.

### Verify a service token [verify-service-account-token]

You can verify a service token, for example, by calling the [authenticate API]({{es-apis}}operation/operation-security-authenticate) (`GET /_security/_authenticate`). This API returns information about the authenticated identity, including its principal, assigned roles, and authentication details.

Set `ELASTICSEARCH_URL` to your deployment's HTTPS endpoint and `SERVICE_ACCOUNT_TOKEN` to your service token:

```bash
curl --request GET "$ELASTICSEARCH_URL/_security/_authenticate" \
  --header "Authorization: Bearer $SERVICE_ACCOUNT_TOKEN"
```

The following examples show the response for each type of service account:

::::{tab-set}

:::{tab-item} Built-in service account

This example uses the `elastic/fleet-server` account, which has predefined privileges:

```json
{
  "username": "elastic/fleet-server",
  "roles": [],
  "full_name": "Service account - elastic/fleet-server",
  "email": null,
  "token": {
    "name": "production",
    "type": "_service_account_index"
  },
  "metadata": {
    "_elastic_service_account": true
  },
  "enabled": true,
  "authentication_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "lookup_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "authentication_type": "token"
}
```

:::

:::{tab-item} User-managed service account
{applies_to}`stack: ga 9.6+`

This example uses the `kibana/automation-client` account with the `automation_client` role:

```json
{
  "username": "kibana/automation-client",
  "roles": [
    "automation_client"
  ],
  "full_name": "User-managed service account - kibana/automation-client",
  "email": null,
  "token": {
    "name": "production",
    "type": "_service_account_index"
  },
  "metadata": {
    "_user_managed_service_account": true
  },
  "enabled": true,
  "authentication_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "lookup_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "authentication_type": "token"
}
```

:::

::::

In both responses:

- `username` is the principal of the authenticated account.
- `roles` lists the assigned role names. Built-in accounts return an empty array because their privileges are predefined.
- `token` describes the credential used for the request. Its `name` is the service token's name, and its `type` identifies the storage backend: `_service_account_index` for tokens stored in the `.security` index, or `_service_account_file` for file-backed tokens used by built-in accounts.
- `metadata` identifies the account type: `_elastic_service_account` for built-in accounts or `_user_managed_service_account` for user-managed accounts.

{applies_to}`stack: ga 9.6+` To authenticate calls to {{kib}} with a user-managed service account, refer to [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).

## Audit user-managed service account activity [audit-service-account-activity]
```{applies_to}
stack: ga 9.6+
serverless: unavailable
```

{{kib}} [audit events](kibana://reference/kibana-audit-events.md) record account creation and deletion, changes to workload assignments, and attempts to run a workload as an account. The `service_account_assume` event identifies the account and workload execution. Events caused by that workload identify the service account as the acting principal.

{{es}} [audit events](elasticsearch://reference/elasticsearch/elasticsearch-audit-events.md) also attribute requests that use a service account credential to the account.

% Follow-up in elastic/kibana: change the service account audit event lifecycle labels from preview to GA for 9.6. The service_account_assume event is already documented after #295817 merged.
