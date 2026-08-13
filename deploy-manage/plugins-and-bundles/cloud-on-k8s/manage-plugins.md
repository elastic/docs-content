---
navigation_title: Extend {{eck}}
description: Choose how to install Elasticsearch plugins and configuration files on Elastic Cloud on Kubernetes.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Add plugins and configuration files in {{eck}} [eck-add-plugins-overview]

On {{eck}}, {{es}} runs in Kubernetes pods. Plugins must be present on disk before the main {{es}} container starts. Configuration files such as synonym dictionaries, scripts, or SAML metadata can also be made available in the configuration directory.

{{eck}} does not use *bundles* (the ZIP-based extension workflow in {{ech}} and {{ece}}). Instead, you choose how to supply plugins and configuration files based on whether you need reproducibility, runtime network access, or standard Kubernetes mounts.

Refer to [Plugins and bundles](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.

## Choose an approach

 Use a custom image or init containers when you need plugins. Prefer ConfigMaps or Secrets when you only need configuration files.

### Custom container image

Build a custom image from the official Elastic image with the required plugins and configuration files already included. Refer to [Create a custom image](custom-configuration-files-plugins.md#create-a-custom-image).

* **Pros**
  * Deployment is reproducible and reusable.
  * Does not require internet access at runtime.
  * Saves bandwidth and is quicker to start.
* **Cons**
  * Requires a container registry and build infrastructure to build and host the custom image.
  * Version upgrades require building a new container image.

### Init containers

Run `elasticsearch-plugin install` in an init container before the main {{es}} container starts. Refer to [Init containers for plugin downloads](init-containers-for-plugin-downloads.md).

* **Pros**
  * Simpler to adopt and to upgrade versions.
* **Cons**
  * Requires pods to have internet access. When using Istio, see the [Istio note](init-containers-for-plugin-downloads.md#istio-note).
  * Adding new {{es}} nodes could randomly fail due to network issues or bad configuration.
  * Each {{es}} node needs to repeat the download, wasting bandwidth and slowing startup.
  * Deployment manifests are more complicated.

### ConfigMaps or Secrets

Mount configuration files into your {{es}} nodes with volumes and volume mounts. Refer to [Use a volume and volume mount together with a ConfigMap or Secret](custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

* **Pros**
  * Best choice for injecting configuration files into your {{es}} nodes.
  * Follows standard Kubernetes methodology to mount files into Pods.
* **Cons**
  * Not valid for plugin installation. Mounting plugin ZIP files does not run `elasticsearch-plugin install`, so {{es}} will not load them.
  * Requires you to maintain the ConfigMaps or Secrets with the content of the files.

## {{kib}} plugins

To run {{kib}} with additional plugins, use a custom container image that already includes them. Refer to [Install {{kib}} plugins](k8s-kibana-plugins.md).
