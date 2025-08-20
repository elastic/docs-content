---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-setting-virtual-memory.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-deploy-the-operator.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-deploy-elasticsearch.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-deploy-agent-beats.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Deploy ECK on GKE Autopilot [k8s-autopilot]

This page shows how to run ECK on GKE Autopilot.

1. It is recommended that each Kubernetes host’s virtual memory kernel settings be modified. Refer to [Virtual memory](virtual-memory.md).
2. It is recommended that {{es}} Pods have an `initContainer` that waits for virtual memory settings to be in place.
3. For Elastic Agent/Beats there are storage limitations to be considered.
4. Ensure you are using a node class that is applicable for your workload by adding a `cloud.google.com/compute-class` label in a `nodeSelector`. Refer to [GKE Autopilot documentation.](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-compute-classes).

## Ensuring virtual memory kernel settings [k8s-autopilot-setting-virtual-memory]

If you are intending to run production workloads on GKE Autopilot then `vm.max_map_count` should be set. The recommended way to set this kernel setting on the Autopilot hosts is with a `Daemonset` as described in the [Virtual memory](virtual-memory.md) section. You must be running at least version 1.25 when on the `regular` channel or using the `rapid` channel, which currently runs version 1.27.

::::{warning}
Only use the provided `Daemonset` exactly as specified or it could be rejected by the Autopilot control plane.
::::

## Install the ECK Operator [k8s-autopilot-deploy-the-operator]

Refer to [*Install ECK*](install.md) for more information on installation options.

## Deploy an {{es}} cluster [k8s-autopilot-deploy-elasticsearch]

Create an {{es}} cluster. If you are using the `Daemonset` described in the [Virtual memory](virtual-memory.md) section to set `max_map_count` you can add the `initContainer` below is also used to ensure the setting is set prior to starting {{es}}.

```shell subs=true
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 1
    # Only uncomment the below section if you are not using the Daemonset to set max_map_count.
    # config:
    #  node.store.allow_mmap: false
    podTemplate:
      spec:
        # This init container ensures that the `max_map_count` setting has been applied before starting Elasticsearch.
        # This is not required, but is encouraged when using the previously mentioned Daemonset to set max_map_count.
        # Do not use this if setting config.node.store.allow_mmap: false
        initContainers:
        - name: max-map-count-check
          command: ['sh', '-c', "while true; do mmc=$(cat /proc/sys/vm/max_map_count); if [ ${mmc} -eq 262144 ]; then exit 0; fi; sleep 1; done"]
EOF
```

## Deploy a standalone Elastic Agent and/or Beats [k8s-autopilot-deploy-agent-beats]

When running Elastic Agent and Beats within GKE Autopilot there are storage constraints to be considered. No `HostPath` volumes are allowed, which the ECK operator defaults to when unset for both `Deployments` and `Daemonsets`. Instead use [Kubernetes ephemeral volumes](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes).

Refer to [Recipes to deploy {{es}}, {{kib}}, Elastic Fleet Server and Elastic Agent and/or Beats within GKE Autopilot](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/autopilot).

