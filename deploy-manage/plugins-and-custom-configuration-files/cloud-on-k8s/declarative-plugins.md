---
description: Declare the Elasticsearch plugins to install on every node of an ECK-managed cluster with the spec.plugins field.
applies_to:
  deployment:
    eck: ga 3.7+
products:
  - id: cloud-kubernetes
navigation_title: Plugins field
---

# Install plugins with `spec.plugins` on {{eck}} [k8s-declarative-plugins]

Use the `spec.plugins` field of the {{es}} resource to declare the plugins to install on all nodes of the cluster. You can't set different plugins for each NodeSet.

{{eck}} (ECK) writes the list to an `elasticsearch-plugins.yml` file on each node. {{es}} reads the file only when it starts, and installs, upgrades, and removes plugins to match it. When you change the list, ECK performs a rolling restart of the cluster to apply it.

::::{important}
`spec.plugins` requires {{es}} 8.17.0 or later. For earlier versions, use [init containers](init-containers-for-plugin-downloads.md) or a [custom image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md).
::::

## Plugin configuration [k8s-declarative-plugins-declare]

The following example installs the official ICU analysis plugin and a custom plugin hosted on an HTTPS server:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  plugins:
    items:
    - id: analysis-icu
    - id: my-custom-plugin
      location: https://plugins.example.com/my-custom-plugin-{{version.stack}}.zip
  nodeSets:
  - name: default
    count: 3
```

The `spec.plugins` field accepts the following settings. For the full schema, refer to the [ECK API reference](cloud-on-k8s://reference/api-reference/index.md).

`items`
:   A list of plugins to install. The list must contain at least one entry, and each `id` must be unique.

    `id`
    :   The name of the plugin. For a custom plugin, it must match the `name` in the plugin's `plugin-descriptor.properties` file, otherwise {{es}} fails to start.

    `location`
    :   The URL, `file://` path, or Maven coordinates of a custom plugin. Omit it for [official {{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md). Any other plugin requires it, otherwise {{es}} fails to start.

`proxy`
:   An optional HTTP proxy, in `host:port` form, that {{es}} uses to download plugins.

Each new node installs the plugins when it first starts. Unless the `location` is a `file://` path, {{es}} downloads each plugin, so the pods need network access to the plugin source.

To check which plugins are installed on each node, run `GET _cat/plugins?v`.

To stop managing plugins with `spec.plugins`, remove the field. ECK restarts the nodes, which then run only the plugins included in the {{es}} image.

## Validation [k8s-declarative-plugins-validation]

When you apply the manifest, the ECK [validating webhook](/deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md) checks the plugin configuration, so you get errors right away instead of a node that fails to start. The webhook checks the following:

* The {{es}} version is 8.17.0 or later.
* No plugin `id` is blank.
* Every `location` is a valid URL, `file://` path, or Maven coordinates. A location without a scheme, such as `/mnt/plugins/my-plugin.zip`, is rejected. Use `file:///mnt/plugins/my-plugin.zip` instead. This check is best effort, so a location that passes it can still fail when {{es}} starts.
* The `proxy` is in `host:port` form, with a numeric port.

The webhook's error messages omit credentials that you might include in a `location` or `proxy` value. If the validating webhook is [disabled](/deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md#k8s-disable-webhook), these checks don't run, and configuration errors only appear when {{es}} starts.

## Init containers and custom images [k8s-declarative-plugins-sync]

Don't combine `spec.plugins` with [init containers](init-containers-for-plugin-downloads.md) that install or remove plugins. Those init containers fail when `spec.plugins` is set, and ECK shows a warning when you apply a manifest that includes one. Move their plugins to `spec.plugins` instead.

If you set `spec.plugins` on a cluster that runs a [custom image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md), list every plugin that you want to keep, including the ones built into the image. {{es}} removes any installed plugin that isn't in the list. Without `spec.plugins`, the plugins built into the image are loaded as usual.

## Upgrades with custom plugins [k8s-declarative-plugins-upgrade]

Custom plugins are built for a specific {{es}} version, so plan their upgrade together with the cluster upgrade. Official plugins don't need any change: {{es}} upgrades them automatically.

To upgrade a cluster that uses custom plugins:

1. Get the build of each custom plugin for the target {{es}} version, and make it available at a location that the nodes can reach.
2. In the {{es}} resource, update `spec.version` and the `location` of each custom plugin in the same change. If you update only one of them, the nodes can fail to start because the plugin and {{es}} versions don't match.
3. Apply the manifest. ECK performs a rolling upgrade, and each node restarts with the new {{es}} version and the matching plugins.

::::{warning}
During the upgrade, a node that hasn't been upgraded yet can fail to start if its {{es}} process restarts, for example after running out of memory. The node picks up the plugins built for the new version, which the old version can't load, and keeps failing until ECK upgrades it. To reduce the risk, make sure the cluster is healthy and has enough resources before you start the upgrade.
::::
