---
navigation_title: To {{eck}}
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
sub:
  local_type_generic: cluster
  remote_type_generic: cluster
  remote_type: ECK-managed
---

# Connect self-managed clusters to {{eck}} clusters [self-to-eck-remote-clusters]

::::{include} _snippets/eck_rcs_intro.md
::::

These steps describe how to configure a remote cluster connection from a self-managed {{es}} cluster, to an ECK-managed cluster.

Once that’s done, you’ll be able to [run {{ccs-init}} queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up {{ccr-init}}](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

:::{include} _snippets/terminology.md
:::

For other remote cluster scenarios with ECK, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md#eck-rcs-setup).

## Allow the remote connection

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

#### Prerequisites and limitations

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::

#### Enable the remote cluster server interface on the remote ECK cluster

:::{include} _snippets/eck_rcs_enable.md
:::

#### Configure external access to the remote cluster server interface

:::{include} _snippets/eck_rcs_expose.md
:::

#### Retrieve the ECK-managed CA certificate of the remote cluster server [fetch-ca-cert]

:::{include} _snippets/eck_rcs_retrieve_ca.md
:::

#### Create a cross-cluster API key on the remote cluster

:::{include} _snippets/apikeys-create-key.md
:::

#### Configure the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/self_rcs_local_config.md
:::

::::::

::::::{tab-item} TLS certificate (deprecated)

:::{include} _snippets/tlscerts-intro.md
:::

#### Make sure both clusters trust each other's certificate authority [mtls-setup-eck]

:::{include} _snippets/eck_rcs_mtls_intro.md
:::

In this example:

* The remote cluster resides inside Kubernetes and is managed by ECK
* The local cluster is a self-managed cluster running outside of Kubernetes.

To allow mutual TLS authentication between the clusters:

1. Extract and save the transport CAs of both clusters:

    1. For the ECK-managed cluster:

        :::{include} _snippets/eck_rcs_certs_retrieve_ca.md
        :::

    2. For the self-managed cluster (self-managed CA pending) take the transport CA from any of the nodes of the cluster. You can save it as `self-managed_ca.crt`.

2. Configure the self-managed cluster to trust the transport CA of the ECK cluster, by adding the CA to the list of CAs in [`xpack.security.transport.ssl.certificate_authorities`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#_pem_encoded_files_3).

3. Configure the ECK managed cluster to trust the transport CA of the self-managed cluster:

    1. Create a config map with the CA certificate you extracted previously:

        ```sh
        kubectl create configmap remote-certs --from-file=ca.crt=<self-managed_ca.crt> <1>
        ```
        1. Substitute `<self-managed_ca.crt>` with the name of the file containing the transport CA of the self-managed cluster.       

    2. Configure the {{es}} resource manifest to trust the config map's CA through the `spec.transport.tls.certificate_authorities` setting:

        ```yaml subs=true
        apiVersion: elasticsearch.k8s.elastic.co/v1
        kind: Elasticsearch
        metadata:
          name: <remote-cluster-name>
        spec:
          version: {{version.stack}}
          transport:
            tls:
              certificateAuthorities:
                configMapName: remote-certs
          nodeSets:
          - count: 3
            name: default
        ```

#### Configure external access to the transport interface of the remote cluster

:::{include} _snippets/eck_expose_transport.md
:::

::::::
:::::::

## Connect to the remote cluster

:::{include} _snippets/eck_rcs_connect_intro.md
:::

:::{admonition} About connection modes
This guide uses the `proxy` connection mode, connecting to the remote cluster through the Kubernetes service abstraction. Refer to [connection modes](./connection-modes.md) documentation for details on each mode and their connectivity requirements.
:::

### Using {{kib}}

:::{include} _snippets/rcs-self-kibana-to-self.md
:::

### Using the {{es}} API

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users

:::{include} _snippets/configure-roles-and-users.md
:::
