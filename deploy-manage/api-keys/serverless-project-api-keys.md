---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/api-keys.html
---

# Serverless project API keys [api-keys]

This content applies to: [![Elasticsearch](../../images/serverless-es-badge.svg "")](../../solutions/search.md) [![Observability](../../images/serverless-obs-badge.svg "")](../../solutions/observability.md) [![Security](../../images/serverless-sec-badge.svg "")](../../solutions/security/elastic-security-serverless.md)

API keys are security mechanisms used to authenticate and authorize access to {{stack}} resources, and ensure that only authorized users or applications are able to interact with the {{stack}}.

For example, if you extract data from an {{es}} cluster on a daily basis, you might create an API key tied to your credentials, configure it with minimum access, and then put the API credentials into a cron job. Or, you might create API keys to automate ingestion of new data from remote sources, without a live user interaction.

You can manage your keys in **{{project-settings}} → {{manage-app}} → {{api-keys-app}}**:

:::{image} ../../images/serverless-api-key-management.png
:alt: API keys UI
:class: screenshot
:::

A *personal API key* allows external services to access the {{stack}} on behalf of a user.

A *managed API key* is created and managed by {{kib}} to correctly run background tasks.


## Create an API key [api-keys-create-an-api-key]

In **{{api-keys-app}}**, click **Create API key**:

:::{image} ../../images/serverless-create-personal-api-key.png
:alt: Create API key UI
:class: screenshot
:::

Once created, you can copy the encoded API key and use it to send requests to the {{es}} HTTP API. For example:

```bash
curl "${ES_URL}" \
-H "Authorization: ApiKey ${API_KEY}"
```

::::{important}
API keys are intended for programmatic access. Don’t use API keys to authenticate access using a web browser.

::::



### Restrict privileges [api-keys-restrict-privileges]

When you create or update an API key, use **Restrict privileges** to limit the permissions. Define the permissions using a JSON `role_descriptors` object, where you specify one or more roles and the associated privileges.

For example, the following `role_descriptors` object defines a `books-read-only` role that limits the API key to `read` privileges on the `books` index.

```json
{
  "books-read-only": {
    "cluster": [],
    "indices": [
      {
        "names": ["books"],
        "privileges": ["read"]
      }
    ],
    "applications": [],
    "run_as": [],
    "metadata": {},
    "transient_metadata": {
      "enabled": true
    }
  }
}
```

For the `role_descriptors` object schema, check out the [`/_security/api_key` endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) docs. For supported privileges, check [Security privileges](../users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices).


## Update an API key [api-keys-update-an-api-key]

In **{{api-keys-app}}**, click on the name of the key. You can update only **Restrict privileges** and **Include metadata**.


## View and delete API keys [api-keys-view-and-delete-api-keys]

The **{{api-keys-app}}** app lists your API keys, including the name, date created, and status. When API keys expire, the status changes from `Active` to `Expired`.

You can delete API keys individually or in bulk.
