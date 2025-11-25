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

{{eck}} manages either a single default PDB, or multiple PDBs per {{es}} resource depending on the license level of the ECK installation.

:::{note}
In {{eck}} 3.1 and earlier, all clusters follow the [default PodDisruptionBudget rules](#default-pdb-rules), regardless of license type.
:::

## Advanced rules (Enterprise license required)

```{applies_to}
deployment:
  eck: ga 3.2
```

In Elasticsearch clusters managed by ECK and licensed with an Enterprise license, PDBs are created based on Elasticsearch node roles, allowing Kubernetes upgrade or maintenance operations to be executed more quickly. Multiple `nodeSets` with the same roles, such as `master` or `ml`, are combined into a single PDB. Each PDB permits one Elasticsearch Pod to be disrupted at a time, provided the Elasticsearch cluster maintains the health status described in the following table.

| Role | Cluster health required | Notes |
|------|------------------------|--------|
| master | Yellow |  |
| data | Green | All Data roles are grouped together into a single PDB, except for data_frozen. |
| data_frozen | Yellow | Since frozen data tier nodes only host partially mounted indices backed by searchable snapshots additional disruptions are allowed. |
| ingest | Yellow |  |
| ml | Yellow |  |
| coordinating | Yellow |  |
| transform | Yellow |  |
| remote_cluster_client | Yellow |  |

Single-node clusters are not considered highly available and can always be disrupted regardless of license type.

## Default rules (Basic license) [default-pdb-rules]

:::{note}
In {{eck}} 3.1 and earlier, all clusters follow this behavior regardless of license type.
:::

In {{eck}} clusters that do not have an Enterprise license, one {{es}} Pod can be taken down at a time, as long as the cluster has a health status of `green`. Single-node clusters are not considered highly available and can always be disrupted.

## Overriding the default behavior

In the {{es}} specification, you can change the default behavior in two ways. By fully overriding the PodDisruptionBudget within the {{es}} spec or by disabling the default PodDisruptionBudget and specifying one or more PodDisruptionBudget(s).

### Specify your own PodDisruptionBudget [k8s-specify-own-pdb]

You can fully override the default PodDisruptionBudget by specifying your own PodDisruptionBudget in the {{es}} spec.

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

### Create a PodDisruptionBudget per nodeSet [k8s-pdb-per-nodeset]

You can specify a PDB per `nodeSet` or node role.

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
