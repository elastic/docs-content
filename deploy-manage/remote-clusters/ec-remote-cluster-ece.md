---
navigation_title: To {{ece}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-ece.html
applies_to:
  deployment:
    ess: ga
    ece: ga
products:
  - id: cloud-hosted
sub:
  local_type_generic: deployment
  remote_type_generic: deployment
  remote_type: Elastic Cloud Enterprise
---

# Connect {{ech}} deployments to an {{ece}} environment [ec-remote-cluster-ece]

This section explains how to configure a deployment to connect remotely to clusters belonging to an {{ECE}} (ECE) environment.

:::{include} _snippets/terminology.md
:::

::::{note}
If network security filters are applied to the remote cluster on ECE, the remote cluster administrator must configure an [IP filter](/deploy-manage/security/ip-filtering-ece.md) to allow traffic from [{{ecloud}} IP addresses](/deploy-manage/security/elastic-cloud-static-ips.md#ec-egress). For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ec_allow_the_remote_connection_3]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

### Prerequisites and limitations [ec_prerequisites_and_limitations_3]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_3]

:::{include} _snippets/apikeys-create-key.md
:::


### Configure the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the Certificate Authority (CA) of the remote ECE environment’s proxy or load balancing infrastructure is public or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ech-remote-public.md
:::

::::

::::{dropdown} The CA is private

:::{include} _snippets/retrieve-ece-ca.md
:::

:::{include} _snippets/apikeys-local-ech-remote-private.md
:::

::::
::::::

::::::{tab-item} TLS certificate (deprecated)
### Configuring trust with clusters of an {{ece}} environment [ec-trust-ece]

A deployment can be configured to trust all or specific deployments in a remote ECE environment:

1. Access the **Security** page of the deployment you want to use for cross-cluster operations.
2. Select **Remote Connections > Add trusted environment** and choose **{{ece}}**. Then click **Next**.
3. Select **Certificates** as authentication mechanism and click **Next**.
4. Enter the environment ID of the ECE environment. You can find it under Platform > Trust Management in your ECE administration UI.
5. Upload the Certificate Authority of the ECE environment. You can download it from Platform > Trust Management in your ECE administration UI.
6. Choose one of following options to configure the level of trust with the ECE environment:

    * **All deployments** - This deployment trusts all deployments in the ECE environment, including new deployments when they are created.
    * **Specific deployments** - Specify which of the existing deployments you want to trust in the ECE environment. The full {{es}} cluster ID must be entered for each remote cluster. The {{es}} `Cluster ID` can be found in the deployment overview page under **Applications**.

7. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
8. Select **Create trust** to complete the configuration.
9. Configure the corresponding deployments of the ECE environment to [trust this deployment](/deploy-manage/remote-clusters/ece-remote-cluster-ece-ess.md#ece-trust-ec). You will only be able to connect two deployments successfully when both of them trust each other.

::::{note}
The environment ID and cluster IDs must be entered fully and correctly. For security reasons, verification of the IDs is not possible. If cross-environment trust does not appear to be working, double-checking the IDs is a good place to start.
::::

::::{dropdown} Using the API
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

:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ec_connect_to_the_remote_cluster_3]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.


### Using {{kib}} [ec_using_kibana_3]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::

::::{note}
If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](/deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md).
::::

### Using the {{es}} API [ec_using_the_elasticsearch_api_3]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

## Configure roles and users [ec_configure_roles_and_users_3]

:::{include} _snippets/configure-roles-and-users.md
:::
