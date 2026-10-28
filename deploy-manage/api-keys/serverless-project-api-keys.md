---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/api-keys.html
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Serverless project API keys [api-keys]

In {{serverless-short}} projects, the following types of API keys exist:

- **Personal** API keys, that you can create to allow external services to access your serverless project, including the [{{es}}]({{es-apis}}) and [{{kib}}]({{kib-apis}}) APIs, on behalf of a user.
- **Managed** API keys, created and managed by {{kib}} to correctly run background tasks.

:::{admonition} Manage {{serverless-short}} project API access using {{ecloud}} API keys
As an alternative to using {{serverless-short}} project API keys, which are tied to a single project, you can create [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md) that include access to projects' {{es}} and {{kib}} APIs. This allows you to create keys that can interact with multiple projects, and manage API access centrally from the {{ecloud}} console. 

The [cross-project search feature](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-and-api-key-access) requires {{ecloud}} API keys for programmatic access.
:::

To manage API keys in {{kib}}, go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /deploy-manage/images/serverless-api-key-management.png
:alt: API keys UI
:screenshot:
:::

## Create an API key [api-keys-create-an-api-key]

The following options are available to create an API key:

* As a quick option, [use the simple API key creation menu](#simple-api-key-creation).
* For more complex key creation needs, [use the API key page](#advanced-api-key-creation).
* Create an API key [using the {{es}} API]({{es-serverless-apis}}operation/operation-security-create-api-key).

### Simple API key creation

You can create a basic personal API key from anywhere in {{kib}}:

  1. From the **Help menu** {icon}`question`, select **Connection details → API key**.
  2. Give the key a name.
  3. Select **Create API key**.

Your personal API key is created with a default expiration of 90 days from the time of creation. You can manage the key from the **API keys** page.

### Advanced API key creation

Use the API key page to create a personal API key with configurable options.

1. Go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create API key**.
3. Give the key a name.
4. Optionally, set an expiry date. By default the API key does not expire, but it's a good security practice to give the key a limited lifespan.
5. Optionally, configure access to specific {{es}} APIs and resources by assigning the key with predefined roles or custom privileges. Refer to [Control security privileges](#api-keys-restrict-privileges) and the [Create API key]({{es-serverless-apis}}operation/operation-security-create-api-key) API documentation to learn more.
6. Add any additional metadata about the API key as one or more key-value pairs. Refer to the [Create API key]({{es-serverless-apis}}operation/operation-security-create-api-key) API documentation for examples.

Once created, you can copy the encoded API key and use it to send requests to the {{es}} HTTP API. For example:

```bash
curl "${ES_URL}" \
-H "Authorization: ApiKey ${API_KEY}"
```
:::{image} /deploy-manage/images/serverless-create-personal-api-key.png
:alt: Create API key UI
:screenshot:
:::

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

For the `role_descriptors` object schema, check out the [`/_security/api_key` endpoint]({{es-serverless-apis}}operation/operation-security-create-api-key) docs. For supported privileges, check [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).

## Update an API key [api-keys-update-an-api-key]

In **API keys**, click on the name of the key. You can update only **Control security privileges** and **Include metadata**.

## View and delete API keys [api-keys-view-and-delete-api-keys]

The **API keys** app lists your API keys, including the name, date created, and status. When API keys expire, the status changes from `Active` to `Expired`.

You can delete API keys individually or in bulk.

## Related pages

* [](/deploy-manage/deploy/elastic-cloud/find-connection-details-serverless.md): Pair a key with your project's {{es}} endpoint to connect clients and tools.
