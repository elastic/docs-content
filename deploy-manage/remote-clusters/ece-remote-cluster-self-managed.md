---
navigation_title: To a self-managed cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-self-managed.html
applies_to:
  deployment:
    ece: ga
    self: ga
products:
  - id: cloud-enterprise
sub:
  local_type_generic: deployment
  remote_type_generic: cluster
  remote_type: Self-managed
---

# Connect {{ece}} deployments to self-managed clusters [ece-remote-cluster-self-managed]

This section explains how to configure a deployment to connect remotely to self-managed clusters.

:::{include} _snippets/terminology.md
:::

## Allow the remote connection [ece_allow_the_remote_connection_4]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ece_prerequisites_and_limitations_4]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::

### Configure the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the Certificate Authority (CA) of the remote environment’s {{es}} HTTPS server, proxy or, load balancing infrastructure is public or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ece-remote-public.md
:::

::::


::::{dropdown} The CA is private

:::{include} _snippets/apikeys-local-ece-remote-private.md
:::

::::
::::::

::::::{tab-item} TLS certificate (deprecated)
To use [TLS certificates](/deploy-manage/remote-clusters/security-models.md#tls-certificate-authentication) for remote clusters, you must establish mutual TLS trust. The local {{ece}} deployment must trust the Certificate Authority (CA) used by the remote self-managed cluster, and the remote self-managed cluster must trust the CA used by the local {{ece}} deployment.

The steps below guide you through both sides of this configuration.

#### Configure trust on the {{ece}} deployment [ece-trust-self-managed]

::::{include} _snippets/configure-trust-ecloud-self.md
::::

#### Optional: reissue self-managed node certificates to follow the {{ecloud}} subject name pattern [self-reissue-certs]

::::{include} _snippets/reissue-certificates-self-ecloud.md
::::

#### Configure trust on the self-managed cluster

::::{include} _snippets/configure-trust-self-ecloud.md
::::

::::::
:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ece_connect_to_the_remote_cluster_4]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.

::::{note}
This configuration of remote clusters uses the [Proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode) and requires the ECE allocators to be able to connect to the remote address endpoint.
::::

### Using {{kib}} [ece_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ece_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ece_configure_roles_and_users_4]

:::{include} _snippets/configure-roles-and-users.md
:::