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

On {{eck}}, {{es}} runs in Kubernetes pods. You can install plugins and make configuration files—such as synonym dictionaries, scripts, or SAML metadata—available in the configuration directory.

Refer to [](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.

## Choose an approach

Plugins must be present on disk before the main {{es}} container starts, so {{eck}} does not use the ZIP *bundle* workflow from {{ech}} and {{ece}}. Pick one of these Kubernetes-native approaches based on whether you need plugins, only configuration files, or both.

* [Custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md): Build from the official Elastic images and install the plugins you need so they are present when the {{es}} container starts. Best when you want reproducible deployments without runtime internet access. You can also include configuration files in the image.

* [Init containers](init-containers-for-plugin-downloads.md): Run `elasticsearch-plugin install` in an init container before {{es}} starts. Easier to try without a registry, but each new node needs network access and redownloads the plugins.

* [ConfigMaps or Secrets](custom-configuration-files-plugins.md): Mount configuration files such as synonym dictionaries, certificates, or SAML metadata into the {{es}} config directory. Use this when you only need files on disk. Mounting a plugin ZIP does not install the plugin.

The following matrix compares these approaches in more detail.

:::{table}
:matrix:

| Consideration | Custom container image | Init containers | ConfigMaps or Secrets |
| --- | --- | --- | --- |
| Best used for | Plugins and optional configuration files included in the image | Plugins installed at pod startup | Configuration files only (dictionaries, certificates, metadata) |
| Runtime internet | Not required | Required (see also [Istio](init-containers-for-plugin-downloads.md#istio-note)) | Not required |
| Reproducibility | High: identical image for every deployment | Lower: each node downloads plugins at startup | High: file content is managed as Kubernetes objects |
| Version upgrades | Build and publish a new image for each {{es}} version | Update the install command or plugin version in the manifest | Update the ConfigMap or Secret |
| Startup cost | Lower: plugins are already in the image | Higher: each new node downloads plugins again | Lower for file mounts; does not install plugins |
| Operational overhead | Requires a container registry and build infrastructure | More complex manifests; new nodes can fail due to network or configuration errors | Requires ongoing maintenance of ConfigMaps or Secrets |
| Installs plugins? | Yes | Yes | No: mounting a plugin ZIP does not run `elasticsearch-plugin install` |

:::

## {{kib}} plugins

To run {{kib}} with additional plugins, use a custom container image that already includes them. Refer to [Install {{kib}} plugins](k8s-kibana-plugins.md).
