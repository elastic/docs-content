---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-uninstalling-eck.html
---

# Uninstall Elastic Cloud on Kubernetes [k8s-uninstalling-eck]

To uninstall the operator:

1. Remove all Elastic resources in all namespaces:

    ```shell
    kubectl get namespaces --no-headers -o custom-columns=:metadata.name \
      | xargs -n1 kubectl delete elastic --all -n
    ```

    This deletes all underlying Elastic Stack resources, including their Pods, Secrets, Services, and so on.

2. Uninstall the operator:

    ```shell
    kubectl delete -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
    kubectl delete -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
    ```


