---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-traffic-splitting.html
---

# Requests routing to Elasticsearch nodes [k8s-traffic-splitting]

The default Kubernetes service created by ECK, named `<cluster_name>-es-http`, is configured to include all the Elasticsearch nodes in that cluster. This configuration is good to get started and is adequate for most use cases. However, if you are operating an Elasticsearch cluster with [different node types](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html) and want control over which nodes handle which types of traffic, you should create additional Kubernetes services yourself.

As an alternative, you can use features provided by third-party software such as service meshes and ingress controllers to achieve more advanced traffic management configurations. Check the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/2.16/config/recipes) in the ECK source repository for a few examples.

The service configurations shown in these sections are based on the following Elasticsearch cluster definition:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: hulk
spec:
  version: 8.16.1
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

The following examples illustrate how to create services for accessing different types of Elasticsearch nodes. The procedure for exposing services publicly is the same as described in [Allow public access](accessing-services.md#k8s-allow-public-access).

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

You can then use your custom service in the `elasticsearchRef` element when specifying connections between Elasticsearch and other stack applications. This is an example on how to target only coordinating node from Kibana:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: hulk
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "hulk"
    serviceName: "hulk-es-coordinating-nodes"
```

