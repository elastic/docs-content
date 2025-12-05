---
navigation_title: From a self-managed cluster
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

# Connect a self-managed {{es}} cluster to an ECK-managed cluster [self-to-eck-remote-clusters]

These steps describe how to configure a remote cluster connection to an ECK-managed {{es}} cluster from another cluster running outside the Kubernetes cluster. Once that’s done, you’ll be able to [run CCS queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up CCR](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

:::{include} _snippets/terminology.md
:::

If the local cluster is part of an {{ech}} or {{ece}} deployment, and the remote cluster is managed by ECK, refer to:
- [](./ec-enable-ccs-for-eck.md)
- [](./ece-enable-ccs-for-eck.md)

For other remote cluster scenarios with ECK, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md).

## Allow the remote connection [ec_allow_the_remote_connection_4]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

#### Prerequisites and limitations [ec_prerequisites_and_limitations_4]

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

#### Create a cross-cluster API key on the remote cluster [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::

#### Configure the local deployment [ec_configure_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

:::{include} _snippets/self_rcs_local_config.md
:::

::::::

::::::{tab-item} TLS certificate (deprecated)

#### Make sure both clusters trust each other’s certificate authority [k8s_make_sure_both_clusters_trust_each_others_certificate_authority]

When using TLS certificate–based authentication, the first step is to establish mutual trust between the clusters at the transport layer. This requires exchanging and trusting each cluster’s transport certificate authority (CA):
* The CA of the remote (ECK-managed) cluster must be added as a trusted CA in the local cluster,
* The local cluster’s transport CA must be added as a trusted CA in the remote cluster.

::::{note}
While it is technically possible to configure remote cluster connections using earlier versions of {{es}}, this guide only covers the setup for {{es}} 7.6 and later. The setup process is significantly simplified in {{es}} 7.6 due to improved support for the indirection of Kubernetes services.
::::

Consider the following example:

* `remote-cluster` resides inside Kubernetes and is managed by ECK
* `local-cluster` is not hosted inside the same Kubernetes cluster as `remote-cluster` and might not even be managed by ECK

To allow mutual TLS authentication between the clusters:

1. The certificate authority (CA) used by ECK to issue certificates for the {{es}} transport layer is stored in a secret named `<cluster_name>-es-transport-certs-public`. Extract the certificate for `remote-cluster` as follows:

    ```sh
    kubectl get secret remote-cluster-es-transport-certs-public \
    -o go-template='{{index .data "ca.crt" | base64decode}}' > remote.ca.crt
    ```

    ::::{note}
    Beware of copying the source secret as-is into a different namespace. Refer to [Copying secrets with Owner References](../../troubleshoot/deployments/cloud-on-k8s/common-problems.md#k8s-common-problems-owner-refs) for more information.
    ::::

    ::::{note}
    CA certificates are automatically rotated after one year by default. You can [configure](../deploy/cloud-on-k8s/configure-eck.md) this period. Make sure to keep the copy of the certificates secret up-to-date.
    ::::

2. Configure `local-cluster` to trust the transport CA of the remote cluster:

    If `local-cluster` is hosted outside of Kubernetes, take the CA certificate that you extracted previously and add it to the list of CAs in [`xpack.security.transport.ssl.certificate_authorities`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#_pem_encoded_files_3).

    If `local-cluster` is also managed by an ECK instance, proceed as follows:

    1. Create a config map with the CA certificate you extracted previously:

        ```sh
        kubectl create configmap remote-certs --from-file=ca.crt=remote.ca.crt
        ```

    2. Use this config map to configure `remote-cluster`'s CA as a trusted CA in `local-cluster`:

        ```yaml
        apiVersion: elasticsearch.k8s.elastic.co/v1
        kind: Elasticsearch
        metadata:
          name: local-cluster
        spec:
          transport:
            tls:
              certificateAuthorities:
                configMapName: remote-certs
          nodeSets:
          - count: 3
            name: default
          version: 8.16.1
        ```
    
3. Repeat the previous steps to configure `remote-cluster` to trust the CA of the local cluster.

#### Configure external access to the transport interface of the remote cluster

:::{include} _snippets/eck_expose_transport.md
:::

::::::
:::::::

## Connect to the remote cluster

:::{include} _snippets/eck_rcs_connect_intro.md
:::

### Using {{kib}}

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users

:::{include} _snippets/configure-roles-and-users.md
:::
