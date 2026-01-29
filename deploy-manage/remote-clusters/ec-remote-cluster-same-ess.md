---
navigation_title: To the same {{ecloud}} organization
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-same-ess.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
sub:
  local_type_generic: deployment
  remote_type_generic: deployment
  remote_type: Elastic Cloud Hosted
---

# Connect to deployments in the same {{ecloud}} organization [ec-remote-cluster-same-ess]

This section explains how to configure a deployment to connect remotely to clusters belonging to the same {{ecloud}} organization.

:::{include} _snippets/terminology.md
:::

::::{note}
If network security policies are applied to the remote cluster, the remote cluster administrator must configure a [private connection policy of type remote cluster](/deploy-manage/security/remote-cluster-filtering.md), using either the organization ID or the Elasticsearch cluster ID of the local cluster as the filtering criteria. For more information, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).
::::

## Allow the remote connection [ec_allow_the_remote_connection]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ec_prerequisites_and_limitations]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment]

:::{include} _snippets/apikeys-create-key.md
:::

### Add the cross-cluster API key to the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/apikeys-local-ech-remote-public.md
:::

::::::

::::::{tab-item} API key with strong identity verification
```{applies_to}
stack: preview 9.3
```

% :::{include} _snippets/rcs_strong_identity_intro.md
% :::

To use [strong identity verification](./security-models.md#remote-cluster-strong-verification) in {{ech}}, the local and remote clusters must be configured to sign request headers and to verify request headers. This can be done through the [cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) or standard [`elasticsearch.yml` settings](/deploy-manage/stack-settings.md#configure-stack-settings).

Follow these steps in addition to those described in the **API key** tab.

#### On the local cluster

When [adding the remote cluster](#ec_using_the_elasticsearch_api) to the local cluster, you must configure it to sign cross-cluster requests with a TLS certificate–private key pair. You can either generate and use your own certificate for this purpose or reuse an existing certificate.

This example configures the local cluster to use the existing transport certificates to sign cross-cluster requests. These certificate files are present in all {{ecloud}} deployments:

```yaml
cluster.remote.<my_remote_cluster>.signing.certificate: "node.crt" <1>
cluster.remote.<my_remote_cluster>.signing.key: "node.key" <1>
```
1. Replace `<my_remote_cluster>` with your remote cluster alias.

If you use your own certificates, upload the certificate and key files [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) and reference them in the settings:

```yaml
cluster.remote.<my_remote_cluster>.signing.certificate: "/app/config/<bundle-zip-directory>/<signing-cert.crt>" <1>
cluster.remote.<my_remote_cluster>.signing.key: "/app/config/<bundle-zip-directory>/<signing-key.key>" <1>
```
1. Replace `<my_remote_cluster>` with your remote cluster alias, and the paths with the paths to your certificate and key files included in the bundle.

#### On the remote cluster

The certificate and key used by the local cluster to sign cross-cluster requests determine how the remote cluster must be configured. Specifically:

* Add the certificate authority (CA) that issued the local cluster certificate to the `cluster.remote.signing.certificate_authorities` setting of the remote cluster:

  ```yaml
  cluster.remote.signing.certificate_authorities: "internal_tls_ca.crt" <1>
  ```
  1. The example configures the regional CA certificate available in all {{ecloud}} clusters, unique per {{ecloud}} region and cloud provider.

  The CA file to configure depends on how the local cluster is setup:

  * If the local cluster uses the default transport certificates, and both the local and remote clusters belong to the same cloud provided and region on {{ecloud}}, you can use the `internal_tls_ca.crt` file that already exist in your cluster. No additional upload is required.

  * If the local cluster uses the default transport certificates, but the remote cluster belongs to a different {{ecloud}} provider or region, download the regional CA of the local cluster (available in the **Security -> CA Certificates** section of the deployment page), add it [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) in the remote cluster, and reference the file in the setting.

  * If you use custom certificates in the local cluster, upload the associated CA to the remote cluster [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), and reference the file in the setting.


* When creating the cross-cluster API key on the remote cluster, you must specify a `certificate_identity` pattern that matches the Distinguished Name (DN) of the certificate used by the local cluster.

  :::{tip}
  In {{ecloud}}, the certificates of all {{es}} nodes follow this Distinguished Name (DN) format:  
  `CN=<node_id>.node.<cluster_id>.cluster.<scope_id>`.

  * The {{es}} `cluster_id` of your deployment can be found on the deployment page in the {{ecloud}} UI by selecting **Copy cluster ID**.  
  * The `scope_id` corresponds to the {{ecloud}} organization ID (ECH), or the ECE environment ID.
  :::

  This example creates a cross-cluster API key with a `certificate_identity` pattern that matches the default {{ecloud}} transport certificates for a specific `cluster_id`:

  ```console
  POST /_security/cross_cluster/api_key
  {
    "name": "my-cross-cluster-api-key",
    "access": {
      "search": [
        {
          "names": ["logs-*"]
        }
      ]
    },
    "certificate_identity": "CN=.*.node.<cluster-id>.cluster.*" <1>
  }
  ```
  1. If the local cluster uses custom certificates, adjust the pattern to match their DN instead.

  The `certificate_identity` field supports regular expressions that are matched against the certificate DN. For example:

  * `"CN=.*.example.com,O=Example Corp,C=US"` matches any certificate with a CN ending in "example.com"
  * `"CN=local-cluster.*,O=Example Corp,C=US"` matches any certificate with a CN starting with "local-cluster"
  * `"CN=.*.node.<cluster-id>.cluster.*"` matches the {{ecloud}} transport certificates for a given `cluster_id`.
  * `"CN=.*.node.*.cluster.<org-id>"` matches the {{ecloud}} tranport certificates of all cluster for a given ECH organization or ECE environment.

For a full list of available strong identity verification settings for remote clusters, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-signing-settings).
::::::

::::::{tab-item} TLS certificate (deprecated)
### Set the default trust with other clusters in the same {{ecloud}} organization [ec_set_the_default_trust_with_other_clusters_in_the_same_elasticsearch_service_organization]

To configure this behavior in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), go to **Trust management** from the lower navigation menu. The **Trust all deployments** option is switched on by default. You can keep it switched on or switch it off.

