---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/api-keys.html
---

# Elasticsearch API keys [api-keys]

API keys are security mechanisms used to authenticate and authorize access to {{es}} resources. They ensure that only authorized users or applications interact with {{es}}.

For example, if you extract data from an {{es}} cluster on a daily basis, you might create an API key tied to your credentials, configure it with minimum access, and then put the API credentials into a cron job. Or you might create API keys to automate ingestion of new data from remote sources, without a live user interaction.

You can use {{kib}} to manage your different API keys:

* User API key: allows external services to access the Elastic Stack on behalf of a user.
* Cross-cluster API key: allows other clusters to connect to this cluster.
* Managed API key: created and managed by Kibana to run background tasks.

To manage API keys, go to the **API Keys** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

![API Keys UI](../../images/kibana-api-keys.png "")


## Security privileges [api-keys-security-privileges]

* To use API keys in {{kib}}, you must have the `manage_security`, `manage_api_key`, or the `manage_own_api_key` cluster privileges.
* To delete API keys, you must have the `manage_api_key` or `manage_own_api_key` privileges.
* To create or update a **user API key**, you must have the `manage_api_key` or the `manage_own_api_key` privilege.
* To create or update a **cross-cluster API key**, you must have the `manage_security` privilege and an Enterprise license.
* To have a read-only view on the API keys, you must have access to the page and the `read_security` cluster privilege.

To manage roles, go to the **Roles** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md), or use the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles).


## Create an API key [create-api-key]

To create an API key, go to the **API Keys** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md), and select **Create API key**.

![Create API Key UI](../../images/kibana-create-ccr-api-key.png "")

Refer to the [create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) documentation to learn more about creating user API keys.

Refer to the [create cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) documentation to learn more about creating cross-cluster API keys.


## Update an API key [udpate-api-key]

To update an API key, go to the **API Keys** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md), and then click on the name of the key. You cannot update the name or the type of API key.

Refer to the [update API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-api-key) documentation to learn more about updating user API keys.

Refer to the [update cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-cross-cluster-api-key) documentation to learn more about updating cross-cluster API keys.


## View and delete API keys [view-api-keys]

The **API Keys** feature in {{kib}} lists your API keys, including the name, date created, and status. If an API key expires, its status changes from `Active` to `Expired`.

If you have `manage_security` or `manage_api_key` permissions, you can view the API keys of all users, and see which API key was created by which user in which realm. If you have only the `manage_own_api_key` permission, you see only a list of your own keys.

You can delete API keys individually or in bulk, but you need the `manage_api_keys` or `manage_own_api_key` privileges.

