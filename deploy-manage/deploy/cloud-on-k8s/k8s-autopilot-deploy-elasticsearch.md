---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-deploy-elasticsearch.html
---

# Deploy an Elasticsearch instance [k8s-autopilot-deploy-elasticsearch]

Create an Elasticsearch cluster. If you are using the `Daemonset` described in the [Virtual memory](virtual-memory.md) section to set `max_map_count` you can add the `initContainer` below is also used to ensure the setting is set prior to starting Elasticsearch.

```shell
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
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

