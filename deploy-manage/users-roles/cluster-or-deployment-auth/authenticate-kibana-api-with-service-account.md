---
navigation_title: Authenticate to Kibana APIs
applies_to:
  stack: ga 9.6+
  serverless: unavailable
description: Create a service token and use a user-managed service account to authenticate to Kibana APIs.
products:
  - id: kibana
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Authenticate to the {{kib}} API with a service account [authenticate-kibana-api-service-account]

Use a user-managed service account to authenticate programmatic requests to {{kib}}. The account provides a non-human identity whose privileges come from its assigned roles.

## Before you begin [authenticate-kibana-api-service-account-prerequisites]

Before you create a service token, make sure you have the following:

- You need an existing user-managed service account. If you don't have one, [create a service account in {{kib}}](manage-service-accounts-in-kibana.md#create-service-account-kibana).
- You need the `manage_security` cluster privilege to create a service token for a user-managed account. The `manage_service_account` privilege permits token management only for built-in accounts in the `elastic` namespace.

## Create a token for your application [create-service-account-api-token]

{{kib}} creates and stores a credential when you create an account in the UI. That credential is used for workload integrations and isn't displayed. For your application, create an additional service token. The following example uses an existing account with the principal `kibana/automation-client`:

1. Use the [create service account token API]({{es-apis}}operation/operation-security-create-service-token) to create a token for the account:

    ```console
    POST /_security/service/kibana/automation-client/credential/token/production
    ```

2. Copy the `token.value` from the response and store it securely, such as in a secrets manager. Service tokens don't expire, and you can't retrieve this value again.

## Call a {{kib}} API [call-kibana-api-service-account]

To call the {{kib}} API using the service account identity, send the token with the `Bearer` authentication scheme:

```shell
curl --request GET "$KIBANA_URL/api/spaces/space" \
  --header "Authorization: Bearer $SERVICE_ACCOUNT_TOKEN"
```

Ensure that your [HTTP authentication configuration](kibana-authentication.md#http-authentication) accepts the `Bearer` scheme.

The response depends on the account's roles. A `403` response means the account authenticated but doesn't have the required privilege. Add privileges by editing the assigned role rather than assigning broad administrative roles to the account.

For requests that change data, also include the headers required by that API, such as `kbn-xsrf`.

## Call an {{es}} API [call-elasticsearch-api-service-account]

You can use the same token to authenticate to {{es}}. For example, verify the account's identity with the authenticate API:

```shell
curl --request GET "$ELASTICSEARCH_URL/_security/_authenticate" \
  --header "Authorization: Bearer $SERVICE_ACCOUNT_TOKEN"
```

## Remove access [remove-service-account-api-access]

Service tokens don't expire. When an application no longer needs access, use the [delete service account token API]({{es-apis}}operation/operation-security-delete-service-token) to delete only its token:

```console
DELETE /_security/service/kibana/automation-client/credential/token/production
```

Deleting the token stops requests that use it without affecting the account or its other service tokens.

To prevent new authentications with any of the account's service tokens, [deactivate the account](manage-service-accounts-in-kibana.md#disable-service-account). To permanently remove the identity and its associated credentials, [delete the account in {{kib}}](manage-service-accounts-in-kibana.md#delete-service-account-kibana).
