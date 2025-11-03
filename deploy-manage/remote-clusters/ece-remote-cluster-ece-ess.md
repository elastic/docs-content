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

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ece_prerequisites_and_limitations_3]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_3]

:::{include} _snippets/apikeys-create-key.md
:::

### Add the cross-cluster API key to the keystore of the local deployment [ece_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/apikeys-local-ece-remote-public.md
:::
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

:::{include} _snippets/configure-roles-and-users.md
:::