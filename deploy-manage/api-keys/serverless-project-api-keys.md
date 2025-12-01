---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/api-keys.html
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Serverless project API keys [api-keys]

In serverless projects, the following types of API keys exist:

- **Personal** API keys, that you can create to allow external services to access your serverless project on behalf of a user.
- **Managed** API keys, created and managed by {{kib}} to correctly run background tasks.

You can manage your keys in **{{project-settings}} → {{manage-app}} → API keys**:

:::{image} /deploy-manage/images/serverless-api-key-management.png
:alt: API keys UI
:screenshot:
:::


## Create an API key [api-keys-create-an-api-key]

In **API keys**, click **Create API key**:

:::{image} /deploy-manage/images/serverless-create-personal-api-key.png
:alt: Create API key UI
:screenshot:
:width: 50%
:::

Once created, you can copy the encoded API key and use it to send requests to the {{es}} HTTP API. For example:

```bash
curl "${ES_URL}" \
-H "Authorization: ApiKey ${API_KEY}"
```

::::{important}
API keys are intended for programmatic access. Don’t use API keys to authenticate access using a web browser.

::::



### Control security privileges [api-keys-restrict-privileges]

When you create or update an API key, use **Control security privileges** to configure access to specific {{es}} APIs and resources. Define the permissions using a JSON `role_descriptors` object, where you specify one or more roles and the associated privileges.

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

For the `role_descriptors` object schema, check out the [`/_security/api_key` endpoint](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-security-create-api-key) docs. For supported privileges, check [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).


## Update an API key [api-keys-update-an-api-key]

In **API keys**, click on the name of the key. You can update only **Restrict privileges** and **Include metadata**.


## View and delete API keys [api-keys-view-and-delete-api-keys]

The **API keys** app lists your API keys, including the name, date created, and status. When API keys expire, the status changes from `Active` to `Expired`.

You can delete API keys individually or in bulk.
