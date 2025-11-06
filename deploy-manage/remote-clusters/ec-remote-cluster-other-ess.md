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
  remote_type: Elastic Cloud Hosted
---

# Connect to deployments in another {{ecloud}} organization [ec-remote-cluster-other-ess]

This section explains how to configure a deployment to connect remotely to clusters belonging to a different {{ecloud}} organization.

::::{note}
If network security policies are applied to the remote cluster, the remote cluster administrator must configure a [private connection policy of type remote cluster](/deploy-manage/security/remote-cluster-filtering.md), using either the organization ID or the Elasticsearch cluster ID of the local cluster as the filtering criteria. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ec_allow_the_remote_connection_2]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ec_prerequisites_and_limitations_2]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_2]

:::{include} _snippets/apikeys-create-key.md
:::

### Add the cross-cluster API key to the keystore of the local deployment [ec_add_the_cross_cluster_api_key_to_the_keystore_of_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/apikeys-local-ech-remote-public.md
:::

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

:::{include} _snippets/configure-roles-and-users.md
:::
