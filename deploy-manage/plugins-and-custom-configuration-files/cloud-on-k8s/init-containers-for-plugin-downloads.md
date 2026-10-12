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

# Install plugins with init containers on {{eck}} [k8s-init-containers-plugin-downloads]

Use an init container to run [`elasticsearch-plugin install`](elasticsearch://reference/elasticsearch-plugins/installation.md) before the main {{es}} container starts. Each new node repeats the download, so the pods need network access to reach the plugin source.

The following example installs the ICU analysis plugin:

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

For more information on how init containers behave in Kubernetes, refer to the [Kubernetes init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) documentation.

:::{tip}
You can also build the plugins into your own {{es}} image, as described in [Create custom images](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md). To compare that approach with init containers, refer to [Add plugins and custom configuration files in {{eck}}](manage-plugins.md).
:::


## What the init container inherits

Unless you override them, the init container inherits:

* The image of the main {{es}} container, if one is not explicitly set.
* The volume mounts from the main container, unless a volume mount with the same name and mount path is already defined on the init container.
* The Pod name and IP address environment variables.

## Note when using Istio [istio-note]

When using Istio, an init container typically has no network access, because the Envoy sidecar that provides connectivity has not started yet. The plugin download then fails. You have three options:

* Allow the outbound ports that the init container needs, so that its traffic bypasses the sidecar. For a manifest that installs a plugin this way, refer to [Using init containers with Istio CNI](/deploy-manage/deploy/cloud-on-k8s/k8s-service-mesh-istio.md#k8s-service-mesh-istio-cni).
* Use a [custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md) that already includes the plugins, so that nothing is downloaded at startup.
* Run the plugin install in the {{es}} container's startup command, as shown in the following section.

## Install plugins from the {{es}} startup command [istio-startup-command]

If allowing the ports and using a custom image are both impractical, you can run the plugin install in the {{es}} container’s startup command before {{es}} starts. You may need to update that command if the entrypoint in the {{es}} image changes, which can cause failures during upgrades. The following is an example.

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
