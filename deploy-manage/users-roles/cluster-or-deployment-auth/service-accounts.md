---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/service-accounts.html
applies_to:
  stack: all
  serverless: ga
description: Learn how built-in and user-managed service accounts provide non-human identities for Elastic services and workloads.
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
---

# Service accounts [service-accounts]

A service account is a non-human identity for a service or workload. Unlike a user, a service account isn't associated with a person and can't log in to the {{kib}} UI.

Service accounts authenticate with tokens. The account defines the identity and privileges, while the token is a credential for that identity.

::::{important}
Don't use service accounts to authenticate individual users. Service account credentials are for software and workloads, not people.
::::

This page refers to {{ech}}, {{ece}}, {{eck}}, and self-managed deployments as {{stack}} deployments. In these environments, {{es}} stores and manages user-managed service accounts. In {{serverless-full}} projects, {{ecloud}} manages these accounts at the organization level. These differences affect account identifiers, credentials, and the available management APIs.

$$$service-accounts-explanation$$$

Each service account has a unique identifier, called a principal. In {{stack}} deployments, the principal has the form `<namespace>/<service>`. The `namespace` groups related accounts, and the `service` name must be unique within that namespace.

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

In {{stack}}, you can create and delete service tokens for these accounts, but you can't change their predefined privileges. On {{serverless-short}}, Elastic manages their credentials.

### User-managed service accounts [user-managed-service-accounts]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

You create user-managed service accounts and assign roles to control their privileges. These accounts belong to the deployment on {{stack}} or to the Cloud organization on {{serverless-short}}, rather than to the user who created them.

In {{stack}}, accounts created in {{kib}} use the `kibana` namespace, and their principals have the form `kibana/<name>`. On {{serverless-short}}, accounts have a generated identifier that is independent of the name you enter in {{kib}}.

Use a user-managed service account when your workload needs its own identity to access {{es}} or {{kib}} APIs. Assign the roles required by the workload.

[Workflows](/explore-analyze/workflows.md) is the only {{kib}} application that supports directly assigning a service account as the execution identity of a workload. To use this integration, create the service account in {{kib}}, which manages the credential for you.

:::{note}
:applies_to: serverless: ga
On {{serverless-short}}, user-managed service accounts can only be used within {{kib}} applications. The {{es}} service account APIs aren't available for these accounts. For programmatic access from external applications, use [API keys](/deploy-manage/api-keys.md).
:::

To manage service accounts and use them in your workloads:

- [Create and manage service accounts in {{kib}}](manage-service-accounts-in-kibana.md).
- {applies_to}`serverless: unavailable` [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).

To use service accounts with {{kib}} Workflows, refer to [Run a workflow as a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md).

On {{stack}}, the {{es}} API reference also documents these operations:

- [Create or replace an account]({{es-apis}}operation/operation-security-put-user-managed-service-account).
- [Delete an account]({{es-apis}}operation/operation-security-delete-user-managed-service-account).

## Service account tokens [service-accounts-tokens]
```{applies_to}
stack: all
serverless: unavailable
```

A service account token, or service token, is a credential that a service or workload uses to authenticate requests to {{es}} or {{kib}} APIs. Treat service tokens as secrets: anyone who has a valid token can authenticate as the service account.

For example, {{fleet}} server uses a service token to authenticate with {{es}} and manage its own API keys. You can create multiple service tokens for the same service account. This lets multiple instances of a service use the same identity without sharing credentials.

:::{note}
:applies_to: stack: ga 9.6+
When you [create a user-managed service account in {{kib}}](manage-service-accounts-in-kibana.md), {{kib}} creates and stores a service token named `kibana-managed` so applications such as Workflows can run on behalf of the account. This token isn't displayed. To authenticate requests from your own application, create an additional service token with the API.
:::

You can create a service token using either:

* The [create service account token API]({{es-apis}}operation/operation-security-create-service-token) (recommended). The API stores the token in the `.security` index and returns the bearer token in the HTTP response. Tokens are available for authentication on all nodes and are included in cluster snapshots.
* The [elasticsearch-service-tokens](elasticsearch://reference/elasticsearch/command-line-tools/service-tokens-command.md) CLI tool, for built-in accounts on self-managed and {{eck}} deployments. The tool stores the token in the [`$ES_HOME/config/service_tokens` file](elasticsearch://reference/elasticsearch/command-line-tools/service-tokens-command.md) and outputs the bearer token to your terminal. This method is intended for environments where an external orchestration process, such as [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) or [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), manages and distributes the file.

Both the API and CLI generate service tokens with a 22-character secret. {{es}} requires a secret of at least 10 characters and rejects shorter secrets without checking their value.

Service tokens never expire. You must actively [delete]({{es-apis}}operation/operation-security-delete-service-token) them if they are no longer needed.

Service tokens are different from short-lived access tokens, which expire automatically. For an overview of these credential types and API keys, refer to [Token-based authentication services](token-based-authentication-services.md).


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

:::{note}
Service accounts are not included in the response of the [get users API]({{es-apis}}operation/operation-security-get-user). To retrieve a service account, use the [get service accounts API]({{es-apis}}operation/operation-security-get-service-accounts). Use the [get service account credentials API]({{es-apis}}operation/operation-security-get-service-credentials) to retrieve all service credentials for a service account.
:::

{applies_to}`stack: ga 9.6+` To authenticate calls to {{kib}} with a user-managed service account, refer to [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).

## Audit user-managed service account activity [audit-service-account-activity]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

{{kib}} [audit events](kibana://reference/kibana-audit-events.md) record account creation and deletion, changes to workload assignments, and attempts to run a workload as an account. The `service_account_assume` event identifies the account and workload execution. Events caused by that workload identify the service account as the acting principal.

In {{stack}}, {{es}} [audit events](elasticsearch://reference/elasticsearch/elasticsearch-audit-events.md) also attribute requests that use a service account credential to the account.

On {{serverless-short}}, configure [audit trail log delivery](/deploy-manage/monitor/log-delivery/audit-trail.md) to collect audit logs from your project.

% Serverless verification: Confirm Elasticsearch audit attribution for UIAM-backed service accounts.
