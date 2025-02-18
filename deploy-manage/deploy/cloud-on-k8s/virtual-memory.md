---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-virtual-memory.html
---

# Virtual memory [k8s-virtual-memory]

By default, Elasticsearch uses memory mapping (`mmap`) to efficiently access indices. Usually, default values for virtual address space on Linux distributions are too low for Elasticsearch to work properly, which may result in out-of-memory exceptions. This is why [the quickstart example](deploy-an-orchestrator.md) disables `mmap` through the `node.store.allow_mmap: false` setting. For production workloads, it is strongly recommended to increase the kernel setting `vm.max_map_count` to `262144` and leave `node.store.allow_mmap` unset.

The kernel setting `vm.max_map_count=262144` can be set on the host directly, by a dedicated init container which must be privileged, or a dedicated Daemonset.

For more information, check the Elasticsearch documentation on [Virtual memory](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).

Optionally, you can select a different type of file system implementation for the storage. For possible options, check the [store module documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-store.html).

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    config:
      index.store.type: niofs
```

## Using an Init Container to set virtual memory [k8s_using_an_init_container_to_set_virtual_memory]

To add an init container that changes the host kernel setting before your Elasticsearch container starts, you can use the following example Elasticsearch spec:

```yaml
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.16.1
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
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
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
          command: ['/usr/local/bin/bash', '-e', '-c', 'echo 262144 > /proc/sys/vm/max_map_count']
      containers:
        - name: sleep
          image: docker.io/bash:5.2.21
          command: ['sleep', 'infinity']
EOF
```

To run an Elasticsearch instance that waits for the kernel setting to be in place:

```yaml
cat <<'EOF' | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
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
          command: ['sh', '-c', "while true; do mmc=$(cat /proc/sys/vm/max_map_count); if [ ${mmc} -eq 262144 ]; then exit 0; fi; sleep 1; done"]
EOF
```


