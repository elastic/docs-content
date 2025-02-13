---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-ece.html
---

# Access deployments of an Elastic Cloud Enterprise environment [ec-remote-cluster-ece]

This section explains how to configure a deployment to connect remotely to clusters belonging to an {{ECE}} (ECE) environment.

## Allow the remote connection [ec_allow_the_remote_connection_3]

Before you start, consider the security model that you would prefer to use for authenticating remote connections between clusters, and follow the corresponding steps.

API key
:   For deployments based on {{stack}} version 8.10 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote deployment fine-grained access controls.

TLS certificate
:   This model uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. A superuser on the local deployment gains total read access to the remote deployment, so it is only suitable for deployments that are in the same security domain.

:::::::{tab-set}

::::::{tab-item} TLS certificate
#### Configuring trust with clusters of an {{ece}} environment [ec-trust-ece]

A deployment can be configured to trust all or specific deployments in a remote ECE environment:

1. Access the **Security** page of the deployment you want to use for cross-cluster operations.
2. Select **Remote Connections > Add trusted environment** and choose **{{ece}}**. Then click **Next**.
3. Select **Certificates** as authentication mechanism and click **Next**.
4. Enter the environment ID of the ECE environment. You can find it under Platform > Trust Management in your ECE administration UI.
5. Upload the Certificate Authority of the ECE environment. You can download it from Platform > Trust Management in your ECE administration UI.
6. Choose one of following options to configure the level of trust with the ECE environment:

    * All deployments - This deployment trusts all deployments in the ECE environment, including new deployments when they are created.
    * Specific deployments - Specify which of the existing deployments you want to trust in the ECE environment. The full Elasticsearch cluster ID must be entered for each remote cluster. The Elasticsearch `Cluster ID` can be found in the deployment overview page under **Applications**.

7. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s Security page.
8. Select **Create trust** to complete the configuration.
9. Configure the corresponding deployments of the ECE environment to [trust this deployment](https://www.elastic.co/guide/en/cloud-enterprise/{{ece-version-link}}/ece-enable-ccs.html). You will only be able to connect 2 deployments successfully when both of them trust each other.

Note that the environment ID and cluster IDs must be entered fully and correctly. For security reasons, no verification of the IDs is possible. If cross-environment trust does not appear to be working, double-checking the IDs is a good place to start.

::::{dropdown} **Using the API**
You can update a deployment using the appropriate trust settings for the {{es}} payload.

In order to trust a deployment with cluster id `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID) in an ECE environment with environment ID `1053523734`, you need to update the trust settings with an additional direct trust relationship like this:

```json
{
  "trust":{
    "accounts":[
      {
         "account_id":"ec38dd0aa45f4a69909ca5c81c27138a",
         "trust_all":true
      }
    ],
    "direct": [
      {
        "type" : "ECE",
        "name" : "My ECE environment",
        "scope_id" : "1053523734",
        "certificates" : [
            {
                "pem" : "-----BEGIN CERTIFICATE-----\nMIIDTzCCA...H0=\n-----END CERTIFICATE-----"
            }
         ],
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


#### Prerequisites and limitations [ec_prerequisites_and_limitations_3]

* The local and remote deployments must be on version 8.12 or later.
* API key authentication can’t be used in combination with traffic filters.
* Contrary to the certificate security model, the API key security model does not require that both local and remote clusters trust each other.


#### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_3]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [Kibana](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


#### Configure the local deployment [ec_configure_the_local_deployment]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

The steps to follow depend on whether the Certificate Authority (CA) of the remote ECE environment’s proxy or load balancing infrastructure is public or private.

**The CA is public**

::::{dropdown}
1. Log in to the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the Elasticsearch Service card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the deployments page to view all of your deployments.

    On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the deployment menu, select **Security**.
4. Locate **Remote connections** and select **Add an API key**.

    1. Add a setting:

        * For the **Setting name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Secret**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart Elasticsearch**.<br>

    ::::{note}
    If the local deployment runs on version 8.13 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you later need to update the remote connection with different permissions, you can replace the API key as detailed in [Update the access level of a remote cluster connection relying on a cross-cluster API key](ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).

::::


**The CA is private**

::::{dropdown}
1. Log in to the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the Elasticsearch Service card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the deployments page to view all of your deployments.

    On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Access the **Security** page of the deployment.
4. Select **Remote Connections > Add trusted environment** and choose **{{ece}}**. Then click **Next**.
5. Select **API keys** as authentication mechanism and click **Next**.
6. Add a the API key:

    1. Fill both fields.

        * For the **Setting name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Secret**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.
    3. Repeat these steps for each API key you want to add. For example, if you want to use several deployments of the remote environment for CCR or CCS.

7. Add the CA certificate of the private proxy or load balancing infrastructure of the remote environment. To find this certificate:

    1. In the remote {{ece}} environment, go to **Platform > Settings > TLS certificates**.
    2. Select **Show certificate chain** under **Proxy**.
    3. Click **Copy root certificate** and paste it into a new file. The root certificate is the last certificate shown in the chain.
    4. Save that file as `.crt`. It is now ready to be uploaded.

        :::{image} ../../images/cloud-remote-clusters-proxy-certificate.png
        :alt: Certificate to copy from the chain
        :::

8. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s Security page.
9. Select **Create trust** to complete the configuration.
10. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart Elasticsearch**.<br>

    ::::{note}
    If the local deployment runs on version 8.13 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you later need to update the remote connection with different permissions, you can replace the API key as detailed in [Update the access level of a remote cluster connection relying on a cross-cluster API key](ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).

::::
::::::

:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ec_connect_to_the_remote_cluster_3]

On the local cluster, add the remote cluster using Kibana or the {{es}} API.


### Using Kibana [ec_using_kibana_3]

1. Open the {{kib}} main menu, and select **Stack Management > Data > Remote Clusters > Add a remote cluster**.
2. Enable **Manually enter proxy address and server name**.
3. Fill in the following fields:

    * **Name**: This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.
    * **Proxy address**: This value can be found on the **Security** page of the Elasticsearch Service deployment you want to use as a remote.<br>

        ::::{tip}
        If you’re using API keys as security model, change the port into `9443`.
        ::::

    * **Server name**: This value can be found on the **Security** page of the Elasticsearch Service deployment you want to use as a remote.

        :::{image} ../../images/cloud-ce-copy-remote-cluster-parameters.png
        :alt: Remote Cluster Parameters in Deployment
        :class: screenshot
        :::

        ::::{note}
        If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-endpoints.html).
        ::::

4. Click **Next**.
5. Click **Add remote cluster** (you have already established trust in a previous step).


### Using the Elasticsearch API [ec_using_the_elasticsearch_api_3]

To configure a deployment as a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* `mode`: `proxy`
* `proxy_address`: This value can be found on the **Security** page of the Elasticsearch Service deployment you want to use as a remote. Also, using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9400` using a semicolon.

::::{tip}
If you’re using API keys as security model, change the port into `9443`.
::::


* `server_name`: This value can be found on the **Security** page of the Elasticsearch Service deployment you want to use as a remote. Also, using the API, this can be obtained from the {{es}} resource info field `metadata.endpoint`.

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

:::::{dropdown} **Stack Version above 6.7.0 and below 7.6.0**
::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model.
::::


When the cluster to be configured as a remote is above 6.7.0 and below 7.6.0, the remote cluster must be configured using the [sniff mode](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html#sniff-mode) with the proxy field. For each remote cluster you need to pass the following fields:

* **Proxy**: This value can be found on the **Security** page of the deployment you want to use as a remote under the name `Proxy Address`. Also, using the API, this can be obtained from the elasticsearch resource info, concatenating the fields `metadata.endpoint` and `metadata.ports.transport_passthrough` using a semicolon.
* **Seeds**: This field is an array that must contain only one value, which is the `server name` that can be found on the **Security** page of the {{es}} deployment you want to use as a remote concatenated with `:1`. Also, using the API, this can be obtained from the {{es}} resource info, concatenating the fields `metadata.endpoint` and `1` with a semicolon.
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



### Using the Elasticsearch Service RESTful API [ec_using_the_elasticsearch_service_restful_api_3]

::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model and when both clusters belong to the same organization (for other scenarios,the Elasticsearch API should be used instead):
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

Note the following when using the Elasticsearch Service RESTful API:

1. A cluster alias must contain only letters, numbers, dashes (-), or underscores (_).
2. To learn about skipping disconnected clusters, refer to the [{{es}} documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html#skip-unavailable-clusters).
3. When remote clusters are already configured for a deployment, the `PUT` request replaces the existing configuration with the new configuration passed. Passing an empty array of resources will remove all remote clusters.

The following API request retrieves the remote clusters configuration:

```sh
curl -X GET -H "Authorization: ApiKey $EC_API_KEY" https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters
```

::::{note}
The response will include just the remote clusters from the same organization in Elasticsearch Service. In order to obtain the whole list of remote clusters, use Kibana or the Elasticsearch API [Elasticsearch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) directly.
::::



## Configure roles and users [ec_configure_roles_and_users_3]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/defining-roles.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).
