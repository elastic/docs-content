---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/api-keys.html
applies_to:
  stack: ga
products:
  - id: kibana
---

# {{es}} API keys [api-keys]

Several types of {{es}} API keys exist:

* **Personal/User** API key: allows external services to access the {{stack}}, including the [{{es}}]({{es-apis}}) and [{{kib}}]({{kib-apis}}) APIs, on behalf of a user.
* **Cross-cluster** API key: allows other clusters to connect to this cluster.
* **Managed** API key: created and managed by {{kib}} to run background tasks.

:::{tip}
:applies_to: serverless:
To create equivalent keys for {{serverless-full}} projects, refer to [](serverless-project-api-keys.md). For Serverless projects, you can also create [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md) that include access to {{es}} and {{kib}} APIs. 
:::

To manage API keys in {{kib}}, go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

![API Keys UI](/deploy-manage/images/kibana-api-keys.png "")


## Security privileges [api-keys-security-privileges]

* To use API keys in {{kib}}, you must have the `manage_security`, `manage_api_key`, or the `manage_own_api_key` cluster privileges.
* To delete API keys, you must have the `manage_api_key` or `manage_own_api_key` privileges.
* To create or update a **user API key**, you must have the `manage_api_key` or the `manage_own_api_key` privilege.
* To create or update a **cross-cluster API key**, you must have the `manage_security` privilege and an Enterprise license.
* To have a read-only view on the API keys, you must have access to the page and the `read_security` cluster privilege.

To manage roles, go to the **Roles** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md), or use the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles).


## Create an API key [create-api-key]

The following are available to create an API key:

* As a quick option to create a personal API key from anywhere in {{kib}}:
  1. From the **Help menu** (![help icon](/deploy-manage/images/help-icon.svg)), select **Connection details > API key**.  
  1. Give the key a name.
  1. Select **Create API key**.
  
  Your personal API key is created with a default expiration of 90 days from the time of creation. You can manage the key from the **API Keys** page.

* To create a personal or cross-cluster API key with configurable options: 
  1. Go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
  2. Select **Create API key**.

![Create API Key UI](/deploy-manage/images/kibana-create-user-api-key.png "")

From the **Create API key** pane, you can configure your new key:
  1. Choose to create either a user or a cross-cluster API key.
  2. Optionally, set an expiry date. By default the API key will not expire, but it's a good security practice to give the key a limited lifespan.
  3. Configure access:
      * For a user API key, you can opt to configure access to specific {{es}} APIs and resources by assigning the key with predefined roles or custom privileges. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) and the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API documentation to learn more.
      * For a cross-cluster API key, you can control the indices that other clusters have access to. Refer to the [Create cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) API documentation to learn more.
  4. Add any additional metadata about the API as one or more key-value pairs. Refer to the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API documentation for examples.

:::{tip}
You can also create an API key [using the {{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).

## Update an API key [update-api-key]

To update an API key, go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the **API keys** page, click on the name of the key you want to update. 

You can't update the name or the type of an API key.

* For a user API key, you can update:
  * The API key's access to {{es}} APIs and resources.
  * The metadata associated with the key.
 
  Refer to the [Update API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-api-key) API documentation to learn more.

* For a cross-cluster API key, you can update:
  * The indices that other clusters have access to.
  * The metadata associated with the key.
 
  Refer to the [Update cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-cross-cluster-api-key) API documentation to learn more.

## View and delete API keys [view-api-keys]

The **API Keys** management page in {{kib}} lists your API keys, including the name, date created, and status. If an API key expires, its status changes from `Active` to `Expired`.

If you have `manage_security` or `manage_api_key` permissions, you can view the API keys of all users, and see which API key was created by which user in which realm. If you have only the `manage_own_api_key` permission, you see only a list of your own keys.

You can delete API keys individually or in bulk, but you need the `manage_api_keys` or `manage_own_api_key` privileges.

