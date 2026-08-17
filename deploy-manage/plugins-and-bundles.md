---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management.html
description: Extend Elasticsearch with plugins and bundles, and find the install path that matches your deployment type.
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: unavailable
navigation_title: Plugins and bundles
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Plugins and bundles in {{es}}

Use plugins and bundles to extend {{es}}'s core functionality with additional analyzers, discovery providers, ingest processors, field types, scripting languages, dictionaries, and related configuration files.

**[Plugins](elasticsearch://reference/elasticsearch-plugins/index.md)** are packages installed in {{es}}. Use them to add capabilities such as language and phonetic analysis, ingest processors for attachments or geo-IP data, additional field types, cloud discovery providers, or scripting languages. Official core plugins are maintained with {{es}} and share its version number. Community and custom plugins are maintained separately and can cover the same kinds of extensions when a core plugin is not available or you need something purpose-built.

**Bundles** are ZIP archives of configuration or data files, such as synonym dictionaries, scripts, or SAML metadata. In {{ech}} and {{ece}}, bundles are managed as *extensions* together with custom plugins. At node startup, {{ecloud}} extracts bundle contents into the node's configuration directory instead of installing them as plugins.
On other deployment types, the same kinds of files are still supported, but you provide them differently: you place them on each node's configuration path for self-managed clusters, or mount them with ConfigMaps or Secrets on {{eck}}.

After you [choose](elasticsearch://reference/elasticsearch-plugins/index.md) or [create](elasticsearch://extend/index.md) a plugin, you can install it by following the steps described on this page that match your deployment type.

::::{admonition} {{serverless-full}}
{{serverless-full}} projects do not support installing plugins or uploading custom plugins and bundles. {{serverless-short}} includes [core analysis plugins](elasticsearch://reference/elasticsearch-plugins/analysis-plugins.md#_core_analysis_plugins) by default. To manage synonyms, use the [synonyms API]({{es-serverless-apis}}group/endpoint-synonyms) or refer to [Search with synonyms](/solutions/search/full-text/search-with-synonyms.md). For differences between {{ech}} and {{serverless-short}} for plugins, bundles, and custom dictionaries, see [Compare {{ech}} and Serverless](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-custom-plugins-and-bundles).
::::


## Manage plugins and bundles by deployment type

How you install and manage plugins, and whether you use bundles or another way to supply equivalent configuration files, depends on your {{es}} [deployment type](/deploy-manage/deploy.md):

* Hosted Cloud deployments such as [{{ech}}](/deploy-manage/plugins-and-bundles/elastic-cloud/add-plugins-extensions.md) and [{{ece}}](/deploy-manage/plugins-and-bundles/cloud-enterprise/add-plugins.md) expose plugin and extension management in the Cloud console and API.
* [Self-managed deployments](/deploy-manage/plugins-and-bundles/self-managed/manage-plugins.md) use a configuration file with the official Docker image, or the `elasticsearch-plugin` CLI for package and archive installs. You add dictionaries and other config files directly on each node's configuration path.
* On [{{eck}}](/deploy-manage/plugins-and-bundles/cloud-on-k8s/manage-plugins.md) deployments, you install plugins by building a custom container image or using init containers, and you add configuration files with ConfigMaps or Secrets.

### Managing plugins for {{ech}} [managing-plugins-for-ech]

```{applies_to}
deployment:
  ess: ga
```

{{ech}} simplifies plugin management by offering compatible plugins for your {{es}} version. These plugins are automatically upgraded with your deployment, except when there are breaking changes.

To add plugins to a hosted deployment, refer to:

* [Add plugins and extensions in {{ech}}](/deploy-manage/plugins-and-bundles/elastic-cloud/add-plugins-extensions.md)
* [Upload custom plugins and bundles](/deploy-manage/plugins-and-bundles/elastic-cloud/upload-custom-plugins-bundles.md)
* [Manage plugins and extensions through the API](/deploy-manage/plugins-and-bundles/elastic-cloud/manage-plugins-extensions-through-api.md)

{{kib}} plugins are not supported on {{ech}}. Refer to [Restrictions and known problems](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins).

### Managing plugins for {{ece}} [managing-plugins-for-ece]

```{applies_to}
deployment:
  ece: ga
```

{{ece}} provides built-in plugins that work with your version of {{es}} and are upgraded along with your deployment, unless there are breaking changes.

To add plugins to an {{ece}} deployment, refer to:

* [Add plugins and bundles in {{ece}}](/deploy-manage/plugins-and-bundles/cloud-enterprise/add-plugins.md)
* [Add custom bundles and plugins](/deploy-manage/plugins-and-bundles/cloud-enterprise/add-custom-bundles-plugins.md)

Unlike {{ech}}, in certain cases, {{ece}} allows additional {{kib}} plugins by building them into a custom {{kib}} Docker image. Refer to [](/deploy-manage/plugins-and-bundles/cloud-enterprise/ece-include-additional-kibana-plugin.md), for more information.

### Managing plugins for self-managed deployments [managing-plugins-for-self-managed]

```{applies_to}
deployment:
  self: ga
```

How you manage plugins depends on how you run {{es}}:

* If you run {{es}} using the [official {{es}} Docker image](https://www.docker.elastic.co/), you manage plugins with a declarative [configuration file](/deploy-manage/plugins-and-bundles/self-managed/manage-plugins-using-configuration-file.md). Each time the container starts, {{es}} installs, removes, or upgrades plugins so the running set matches that file.
* For package and archive installs, use the [`elasticsearch-plugin` command-line tool](/deploy-manage/plugins-and-bundles/self-managed/install-plugins.md) to install, list, and remove plugins on each node.

### Managing plugins for {{eck}} [managing-plugins-for-eck]

```{applies_to}
deployment:
  eck: ga
```

On {{eck}}, {{es}} runs in Kubernetes pods. Plugins must be present on disk before the main {{es}} container starts. Use one of these approaches:

* [Using a custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md). You build a custom image from the official Elastic image with the required plugins pre-installed. This option is reproducible, works without internet access at runtime, and starts quickly, but requires a container registry and a new image for each {{es}} version upgrade.
* [Using init containers](/deploy-manage/plugins-and-bundles/cloud-on-k8s/init-containers-for-plugin-downloads.md). You use an init container to run `elasticsearch-plugin install` before the main {{es}} container starts. This option is easier to get started with, but requires pod internet access and repeats the download on each new node.

::::{note}
You can inject configuration files, such as synonym dictionaries, SAML metadata, or TLS certificates by [mounting them with ConfigMaps or Secrets](/deploy-manage/plugins-and-bundles/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret). However, mounting plugin files into a pod does not run `elasticsearch-plugin install`, so {{es}} will not load them at startup. Instead, to install plugins, use a custom container image or init container.
::::

## Related resources

* [{{es}} plugins reference](elasticsearch://reference/elasticsearch-plugins/index.md): Official plugins and settings.
* [Stack settings](/deploy-manage/stack-settings.md): Configure `elasticsearch.yml`, `kibana.yml`, and related settings by deployment type.
* [Secure settings](/deploy-manage/security/secure-settings.md): Store sensitive values in the {{es}} or {{kib}} keystore.
