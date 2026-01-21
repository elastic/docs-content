---
navigation_title: To the same ECE environment
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-same-ece.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
sub:
  local_type_generic: deployment
  remote_type_generic: deployment
  remote_type: Elastic Cloud Enterprise
---

# Connect to deployments in the same {{ece}} environment [ece-remote-cluster-same-ece]

This section explains how to configure a deployment to connect remotely to clusters belonging to the same {{ece}} environment.

:::{include} _snippets/terminology.md
:::

::::{note}
If network security filters are applied to the remote cluster, the remote cluster administrator must configure a [remote cluster filter](/deploy-manage/security/remote-cluster-filtering.md), using either the ECE environment ID or the Elasticsearch cluster ID of the local cluster as the filtering criteria. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ece_allow_the_remote_connection]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ece_prerequisites_and_limitations]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment]

:::{include} _snippets/apikeys-create-key.md
:::

### Add the cross-cluster API key to the keystore of the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/apikeys-local-ece-remote-public.md
:::
::::::

::::::{tab-item} TLS certificate (deprecated)
### Default trust with other clusters in the same ECE environment [ece_default_trust_with_other_clusters_in_the_same_ece_environment]

By default, any deployment that you or your users create trusts all other deployments in the same {{ece}} environment. You can change this behavior in the Cloud UI under **Platform** > **Trust Management**, so that when a new deployment is created it does not automatically trust any other deployment. You can choose one of the following options:

* Trust all my deployments - All of your organization’s deployments created while this option is selected already trust each other. If you keep this option, that includes any deployments you’ll create in the future. You can directly jump to [Connect to the remote cluster](/deploy-manage/remote-clusters/ece-remote-cluster-same-ece.md#ece_connect_to_the_remote_cluster) to finalize the CCS or CCR configuration.
* Trust no deployment - New deployments won’t trust any other deployment when they are created. You can instead configure trust individually for each of them in their security settings, as described in the next section.

:::{image} /deploy-manage/images/cloud-enterprise-ce-environment-trust-management.png
:alt: Trust management at the environment Level
:screenshot:
:::

::::{note}
* The level of trust of existing deployments is not modified when you change this setting. You must instead update the trust settings individually for each deployment you wish to change.
* Deployments created before {{ece}} version `2.9.0` trust only themselves. You have to update the trust setting for each deployment that you want to either use as a remote cluster or configure to work with a remote cluster.

::::



### Specify the deployments trusted to be used as remote clusters [ece_specify_the_deployments_trusted_to_be_used_as_remote_clusters]

If your organization’s deployments already trust each other by default, you can skip this section. If that’s not the case, follow these steps to configure which are the specific deployments that should be trusted.

1. Go to the **Security** page of your deployment.
2. From the list of existing trust configurations, edit the one labeled as your organization.
3. Choose one of following options to configure the level of trust on each of your deployments:

    * Trust all deployments - This deployment trusts all other deployments in this environment, including new deployments when they are created.
    * Trust specific deployments - Choose which of the existing deployments from your environment you want to trust.
    * Trust no deployment - No deployment in this {{ece}} environment is trusted.

    ::::{note}
    When trusting specific deployments, the more restrictive [CCS](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode) version policy is used (even if you only want to use [CCR](/deploy-manage/tools/cross-cluster-replication.md)). To work around this restriction for CCR-only trust, it is necessary to use the API as described below.
    ::::


1. Repeat these steps from each of the deployments you want to use for CCS or CCR. You will only be able to connect 2 deployments successfully when both of them trust each other.

::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

The current trust settings can be found in the path `.resources.elasticsearch[0].info.settings.trust` when calling:

```sh
curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID?show_settings=true
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
:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ece_connect_to_the_remote_cluster]

On the local cluster, add the remote cluster using {{kib}}, the {{es}} API, or the ECE API.

::::{note}
This configuration of remote clusters uses the [Proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode) and requires the ECE allocators to be able to connect to the remote address endpoint.
::::

### Using {{kib}} [ece_using_kibana]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::

::::{note}
If you’re having issues establishing the connection and the remote cluster is part of an {{ece}} environment with a private certificate, make sure that the proxy address and server name match with the the certificate information. For more information, refer to [Administering endpoints in {{ece}}](/deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md).
::::

### Using the {{es}} API [ece_using_the_elasticsearch_api]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

### Using the {{ece}} API [ece_using_the_elastic_cloud_enterprise_restful_api]
```{applies_to}
deployment:
  ece: deprecated
```

::::{note}
This section only applies if you’re using TLS certificates as cross-cluster security model and when both clusters belong to the same ECE environment. For other scenarios, the [{{es}} API](#ece_using_the_elasticsearch_api) should be used instead.
::::


```sh
curl -k -H 'Content-Type: application/json' -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters -d '
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

Note the following when using the {{ece}} RESTful API:

1. A cluster alias must contain only letters, numbers, dashes (-), or underscores (_).
2. To learn about skipping disconnected clusters, refer to the [{{es}} documentation](/explore-analyze/cross-cluster-search.md#skip-unavailable-clusters).
3. When remote clusters are already configured for a deployment, the `PUT` request replaces the existing configuration with the new configuration passed. Passing an empty array of resources will remove all remote clusters.

The following API request retrieves the remote clusters configuration:

```sh
curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters
```

::::{note}
The response includes just the remote clusters from the same ECE environment. In order to obtain the whole list of remote clusters, use {{kib}} or the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) directly.
::::

## Configure roles and users [ece_configure_roles_and_users]

:::{include} _snippets/configure-roles-and-users.md
:::
