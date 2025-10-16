---
navigation_title: To {{ecloud}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-ece-ess.html
applies_to:
  deployment:
    ece: ga
    ess: ga
products:
  - id: cloud-enterprise
sub:
  remote_type: Elastic Cloud Hosted deployment
---

# Connect {{ece}} deployments to an {{ecloud}} organization [ece-remote-cluster-ece-ess]

This section explains how to configure an {{ece}} (ECE) deployment to connect remotely to clusters belonging to an {{ecloud}} organization.

::::{note}
If network security filters are applied to the remote cluster on {{ecloud}}, the remote cluster administrator must configure an [IP filter](/deploy-manage/security/ip-filtering-cloud.md) to allow connections from the IP addresses (or CIDR ranges) of the local ECE allocator hosts. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ece_allow_the_remote_connection_3]

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


### Prerequisites and limitations [ece_prerequisites_and_limitations_3]

* The local and remote deployments must be on {{stack}} 8.14 or later.


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_3]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


### Add the cross-cluster API key to the keystore of the local deployment [ece_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment_2]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the deployment menu, select **Security**.
4. Locate **Remote Connections > Trust management > Connections using API keys** and select **Add API key**.

    1. Fill both fields.

        * For the **Remote cluster name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ece-edit-remove-trusted-environment.md#ece-edit-remove-trusted-environment-api-key).
::::::

::::::{tab-item} TLS certificate (deprecated)
### Configuring trust with clusters in {{ecloud}} [ece-trust-ec]

A deployment can be configured to trust all or specific deployments from an organization in [{{ecloud}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md):

1. From the **Security** menu, select **Remote Connections > Add trusted environment** and select **{{ecloud}} Organization**.
2. Enter the organization ID (which can be found near the organization name).
3. Upload the Certificate Authorities of the deployments you want to trust. These can be downloaded from the **Security** page of each deployment (not only the current CA, but also future certificates in case they are expiring soon since they are periodically rotated). Deployments from the same region are signed by the same CA, so you will only need to upload one for each region.
4. Choose one of following options to configure the level of trust with the Organization:

    * All deployments - This deployment trusts all deployments in the organization in the regions whose certificate authorities have been uploaded, including new deployments when they are created.
    * Specific deployments - Specify which of the existing deployments you want to trust from this organization. The full {{es}} cluster ID must be entered for each remote cluster. The {{es}} `Cluster ID` can be found in the deployment overview page under **Applications**.

5. Configure the deployment in {{ecloud}} to [trust this deployment](/deploy-manage/remote-clusters/ec-remote-cluster-ece.md#ec-trust-ece), so that both deployments are configured to trust each other.

Note that the organization ID and cluster IDs must be entered fully and correctly. For security reasons, no verification of the IDs is possible. If cross-environment trust does not appear to be working, double-checking the IDs is a good place to start.

::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

In order to trust a deployment with cluster id `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID) in an organization with organization ID `803289842`, you need to update the trust settings with an additional direct trust relationship like this:

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
        "type" : "ESS",
        "name" : "My Organization",
        "scope_id" : "803289842",
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
:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ece_connect_to_the_remote_cluster_3]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.

::::{note}
This configuration of remote clusters uses the [Proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode) and requires the ECE allocators to be able to connect to the remote address endpoint.
::::


### Using {{kib}} [ece_using_kibana_3]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::

### Using the {{es}} API [ece_using_the_elasticsearch_api_3]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

## Configure roles and users [ece_configure_roles_and_users_3]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).