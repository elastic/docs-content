---
navigation_title: In ECE
description: Extend Elasticsearch on Elastic Cloud Enterprise with built-in plugins, custom bundles, or additional Kibana plugins.
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
  - id: elasticsearch
---

# Add plugins and bundles in {{ece}}

On {{ece}}, you extend {{es}} with plugins that the platform provides, custom plugin or configuration bundles, and in certain cases, additional {{kib}} plugins.


For an overview of plugins and configuration files, and the options that apply to other deployment types, refer to [](/deploy-manage/plugins-and-configuration-files.md).

## Add {{es}} plugins

You can add plugins to a deployment in one of two ways, depending on whether {{ece}} provides the plugin or you supply it yourself:

* [Provided with {{ece}}](add-plugins-provided-with-ece.md): {{ece}} hosts compatible [official {{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md) for your {{es}} version and upgrades them with your deployment, unless there are breaking changes. You enable the plugins per deployment.

* [Custom bundles and plugins](add-custom-bundles-plugins.md): When you need a plugin that is not built into {{ece}}, or shared configuration files such as synonym dictionaries or SAML metadata, you reference a ZIP bundle from an HTTP or HTTPS URL. You can also [create](elasticsearch://extend/index.md) your own plugins.

## Add configuration bundles

On {{ece}}, you reference a bundle ZIP from an HTTP or HTTPS URL rather than uploading the file. To prepare and attach a bundle, refer to [Add custom bundles and plugins](add-custom-bundles-plugins.md).

## Include additional {{kib}} plugins

Unlike {{ech}}, {{ece}} supports additional {{kib}} plugins in certain cases by including them in a custom {{kib}} Docker image and updating your stack pack. Refer to [Include additional {{kib}} plugins](ece-include-additional-kibana-plugin.md).
