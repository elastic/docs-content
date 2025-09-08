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

### Enterprise licensed customers
```{applies_to}
deployment:
  eck: ga 3.2
```

A separate PDB is created for each type of nodeSet defined in the manifest allowing upgrade or maintenance operations to be more quickly executed. The PDBs allow one {{es}} Pod per nodeSet to simultaneously be taken down as long as the cluster has the health defined in the following table:

| Role | Cluster health required | Notes |
|------|------------------------|--------|
| Master | Yellow |  |
| Data | Green | All Data roles are grouped together into a single PDB, except for data_frozen. |
| Data Frozen | Yellow | Since the frozen tier are essentially stateless, managing searchable snapshots, additional disruptions are allowed. |
| Ingest | Yellow |  |
| ML | Yellow |  |
| Coordinating | Yellow |  |
| Transform | Yellow |  |
| Remote cluster client | Yellow |  |

Single-node clusters are not considered highly available and can always be disrupted.

### Non-enterprise licensed customers
:::{note}
In ECK 3.1 and earlier, all clusters follow this behavior regardless of license type.
:::

It allows one {{es}} Pod to be taken down, as long as the cluster has a `green` health. Single-node clusters are not considered highly available and can always be disrupted.

## Overriding the default behavior

In the {{es}} specification, you can change the default behavior as follows:

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

This will cause the ECK operator to only create the PodDisruptionBudget defined in the spec and will not create any additional PodDisruptionBudgets.

::::{note}
[`maxUnavailable`](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#arbitrary-controllers-and-selectors) cannot be used with an arbitrary label selector, therefore `minAvailable` is used in this example.
::::

## Pod disruption budget per nodeSet [k8s-pdb-per-nodeset]

You can specify a PDB per nodeSet or node role.

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
