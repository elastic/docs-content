---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-enrollment-tokens.html
---

# Fleet enrollment tokens [fleet-enrollment-tokens]

A {{fleet}} enrollment token (referred to as an `enrollment API key` in the {{fleet}} API documentation) is an {{es}} API key that you use to enroll one or more {{agent}}s in {{fleet}}. The enrollment token enrolls the {{agent}} in a specific agent policy that defines the data to be collected by the agent. You can use the token as many times as required. It will remain valid until you revoke it.

The enrollment token is used for the initial communication between {{agent}} and {{fleet-server}}. After the initial connection request from the {{agent}}, the {{fleet-server}} passes two API keys to the {{agent}}:

* An output API key

    This API key is used to send data to {{es}}. It has the minimal permissions needed to ingest all the data specified by the agent policy. If the API key is invalid, the {{agent}} stops ingesting data into {{es}}.

* A communication API key

    This API key is used to communicate with the {{fleet-server}}. It has only the permissions needed to communicate with the {{fleet-server}}. If the API key is invalid, {{fleet-server}} stops communicating with the {{agent}}.



## Create enrollment tokens [create-fleet-enrollment-tokens]

Create enrollment tokens and use them to enroll {{agent}}s in specific policies.

::::{tip}
When you use the {{fleet}} UI to add an agent or create a new policy, {{fleet}} creates an enrollment token for you automatically.
::::


To create an enrollment token:

1. In {{kib}}, go to **Management → {{fleet}} → Enrollment tokens**.
2. Click  **Create enrollment token**. Name your token and select an agent policy.

    Note that the token name you specify must be unique so as to avoid conflict with any existing API keys.

    :::{image} images/create-token.png
    :alt: Enrollment tokens tab in {fleet}
    :class: screenshot
    :::

3. Click **Create enrollment token**.
4. In the list of tokens, click the **Show token** icon to see the token secret.

    :::{image} images/show-token.png
    :alt: Enrollment tokens tab with Show token icon highlighted
    :class: screenshot
    :::


All {{agent}}s enrolled through this token will use the selected policy unless you assign or enroll them in a different policy.

To learn how to install {{agent}}s and enroll them in {{fleet}}, refer to [*Install {{agent}}s*](/reference/ingestion-tools/fleet/install-elastic-agents.md).

::::{tip}
You can use the {{fleet}} API to get a list of enrollment tokens. For more information, refer to [{{kib}} {{fleet}} APIs](/reference/ingestion-tools/fleet/fleet-api-docs.md).
::::



## Revoke enrollment tokens [revoke-fleet-enrollment-tokens]

You can revoke an enrollment token that you no longer wish to use to enroll {{agents}} in an agent policy in {{fleet}}. Revoking an enrollment token essentially invalidates the API key used by agents to communicate with {{fleet-server}}.

To revoke an enrollment token:

1. In {{fleet}}, click **Enrollment tokens**.
2. Find the token you want to revoke in the list and click the **Revoke token** icon.

    :::{image} images/revoke-token.png
    :alt: Enrollment tokens tab with Revoke token highlighted
    :class: screenshot
    :::

3. Click **Revoke enrollment token**. You can no longer use this token to enroll {{agent}}s. However, the currently enrolled agents will continue to function.

    To re-enroll your {{agent}}s, use an active enrollment token.


Note that when an enrollment token is revoked it is not immediately deleted. Deletion occurs automatically after the duration specified in the {{es}} [`xpack.security.authc.api_key.delete.retention_period`](elasticsearch://docs/reference/elasticsearch/configuration-reference/security-settings.md#api-key-service-settings-delete-retention-period) setting has expired (see [Invalidate API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-invalidate-api-key) for details).

Until the enrollment token has been deleted:

* The token name may not be re-used when you [create an enrollment token](#create-fleet-enrollment-tokens).
* The token continues to be visible in the {{fleet}} UI.
* The token continues to be returned by a `GET /api/fleet/enrollment_api_keys` API request. Revoked enrollment tokens are identified as `"active": false`.
