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
  remote_type: Self-managed
---

# Connect a self-managed {{es}} cluster to an ECK-managed cluster [self-to-eck-remote-clusters]

(this doc is a WIP)

These steps describe how to configure remote clusters between a self-managed {{es}} cluster and an {{es}} cluster managed by [{{eck}} (ECK)](/deploy-manage/deploy/cloud-on-k8s.md). Once that’s done, you’ll be able to [run CCS queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up CCR](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

If the local deployment is on ECH or ECE, refer to:
- EC doc
- ECE doc

For other remote cluster scenarios with ECK, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md).

Intro, if the external cluster is managed by a different ECK, refer to "to external".
Intro: this doc assumes the local cluster is a self-managed cluster.


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
- extra reqs to include?

### Enable the remote cluster server interface on the remote ECK cluster

:::{include} _snippets/eck_rcs_enable.md
:::

### Configure external access to the remote cluster server interface

:::{include} _snippets/eck_rcs_expose.md
:::


### Retrieve the ECK-managed CA certificate of the remote cluster server [fetch-ca-cert]

:::{include} _snippets/eck_rcs_retrieve_ca.md
:::

### Create a cross-cluster API key on the remote cluster [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::


### Configure the local deployment [ec_configure_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the certificate authority (CA) presented by the remote cluster server, proxy, or load-balancing infrastructure is publicly trusted or private.

::::{dropdown} The CA is public

Needs to be done, ECH snippet is not valid.

::::

::::{dropdown} The CA is private (ECK-managed transport certificates)

When adding the CA certificate in the next steps, use either the ECK-managed transport CA obtained [previously](#fetch-ca-cert), or the CA of the component that terminates TLS connections to clients.

Needs to be done, ECH snippet is not valid.

::::

::::::

::::::{tab-item} TLS certificate (deprecated)

### Establish mutual trust between the clusters [ec_establish_trust_between_two_clusters]
#### Establish trust in the ECH cluster [ec_establish_trust_in_the_elasticsearch_service_cluster]
#### Establish trust in the ECK cluster [ec_establish_trust_in_the_eck_cluster]


::::{note}
While it is technically possible to configure remote cluster connections using older versions of {{es}}, this guide only covers the setup for {{es}} 7.6 and later. The setup process is significantly simplified in {{es}} 7.6 due to improved support for the indirection of Kubernetes services.
::::

You can configure a remote cluster connection to an ECK-managed {{es}} cluster from another cluster running outside the Kubernetes cluster as follows:

1. Make sure that both clusters trust each other’s certificate authority.
2. Configure the remote cluster connection through the {{es}} REST API.

Consider the following example:

* `cluster-one` resides inside Kubernetes and is managed by ECK
* `cluster-two` is not hosted inside the same Kubernetes cluster as `cluster-one` and may not even be managed by ECK

To configure `cluster-one` as a remote cluster in `cluster-two`:

#### Make sure both clusters trust each other’s certificate authority [k8s_make_sure_both_clusters_trust_each_others_certificate_authority]

The certificate authority (CA) used by ECK to issue certificates for the {{es}} transport layer is stored in a secret named `<cluster_name>-es-transport-certs-public`. Extract the certificate for `cluster-one` as follows:

```sh
kubectl get secret cluster-one-es-transport-certs-public \
-o go-template='{{index .data "ca.crt" | base64decode}}' > remote.ca.crt
```

You then need to configure the CA as one of the trusted CAs in `cluster-two`. If that cluster is hosted outside of Kubernetes, take the CA certificate that you have just extracted and add it to the list of CAs in [`xpack.security.transport.ssl.certificate_authorities`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#_pem_encoded_files_3).

::::{note}
Beware of copying the source Secret as-is into a different namespace. Check [Common Problems: Owner References](../../troubleshoot/deployments/cloud-on-k8s/common-problems.md#k8s-common-problems-owner-refs) for more information.
::::


::::{note}
CA certificates are automatically rotated after one year by default. You can [configure](../deploy/cloud-on-k8s/configure-eck.md) this period. Make sure to keep the copy of the certificates Secret up-to-date.
::::


If `cluster-two` is also managed by an ECK instance, proceed as follows:

1. Create a config map with the CA certificate you just extracted:

    ```sh
    kubectl create configmap remote-certs --from-file=ca.crt=remote.ca.crt
    ```

2. Use this config map to configure `cluster-one`'s CA as a trusted CA in `cluster-two`:

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: cluster-two
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

3. Repeat steps 1 and 2 to add the CA of `cluster-two` to `cluster-one` as well.

### Configure external access to the transport interface of your ECK cluster

Expose the transport layer of `cluster-one`.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: cluster-one
spec:
  transport:
    service:
      spec:
        type: LoadBalancer <1>
```

1. On cloud providers which support external load balancers, setting the type field to LoadBalancer provisions a load balancer for your Service. Alternatively, expose the service through one of the Kubernetes Ingress controllers that support TCP services.

**Include to compare:**

:::{include} _snippets/eck_expose_transport.md
:::

::::::
:::::::

## Connect to the remote cluster [ec_connect_to_the_remote_cluster_4]

Esto viene de TLS, hay que ver si los otros metodos valen, que seguro que sí!

H4 - Configure the remote cluster connection through the {{es}} REST API:

Finally, configure `cluster-one` as a remote cluster in `cluster-two` using the {{es}} REST API:

```sh
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster-one": {
          "mode": "proxy", <1>
          "proxy_address": "${LOADBALANCER_IP}:9300" <2>
        }
      }
    }
  }
}
```

1. Use "proxy" mode as `cluster-two` will be connecting to `cluster-one` through the Kubernetes service abstraction.
2. Replace `${LOADBALANCER_IP}` with the IP address assigned to the `LoadBalancer` configured in the previous code sample. If you have configured a DNS entry for the service, you can use the DNS name instead of the IP address as well.


:::{include} _snippets/eck_rcs_connect_intro.md
:::

### Using {{kib}} [ec_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ec_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ec_configure_roles_and_users_4]

:::{include} _snippets/configure-roles-and-users.md
:::
