---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/grant-access-to-elasticsearch.html
---

# Grant standalone Elastic Agents access to Elasticsearch [grant-access-to-elasticsearch]

You can use either API keys or user credentials to grant standalone {{agent}}s access to {{es}} resources. The following minimal permissions are required to send logs, metrics, traces, and synthetics to {{es}}:

* `monitor` cluster privilege
* `auto_configure` and `create_doc` index privileges on `logs-*-*`, `metrics-*-*`, `traces-*-*`, and `synthetics-*-*`.

It’s recommended that you use API keys to avoid exposing usernames and passwords in configuration files.

If you’re using {{fleet}}, refer to [{{fleet}} enrollment tokens](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md).


## Create API keys for standalone agents [create-api-key-standalone-agent]

::::{note}
API keys are sent as plain-text, so they only provide security when used in combination with Transport Layer Security (TLS). [{{ecloud}}](https://www.elastic.co/cloud/elasticsearch-service?page=docs&placement=docs-body) provides secure, encrypted connections out of the box! For self-managed {{es}} clusters, refer to [Public Key Infrastructure (PKI) certificates](/reference/ingestion-tools/fleet/elasticsearch-output.md#output-elasticsearch-pki-certs-authentication-settings).
::::


You can set API keys to expire at a certain time, and you can explicitly invalidate them. Any user with the `manage_api_key` or `manage_own_api_key` cluster privilege can create API keys.

For security reasons, we recommend using a unique API key per {{agent}}. You can create as many API keys per user as necessary.

If you are using [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), API key authentication is required.

To create an API key for {{agent}}:

1. In an {{ecloud}} or on premises environment, in {{kib}} navigate to **{{stack-manage-app}} > API keys** and click **Create API key**.

    In a {{serverless-short}} environment, in {{kib}} navigate to **Project settings** > **Management** > **API keys** and click **Create API key**.

2. Enter a name for your API key and select **Control security privileges**.
3. In the role descriptors box, copy and paste the following JSON. This example creates an API key with privileges for ingesting logs, metrics, traces, and synthetics:

    ```json
    {
      "standalone_agent": {
        "cluster": [
          "monitor"
        ],
        "indices": [
          {
            "names": [
              "logs-*-*", "metrics-*-*", "traces-*-*", "synthetics-*-*" <1>
            ],
            "privileges": [
              "auto_configure", "create_doc"
            ]
          }
        ]
      }
    }
    ```

    1. Adjust this list to match the data you want to collect. For example, if you aren’t using APM or synthetics, remove `"traces-*-*"` and `"synthetics-*-*"` from this list.

4. To set an expiration date for the API key, select **Expire after time** and input the lifetime of the API key in days.
5. Click **Create API key**.

    You’ll see a message indicating that the key was created, along with the encoded key. By default, the API key is Base64 encoded, but that won’t work for {{agent}}.


1. Click the down arrow next to Base64 and select **Beats**.

    :::{image} images/copy-api-key.png
    :alt: Message with field for copying API key
    :class: screenshot
    :::

2. Copy the API key. You will need this for the next step, and you will not be able to view it again.
3. To use the API key, specify the `api_key` setting in the `elastic-agent.yml` file. For example:

    ```yaml
    [...]
    outputs:
      default:
        type: elasticsearch
        hosts:
          - 'https://da4e3a6298c14a6683e6064ebfve9ace.us-central1.gcp.cloud.es.io:443'
        api_key: _Nj4oH0aWZVGqM7MGop8:349p_U1ERHyIc4Nm8_AYkw <1>
    [...]
    ```

    1. The format of this key is `<id>:<key>`. Base64 encoded API keys are not currently supported in this configuration.


For more information about creating API keys in {{kib}}, see [API Keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).


## Create a standalone agent role [create-role-standalone-agent]

Although it’s recommended that you use an API key instead of a username and password to access {{es}} (and an API key is required in a {{serverless-short}} environment), you can create a role with the required privileges, assign it to a user, and specify the user’s credentials in the `elastic-agent.yml` file.

1. In {{kib}}, go to **{{stack-manage-app}} > Roles**.
2. Click **Create role** and enter a name for the role.
3. In **Cluster privileges**, enter `monitor`.
4. In **Index privileges**, enter:

    1. `logs-*-*`, `metrics-*-*`, `traces-*-*` and `synthetics-*-*` in the **Indices** field.

        ::::{note}
        Adjust this list to match the data you want to collect. For example, if you aren’t using APM or synthetics, remove `traces-*-*` and `synthetics-*-*` from this list.
        ::::

    2. `auto_configure` and `create_doc` in the **Privileges** field.

        :::{image} images/create-standalone-agent-role.png
        :alt: Create role settings for a standalone agent role
        :class: screenshot
        :::

5. Create the role and assign it to a user. For more information about creating roles, refer to [{{kib}} role management](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
6. To use these credentials, set the username and password in the `elastic-agent.yml` file:

    ```yaml
    [...]
    outputs:
      default:
        type: elasticsearch
        hosts:
          - 'https://da4e3a6298c14a6683e6064ebfve9ace.us-central1.gcp.cloud.es.io:443'
        username: ES_USERNAME <1>
        password: ES_PASSWORD
    [...]
    ```

    1. For security reasons, specify a user with the minimal privileges described here. It’s recommended that you do not use the `elastic` superuser.


