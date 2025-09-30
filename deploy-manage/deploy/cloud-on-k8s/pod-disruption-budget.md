---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-pod-disruption-budget.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Pod disruption budget [k8s-pod-disruption-budget]

A [Pod Disruption Budget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/) (PDB) allows you to limit the disruption to your application when its pods need to be rescheduled for some reason such as upgrades or routine maintenance work on the Kubernetes nodes.

ECK manages either a single default PDB, or multiple PDBs per {{es}} resource according to the license available.

:::{note}
In ECK 3.1 and earlier, all clusters follow the [non-enterprise behavior](#non-enterprise-licensed-customers), regardless of license type.
:::

## Enterprise licensed customers
```{applies_to}
deployment:
  eck: ga 3.2
```

In {{eck}} clusters licensed with an enterprise license, a separate PDB is created for each type of nodeSet defined in the manifest allowing upgrade or maintenance operations to be more quickly executed. The PDBs allow one {{es}} Pod per nodeSet to simultaneously be taken down as long as the cluster has the health defined in the following table:

| Role | Cluster health required | Notes |
|------|------------------------|--------|
| master | Yellow |  |
| data | Green | All Data roles are grouped together into a single PDB, except for data_frozen. |
| data_frozen | Yellow | Since data_frozen nodes are essentially stateless, managing searchable snapshots when compared to other data node types, additional disruptions are allowed. |
| ingest | Yellow |  |
| ml | Yellow |  |
| coordinating | Yellow |  |
| transform | Yellow |  |
| remote_cluster_client | Yellow |  |

Single-node clusters are not considered highly available and can always be disrupted.

### Non-enterprise licensed customers
:::{note}
In ECK 3.1 and earlier, all clusters follow this behavior regardless of license type.
:::

In {{eck}} clusters that do not have an enterprise license, one {{es}} Pod can be taken down at a time, as long as the cluster has a health status of `green`. Single-node clusters are not considered highly available and can always be disrupted.

## Overriding the default behavior

In the {{es}} specification, you can change the default behavior in 2 ways. By fully overriding the PodDisruptionBudget within the {{es}} spec or by disabling the default PodDisruptionBudget and specifying one or more PodDisruptionBudget(s).

### Fully override the PodDisruptionBudget within the {{es}} spec [k8s-override-default-pdb]

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
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

This will cause the ECK operator to only create the PodDisruptionBudget defined in the spec. It will not create any additional PodDisruptionBudgets.

::::{note}
[`maxUnavailable`](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#arbitrary-controllers-and-selectors) cannot be used with an arbitrary label selector, therefore `minAvailable` is used in this example.
::::

### Pod disruption budget per nodeSet [k8s-pdb-per-nodeset]

You can specify a PDB per nodeSet or node role.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  podDisruptionBudget: {} <1>
  version: {{version.stack}}
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
