A DaemonSet runs Pods only on the nodes whose taints those Pods tolerate. Control plane nodes are typically tainted, so the Pods that the `daemonSet` element creates don't run on them by default.

To collect data from the control plane nodes as well, add a matching toleration to the `podTemplate`. The taint key depends on the {{k8s}} distribution:

* Upstream {{k8s}}: `node-role.kubernetes.io/control-plane`
* OpenShift: `node-role.kubernetes.io/master`

To list the taints of your nodes, run `kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints`.

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
