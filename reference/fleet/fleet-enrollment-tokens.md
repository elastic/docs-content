---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-enrollment-tokens.html
description: Create, filter, revoke, and delete Fleet enrollment tokens that enroll Elastic Agents into agent policies, individually or in bulk.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Fleet enrollment tokens [fleet-enrollment-tokens]

A {{fleet}} enrollment token (referred to as an `enrollment API key` in the {{fleet}} API documentation) is an {{es}} API key that you use to enroll one or more {{agents}} in {{fleet}}. The enrollment token enrolls the {{agent}} in a specific agent policy that defines the data to be collected by the agent and which output to use. You can use the token as many times as needed. It remains valid until you revoke or delete it.

The enrollment token is used for the initial communication between {{agent}} and {{fleet-server}}. After the initial connection request from {{agent}}, {{fleet-server}} passes a communication API key to the agent. This API key includes only the necessary permissions to communicate with {{fleet-server}}. If the API key is not valid, {{fleet-server}} stops communicating with {{agent}}.

Depending on the agent policy's output type, {{fleet-server}} also passes additional data to {{agent}}:

* For the {{es}} and remote {{es}} outputs, it passes an output API key.

    This API key is used to send data to {{es}}. It has the minimal permissions needed to ingest all the data specified by the agent policy. If the API key is not valid, {{agent}} stops ingesting data into {{es}}.

* For the Kafka output, it passes authentication parameters.

    The authentication parameters are defined in the authentication settings of the Kafka output and are used by {{agent}} to authenticate with the Kafka cluster before sending data to it.

* For the {{ls}} output, it passes SSL/TLS configuration details.

    The SSL/TLS configuration details such as the SSL certificate authority, the SSL certificate, and the SSL certificate key are defined during {{ls}} output creation. {{agent}} uses SSL/TLS client authentication to authenticate with the {{ls}} pipeline before sending data to it.

:::{note}
Although an API key is generated during {{ls}} output creation, this key is not passed to {{agent}} by {{fleet-server}}. If the {{ls}} pipeline uses the {{es}} output, this API key is used by {{ls}} to authenticate with the {{es}} cluster before sending data to it.
:::

## Create enrollment tokens [create-fleet-enrollment-tokens]

Create enrollment tokens and use them to enroll {{agents}} in specific policies.

::::{tip}
When you use the {{fleet}} UI to create a new agent policy, {{fleet}} automatically creates an enrollment token for that policy.
::::

To create an enrollment token:

1. In {{kib}}, find {{fleet}} in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Open the **Enrollment tokens** tab, then click **Create enrollment token**. 
3. Name your token and select an agent policy.

    The token name you specify must be unique to avoid conflict with any existing API keys.

4. Click **Create enrollment token**.
5. In the list of tokens, click the **Show token** icon {icon}`eye` to display the token secret.

All {{agents}} enrolled with this token use the selected policy unless you assign or enroll them in a different policy.

To learn how to install {{agents}} and enroll them in {{fleet}}, refer to [Install {{agents}}](/reference/fleet/install-elastic-agents.md).

::::{tip}
You can use the {{fleet}} API to get a list of enrollment tokens. For more information, refer to [Fleet enrollment API keys](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-fleet-enrollment-api-keys).
::::

## Filter enrollment tokens [filter-fleet-enrollment-tokens]

The **Enrollment tokens** tab provides controls to help you find specific tokens:

* Use the search bar to filter tokens using [Kibana Query Language (KQL)](elasticsearch://reference/query-languages/kql.md).
* {applies_to}`stack: ga 9.5+` Use the **Agent policy** dropdown to select one or more policies and show only tokens associated with those policies.
* {applies_to}`stack: ga 9.5+` Use the **Active** and **Inactive** filters to show tokens in that status. The **Active** filter is selected by default.

## Revoke enrollment tokens [revoke-fleet-enrollment-tokens]

You can revoke an enrollment token that you no longer want to use to enroll {{agents}} in an agent policy in {{fleet}}. Revoking an enrollment token invalidates the API key, so you can no longer use this token to enroll agents. Agents that are already enrolled continue to function.

To revoke an enrollment token:

1. In {{fleet}}, open the **Enrollment tokens** tab.
2. Locate the token you want to revoke. Use the [filters](#filter-fleet-enrollment-tokens) if needed.
3. In the **Actions** column for the token:

   * {applies_to}`stack: ga 9.5+` Click the actions icon {icon}`ellipsis`, then select **Revoke**.
   * {applies_to}`stack: ga 9.0-9.4` Click the **Revoke token** icon {icon}`trash`.

4. In the confirmation dialog, confirm the action.

{applies_to}`stack: ga 9.5+` To revoke several tokens in a single operation, refer to [Bulk revoke or delete enrollment tokens](#bulk-revoke-delete-fleet-enrollment-tokens).

Revoking an enrollment token doesn't delete it immediately. Deletion occurs automatically after the duration specified in the {{es}} [`xpack.security.authc.api_key.delete.retention_period`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#api-key-service-settings-delete-retention-period) setting has expired. Refer to [Invalidate API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-invalidate-api-key) for details.

Until the enrollment token is deleted:

* The token name can't be reused when you [create an enrollment token](#create-fleet-enrollment-tokens).
* You can still view the token in the {{fleet}} UI.
* The token is returned by a `GET /api/fleet/enrollment_api_keys` API request. Revoked enrollment tokens are identified by `"active": false`.

## Delete enrollment tokens [delete-fleet-enrollment-tokens]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Deleting an enrollment token invalidates the underlying API key and removes the token document from {{es}}.

:::{note}
Tokens that belong to managed or agentless agent policies don't appear on the **Enrollment tokens** tab and can't be managed from the UI.
:::

To delete an enrollment token:

1. In {{fleet}}, open the **Enrollment tokens** tab.
2. Locate the token to delete. Use the [filters](#filter-fleet-enrollment-tokens) if needed.
3. In the **Actions** column for the token, click the actions icon {icon}`ellipsis`, then select **Delete token**.
4. In the confirmation dialog, click **Delete token**.

## Revoke or delete multiple enrollment tokens [bulk-revoke-delete-fleet-enrollment-tokens]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

To revoke or delete multiple enrollment tokens at the same time:

1. In {{fleet}}, open the **Enrollment tokens** tab.
2. Use the [filters](#filter-fleet-enrollment-tokens) to narrow the list, if needed.
3. Select the checkboxes for the tokens you want to manage. To select every token that matches the current filters, select the checkbox in the table header.
4. From the **_x_ tokens selected** menu, select **Revoke tokens** or **Delete tokens**.
5. In the confirmation dialog, confirm the action.

A notification reports the number of tokens that were processed successfully and any errors that occurred. Tokens that belong to managed or agentless policies are skipped automatically.

::::{tip}
To perform bulk operations programmatically, use the `POST /api/fleet/enrollment_api_keys/_bulk_delete` endpoint. For more information, refer to [Bulk revoke or delete enrollment API keys](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-enrollment-api-keys-bulk-delete).
::::