---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-api-authentication.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
---

# {{ecloud}} API keys [ec-api-authentication]

{{ecloud}} API keys allow you to use the [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud/) and [{{ecloud}} serverless](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless/) APIs.

With a valid {{ecloud}} API key, you can access the API from its base URL at `api.elastic-cloud.com`.

Only **Organization owners** can create and manage API keys. An API key is not tied to the user who created it. When creating a key, you assign it specific roles to control its access to organizational resources, including hosted deployments and serverless projects. If a user leaves the organization, the API keys they have created will still function until they expire.

You can have multiple API keys for different purposes, and you can revoke them when you no longer need them.

::::{note}
These keys provides access to the API that enables you to manage your deployments. It does not provide access to {{es}}. To access {{es}} with an API key, create a key [in {{kib}}](elasticsearch-api-keys.md) or [using the {{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).
::::

## Create an API key [ec-api-keys]

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Go to your avatar in the upper right corner and choose **Organization**.
3. On the **API keys** tab of the **Organization** page, click **Create API key**.
4. On the **Create API key** flyout, you can configure your new key by adding a name, set expiration, or assign [roles](../users-roles/cloud-organization/user-roles.md).

    By default, API keys expire after three months. You can set the expiration to a different preset value or to a specific date, up to one year. If you need the key to work indefinitely, you can also set its expiration to Never. In this case, the key won’t expire.
    Each organization can have up to 500 active API keys.

    ::::{note}
    When an API key is nearing expiration, Elastic sends an email to the creator of the API key and each of the operational contacts. When you use an API key to authenticate, the API response header `X-Elastic-Api-Key-Expiration` indicates the key’s expiration date. You can log this value to detect API keys that are nearing expiration.

    Once an API key expires, it will automatically be removed from the API Keys tab.
    ::::

6. Click **Create API key**, copy the generated API key, and store it in a safe place. You can also download the key as a CSV file.

The API key needs to be supplied in the `Authorization` header of a request, in the following format:

```sh
Authorization: ApiKey $EC_API_KEY
```


## Revoke an API key [ec_revoke_an_api_key]

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Go to your avatar in the upper right corner and choose **Organization**.

    The keys currently associated with your organization are listed under the API keys tab of the **Organization** page.

3. Find the key you want to revoke, and click the trash icon under **Actions**.
