---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-es.html
---

# Deploy Elastic Maps Server [k8s-maps-es]

::::{warning} 
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Deploying Elastic Maps Server can be done with a simple manifest:

```yaml
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
```

Versions of Elastic Maps Server prior to 7.14 need a connection to Elasticseach to verify the installed license. You define the connection with the `elasticsearchRef` attribute:

```yaml
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: 7.13
  count: 1
  elasticsearchRef:
    name: quickstart
    namespace: default
```

The use of `namespace` is optional if the Elasticsearch cluster is running in the same namespace as Elastic Maps Server.

::::{note} 
Any Elastic Maps Server can reference (and thus access) any Elasticsearch instance as long as they are both in namespaces that are watched by the same ECK instance. ECK will copy the required Secret from Elasticsearch to the Elastic Maps Server namespace. Elastic Maps Server cannot automatically connect to Elasticsearch (through `elasticsearchRef`) in a namespace managed by a different ECK instance. For more information, check [Restrict cross-namespace resource associations](restrict-cross-namespace-resource-associations.md).
::::


The Elastic Maps Server configuration file is automatically setup by ECK to establish a secure connection to Elasticsearch.

