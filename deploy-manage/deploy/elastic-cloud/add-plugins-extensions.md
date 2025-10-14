---
navigation_title: Add plugins and extensions
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-adding-plugins.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-adding-elastic-plugins.html
  - https://www.elastic.co/guide/en/cloud/current/ec-adding-plugins.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Add plugins and extensions in {{ech}} [ec-adding-plugins]

Plugins extend the core functionality of {{es}}. There are many suitable plugins, including:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

Plugins can come from different sources: the official ones created or at least maintained by Elastic, community-sourced plugins from other users, and plugins that you provide. Some of the official plugins are always provided with our service, and can be [enabled per deployment](elasticsearch://reference/elasticsearch-plugins/plugin-management.md).

There are two ways to add plugins to a hosted deployment in {{ecloud}}:

* [Enable one of the official plugins already available in {{ecloud}}](elasticsearch://reference/elasticsearch-plugins/plugin-management.md).
* [Upload a custom plugin and then enable it per deployment](upload-custom-plugins-bundles.md).

Custom plugins can include the official {{es}} plugins not provided with {{ecloud}}, any of the community-sourced plugins, or [plugins that you write yourself](elasticsearch://extend/index.md). Uploading custom plugins is available only to Gold, Platinum, and Enterprise subscriptions. For more information, check [Upload custom plugins and bundles](upload-custom-plugins-bundles.md).

To learn more about the official and community-sourced plugins, refer to [{{es}} Plugins and Integrations](elasticsearch://reference/elasticsearch-plugins/index.md).

For a detailed guide with examples of using the {{ecloud}} API to create, get information about, update, and delete extensions and plugins, check [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).

Plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](restrictions-known-problems.md#ec-restrictions-plugins).




