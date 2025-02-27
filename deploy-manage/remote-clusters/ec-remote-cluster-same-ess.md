---
applies_to:
  deployment:
    ess: ga
navigation_title: Within the same {{ecloud}} organization
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-same-ess.html
---

# Access other deployments of the same {{ecloud}} organization [ec-remote-cluster-same-ess]

This section explains how to configure a deployment to connect remotely to clusters belonging to the same {{ecloud}} organization.

## Allow the remote connection [ec_allow_the_remote_connection]

Before you start, consider the security model that you would prefer to use for authenticating remote connections between clusters, and follow the corresponding steps.

API key
:   For deployments based on {{stack}} 8.14 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote deployment fine-grained access controls.

TLS certificate (deprecated in {{stack}} 9.0.0)
:   This model uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. A superuser on the local deployment gains total read access to the remote deployment, so it is only suitable for deployments that are in the same security domain.

:::::::{tab-set}

::::::{tab-item} API key
API key authentication enables a local cluster to authenticate itself with a remote cluster via a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key and grants access, based on the API key’s privileges.

All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search and/or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. Note it is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).


### Prerequisites and limitations [ec_prerequisites_and_limitations]

* The local and remote deployments must be on {{stack}} 8.14 or later.
* API key authentication can’t be used in combination with traffic filters.
* Contrary to the certificate security model, the API key security model does not require that both local and remote clusters trust each other.


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


### Add the cross-cluster API key to the keystore of the local deployment [ec_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the home page, find your hosted deployment and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the deployment menu, select **Security**.
4. Locate **Remote connections** and select **Add an API key**.

    1. Fill both fields.

        * For the **Setting name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Secret**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you later need to update the remote connection with different permissions, you can replace the API key as detailed in [Update the access level of a remote cluster connection relying on a cross-cluster API key](ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).
::::::

::::::{tab-item} TLS certificate (deprecated)
### Set the default trust with other clusters in the same {{ecloud}} organization [ec_set_the_default_trust_with_other_clusters_in_the_same_elasticsearch_service_organization]

By default, any deployment that you create trusts all other deployments in the same organization. You can change this behavior in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) under **Features** > **Trust**, so that when a new deployment is created it does not automatically trust any other deployment. You can choose one of the following options:

