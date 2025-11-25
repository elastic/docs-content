---
navigation_title: To the same ECK environment
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-remote-clusters.html
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---

# Connect to {{es}} clusters in the same ECK environment [k8s-remote-clusters-connect-internal]

::::{include} _snippets/eck_rcs_intro.md
::::


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
```{applies_to}
stack: deprecated 9.0
```

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
