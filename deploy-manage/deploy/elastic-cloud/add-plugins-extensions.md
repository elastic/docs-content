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

Plugins extend the core functionality of {{es}}. On {{ech}}, you can add plugins to a deployment in one of two ways, depending on whether {{ecloud}} provides the plugin or you supply it yourself:

* [Add plugins provided with {{ech}}](add-plugins-provided-with-ech.md): {{ecloud}} includes compatible official plugins for your {{es}} version. Enable them per deployment from the **Extensions** list. When you upgrade {{es}}, these plugins are upgraded with the rest of your deployment, except when there are breaking changes.
* [Upload custom plugins and bundles](upload-custom-plugins-bundles.md): Upload a plugin to install software that extends {{es}}, such as an official plugin not provided with {{ecloud}}, a community-sourced plugin, or [one you write yourself](elasticsearch://extend/index.md). Upload a bundle to supply files that every node needs, such as synonym dictionaries, stop-word lists, scripts, or SAML metadata; bundles are extracted to the configuration directory and are not installed as plugins. Uploading custom plugins requires a Gold, Platinum, or Enterprise subscription. All subscription levels, including Standard, can upload scripts and dictionaries.

Plugin availability depends on your {{es}} version.

There are many categories of plugins available, including:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

To learn more about official and community-sourced plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).

For a detailed guide with examples of using the {{ecloud}} API to create, get information about, update, and delete extensions and plugins, check [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).

Plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](restrictions-known-problems.md#ec-restrictions-plugins).