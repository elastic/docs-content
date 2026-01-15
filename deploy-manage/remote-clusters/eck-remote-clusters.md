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

# Connect to {{es}} clusters in the same {{eck}} environment [k8s-remote-clusters-connect-internal]

These steps describe how to configure remote clusters between two {{es}} clusters that are managed by the same {{eck}} (ECK) operator. 

After the connection is established, you’ll be able to [run {{ccs-init}} queries from {{es}}](/explore-analyze/cross-cluster-search.md) or [set up {{ccr-init}}](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

::::{note}
The remote clusters feature requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::

::::{include} _snippets/terminology.md
::::

To create a remote cluster connection to another {{es}} cluster deployed in the same ECK environment, specify the `remoteClusters` attribute in your {{es}} spec. In this scenario, the operator automatically orchestrates all required configuration across both clusters, based on the selected security model.

For other remote cluster scenarios with ECK, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md#eck-rcs-setup).

## Security models [k8s_security_models]

:::{include} _snippets/allow-connection-intro.md
:::


## Setup [k8s_using_the_api_key_security_model]

Based on the selected security model, use one of the following setup procedures.

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

### Enable the remote cluster server interface on the remote cluster

:::{include} _snippets/eck_rcs_enable.md
:::

### Configure the local cluster

Once the remote cluster server is enabled and running on the remote cluster, you can configure the {{es}} reference on the local cluster and include the desired permissions for {{ccs}} and {{ccr}} under the `spec.remoteClusters` field.

Permissions have to be included under the `apiKey` field. The API model of the {{es}} resource is compatible with the [{{es}} cross-cluster API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) model. Fine-grained permissions can therefore be configured in both the `search` and `replication` fields.

The following example shows how to connect a local cluster to a remote cluster and specify the cross-cluster permissions under the `apiKey` field. This configuration is applied to the local cluster manifest:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: <local-cluster-name>
  namespace: <ns-local>
spec:
  version: {{version.stack}}
  remoteClusters:
  - name: <remote-cluster-name>
    elasticsearchRef:
      name: <remote-cluster-name> <1>
      namespace: <ns-remote> <2>
    apiKey:
      access:
        search:
          names:
            - kibana_sample_data_ecommerce  <3>
        replication:
          names:
            - kibana_sample_data_ecommerce  <3>
  nodeSets:
  - count: 3
    name: default
  ...
  ...
```
1. The name and namespace of the remote {{es}} cluster you are connecting to.
2. The namespace declaration can be omitted if both clusters reside in the same namespace.
3. This example requires the [{{kib}} sample data](/explore-analyze/index.md#gs-get-data-into-kibana).

You can find a complete example in the [{{eck}} repository's recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/remoteclusters).
::::::

::::::{tab-item} TLS certificate (deprecated)
The following example shows how to connect a local cluster to a remote cluster using the certificate-based security model. The configuration is applied to the local cluster manifest:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: <local-cluster-name>
  namespace: <ns-local>
spec:
  version: 8.16.1
  remoteClusters:
  - name: <remote-cluster-name>
    elasticsearchRef:
      name: <remote-cluster-name> <1>
      namespace: <ns-remote> <2>
  nodeSets:
  - count: 3
    name: default
  ...
  ...
```
1. The name and namespace of the remote {{es}} cluster you are connecting to.
2. The namespace declaration can be omitted if both clusters reside in the same namespace.
::::::
:::::::

## Configure roles and users

:::{include} _snippets/configure-roles-and-users.md
:::