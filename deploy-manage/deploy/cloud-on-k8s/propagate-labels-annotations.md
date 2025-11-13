---
applies_to:
  deployment:
    eck: preview 3.1
products:
  - id: cloud-kubernetes
---

# Propagate labels and annotations [k8s-propagate-labels-annotations]

Starting with version `3.1.0`, {{eck}} supports propagating labels and annotations from the parent resource to the child resources it creates. This can be used on all custom resources managed by ECK, such as {{eck_resources_list}}.

The example below demonstrates how to use this feature on a {{es}} cluster, however, as mentioned above, this can be also applied to any custom resource managed by {{eck}}.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  annotations:
    # Some custom annotations to be propagated to resources created by the operator.
    my-annotation1: "my-annotation1-value"
    my-annotation2: "my-annotation2-value"
    # Instructions for the operator to propagate these annotations and labels to resources it creates.
    eck.k8s.alpha.elastic.co/propagate-annotations: "my-annotation1, my-annotation2"
    eck.k8s.alpha.elastic.co/propagate-labels: "my-label1, my-label2"
  labels:
    # Some custom labels to be propagated to resources created by the operator.
    my-label1: "my-label1-value"
    my-label2: "my-label2-value"
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  nodeSets:
    - name: default
      config:
        # this allows ES to run on nodes even if their vm.max_map_count has not been increased, at a performance cost
        node.store.allow_mmap: false
      count: 1
```

The custom labels and annotations specified in the `metadata` section of the parent resource will be propagated to all child resources created by {{eck}}, such as StatefulSets, Pods, Services, and Secrets. This ensures that all resources have consistent metadata, which can be useful for filtering, monitoring, and managing resources in Kubernetes:

```sh
kubectl get sts,pods,svc -l my-label1=my-label1-value,my-label2=my-label2-value
```

```sh
NAME                                               READY   AGE
statefulset.apps/elasticsearch-sample-es-default   1/1     4m10s

NAME                                    READY   STATUS    RESTARTS   AGE
pod/elasticsearch-sample-es-default-0   1/1     Running   0          4m9s

NAME                                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/elasticsearch-sample-es-default         ClusterIP   None             <none>        9200/TCP   4m12s
service/elasticsearch-sample-es-http            ClusterIP   XX.XX.XX.XX      <none>        9200/TCP   4m14s
service/elasticsearch-sample-es-internal-http   ClusterIP   XX.XX.XX.XX      <none>        9200/TCP   4m14s
service/elasticsearch-sample-es-transport       ClusterIP   None             <none>        9300/TCP   4m14s
```

It is possible to use `*` as a wildcard to propagate all labels and annotations from the parent resource to the child resources. For example:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  annotations:
    # Instructions for the operator to propagate all the annotations and labels to resources it creates.
    eck.k8s.alpha.elastic.co/propagate-annotations: "*"
    eck.k8s.alpha.elastic.co/propagate-labels: "*"
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  nodeSets:
    - name: default
      config:
        # this allows ES to run on nodes even if their vm.max_map_count has not been increased, at a performance cost
        node.store.allow_mmap: false
      count: 1
```

::::{note}
Note the following considerations when using this feature:
* Propagated labels and annotations are not automatically deleted. If you want to remove them from the child resources, you need to do so manually or use a cleanup script.
* To prevent conflicts, some labels and annotations reserved for internal use by ECK or Kubernetes are not propagated. This is the case for labels and annotations that match `*.k8s.*.elastic.co/` and also `kubectl.kubernetes.io/last-applied-configuration`.
::::
