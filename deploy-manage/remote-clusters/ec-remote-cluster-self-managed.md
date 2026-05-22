---
navigation_title: To a self-managed cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-self-managed.html
applies_to:
  deployment:
    ess: ga
    self: ga
products:
  - id: cloud-hosted
sub:
  local_type_generic: deployment
  remote_type_generic: cluster
  remote_type: Self-managed
---

# Connect {{ech}} deployments to self-managed clusters [ec-remote-cluster-self-managed]

This section explains how to configure a deployment to connect remotely to self-managed clusters.

:::{include} _snippets/terminology.md
:::

## Allow the remote connection [ec_allow_the_remote_connection_4]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ec_prerequisites_and_limitations_4]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::

### Configure the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the Certificate Authority (CA) of the remote environment’s {{es}} remote cluster server, proxy, or load balancing infrastructure is public or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ech-remote-public.md
:::

::::


::::{dropdown} The CA is private

:::{include} _snippets/apikeys-local-ech-remote-private.md
:::

::::
::::::

::::::{tab-item} TLS certificate (deprecated)

To use [TLS certificates](/deploy-manage/remote-clusters/security-models.md#tls-certificate-authentication) for remote clusters, you must establish mutual TLS trust. The local {{ech}} deployment must trust the Certificate Authority (CA) used by the remote self-managed cluster, and the remote self-managed cluster must trust the CA used by the local {{ech}} deployment.

The steps below guide you through both sides of this configuration.

#### Retrieve the CAs of both clusters [download-ca]

::::{include} _snippets/configure-trust-download-ca.md
::::

#### Configure trust on the {{ech}} deployment [configure-trust-deployment]

::::{include} _snippets/configure-trust-ecloud-self.md
::::

#### Optional: Reissue self-managed node certificates to follow the {{ecloud}} subject name pattern  [self-reissue-certs]

::::{include} _snippets/reissue-certificates-self-ecloud.md
::::

#### Configure trust on the self-managed cluster

::::{include} _snippets/configure-trust-self-ecloud.md
::::

::::::
:::::::

You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ec_connect_to_the_remote_cluster_4]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.


### Using {{kib}} [ec_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ec_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ec_configure_roles_and_users_4]

:::{include} _snippets/configure-roles-and-users.md
:::
