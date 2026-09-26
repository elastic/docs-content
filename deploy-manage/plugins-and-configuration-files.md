---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management.html
description: Install Elasticsearch plugins and supply configuration files to your nodes, using the approach that matches your deployment type.
applies_to:
  stack: ga
  serverless: unavailable
navigation_title: Plugins and configuration files
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Plugins and configuration files

Use plugins and configuration files to extend {{es}}'s core functionality with additional analyzers, discovery providers, ingest processors, field types, scripting languages, dictionaries, and other configuration files.

There are two ways to extend a standard {{es}} installation: plugins, which add code to {{es}} itself, and configuration files, which {{es}} reads at runtime. {{es}} loads both from each node's local filesystem rather than through an API, so they must be in place on every node that needs them.

**[Plugins](elasticsearch://reference/elasticsearch-plugins/index.md)** are packages installed in {{es}}. Use them to add capabilities such as language and phonetic analysis, ingest processors for attachments or geo-IP data, additional field types, cloud discovery providers, or scripting languages. Official core plugins are maintained with {{es}} and share its version number. Community and custom plugins are maintained separately and can cover the same kinds of extensions when a core plugin is not available. You can also [build your own](elasticsearch://extend/index.md) when you need something purpose-built.

**Configuration files** are files that {{es}} reads at runtime, such as synonym dictionaries, SAML metadata, GeoIP databases, or certificates. What these are called depends on where you run {{es}}: on {{ech}} and {{ece}} you package them as ZIP archives called *bundles*, on {{eck}} you mount them from ConfigMaps or Secrets, and in self-managed clusters you place them in each node's configuration directory.

::::{admonition} {{serverless-full}}
{{serverless-full}} projects do not support installing plugins or uploading custom plugins and bundles. {{serverless-short}} includes [core analysis plugins](elasticsearch://reference/elasticsearch-plugins/analysis-plugins.md#_core_analysis_plugins) by default. To manage synonyms, use the [synonyms API]({{es-serverless-apis}}group/endpoint-synonyms) or refer to [Search with synonyms](/solutions/search/full-text/search-with-synonyms.md). For differences between {{ech}} and {{serverless-short}} for plugins, bundles, and custom dictionaries, see [Compare {{ech}} and Serverless](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-custom-plugins-and-bundles).
::::


## Manage plugins and configuration files by deployment type [plugins-by-deployment-type]

How you install plugins, and how you supply configuration files such as synonym dictionaries or SAML metadata, depends on your {{es}} [deployment type](/deploy-manage/deploy.md).

| Deployment type | {{es}} plugins | Configuration files |
| --- | --- | --- |
| **{{ech}}** | [Enable a provided plugin](/deploy-manage/plugins-and-configuration-files/elastic-cloud/add-plugins-provided-with-ech.md) or [upload your own](/deploy-manage/plugins-and-configuration-files/elastic-cloud/upload-custom-plugins-bundles.md), from the console or [through the API](/deploy-manage/plugins-and-configuration-files/elastic-cloud/manage-plugins-extensions-through-api.md) | [Upload as a custom bundle](/deploy-manage/plugins-and-configuration-files/elastic-cloud/upload-custom-plugins-bundles.md) |
| **{{ece}}** | [Enable a provided plugin](/deploy-manage/plugins-and-configuration-files/cloud-enterprise/add-plugins-provided-with-ece.md) or [add your own](/deploy-manage/plugins-and-configuration-files/cloud-enterprise/add-custom-bundles-plugins.md) from a ZIP URL | [Add as a custom bundle](/deploy-manage/plugins-and-configuration-files/cloud-enterprise/add-custom-bundles-plugins.md) |
| **Self-managed** | [Use the `elasticsearch-plugin` CLI](/deploy-manage/plugins-and-configuration-files/self-managed/manage-plugins.md#self-managed-plugins-cli), or a [declarative configuration file](/deploy-manage/plugins-and-configuration-files/self-managed/manage-plugins.md#self-managed-plugins-docker) with the Docker image | Place them in each node's [configuration directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) |
| **{{eck}}** | [Build a custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md), or [install them with init containers](/deploy-manage/plugins-and-configuration-files/cloud-on-k8s/init-containers-for-plugin-downloads.md) | [Mount them with ConfigMaps or Secrets](/deploy-manage/plugins-and-configuration-files/cloud-on-k8s/custom-configuration-files-plugins.md) |

On {{ech}} and {{ece}}, provided plugins are upgraded with your deployment automatically, unless there are breaking changes. On {{eck}}, plugins must be present on disk before the main {{es}} container starts, which is why both options run before startup rather than installing into a running node.

{{kib}} plugins work differently: {{ech}} [does not support them](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins), while {{ece}} and {{eck}} require you to build a custom {{kib}} image, for [{{ece}}](/deploy-manage/plugins-and-configuration-files/cloud-enterprise/ece-include-additional-kibana-plugin.md) and for [{{eck}}](/deploy-manage/plugins-and-configuration-files/cloud-on-k8s/k8s-kibana-plugins.md) respectively.

## Related resources

* [{{es}} plugins reference](elasticsearch://reference/elasticsearch-plugins/index.md): Official plugins and settings.
* [Stack settings](/deploy-manage/stack-settings.md): Configure `elasticsearch.yml`, `kibana.yml`, and related settings by deployment type.
* [Secure settings](/deploy-manage/security/secure-settings.md): Store sensitive values in the {{es}} or {{kib}} keystore.
