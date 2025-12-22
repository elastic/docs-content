---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-uninstalling-eck.html
applies_to:
  deployment:
    eck:
products:
  - id: cloud-kubernetes
---

# Uninstall {{eck}} [k8s-uninstalling-eck]

This page provides instructions for uninstalling {{eck}}, including removing all Elastic resources and the {{eck}} operator from your cluster.

To uninstall the operator:

1. Remove all Elastic resources in all namespaces:

    ```shell
    kubectl get namespaces --no-headers -o custom-columns=:metadata.name \
      | xargs -n1 kubectl delete elastic --all -n
    ```

    This deletes all underlying {{stack}} resources, including their Pods, Secrets, Services, and so on.

2. Uninstall the operator:

    ```shell subs=true
    kubectl delete -f https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml
    kubectl delete -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
    ```

::::{warning}
Deleting CRDs will trigger deletion of all custom resources ({{es}}, {{kib}}, APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash) in all namespaces of the cluster, regardless of whether they are managed by a single operator or multiple operators.
::::