* When **Trust all deployments** is switched on - All deployments trust all other deployments in the same organization, including new deployments when they are created. If you keep this setting switched on, you can jump to [Connect to the remote cluster](/deploy-manage/remote-clusters/ec-remote-cluster-same-ess.md#ec_connect_to_the_remote_cluster) to finalize the CCS or CCR configuration.
* When **Trust all deployments** is switched off - New deployments won’t trust any other deployments. Instead, you can configure trust for each of them in their security settings, as described in the next section.

::::{note}
* The level of trust of existing deployments is not modified when you change this setting. Instead, you must update the individual trust settings for each deployment you wish to change.
* Deployments created before the {{ecloud}} February 2021 release trust only themselves. You have to update the trust setting for each deployment that you want to either use as a remote cluster or configure to work with a remote cluster.

::::



### Specify the deployments trusted to be used as remote clusters [ec_specify_the_deployments_trusted_to_be_used_as_remote_clusters]

If your organization’s deployments already trust each other by default, you can skip this section. If that’s not the case, follow these steps to configure which specific deployments should be trusted.

1. Go to the **Security** page of your deployment.
2. From the list of existing trust configurations, edit the one labeled as your organization.
3. Choose one of following options to configure the level of trust on each of your deployments:

    * **All deployments** - This deployment trusts all other deployments in this environment, including new deployments when they are created.
    * **Specific deployments** - Choose which of the existing deployments from your environment you want to trust.
    * **None** - No deployment in this environment is trusted.

    ::::{note}
    When trusting specific deployments, the more restrictive [CCS](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode) version policy is used (even if you only want to use [CCR](/deploy-manage/tools/cross-cluster-replication.md)). To work around this restriction for CCR-only trust, it is necessary to use the API as described below.
    ::::


1. Repeat these steps from each of the deployments you want to use for CCS or CCR. You will only be able to connect two deployments successfully when both of them trust each other.

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

On the local cluster, add the remote cluster using {{kib}}, the {{es}} API, or the {{ecloud}} API.


### Using {{kib}} [ec_using_kibana]

:::{include} _snippets/rcs-kibana-api-snippet.md
:::

### Using the {{es}} API [ec_using_the_elasticsearch_api]

:::{include} _snippets/rcs-elasticsearch-api-snippet.md
:::

### Using the {{ecloud}} API [ec_using_the_elasticsearch_service_restful_api]
```{applies_to}
deployment:
  ess: deprecated
```

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
2. To learn about skipping disconnected clusters, refer to the [{{es}} documentation](/explore-analyze/cross-cluster-search.md#skip-unavailable-clusters).
3. When remote clusters are already configured for a deployment, the `PUT` request replaces the existing configuration with the new configuration passed. Passing an empty array of resources will remove all remote clusters.

The following API request retrieves the remote clusters configuration:

```sh
curl -X GET -H "Authorization: ApiKey $EC_API_KEY" https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/remote-clusters
```

::::{note}
The response will include just the remote clusters from the same {{ecloud}} organization. In order to obtain the whole list of remote clusters, use {{kib}} or the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) directly.
::::

## Configure roles and users [ec_configure_roles_and_users]

:::{include} _snippets/configure-roles-and-users.md
:::
