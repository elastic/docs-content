---
navigation_title: To a different {{ecloud}} organization
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-other-ess.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
sub:
  remote_type: Elastic Cloud Hosted deployment
---

# Connect to deployments in another {{ecloud}} organization [ec-remote-cluster-other-ess]

This section explains how to configure a deployment to connect remotely to clusters belonging to a different {{ecloud}} organization.

::::{note}
If network security policies are applied to the remote cluster, the remote cluster administrator must configure a [private connection policy of type remote cluster](/deploy-manage/security/remote-cluster-filtering.md), using either the organization ID or the Elasticsearch cluster ID of the local cluster as the filtering criteria. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ec_allow_the_remote_connection_2]

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


### Prerequisites and limitations [ec_prerequisites_and_limitations_2]

* The local and remote deployments must be on {{stack}} 8.14 or later.
* Contrary to the certificate security model, the API key security model does not require that both local and remote clusters trust each other.


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_2]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


### Add the cross-cluster API key to the keystore of the local deployment [ec_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment_2]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the home page, find your hosted deployment and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Hosted deployments** page to view all of your deployments.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the navigation menu, select **Security**.
4. Locate **Remote Connections > Trust management > Connections using API keys** and select **Add API key**.

    1. Fill both fields.

        * For the **Remote cluster name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).
::::::

::::::{tab-item} TLS certificate (deprecated)
### Specify the deployments trusted to be used as remote clusters [ec-trust-other-organization]

A deployment can be configured to trust all or specific deployments in another {{ech}} [organization](../users-roles/cloud-organization.md). To add cross-organization trust:

1. From the **Security** page, select **Remote Connections > Add trusted environment** and select **{{ecloud}}**. Then click **Next**.
2. Select **Certificates** as authentication mechanism and click **Next**.
3. Enter the ID of the deployment’s organization which you want to establish trust with. You can find that ID on the **Organization** page. It is usually made of 10 digits.
4. Choose one of following options to configure the level of trust with the other organization:

    * **All deployments** - This deployment trusts all deployments in the other organization, including new deployments when they are created.
    * **Specific deployments** - Specify which of the existing deployments you want to trust in the other organization. The full {{es}} cluster ID must be entered for each remote cluster. The {{es}} `Cluster ID` can be found in the deployment overview page under **Applications**.

5. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
6. Select **Create trust** to complete the configuration.
7. Repeat these steps from each of the deployments you want to use for CCS or CCR in both organizations. You will only be able to connect two deployments successfully when both of them trust each other.

::::{note}
The organization ID and cluster IDs must be entered fully and correctly. For security reasons, verification of the IDs is not possible. If cross-organization trust does not appear to be working, double-checking the IDs is a good place to start.
::::

::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

In order to trust a deployment with cluster id `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID) in another organization with Organization ID `1053523734`, you need to update the trust settings with an additional account like this:

```json
{
  "trust":{
    "accounts":[
      {
         "account_id":"ec38dd0aa45f4a69909ca5c81c27138a",
         "trust_all":true
      },
      {
         "account_id":"1053523734",
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


## Connect to the remote cluster [ec_connect_to_the_remote_cluster_2]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.


### Using {{kib}} [ec_using_kibana_2]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::


### Using the {{es}} API [ec_using_the_elasticsearch_api_2]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

## Configure roles and users [ec_configure_roles_and_users_2]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).
