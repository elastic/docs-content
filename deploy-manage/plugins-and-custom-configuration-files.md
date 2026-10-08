---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management.html
description: Install Elasticsearch plugins and supply custom configuration files to your nodes, using the approach that matches your deployment type.
applies_to:
  stack: ga
  serverless: unavailable
navigation_title: Plugins and custom configuration files
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Plugins and custom configuration files

Use plugins and custom configuration files to extend {{es}}'s core functionality with additional analyzers, discovery providers, ingest processors, field types, scripting languages, and dictionaries.

There are two ways to extend {{es}}:

* **[Plugins](elasticsearch://reference/elasticsearch-plugins/index.md)** are packages installed in {{es}}. Use them to add capabilities such as language and phonetic analysis, ingest processors for attachments or geo-IP data, additional field types, cloud discovery providers, or scripting languages. Official core plugins are maintained with {{es}} and share its version number. Community and custom plugins are maintained separately and can cover the same kinds of extensions when a core plugin is not available. You can also [build your own](elasticsearch://extend/index.md) if no existing plugin covers what you need.

* **Custom configuration files** are files that you supply and {{es}} reads at runtime, such as synonym dictionaries, SAML metadata, GeoIP databases, or certificates. The way these are installed depends on where you run {{es}}: on {{ech}} and {{ece}} you package them as ZIP archives called *bundles*, on {{eck}} you mount them from ConfigMaps or Secrets, and in self-managed clusters you place them in each node's configuration directory.

To change {{es}} or {{kib}} settings in files such as `elasticsearch.yml` and `kibana.yml`, refer to [](/deploy-manage/stack-settings.md) instead.

::::{admonition} {{serverless-full}} support
This page applies to {{ech}}, {{ece}}, {{eck}}, and Elastic self-managed deployments only. 
{{serverless-full}} projects do not support custom plugin or bundle uploads, including dictionary files used for synonyms, stop words, or [language analyzers](elasticsearch://reference/text-analysis/analysis-lang-analyzer.md). 

If you use {{serverless-short}} and need to manage synonyms, use the [synonyms APIs]({{es-serverless-apis}}group/endpoint-synonyms) or refer to [Search with synonyms](/solutions/search/full-text/search-with-synonyms.md). For how {{ech}} and Serverless differ on plugins, bundles, and dictionary options, see [Compare {{ech}} and Serverless](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-custom-plugins-and-bundles).
::::


## Manage plugins and custom configuration files by deployment type [plugins-by-deployment-type]

How you install plugins, and how you supply custom configuration files such as synonym dictionaries or SAML metadata, depends on your [deployment type](/deploy-manage/deploy.md).

| Deployment type | {{es}} plugins | Custom configuration files |
| --- | --- | --- |
| **{{ech}}** | [Enable a provided plugin](/deploy-manage/plugins-and-custom-configuration-files/elastic-cloud/add-plugins-provided-with-ech.md) or [upload your own](/deploy-manage/plugins-and-custom-configuration-files/elastic-cloud/upload-custom-plugins-bundles.md), from the console or [through the API](/deploy-manage/plugins-and-custom-configuration-files/elastic-cloud/manage-plugins-extensions-through-api.md) | [Upload as a custom bundle](/deploy-manage/plugins-and-custom-configuration-files/elastic-cloud/upload-custom-plugins-bundles.md) |
| **{{ece}}** | [Enable a provided plugin](/deploy-manage/plugins-and-custom-configuration-files/cloud-enterprise/add-plugins-provided-with-ece.md) or [add your own](/deploy-manage/plugins-and-custom-configuration-files/cloud-enterprise/add-custom-bundles-plugins.md) from a ZIP URL | [Add as a custom bundle](/deploy-manage/plugins-and-custom-configuration-files/cloud-enterprise/add-custom-bundles-plugins.md) |
| **Self-managed** | [Use the `elasticsearch-plugin` CLI](/deploy-manage/plugins-and-custom-configuration-files/self-managed/manage-plugins.md#self-managed-plugins-cli), or a [declarative configuration file](/deploy-manage/plugins-and-custom-configuration-files/self-managed/manage-plugins.md#self-managed-plugins-docker) with the Docker image | Place in each node's [configuration directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) |
| **{{eck}}** | [Build a custom container image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md), or [install with init containers](/deploy-manage/plugins-and-custom-configuration-files/cloud-on-k8s/init-containers-for-plugin-downloads.md) | [Mount with ConfigMaps or Secrets](/deploy-manage/plugins-and-custom-configuration-files/cloud-on-k8s/custom-configuration-files-plugins.md) |

On {{ech}} and {{ece}}, plugins provided by the platform are upgraded with your deployment automatically, unless there are breaking changes. When you upgrade, plugins and custom configuration files that you supply must be updated to match the new {{es}} version: update your custom plugins and bundles on {{ech}} and {{ece}}, rebuild your custom image on {{eck}}, and reinstall plugins on each node of a self-managed cluster. Refer to [](/deploy-manage/upgrade/prepare-to-upgrade.md) for the checks to run before you upgrade.

### Add {{kib}} plugins [kibana-plugins]

{{kib}} plugins add features to the {{kib}} UI. How you install them, and whether they are supported, depends on your deployment type:

* **{{ech}}**: {{kib}} plugins [are not supported](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins).
* **{{ece}}**: supported in certain cases, by [including the plugins in a custom {{kib}} image](/deploy-manage/plugins-and-custom-configuration-files/cloud-enterprise/ece-include-additional-kibana-plugin.md) and updating your stack pack.
* **{{eck}}**: [build a custom {{kib}} image](/deploy-manage/plugins-and-custom-configuration-files/cloud-on-k8s/k8s-kibana-plugins.md) that already includes the plugins.
* **Self-managed**: install plugins on each {{kib}} instance with the [`kibana-plugin` CLI](kibana://reference/kibana-plugins.md), then restart {{kib}}.

## Related resources

* [{{es}} plugins reference](elasticsearch://reference/elasticsearch-plugins/index.md): Official plugins and settings.
* [Stack settings](/deploy-manage/stack-settings.md): Configure `elasticsearch.yml`, `kibana.yml`, and related settings by deployment type.
* [Secure settings](/deploy-manage/security/secure-settings.md): Store sensitive values in the {{es}} or {{kib}} keystore.
