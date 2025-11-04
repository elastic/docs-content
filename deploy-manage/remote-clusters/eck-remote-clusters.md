---
navigation_title: On Elastic Cloud on Kubernetes
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-remote-clusters.html
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---

# Remote clusters on {{eck}} [k8s-remote-clusters]

The [remote clusters module](/deploy-manage/remote-clusters.md) in {{es}} enables you to establish uni-directional connections to a remote cluster. This functionality is used in cross-cluster replication and cross-cluster search.

When using remote cluster connections with ECK, the setup process depends on where the remote cluster is deployed.

## Connect to {{es}} clusters in the same ECK environment [k8s-remote-clusters-connect-internal]

::::{note}
The remote clusters feature requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


To create a remote cluster connection to another {{es}} cluster deployed within the same Kubernetes cluster, specify the `remoteClusters` attribute in your {{es}} spec.

### Security models [k8s_security_models]

:::{include} _snippets/allow-connection-intro.md
:::

### Using the API key security model [k8s_using_the_api_key_security_model]

To enable the API key security model you must first enable the remote cluster server on the remote {{es}} cluster:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: cluster-two
  namespace: ns-two
spec:
  version: 8.16.1
  remoteClusterServer:
    enabled: true
  nodeSets:
    - name: default
      count: 3
```

::::{note}
Enabling the remote cluster server triggers a restart of the {{es}} cluster.
::::


Once the remote cluster server is enabled and started on the remote cluster you can configure the {{es}} reference on the local cluster to include the desired permissions for cross-cluster search, and cross-cluster replication.

Permissions have to be included under the `apiKey` field. The API model of the {{es}} resource is compatible with the [{{es}} Cross-Cluster API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) model. Fine-grained permissions can therefore be configured in both the `search` and `replication` fields:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: cluster-one
  namespace: ns-one
spec:
  nodeSets:
  - count: 3
    name: default
  remoteClusters:
  - name: cluster-two
    elasticsearchRef:
      name: cluster-two
      namespace: ns-two
    apiKey:
      access:
        search:
          names:
            - kibana_sample_data_ecommerce  <1>
        replication:
          names:
            - kibana_sample_data_ecommerce  <1>
  version: 8.16.1
```

1. This requires the sample data: [/explore-analyze/index.md#gs-get-data-into-kibana](/explore-analyze/index.md#gs-get-data-into-kibana)


You can find a complete example in the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/remoteclusters).


### Using the certificate security model [k8s_using_the_certificate_security_model]

The following example describes how to configure `cluster-two` as a remote cluster in `cluster-one` using the certificate security model:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: cluster-one
  namespace: ns-one
spec:
  nodeSets:
  - count: 3
    name: default
  remoteClusters:
  - name: cluster-two
    elasticsearchRef:
      name: cluster-two
      namespace: ns-two <1>
  version: 8.16.1
```

1. The namespace declaration can be omitted if both clusters reside in the same namespace.




## Connect from an {{es}} cluster running outside the Kubernetes cluster [k8s-remote-clusters-connect-external]

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

### Make sure both clusters trust each other’s certificate authority [k8s_make_sure_both_clusters_trust_each_others_certificate_authority]

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


### Configure the remote cluster connection through the {{es}} REST API [k8s_configure_the_remote_cluster_connection_through_the_elasticsearch_rest_api]

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




