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


{{ecloud}} API keys allow you to programmatically access the following resources:

* [{{ecloud}}]({{cloud-apis}}) APIs
* [{{ecloud}} {{serverless-short}}]({{cloud-serverless-apis}}) APIs
* {applies_to}`serverless: ga` Optionally, [{{es}} {{serverless-full}}]({{es-serverless-apis}}) and [{{kib}} {{serverless-full}}]({{kib-serverless-apis}})  APIs

Only **Organization owners** can create and manage API keys. An API key is not tied to the user who created it. When creating a key, you assign it specific roles to control its access to organizational resources, including hosted deployments and serverless projects. If a user leaves the organization, the API keys they have created will still function until they expire.

You can have multiple API keys for different purposes, and you can revoke them when you no longer need them. Each organization can have up to 500 active API keys.

:::{admonition} {{es}} and {{kib}} API access 
:applies_to: ech:

By default, {{ecloud}} API keys provide access to the APIs for managing your organization, deployments, and projects. 

In the case of {{ech}} deployments, {{ecloud}} API keys do not provide access to {{es}} or {{kib}} APIs. [Learn how to create an {{es}} API key for ECH deployments](elasticsearch-api-keys.md).

In the case of {{serverless-full}} projects, you can optionally grant access to [{{es}} {{serverless-short}}]({{es-serverless-apis}}) and [{{kib}} {{serverless-short}}]({{kib-serverless-apis}}) APIs when you [assign roles to the API key](#roles).
:::

## Create an API key [ec-api-keys]

::::{tab-set}
:::{tab-item} Using the {{ecloud}} Console
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Go to your avatar in the upper right corner and choose **Organization**.
3. On the **API keys** tab of the **Organization** page, click **Create API key**.
4. On the **Create API key** flyout, you can configure your new key:
   1. Add a unique name for the key.
   2. Set the [expiration](#expiration) for the key.
   3. Assign [roles](#roles).
5. Click **Create API key**, copy the generated API key, and store it in a safe place. You can also download the key as a CSV file.

The API key needs to be supplied in the `Authorization` header of a request, in the following format:

```sh
Authorization: ApiKey $EC_API_KEY
```
:::
:::{tab-item} Using the {{ecloud}} API

You can create an API key using the [Create API key]({{cloud-apis}}/operation/operation-create-api-key) API.

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/users/auth/keys

{
  "description": "api-created-key",
  "expiration": "90d",
  "role_assignments": {
    "project": {
      "elasticsearch": [
        {
          "role_id": "elasticsearch-admin",
          "organization_id": "ORG_ID_PLACEHOLDER",
          "all": false,
          "project_ids": [
            "PROJECT_ID_PLACEHOLDER"
          ],
          "application_roles": [ 
            "admin"
          ] <1>
        }
      ]
    }
  }
}
```

1. Roles granted for [project-level access](#project-access) through the {{es}} and {{kib}} APIs.
:::
::::

## Revoke an API key [ec_revoke_an_api_key]

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Go to your avatar in the upper right corner and choose **Organization**.

    The keys currently associated with your organization are listed under the API keys tab of the **Organization** page.

3. Find the key you want to revoke, and click the trash icon under **Actions**.
   
## API key expiration [expiration]

By default, API keys expire after three months. You can set the expiration to a different preset value or to a specific date, up to one year. If you need the key to work indefinitely, you can also set its expiration to **Never**. In this case, the key won’t expire.

When an API key is nearing expiration, Elastic sends an email to the creator of the API key and each of the operational contacts. When you use an API key to authenticate, the API response header `X-Elastic-Api-Key-Expiration` indicates the key’s expiration date. You can log this value to detect API keys that are nearing expiration.

When an API key expires, it is automatically removed from the **API keys** tab.

## Applying roles to API keys [roles]

Roles grant an API key specific privileges to your {{ecloud}} organization and resources.

You can grant a cloud API key [the same types of roles that you assign to users](/deploy-manage/users-roles/cloud-organization/user-roles.md#types-of-roles): organization-level roles, cloud resource access roles, and connected cluster roles.

### Granting {{es}} and {{kib}} API access [project-access]
```{applies_to}
serverless: ga
```

When you grant **Organization owner** access, or **Cloud resource** access for one or more {{serverless-short}} projects, you can select your level of API access:

| Access | Grant |
| --- | --- |
| **Cloud API** (default) | Grants access to only [{{ecloud}}]({{cloud-apis}}) and [{{ecloud}} {{serverless-short}}]({{cloud-serverless-apis}}) APIs. No direct access to project {{es}} or {{kib}} API endpoints. |
| **Cloud, {{es}} and {{kib}} API** | Grants the following access:<br><br>•[{{ecloud}}]({{cloud-apis}}) and [{{ecloud}} {{serverless-short}}]({{cloud-serverless-apis}}) APIs.<br><br>• [{{es}} {{serverless-short}}]({{es-serverless-apis}}), and [{{kib}} {{serverless-short}}]({{kib-serverless-apis}}) API endpoints for the relevant projects. |

Using {{ecloud}} keys for project-level API access, rather than [granting keys from within each {{serverless-short}} project](serverless-project-api-keys.md), allows you to create keys that can interact with multiple projects, and manage API access centrally from the {{ecloud}} console.

When granting Cloud resource access, you can apply a [predefined role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) or [custom role](/deploy-manage/users-roles/serverless-custom-roles.md) to granularly control access to the specified resources. The role that you select controls the resources that you can access in all relevant APIs. 

#### Considerations

All roles include permissions to both Cloud APIs and {{es}} and {{kib}} APIs. Your **API access** selection limits the role's scope, and, in some cases, can disable core functionality.

* **Cloud API access**: The API key can use the role’s permissions for organization-level actions in {{ecloud}}, but it has no direct access to the project itself. Roles designed for project use, such as the Security **Tier 1 analyst** role, have only **Viewer** access to the relevant projects through {{ecloud}} APIs. 
  
  API keys with custom roles are also limited to **Viewer** access in the project.

* **Cloud, {{es}} and {{kib}} API access**: The API key can use the role’s permissions to fully interact with the project. This selection is required for custom roles to work as intended, because they rely on the {{es}} and {{kib}} serverless APIs for project-level access.

For details on the permissions granted for each role, refer to the [predefined roles table](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table).