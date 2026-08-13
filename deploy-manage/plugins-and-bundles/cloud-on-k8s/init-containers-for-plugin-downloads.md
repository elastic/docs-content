---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-init-containers-plugin-downloads.html
description: Download and install Elasticsearch plugins at pod startup on ECK with an init container.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Init containers
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

You can also override the {{es}} container image to use your own image with the plugins already installed, as described in [Create custom images](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md). For more information on both options, refer to [Add plugins and configuration files in {{eck}}](manage-plugins.md) and the Kubernetes documentation on [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

The init container inherits:

* The image of the main container image, if one is not explicitly set.
* The volume mounts from the main container unless a volume mount with the same name and mount path is present in the init container definition
* The Pod name and IP address environment variables.

## Note when using Istio [istio-note]

When using Istio, init containers do **not** have network access, as the Envoy sidecar that provides network connectivity is not started yet. In this scenario, custom containers are the best option. If custom containers are simply not a viable option, then it is possible to adjust the startup command for the {{es}} container itself to run the plugin installation before starting {{es}}, as the following example describes. Note that this approach will require updating the startup command if it changes in the {{es}} image, which could potentially cause failures during upgrades.

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          command:
          - /usr/bin/env
          - bash
          - -c
          - |
            #!/usr/bin/env bash
            set -e
            bin/elasticsearch-plugin remove --purge repository-s3 || true
            bin/elasticsearch-plugin install --batch repository-s3
            /bin/tini -- /usr/local/bin/docker-entrypoint.sh
```
