A DaemonSet runs only on the nodes whose taints its Pods tolerate. Control plane nodes are usually tainted, so the Pods of a DaemonSet don't run on them by default. To also collect data from the control plane nodes, add a toleration for the taint to the `podTemplate`. The taint key depends on the {{k8s}} distribution: it is `node-role.kubernetes.io/control-plane` on upstream {{k8s}} and `node-role.kubernetes.io/master` on OpenShift. To list the taints of your nodes, run `kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints`.

```yaml
spec:
  daemonSet:
    podTemplate:
      spec:
        tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
```
