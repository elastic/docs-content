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
4. Ensure you are using a node class that is applicable for your workload by adding a `cloud.google.com/compute-class` label in a `nodeSelector`. Refer to [GKE Autopilot documentation](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-compute-classes).

## Ensuring virtual memory kernel settings [k8s-autopilot-setting-virtual-memory]

If you are intending to run production workloads on GKE Autopilot then `vm.max_map_count` should be set. The recommended way to set this kernel setting on the Autopilot hosts depends on your ECK version:

* {applies_to}`eck: ga 3.0-3.1` [Use a DaemonSet](/deploy-manage/deploy/cloud-on-k8s/virtual-memory.md#k8s_using_a_daemonset_to_set_virtual_memory). You must be running at least version 1.25 when on the `regular` channel or using the `rapid` channel, which currently runs version 1.27.
  
  ::::{warning}
  Use the provided `Daemonset` exactly as specified, with a `max_map_count` value of `262144`, or it could be rejected by the Autopilot control plane.
  ::::
* {applies_to}`eck: ga 3.2+` [Use a custom ComputeClass](/deploy-manage/deploy/cloud-on-k8s/virtual-memory.md#k8s_using_a_computeclass_to_set_virtual_memory). Using a custom ComputeClass allows you to set a higher value for `max_map_count` due to limitations on the `DaemonSet`.

## Install the ECK Operator [k8s-autopilot-deploy-the-operator]

Refer to [*Install ECK*](install.md) for more information on installation options.

## Deploy an {{es}} cluster [k8s-autopilot-deploy-elasticsearch]

Create an {{es}} cluster. The information that you need to provide in your spec depends on whether you've increased your virtual memory kernel setting, and the method that you used.

::::{tab-set}

:::{tab-item} Using a custom ComputeClass
If you used a custom ComputeClass to set `max_map_count`, then you need to reference the custom ComputeClass as part of your template spec.

```yaml subs=true
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
    podTemplate:
      spec:
        nodeSelector:
          cloud.google.com/compute-class: "elasticsearch"
EOF
```
:::


:::{tab-item} Using a DaemonSet

If you used a DaemonSet to set `max_map_count`, you can add the following `initContainer` to ensure the setting is set prior to starting {{es}}.

```yaml subs=true
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
    podTemplate:
      spec:
        # This init container ensures that the `max_map_count` setting has been applied before starting Elasticsearch.
        # This is not required, but is encouraged when using the Daemonset to set max_map_count.
        # Do not use this if setting config.node.store.allow_mmap: false
        initContainers:
        - name: max-map-count-check
          command: ['sh', '-c', "while true; do mmc=$(cat /proc/sys/vm/max_map_count); if [ ${mmc} -eq 262144 ]; then exit 0; fi; sleep 1; done"]     
EOF
```
:::
::::

### Deploy without custom virtual memory

If you didn't increase your virtual memory, then you need to set `node.store.allow_mmap` to `false`.

```yaml subs=true
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
    config:
      node.store.allow_mmap: false
EOF
```
:::
::::

## Deploy a standalone Elastic Agent and/or Beats [k8s-autopilot-deploy-agent-beats]

When running Elastic Agent and Beats within GKE Autopilot there are storage constraints to be considered. No `HostPath` volumes are allowed, which the ECK operator defaults to when unset for both `Deployments` and `DaemonSets`. Instead use [Kubernetes ephemeral volumes](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes).

Refer to [Recipes to deploy {{es}}, {{kib}}, Elastic Fleet Server and Elastic Agent and/or Beats within GKE Autopilot](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/autopilot).

