---
navigation_title: To a different ECE environment
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-other-ece.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
sub:
  remote_type: Elastic Cloud Enterprise deployment
---

# Connect to deployments in a different {{ece}} environment [ece-remote-cluster-other-ece]

This section explains how to configure a deployment to connect remotely to clusters belonging to a different {{ece}} environment.

::::{note}
If network security filters are applied to the remote cluster on ECE, the remote cluster administrator must configure an [IP filter](/deploy-manage/security/ip-filtering-ece.md) to allow connections from the IP addresses (or CIDR ranges) of the local ECE allocator hosts. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ece_allow_the_remote_connection_2]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ece_prerequisites_and_limitations_2]

* The local and remote deployments must be on {{stack}} 8.14 or later.

### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_2]

:::{include} _snippets/apikeys-create-key.md
:::

### Configure the local deployment [ece_configure_the_local_deployment]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

The steps to follow depend on whether the Certificate Authority (CA) of the remote ECE environment’s proxy or load balancing infrastructure is public or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ece-remote-public.md
:::

::::


::::{dropdown} The CA is private
1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

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

        :::{image} /deploy-manage/images/cloud-enterprise-remote-clusters-proxy-certificate.png
        :alt: Certificate to copy from the chain
        :::

8. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
9. Select **Create trust** to complete the configuration.
10. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ece-edit-remove-trusted-environment.md#ece-edit-remove-trusted-environment-api-key).

::::
::::::

::::::{tab-item} TLS certificate (deprecated)
### Configuring platform level trust [ece-trust-remote-environments]

In order to configure remote clusters in other ECE environments, you first need to establish a bi-directional trust relationship between both ECE environment’s platform:

1. Download the certificate and copy the environment ID from your first ECE environment under **Platform** > **Trust Management** > **Trust parameters**.
2. Create a new trust relationship in the other ECE environment under **Platform** > **Trust Management** > **Trusted environments** using the certificate and environment ID from the previous step.
3. Download the certificate and copy the environment ID from your second ECE environment and create a new trust relationship with those in the first ECE environment.

Now, deployments in those environments will be able to configure trust with deployments in the other environment. Trust must always be bi-directional (local cluster must trust remote cluster and vice versa) and it can be configured in each deployment’s security settings.


### Configuring trust with clusters of an {{ece}} environment [ece-trust-ece]

1. Access the **Security** page of the deployment you want to use for cross-cluster operations.
2. Select **Remote Connections > Add trusted environment** and choose **{{ece}}**. Then click **Next**.
3. Select **Certificates** as authentication mechanism and click **Next**.
4. From the dropdown, select one of the environments configured in [Configuring platform level trust](#ece-trust-remote-environments).
5. Choose one of following options to configure the level of trust with the ECE environment:

    * All deployments - This deployment trusts all deployments in the ECE environment, including new deployments when they are created.
    * Specific deployments - Specify which of the existing deployments you want to trust in the ECE environment. The full {{es}} cluster ID must be entered for each remote cluster. The {{es}} `Cluster ID` can be found in the deployment overview page under **Applications**.

6. Select **Create trust** to complete the configuration.
7. Configure the corresponding deployments of the ECE environment to [trust this deployment](/deploy-manage/remote-clusters/ece-enable-ccs.md). You will only be able to connect 2 deployments successfully when both of them trust each other.

Note that the environment ID and cluster IDs must be entered fully and correctly. For security reasons, no verification of the IDs is possible. If cross-environment trust does not appear to be working, double-checking the IDs is a good place to start.

::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

Establishing the trust between the two {{ece}} environments can be done using the [trust relationships API](https://www.elastic.co/docs/api/doc/cloud-enterprise/group/endpoint-platformconfigurationtrustrelationships). For example, the list of trusted environments can be obtained calling the [list trust relationships endpoint](https://www.elastic.co/docs/api/doc/cloud-enterprise/group/endpoint-platformconfigurationtrustrelationships):

```sh
curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443//api/v1/regions/ece-region/platform/configuration/trust-relationships?include_certificate=false
```

For each remote ECE environment, it will return something like this:

```json
{
   "id":"83a7b03f2a4343fe99f09bd27ca3d9ec",
   "name":"ECE2",
   "trust_by_default":false,
   "account_ids":[
      "651598b101e54ccab1bfdcd8b6e3b8be"
   ],
   "local":false,
   "last_modified":"2022-01-9T14:33:20.465Z"
}
```

In order to trust a deployment with cluster id `cf659f7fe6164d9691b284ae36811be1` (NOTE: use the {{es}} cluster ID, not the deployment ID) in this environment named `ECE2`, you need to update the trust settings with an external trust relationship like this:

```json
{
  "trust":{
    "accounts":[
      {
         "account_id":"ec38dd0aa45f4a69909ca5c81c27138a",
         "trust_all":true
      }
    ],
    "external":[
      {
         "trust_relationship_id":"83a7b03f2a4343fe99f09bd27ca3d9ec",
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


## Connect to the remote cluster [ece_connect_to_the_remote_cluster_2]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.

::::{note}
This configuration of remote clusters uses the [Proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode) and requires the ECE allocators to be able to connect to the remote address endpoint.
::::

### Using {{kib}} [ece_using_kibana_2]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::

::::{note}
If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](/deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md).
::::


### Using the {{es}} API [ece_using_the_elasticsearch_api_2]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

## Configure roles and users [ece_configure_roles_and_users_2]

:::{include} _snippets/configure-roles-and-users.md
:::