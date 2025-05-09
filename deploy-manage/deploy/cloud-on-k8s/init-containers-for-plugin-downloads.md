---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-init-containers-plugin-downloads.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Init containers for plugin downloads [k8s-init-containers-plugin-downloads]

You can install custom plugins before the {{es}} container starts with an `initContainer`. For example:

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        initContainers:
        - name: install-plugins
          command:
          - sh
          - -c
          - |
            bin/elasticsearch-plugin remove --purge analysis-icu
            bin/elasticsearch-plugin install --batch analysis-icu
```

You can also override the {{es}} container image to use your own image with the plugins already installed, as described in [custom images](create-custom-images.md). For more information on both these options, you can check the [Create automated snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md) section and the Kubernetes documentation on [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

The init container inherits:

* The image of the main container image, if one is not explicitly set.
* The volume mounts from the main container unless a volume mount with the same name and mount path is present in the init container definition
* The Pod name and IP address environment variables.

