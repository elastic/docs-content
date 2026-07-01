---
navigation_title: Add plugins and extensions
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-adding-plugins.html
  - https://www.elastic.co/guide/en/cloud/current/ec-adding-plugins.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Add plugins and extensions in {{ech}} [ec-adding-plugins]

On {{ech}}, you extend the core functionality of {{es}} with plugins or bundles. In the {{ecloud}} console and API, both are referred to as extensions.

## Plugins

Plugins are software packages that you install in {{es}} to extend its core functionality to include additional analyzers, discovery providers, or ingest processors. Availability depends on your {{es}} version. Common categories include:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

You can add plugins to a deployment in one of two ways, depending on whether Elastic Cloud provides the plugin or you supply it yourself:

* [Provided with {{ech}}](add-plugins-provided-with-ech.md): {{ecloud}} hosts compatible official plugins for your {{es}} version and upgrades them with your deployment, except when there are breaking changes. You enable the plugins per deployment. To learn about official and community plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).

* [Custom plugins](upload-custom-plugins-bundles.md): When you need to install an official plugin not included with {{ech}}, such as a community-sourced plugin, or [one you write yourself](elasticsearch://extend/index.md), you upload a custom plugin. Uploading custom plugins requires a Gold, Platinum, or Enterprise subscription.

Plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](restrictions-known-problems.md#ec-restrictions-plugins).

## Bundles

Bundles are ZIP files of configuration and data files. They are not installed as plugins. Instead, when a node starts, {{ecloud}} extracts the bundle contents into each node's `/app/config` configuration directory.

Use a bundle when every node needs the same files, such as:

* Synonym, stop-word, or compound-word dictionaries
* Scripts referenced in queries
* Cluster configuration files, such as SAML metadata

Bundles use the same extensions workflow as custom plugins where you upload a ZIP file, choose the bundle type, and then enable the extension on your deployment. The difference happens at runtime: plugins are installed into {{es}} while bundles are extracted as files on disk.

All subscription levels, including Standard, can upload scripts and dictionaries. To prepare, upload, and enable a bundle, refer to [Upload custom plugins and bundles](upload-custom-plugins-bundles.md).

## Manage through the API

To create, update, enable, or delete extensions programmatically, refer to [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).
