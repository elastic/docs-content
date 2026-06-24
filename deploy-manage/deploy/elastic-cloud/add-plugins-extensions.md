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

Plugins extend the core functionality of {{es}}. {{ech}} simplifies plugin management by offering compatible plugins for your {{es}} version. These plugins are automatically upgraded with your deployment, except when there are breaking changes.

In {{ech}} deployments, you can add plugins by selecting them from the available list. Plugin availability depends on your {{es}} version.

There are many suitable plugins, including:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

Plugins can come from different sources: official ones created or maintained by Elastic, community-sourced plugins from other users, and plugins that you provide. Some of the official plugins are always provided with our service, and can be [enabled per deployment](#ec-adding-elastic-plugins).

To add plugins to a hosted deployment in {{ecloud}}, you can:

* [Enable one of the official plugins already available in {{ecloud}}](#ec-adding-elastic-plugins). To learn more about the official and community-sourced plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).
* [Upload a custom plugin and then enable it per deployment](upload-custom-plugins-bundles.md). Custom plugins can include the official {{es}} plugins not provided with {{ecloud}}, any of the community-sourced plugins, or [plugins that you write yourself](elasticsearch://extend/index.md).


For a detailed guide with examples of using the {{ecloud}} API to create, get information about, update, and delete extensions and plugins, check [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).

## Add plugins provided with {{ech}} [ec-adding-elastic-plugins]

You can use a variety of official plugins that are compatible with your version of {{es}}. When you upgrade to a new {{es}} version, these plugins are upgraded with the rest of your deployment.

### Before you begin [ec_before_you_begin_6]

Some restrictions apply when adding plugins. For example, plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](restrictions-known-problems.md#ec-restrictions-plugins).

Only Gold, Platinum, Enterprise, and Private subscriptions have access to uploading custom plugins. All subscription levels, including Standard, can upload scripts and dictionaries.

### Enable plugins for a deployment

:::{include} _snippets/enable-extensions-on-deployment.md
:::