* Trust all my deployments - All of your organization’s deployments created while this option is selected already trust each other. If you keep this option, that includes any deployments you’ll create in the future. You can directly jump to [Connect to the remote cluster](/deploy-manage/remote-clusters/ec-remote-cluster-same-ess.md#ec_connect_to_the_remote_cluster) to finalize the CCS or CCR configuration.
* Trust no deployment - New deployments won’t trust any other deployment when they are created. You can instead configure trust individually for each of them in their security settings, as described in the next section.

:::{image} ../../images/cloud-ec-account-trust-management.png
:alt: Trust management at the account Level
:class: screenshot
:::

::::{note}
* The level of trust of existing deployments is not modified when you change this setting. You must instead update the trust settings individually for each deployment you wish to change.
* Deployments created before the {{ecloud}} February 2021 release trust only themselves. You have to update the trust setting for each deployment that you want to either use as a remote cluster or configure to work with a remote cluster.

::::



### Specify the deployments trusted to be used as remote clusters [ec_specify_the_deployments_trusted_to_be_used_as_remote_clusters]

If your organization’s deployments already trust each other by default, you can skip this section. If that’s not the case, follow these steps to configure which are the specific deployments that should be trusted.

1. Go to the **Security** page of your deployment.
2. From the list of existing trust configurations, edit the one labeled as your organization.
3. Choose one of following options to configure the level of trust on each of your deployments:

    * Trust all deployments - This deployment trusts all other deployments in this environment, including new deployments when they are created.
    * Trust specific deployments - Choose which of the existing deployments from your environment you want to trust.
    * Trust no deployment - No deployment in this {{ech}} environment is trusted.

    ::::{note}
    When trusting specific deployments, the more restrictive [CCS](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode) version policy is used (even if you only want to use [CCR](/deploy-manage/tools/cross-cluster-replication.md)). To work around this restriction for CCR-only trust, it is necessary to use the API as described below.
    ::::


1. Repeat these steps from each of the deployments you want to use for CCS or CCR. You will only be able to connect 2 deployments successfully when both of them trust each other.

::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

The current trust settings can be found in the path `.resources.elasticsearch[0].info.settings.trust` when calling:

```sh
curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID?show_settings=true
```

For example:

```json
{
  "accounts": [
    {
      "account_id": "ec38dd0aa45f4a69909ca5c81c27138a",
      "trust_all": true
    }
  ]
}
```

The `account_id` above represents the only account in an {{es}} environment, and therefore is the one used to update the trust level with deployments in the current {{es}} environment. For example, to update the trust level to trust only the deployment with cluster ID `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID), the trust settings in the body would look like this:

```json
{
  "trust":{
    "accounts":[
      {
         "account_id":"ec38dd0aa45f4a69909ca5c81c27138a",
         "trust_all":false,
         "trust_allowlist":[
            "cf659f7fe6164d9691b284ae36811be1"
         ]
      }
    ]
  }
}
```

::::
::::::
:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ec_connect_to_the_remote_cluster]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.


### Using {{kib}} [ec_using_kibana]

1. Open the {{kib}} main menu, and select **Stack Management > Data > Remote Clusters > Add a remote cluster**.
2. Enable **Manually enter proxy address and server name**.
3. Fill in the following fields:

    * **Name**: This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.
    * **Proxy address**: This value can be found on the **Security** page of the {{ech}} deployment you want to use as a remote.<br>

      ::::{tip}
      If you’re using API keys as security model, change the port into `9443`.
      ::::

    * **Server name**: This value can be found on the **Security** page of the {{ech}} deployment you want to use as a remote.

      :::{image} ../../images/cloud-ce-copy-remote-cluster-parameters.png
      :alt: Remote Cluster Parameters in Deployment
      :class: screenshot
      :::

      ::::{note}
      If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](/deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md).
      ::::

4. Click **Next**.
5. Click **Add remote cluster** (you have already established trust in a previous step).


### Using the {{es}} API [ec_using_the_elasticsearch_api]

To configure a deployment as a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* `mode`: `proxy`
* `proxy_address`: This value can be found on the **Security** page of the {{ech}} deployment you want to use as a remote. Also, using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9400` using a semicolon.

  ::::{tip}
  If you’re using API keys as security model, change the port into `9443`.
  ::::


* `server_name`: This value can be found on the **Security** page of the {{ech}} deployment you want to use as a remote. Also, using the API, this can be obtained from the {{es}} resource info field `metadata.endpoint`.

This is an example of the API call to `_cluster/settings`:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": {
          "mode":"proxy",
          "proxy_address": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:9400",
          "server_name": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io"
        }
      }
    }
  }
}
```


### Using the {{ecloud}} RESTful API [ec_using_the_elasticsearch_service_restful_api]

::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model and when both clusters belong to the same organization. For other scenarios, the [{{es}} API](#ec_using_the_elasticsearch_api) should be used instead.
::::


```sh
curl -H 'Content-Type: application/json' -X PUT -H "Authorization: ApiKey $EC_API_KEY" https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters -d '
{
  "resources" : [
    {
      "deployment_id": "$DEPLOYMENT_ID_REMOTE",
      "elasticsearch_ref_id": "$REF_ID_REMOTE",
      "alias": "alias-your-remote",
      "skip_unavailable" : true
    }
  ]
}'
```

`DEPLOYMENT_ID_REMOTE`
:   The ID of your remote deployment, as shown in the Cloud UI or obtained through the API.

`REF_ID_REMOTE`
:   The unique ID of the {{es}} resources inside your remote deployment (you can obtain these values through the API).

Note the following when using the {{ecloud}} RESTful API:

1. A cluster alias must contain only letters, numbers, dashes (-), or underscores (_).
2. To learn about skipping disconnected clusters, refer to the [{{es}} documentation](/solutions/search/cross-cluster-search.md#skip-unavailable-clusters).
3. When remote clusters are already configured for a deployment, the `PUT` request replaces the existing configuration with the new configuration passed. Passing an empty array of resources will remove all remote clusters.

The following API request retrieves the remote clusters configuration:

```sh
curl -X GET -H "Authorization: ApiKey $EC_API_KEY" https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters
```

::::{note}
The response will include just the remote clusters from the same {{ecloud}} organization. In order to obtain the whole list of remote clusters, use {{kib}} or the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) directly.
::::


## Configure roles and users [ec_configure_roles_and_users]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/defining-roles.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).
