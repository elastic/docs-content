---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-traffic-splitting.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Requests routing to {{es}} nodes [k8s-traffic-splitting]

The default Kubernetes service created by ECK, named `<cluster_name>-es-http`, is configured to include all the {{es}} nodes in that cluster. This configuration is good to get started and is adequate for most use cases. However, if you are operating an {{es}} cluster with [different node types](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md) and want control over which nodes handle which types of traffic, you should create additional Kubernetes services yourself.

As an alternative, you can use features provided by third-party software such as service meshes and ingress controllers to achieve more advanced traffic management configurations. Check the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes) in the ECK source repository for a few examples.

:::{admonition} Support scope for Ingress Controllers
[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is a standard Kubernetes concept. While ECK-managed workloads can be publicly exposed using ingress resources, and we provide [example configurations](/deploy-manage/deploy/cloud-on-k8s/recipes.md), setting up an Ingress controller requires in-house Kubernetes expertise.

If ingress configuration is challenging or unsupported in your environment, consider using standard `LoadBalancer` services as a simpler alternative.
:::


The service configurations shown in these sections are based on the following {{es}} cluster definition:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: hulk
spec:
  version: {{version.stack}}
  nodeSets:
  # Dedicated master nodes
  - name: master
    count: 3
    config:
      node.roles: ["master"]
  # Dedicated data nodes
  - name: data
    count: 6
    config:
      node.roles: ["data"]
  # Dedicated ingest nodes
  - name: ingest
    count: 3
    config:
      node.roles: ["ingest"]
  # Dedicated coordinating nodes
  - name: coordinating
    count: 3
    config:
      node.roles: []
  # Dedicated machine learning nodes
  - name: ml
    count: 3
    config:
      node.roles: ["ml"]
  # Dedicated transform nodes
  - name: transform
    count: 3
    config:
      node.roles: ["transform"]
```


## Create services for exposing different node types [k8s-traffic-splitting-by-node-type]

The following examples illustrate how to create services for accessing different types of {{es}} nodes. The procedure for exposing services publicly is the same as described in [Allow public access](accessing-services.md#k8s-allow-public-access).

$$$k8s-traffic-splitting-coordinating-nodes$$$

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hulk-es-coordinating-nodes
spec:
  ports:
    - name: https
      port: 9200
      targetPort: 9200
  selector:
    elasticsearch.k8s.elastic.co/cluster-name: "hulk"
    elasticsearch.k8s.elastic.co/node-master: "false"
    elasticsearch.k8s.elastic.co/node-data: "false"
    elasticsearch.k8s.elastic.co/node-ingest: "false"
    elasticsearch.k8s.elastic.co/node-ml: "false"
    elasticsearch.k8s.elastic.co/node-transform: "false"
```

$$$k8s-traffic-splitting-ingest-nodes$$$

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hulk-es-ingest-nodes
spec:
  ports:
    - name: https
      port: 9200
      targetPort: 9200
  selector:
    elasticsearch.k8s.elastic.co/cluster-name: "hulk"
    elasticsearch.k8s.elastic.co/node-ingest: "true"
```

$$$k8s-traffic-splitting-non-master-nodes$$$

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hulk-es-non-master-nodes
spec:
  ports:
    - name: https
      port: 9200
      targetPort: 9200
  selector:
    elasticsearch.k8s.elastic.co/cluster-name: "hulk"
    elasticsearch.k8s.elastic.co/node-master: "false"
```

## Specify a custom service in elasticsearchRef [k8s-traffic-splitting-with-service-name]

You can then use your custom service in the `elasticsearchRef` element when specifying connections between {{es}} and other stack applications. This is an example on how to target only coordinating node from {{kib}}:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: hulk
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: "hulk"
    serviceName: "hulk-es-coordinating-nodes"
```

