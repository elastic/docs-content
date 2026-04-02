---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-update-strategy.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Update strategy
---

# Pod update strategy for Logstash on ECK [k8s-logstash-update-strategy]

The operator takes a Pod down to restart and applies a new configuration value. All Pods are restarted in reverse ordinal order.

## Default behavior [k8s_default_behavior_2]

When `updateStrategy` is not present in the specification, it defaults to the following:

```yaml
spec:
  updateStrategy:
    type: "RollingUpdate" <1>
    rollingUpdate:
      partition: 0        <2>
      maxUnavailable: 1   <3>
```

1. The `RollingUpdate` strategy will update Pods one by one in reverse ordinal order.
2. This means that all the Pods from ordinal Replicas-1 to `partition` are updated . You can split the update into partitions to perform [canary rollout](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/#rolling-out-a-canary).
3. This ensures that the cluster has no more than one unavailable Pod at any given point in time.



## OnDelete [k8s_ondelete]

```yaml
spec:
  updateStrategy:
    type: "OnDelete"
```

`OnDelete` strategy does not automatically update Pods when a modification is made. You need to restart Pods yourself.


