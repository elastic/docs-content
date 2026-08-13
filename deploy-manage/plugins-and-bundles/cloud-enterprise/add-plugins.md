---
navigation_title: Extend {{ece}}
description: Extend Elasticsearch on Elastic Cloud Enterprise with built-in plugins, custom bundles, or additional Kibana plugins.
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
  - id: elasticsearch
---

# Add plugins and extensions in {{ece}}

On {{ece}}, you extend {{es}} with plugins that the platform provides, custom plugin or configuration bundles, and—in certain cases—additional {{kib}} plugins.

Refer to [Plugins and bundles](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.

## Plugins

Plugins are software packages that you install in {{es}} to extend its core functionality, for example with additional analyzers, ingest processors, or field types. Availability depends on your {{es}} version. Common purposes include:

* National language support, phonetic analysis, and extended unicode support
* Ingesting attachments in common formats and ingesting information about the geographic location of IP addresses
* Adding new field datatypes to {{es}}

You can add plugins to a deployment in one of two ways, depending on whether {{ece}} provides the plugin or you supply it yourself:

* [Provided with {{ece}}](add-plugins-provided-with-ece.md): {{ece}} hosts compatible plugins for your {{es}} version and upgrades them with your deployment, except when there are breaking changes. You enable the plugins per deployment.

* [Custom bundles and plugins](add-custom-bundles-plugins.md): When you need a plugin that is not built into {{ece}}, or shared configuration files such as synonym dictionaries or SAML metadata, you reference a ZIP bundle from an HTTP or HTTPS URL. You can also [create](elasticsearch://extend/index.md) your own plugins.

## Bundles

Bundles are ZIP files of configuration and data files. They are not installed as plugins. Instead, when a node starts, {{ece}} makes the bundle contents available in the node's configuration directory.

Use a bundle when every node needs the same files, such as:

* Synonym, stop-word, or compound-word dictionaries
* Scripts referenced in queries
* Cluster configuration files, such as SAML metadata

To prepare and attach a bundle, refer to [Add custom bundles and plugins](add-custom-bundles-plugins.md).

## Additional {{kib}} plugins

Unlike {{ech}}, {{ece}} supports additional {{kib}} plugins in certain cases by including them in a custom {{kib}} Docker image and updating your stack pack. Refer to [Include additional {{kib}} plugins](ece-include-additional-kibana-plugin.md).
