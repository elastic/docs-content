---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-virtual-memory.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Virtual memory [k8s-virtual-memory]

By default, {{es}} uses memory mapping (`mmap`) to efficiently access indices. Default values for virtual address space on Linux distributions can be too low for {{es}} to work properly, which may result in out-of-memory exceptions. This is why [the quickstart example](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) disables `mmap` through the `node.store.allow_mmap: false` setting. For production workloads, we recommended you increase the kernel setting `vm.max_map_count` to `1048576` and leave `node.store.allow_mmap` unset.

The kernel setting `vm.max_map_count=1048576` can be set on the host directly, by a dedicated init container which must be privileged, a dedicated Daemonset, or a dedicated ComputeClass.

:::{important}
For {{es}} version 8.16 and later, set the `vm.max_map_count` kernel setting to `1048576`; for {{es}} version 8.15 and earlier, set `vm.max_map_count` to `262144`. 

The exception is in GKE Autopilot environments. Your options depend on your GKE version:
* **GKE 1.30.3-gke.1451000+**: Use a custom `ComputeClass`, rather than a `DaemonSet`, to override the kernel setting.
* **Earlier versions**: `vm.max_map_count` must be set to `262144`.
:::

For more information, check the {{es}} documentation on [Virtual memory](/deploy-manage/deploy/self-managed/vm-max-map-count.md).

Optionally, you can select a different type of file system implementation for the storage. For possible options, check the [store module documentation](elasticsearch://reference/elasticsearch/index-settings/store.md).

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    config:
      index.store.type: niofs
```

## Using an Init Container to set virtual memory [k8s_using_an_init_container_to_set_virtual_memory]

To add an init container that changes the host kernel setting before your {{es}} container starts, you can use the following example {{es}} spec:

```yaml subs=true
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        initContainers:
        - name: sysctl
          securityContext:
            privileged: true
            runAsUser: 0
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=1048576']
EOF
```

Note that this requires the ability to run privileged containers, which is likely not the case on many secure clusters.


## Using a Daemonset to set virtual memory [k8s_using_a_daemonset_to_set_virtual_memory]

To use a Daemonset that changes the host kernel setting on all nodes:

```yaml
cat <<EOF | kubectl apply -n elastic-system -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: max-map-count-setter
  labels:
    k8s-app: max-map-count-setter
spec:
  selector:
    matchLabels:
      name: max-map-count-setter
  template:
    metadata:
      labels:
        name: max-map-count-setter
    spec:
      initContainers:
        - name: max-map-count-setter
          image: docker.io/bash:5.2.21
          resources:
            limits:
              cpu: 100m
              memory: 32Mi
          securityContext:
            privileged: true
            runAsUser: 0
          command: ['/usr/local/bin/bash', '-e', '-c', 'echo 1048576 > /proc/sys/vm/max_map_count'] <1>
      containers:
        - name: sleep
          image: docker.io/bash:5.2.21
          command: ['sleep', 'infinity']
EOF
```
1. In GKE Autopilot environments, `vm.max_map_count` must be set to 262144 when using a DaemonSet.

To run an {{es}} instance that waits for the kernel setting to be in place:

```yaml subs=true
cat <<'EOF' | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 1
    # Only uncomment the below section if you are not using the previous Daemonset to set max_map_count.
    # config:
    #  node.store.allow_mmap: false
    podTemplate:
      spec:
        # This init container ensures that the `max_map_count` setting has been applied before starting Elasticsearch.
        # This is not required, but is encouraged when using the previous Daemonset to set max_map_count.
        # Do not use this if setting config.node.store.allow_mmap: false
        initContainers:
        - name: max-map-count-check
          command: ['sh', '-c', "while true; do mmc=$(cat /proc/sys/vm/max_map_count); if [ ${mmc} -eq 262144 ]; then exit 0; fi; sleep 1; done"] <1>
EOF
```
1. In GKE Autopilot environments, `vm.max_map_count` must be set to 262144 when using a DaemonSet.


## Using a custom ComputeClass to set virtual memory [k8s_using_a_computeclass_to_set_virtual_memory]
```{applies_to}
deployment:
  eck: ga 3.2+
```

If you're using [GKE Autopilot](/deploy-manage/deploy/cloud-on-k8s/deploy-eck-on-gke-autopilot.md) to run ECK, then you can use a custom ComputeClass, rather than a DaemonSet, to increase the `vm.max_map_count` setting. This allows you to set a higher value, which is not possible with a DaemonSet.

1. Create a ComputeClass that changes the host kernel setting on all nodes:

    ```yaml
    cat <<EOF | kubectl apply -f -
    apiVersion: cloud.google.com/v1
    kind: ComputeClass
    metadata:
      name: elasticsearch
    spec:
      whenUnsatisfiable: "DoNotScaleUp" <1>
      nodePoolAutoCreation:
        enabled: true
      priorityDefaults: <2>
        nodeSystemConfig:
          linuxNodeConfig:
            sysctls:
              vm.max_map_count: 1048576
      priorities:
        - machineFamily: n2
    EOF
    ```
    1. Default since GKE 1.33
    2. `priorityDefaults` is available only since GKE 1.32.1-gke.1729000

2. Create your {{es}} instance using the custom ComputeClass:

    ```yaml subs=true
    cat <<'EOF' | kubectl apply -f -
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: elasticsearch
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