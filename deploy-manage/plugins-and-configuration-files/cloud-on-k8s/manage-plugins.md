---
navigation_title: In ECK
description: Choose how to install Elasticsearch plugins and configuration files on Elastic Cloud on Kubernetes.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Add plugins and configuration files in {{eck}} [eck-add-plugins-overview]

On {{eck}}, {{es}} runs in Kubernetes pods. Unlike {{ech}} and {{ece}}, {{eck}} does not host a catalog of plugins that you enable on a deployment. You must install any plugin that is not already in the base image before the main {{es}} container starts. That includes [official {{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md), community or third-party plugins, and [plugins you write yourself](elasticsearch://extend/index.md).

You can also add configuration files such as synonym dictionaries, SAML metadata, or CA certificates to the {{es}} configuration directory.

Refer to [](/deploy-manage/plugins-and-configuration-files.md) for options that apply to other deployment types.

## Choose an approach

The approach depends on what you are adding. Plugins require a custom container image or an init container. Configuration files can be mounted from a ConfigMap or Secret.

### Install plugins

Custom container images and init containers install the same plugins. They differ in when the installation occurs: a custom image includes the plugins at build time, while an init container installs them each time a pod starts. This determines the infrastructure you need to maintain, how quickly nodes become ready, and whether node startup depends on network access.

With a [custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md), you build the plugins into an image based on the official Elastic images, so they are already in place when the container starts. Nodes start faster, need no internet access at runtime, and every node runs an identical image. In exchange, you need a container registry and build infrastructure, and each {{es}} version upgrade means building and publishing a new image. You can include configuration files in the image as well.

With [init containers](init-containers-for-plugin-downloads.md), an init container runs `elasticsearch-plugin install` before {{es}} starts. You can get started without a registry and change plugin versions by editing the manifest, but every new node repeats the download, which uses bandwidth and delays startup. It also ties node creation to network availability, so a network problem or an incorrect plugin reference can cause new nodes to fail. If your pods run in a service mesh, review [the note about using Istio](init-containers-for-plugin-downloads.md#istio-note).

Use a custom image when reproducibility and predictable startup are priorities, such as in production environments. Use init containers when you need to iterate quickly, or when maintaining a container registry and build pipeline is not practical.

### Add configuration files

To make files such as synonym dictionaries, certificates, or SAML metadata available to {{es}}, [mount them from a ConfigMap or Secret](custom-configuration-files-plugins.md) using a volume and volume mount. This is the standard Kubernetes way to get files into a pod, and file content stays managed as Kubernetes objects, so updating a file means updating the ConfigMap or Secret instead of rebuilding an image. The trade-off is that you maintain those objects alongside your {{es}} manifests.

This approach cannot install plugins. If you need both, combine it with a custom image or init containers.

## {{kib}} plugins

To run {{kib}} with additional plugins, use a custom container image that already includes them. Refer to [Install {{kib}} plugins](k8s-kibana-plugins.md) for more information.
