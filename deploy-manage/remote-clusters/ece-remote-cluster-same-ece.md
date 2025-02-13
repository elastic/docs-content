---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-same-ece.html
---

# Access other deployments of the same Elastic Cloud Enterprise environment [ece-remote-cluster-same-ece]

This section explains how to configure a deployment to connect remotely to clusters belonging to the same Elastic Cloud Enterprise environment.


## Allow the remote connection [ece_allow_the_remote_connection]

Before you start, consider the security model that you would prefer to use for authenticating remote connections between clusters, and follow the corresponding steps.

API key
:   For deployments based on {{stack}} version 8.10 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote deployment fine-grained access controls.

TLS certificate
:   This model uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. A superuser on the local deployment gains total read access to the remote deployment, so it is only suitable for deployments that are in the same security domain.

:::::::{tab-set}

::::::{tab-item} TLS certificate
### Default trust with other clusters in the same ECE environment [ece_default_trust_with_other_clusters_in_the_same_ece_environment]

By default, any deployment that you or your users create trusts all other deployments in the same Elastic Cloud Enterprise environment. You can change this behavior in the Cloud UI under **Platform** > **Trust Management**, so that when a new deployment is created it does not automatically trust any other deployment. You can choose one of the following options:

* Trust all my deployments - All of your organization’s deployments created while this option is selected already trust each other. If you keep this option, that includes any deployments you’ll create in the future. You can directly jump to [Connect to the remote cluster](https://www.elastic.co/guide/en/cloud-enterprise/{{ece-version-link}}/ece-remote-cluster-same-ece.html#ece_connect_to_the_remote_cluster) to finalize the CCS or CCR configuration.
* Trust no deployment - New deployments won’t trust any other deployment when they are created. You can instead configure trust individually for each of them in their security settings, as described in the next section.

:::{image} ../../images/cloud-enterprise-ce-environment-trust-management.png
:alt: Trust management at the environment Level
:class: screenshot
:::

::::{note}
* The level of trust of existing deployments is not modified when you change this setting. You must instead update the trust settings individually for each deployment you wish to change.
* Deployments created before Elastic Cloud Enterprise version `2.9.0` trust only themselves. You have to update the trust setting for each deployment that you want to either use as a remote cluster or configure to work with a remote cluster.

::::



### Specify the deployments trusted to be used as remote clusters [ece_specify_the_deployments_trusted_to_be_used_as_remote_clusters]

If your organization’s deployments already trust each other by default, you can skip this section. If that’s not the case, follow these steps to configure which are the specific deployments that should be trusted.

1. Go to the **Security** page of your deployment.
2. From the list of existing trust configurations, edit the one labeled as your organization.
3. Choose one of following options to configure the level of trust on each of your deployments:

    * Trust all deployments - This deployment trusts all other deployments in this environment, including new deployments when they are created.
    * Trust specific deployments - Choose which of the existing deployments from your environment you want to trust.
    * Trust no deployment - No deployment in this Elastic Cloud Enterprise environment is trusted.


::::{note}
When trusting specific deployments, the more restrictive [CCS](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html#sniff-mode) version policy is used (even if you only want to use [CCR](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-ccr.html)). To work around this restriction for CCR-only trust, it is necessary to use the API as described below.
::::


1. Repeat these steps from each of the deployments you want to use for CCS or CCR. You will only be able to connect 2 deployments successfully when both of them trust each other.

::::{dropdown} **Using the API**
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

The `account_id` above represents the only account in an ECE environment, and therefore is the one used to update the trust level with deployments in the current ECE environment. For example, to update the trust level to trust only the deployment with cluster ID `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID), the trust settings in the body would look like this:

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

::::::{tab-item} API key
API key authentication enables a local cluster to authenticate itself with a remote cluster via a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key and grants access, based on the API key’s privileges.

All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search and/or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. Note it is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

If you run into any issues, refer to [Troubleshooting](remote-clusters-troubleshooting.md).


### Prerequisites and limitations [ece_prerequisites_and_limitations]

* The local and remote deployments must be on version 8.12 or later.


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [Kibana](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


### Add the cross-cluster API key to the keystore of the local deployment [ece_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the deployments page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the deployment menu, select **Security**.
4. Locate **Remote connections** and select **Add an API key**.

    1. Fill both fields.

        * For the **Setting name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Secret**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart Elasticsearch**.<br>

    ::::{note}
    If the local deployment runs on version 8.13 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you later need to update the remote connection with different permissions, you can replace the API key as detailed in [Update the access level of a remote cluster connection relying on a cross-cluster API key](ece-edit-remove-trusted-environment.md#ece-edit-remove-trusted-environment-api-key).
::::::

:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ece_connect_to_the_remote_cluster]

On the local cluster, add the remote cluster using Kibana or the {{es}} API.


### Using Kibana [ece_using_kibana]

1. Open the {{kib}} main menu, and select **Stack Management > Data > Remote Clusters > Add a remote cluster**.
2. Enable **Manually enter proxy address and server name**.
3. Fill in the following fields:

    * **Name**: This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.
    * **Proxy address**: This value can be found on the **Security** page of the Elastic Cloud Enterprise deployment you want to use as a remote.<br>

        ::::{tip}
        If you’re using API keys as security model, change the port into `9443`.
        ::::

    * **Server name**: This value can be found on the **Security** page of the Elastic Cloud Enterprise deployment you want to use as a remote.

        :::{image} ../../images/cloud-enterprise-ce-copy-remote-cluster-parameters.png
        :alt: Remote Cluster Parameters in Deployment
        :class: screenshot
        :::

        ::::{note}
        If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-endpoints.html).
        ::::

4. Click **Next**.
5. Click **Add remote cluster** (you have already established trust in a previous step).

::::{note}
This configuration of remote clusters uses the [Proxy mode](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html#proxy-mode) and it requires that the allocators can communicate via http with the proxies.
::::



### Using the Elasticsearch API [ece_using_the_elasticsearch_api]

To configure a deployment as a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* `mode`: `proxy`
* `proxy_address`: This value can be found on the **Security** page of the Elastic Cloud Enterprise deployment you want to use as a remote. Also, using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9300` using a semicolon.

::::{tip}
If you’re using API keys as security model, change the port into `9443`.
::::


* `server_name`: This value can be found on the **Security** page of the Elastic Cloud Enterprise deployment you want to use as a remote. Also, using the API, this can be obtained from the {{es}} resource info field `metadata.endpoint`.

This is an example of the API call to `_cluster/settings`:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": {
          "mode":"proxy",
          "proxy_address": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:9300",
          "server_name": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io"
        }
      }
    }
  }
}
```

:::::{dropdown} **Stack Version above 6.7.0 and below 7.6.0**
::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model.
::::


When the cluster to be configured as a remote is above 6.7.0 and below 7.6.0, the remote cluster must be configured using the [sniff mode](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html#sniff-mode) with the proxy field. For each remote cluster you need to pass the following fields:

* **Proxy**: This value can be found on the **Security** page of the deployment you want to use as a remote under the name `Proxy Address`. Also, using the API, this can be obtained from the elasticsearch resource info, concatenating the fields `metadata.endpoint` and `metadata.ports.transport_passthrough` using a semicolon.
* **Seeds**: This field is an array that must contain only one value, which is the `server name` that can be found on the **Security** page of the ECE deployment you want to use as a remote concatenated with `:1`. Also, using the API, this can be obtained from the {{es}} resource info, concatenating the fields `metadata.endpoint` and `1` with a semicolon.
* **Mode**: sniff (or empty, since sniff is the default value)

This is an example of the API call to `_cluster/settings`:

```json
{
  "persistent": {
    "cluster": {
      "remote": {
        "my-remote-cluster-1": {
          "seeds": [
            "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:1"
          ],
          "proxy": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:9400"
        }
      }
    }
  }
}
```

:::::



### Using the Elastic Cloud Enterprise RESTful API [ece_using_the_elastic_cloud_enterprise_restful_api]

::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model and when both clusters belong to the same ECE environment (for other scenarios, the {{es}} API should be used instead):
::::


```sh
curl -k -H 'Content-Type: application/json' -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters -d '
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

Note the following when using the Elastic Cloud Enterprise RESTful API:

1. A cluster alias must contain only letters, numbers, dashes (-), or underscores (_).
2. To learn about skipping disconnected clusters, refer to the [{{es}} documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html#skip-unavailable-clusters).
3. When remote clusters are already configured for a deployment, the `PUT` request replaces the existing configuration with the new configuration passed. Passing an empty array of resources will remove all remote clusters.

The following API request retrieves the remote clusters configuration:

```sh
curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters
```

::::{note}
The response includes just the remote clusters from the same ECE environment. In order to obtain the whole list of remote clusters, use Kibana or the {{es}} API [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) directly.
::::



## Configure roles and users [ece_configure_roles_and_users]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/defining-roles.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).
