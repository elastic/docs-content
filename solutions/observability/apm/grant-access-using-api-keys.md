---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-beats-api-keys.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Grant access using API keys [apm-beats-api-keys]

Instead of using usernames and passwords, you can use API keys to grant access to {{es}} resources. You can set API keys to expire at a certain time, and you can explicitly invalidate them. Any user with the `manage_api_key` or `manage_own_api_key` cluster privilege can create API keys.

APM Server instances typically send both collected data and monitoring information to {{es}}. If you are sending both to the same cluster, you can use the same API key. For different clusters, you need to use an API key per cluster.

::::{note}
For security reasons, we recommend using a unique API key per APM Server instance. You can create as many API keys per user as necessary.
::::

## Create an API key for writing events [apm-beats-api-key-publish]

To create an API key:

1. Open the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create API key**.

    :::{image} /solutions/images/observability-server-api-key-create.png
    :alt: API key creation
    :screenshot:
    :::

3. Enter a name for your API key and select **Restrict privileges**. In the role descriptors box, assign the appropriate privileges to the new API key. For example:

    ```json
    {
        "apm_writer": {
            "cluster": ["monitor"],
            "index": [
                {
                    "names": ["traces-apm*","logs-apm*", "metrics-apm*"],
                    "privileges": ["auto_configure", "create_doc"]
                }
            ]
        },
        "apm_sourcemap": {
            "index": [
                {
                    "names": [".apm-source-map"],
                    "privileges": ["read"]
                }
            ]
        },
        "apm_agentcfg": {
            "index": [
                {
                    "names": [".apm-agent-configuration"],
                    "privileges": ["read"],
                    "allow_restricted_indices": true
                }
            ]
        },
        "apm_tail_based_sampling": {
            "index": [
                {
                    "names": ["traces-apm.sampled"],
                    "privileges": ["read"]
                }
            ]
        }
    }
    ```

    ::::{note}
    This example only provides privileges for **writing data**. See [Use feature roles](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md) for additional privileges and information.
    ::::

4. To set an expiration date for the API key, select **Expire after time** and input the lifetime of the API key in days.
5. Click **Create API key**.
6. You *must* set the API key to be configured to {{beats}}. Immediately after the API key is generated and while it is still being displayed, click the **Encoded** button next to the API key and select **Beats** from the list in the tooltip. Base64 encoded API keys are not currently supported in this configuration.

    :::{image} /solutions/images/observability-apm-api-key-beats.png
    :alt: API key dropdown highlighting the Beats option
    :::

You can now use this API key in your `apm-server.yml` configuration file:

```yaml
output.elasticsearch:
  api_key: TiNAGG4BaaMdaH1tRfuU:KnR6yE41RrSowb0kQ0HWoA <1>
```

1. Format is `id:api_key` (as shown in the {{beats}} dropdown)

## Create an API key for monitoring [apm-beats-api-key-monitor]

To open the **API keys** management page, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Click **Create API key**.

:::{image} /solutions/images/observability-server-api-key-create.png
:alt: API key creation
:screenshot:
:::

Enter a name for your API key and select **Restrict privileges**. In the role descriptors box, assign the appropriate privileges to the new API key. For example:

```json
{
    "apm_monitoring": {
        "index": [
            {
                "names": [".monitoring-beats-*"],
                "privileges": ["create_index", "create_doc"]
            }
      ]
    }
}
```

::::{note}
This example only provides privileges for **publishing monitoring data**. See [Use feature roles](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md) for additional privileges and information.
::::

To set an expiration date for the API key, select **Expire after time** and input the lifetime of the API key in days.

Click **Create API key**. In the dropdown, switch to **{{beats}}** and copy the API key.

You can now use this API key in your `apm-server.yml` configuration file like this:

```yaml
monitoring.elasticsearch:
  api_key: TiNAGG4BaaMdaH1tRfuU:KnR6yE41RrSowb0kQ0HWoA <1>
```

1. Format is `id:api_key` (as shown in the {{beats}} dropdown)

## Create an API key with {{es}} APIs [apm-beats-api-key-es]

You can also use {{es}}'s [Create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) to create a new API key. For example:

```console
POST /_security/api_key
{
  "name": "apm_host001", <1>
  "role_descriptors": {
    "apm_writer": { <2>
      "cluster": ["monitor"],
      "index": [
        {
          "names": ["traces-apm*","logs-apm*", "metrics-apm*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    },
    "apm_sourcemap": {
      "index": [
        {
          "names": [".apm-source-map"],
          "privileges": ["read"]
        }
      ]
    },
    "apm_agentcfg": {
      "index": [
        {
          "names": [".apm-agent-configuration"],
          "privileges": ["read"],
          "allow_restricted_indices": true
        }
      ]
    },
    "apm_tail_based_sampling": {
        "index": [
            {
                "names": ["traces-apm.sampled"],
                "privileges": ["read"]
            }
        ]
    }
  }
}
```

1. Name of the API key
2. Granted privileges, see [Use feature roles](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md)

See the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) reference for more information.

## Learn more about API keys [apm-learn-more-api-keys]

See the {{es}} API key documentation for more information:

* [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key)
* [Get API key information](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-api-key)
* [Invalidate API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-invalidate-api-key)
