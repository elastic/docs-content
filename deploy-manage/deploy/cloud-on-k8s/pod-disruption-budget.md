---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-pod-disruption-budget.html
---

# Pod disruption budget [k8s-pod-disruption-budget]

A [Pod Disruption Budget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/) (PDB) allows you to limit the disruption to your application when its pods need to be rescheduled for some reason such as upgrades or routine maintenance work on the Kubernetes nodes.

ECK manages a default PDB per {{es}} resource. It allows one {{es}} Pod to be taken down, as long as the cluster has a `green` health. Single-node clusters are not considered highly available and can always be disrupted.

In the {{es}} specification, you can change the default behaviour as follows:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.16.1
  nodeSets:
  - name: default
    count: 3
  podDisruptionBudget:
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          elasticsearch.k8s.elastic.co/cluster-name: quickstart
```

::::{note} 
[`maxUnavailable`](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#arbitrary-controllers-and-selectors) cannot be used with an arbitrary label selector, therefore `minAvailable` is used in this example.
::::


## Pod disruption budget per nodeset [k8s-pdb-per-nodeset]

You can specify a PDB per nodeset or node role.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  podDisruptionBudget: {} <1>
  version: 8.16.1
  nodeSets:
    - name: master
      count: 3
      config:
        node.roles: "master"
        node.store.allow_mmap: false
    - name: hot
      count: 2
      config:
        node.roles: ["data_hot", "data_content", "ingest"]
        node.store.allow_mmap: false

apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: hot-nodes-pdb
spec:
  minAvailable: 1 <5>
  selector:
    matchLabels:
      elasticsearch.k8s.elastic.co/cluster-name: quickstart <3>
      elasticsearch.k8s.elastic.co/statefulset-name: quickstart-es-hot <6>
```

1. Disable the default {{es}} pod disruption budget.
2. Specify pod disruption budget to have 2 master nodes available.
3. The pods should be in the "quickstart" cluster.
4. Pod disruption budget applies on all master nodes.
5. Specify pod disruption budget to have 1 hot node available.
6. Pod disruption budget applies on nodes of the same nodeset.



