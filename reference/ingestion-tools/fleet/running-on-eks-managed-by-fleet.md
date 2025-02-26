---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/running-on-eks-managed-by-fleet.html
---

# Run Elastic Agent on Amazon EKS managed by Fleet [running-on-eks-managed-by-fleet]

Please follow the steps to run the {{agent}} on [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md) page.


## Important notes: [_important_notes_3]

On managed Kubernetes solutions like EKS, {{agent}} has no access to several data sources. Find below the list of the non available data:

1. Metrics from [Kubernetes control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) components are not available. Consequently metrics are not available for `kube-scheduler` and `kube-controller-manager` components. In this regard, the respective **dashboards** will not be populated with data.
2. **Audit logs** are available only on Kubernetes master nodes as well, hence cannot be collected by {{agent}}.
3. Fields `orchestrator.cluster.name` and `orchestrator.cluster.url` are not populated. `orchestrator.cluster.name` field is used as a cluster selector for default Kubernetes dashboards, shipped with [Kubernetes integration](integration-docs://docs/reference/kubernetes.md).

    In this regard, you can use [`add_fields` processor](beats://docs/reference/filebeat/add-fields.md) to add `orchestrator.cluster.name` and `orchestrator.cluster.url` fields for each [Kubernetes integration](integration-docs://docs/reference/kubernetes.md)'s component:

    ```yaml
    - add_fields:
        target: orchestrator.cluster
        fields:
          name: clusterName
          url: clusterURL
    ```
