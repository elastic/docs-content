---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-prestop.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Pod PreStop hook [k8s-prestop]

When an {{es}} `Pod` is terminated, its `Endpoint` is removed from the `Service` and the {{es}} process is terminated. As these two operations happen in parallel, a race condition exists. If the {{es}} process is already shut down, but the `Endpoint` is still a part of the `Service`, any new connection might fail. For more information, check [Termination of pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods).

Moreover, kube-proxy resynchronizes its rules [every 30 seconds by default](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/#options). During that time window of 30 seconds, the terminating Pod IP may still be used when targeting the service. Note the resync operation itself may take some time, especially if kube-proxy is configured to use iptables with a lot of services and rules to apply.

To address this issue and minimize unavailability, ECK relies on a [PreStop lifecycle hook](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/). It waits for an additional `PRE_STOP_ADDITIONAL_WAIT_SECONDS` (defaulting to 50). The additional wait time is used to:

1. Give time to in-flight requests to be completed.
2. Give clients time to use the terminating Pod IP resolved just before DNS record was updated.
3. Give kube-proxy time to refresh ipvs or iptables rules on all nodes, depending on its sync period setting.

The exact behavior is configurable using an environment variable, for example:

```yaml
spec:
  version: {{version.stack}}
  nodeSets:
    - name: default
      count: 1
      podTemplate:
        spec:
          containers:
          - name: elasticsearch
            env:
            - name: PRE_STOP_ADDITIONAL_WAIT_SECONDS
              value: "5"
```

The pre-stop lifecycle hook also tries to gracefully shut down the {{es}} node in case of a termination that is not caused by the ECK operator. Examples of such terminations could be Kubernetes node maintenance or a Kubernetes upgrade. In these cases the script will try to interact with the {{es}} API to notify {{es}} of the impending termination of the node. The intent is to avoid relocation and recovery of shards while the {{es}} node is only temporarily unavailable.

This is done on a best effort basis. In particular requests to an {{es}} cluster already in the process of shutting down might fail if the Kubernetes service has already been removed. The script allows for `PRE_STOP_MAX_DNS_ERRORS` which default to 2 before giving up.

When using local persistent volumes a different behavior might be desirable because the {{es}} node’s associated storage will not be available anymore on the new Kubernetes node. `PRE_STOP_SHUTDOWN_TYPE` allows to override the default shutdown type to one of the [possible values](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-shutdown-put-node). Be aware that setting it to anything other than `restart` might mean that the pre-stop hook will run longer than `terminationGracePeriodSeconds` of the Pod while moving data out of the terminating Pod and will not be able to complete unless you also adjust that value in the `podTemplate`.

