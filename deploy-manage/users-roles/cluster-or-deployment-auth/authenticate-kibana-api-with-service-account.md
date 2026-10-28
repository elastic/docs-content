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

- You need the `manage_security` cluster privilege to create a user-managed account and its service token.
- Create a role that grants only the {{kib}} and {{es}} privileges required by the API operations.
- Store the service token in a secrets manager. Service tokens don't expire and grant direct access to the account's privileges.

## Create a token for your application [create-service-account-api-token]

{{kib}} creates and stores a credential when you create an account in the UI. That credential is used for workload integrations and isn't displayed. For your application, create an additional service token:

1. [Create a service account in {{kib}}](manage-service-accounts-in-kibana.md#create-service-account-kibana). For this example, name it `automation-client` and assign the `automation_client` role. The account's principal is `kibana/automation-client`.

2. Use the [create service account token API]({{es-apis}}operation/operation-security-create-service-token) to create a token for the account:

    ```console
    POST /_security/service/kibana/automation-client/credential/token/production
    ```

3. Copy the `token.value` from the response and store it securely. You can't retrieve the value again.

:::{note}
The `elasticsearch.serviceAccountToken` {{kib}} setting has a different purpose. It configures the {{kib}} server to connect to {{es}} as the built-in `elastic/kibana` account. It doesn't provide a token for an external API client or bind a user-managed account to a workload.
:::

## Call a {{kib}} API [call-kibana-api-service-account]

To call the {{kib}} API using the service account identity, send the token with the `Bearer` authentication scheme:

```shell
curl --request GET "$KIBANA_URL/api/spaces/space" \
  --header "Authorization: Bearer $SERVICE_ACCOUNT_TOKEN"
```

Ensure that your [HTTP authentication configuration](kibana-authentication.md#http-authentication) accepts the `Bearer` scheme.

The response depends on the account's roles. A `403` response means the account authenticated but doesn't have the required privilege. Add privileges by editing the assigned role rather than assigning broad administrative roles to the account.

For requests that change data, also include the headers required by that API, such as `kbn-xsrf`.

## Remove access [remove-service-account-api-access]

Delete an individual service token to stop one client without affecting other clients that use the same account. Delete the account or set `enabled: false` to stop new authentications for all its service tokens.

Deleting an account invalidates its service tokens and access tokens, but it doesn't invalidate API keys owned by the account. Rules and tasks that obtained an API key while authenticated as the account can continue to run with that key. To revoke this access, [invalidate the API keys]({{es-apis}}operation/operation-security-invalidate-api-key) explicitly.

To manage an account in the UI, refer to [Create and manage service accounts in {{kib}}](manage-service-accounts-in-kibana.md).
