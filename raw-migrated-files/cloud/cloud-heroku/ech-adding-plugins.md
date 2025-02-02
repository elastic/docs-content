# Add plugins and extensions [ech-adding-plugins]

Plugins extend the core functionality of {{es}}. There are many suitable plugins, including:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

Plugins can come from different sources: the official ones created or at least maintained by Elastic, community-sourced plugins from other users, and plugins that you provide. Some of the official plugins are always provided with our service, and can be [enabled per deployment](../../../deploy-manage/deploy/elastic-cloud/add-plugins-provided-with-elastic-cloud-hosted.md).

There are two ways to add plugins to a deployment in Elasticsearch Add-On for Heroku:

* [Enable one of the official plugins already available in Elasticsearch Add-On for Heroku](../../../deploy-manage/deploy/elastic-cloud/add-plugins-provided-with-elastic-cloud-hosted.md).
* [Upload a custom plugin and then enable it per deployment](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).

Custom plugins can include the official {{es}} plugins not provided with Elasticsearch Add-On for Heroku, any of the community-sourced plugins, or [plugins that you write yourself](https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-authors.html). Uploading custom plugins is available only to Gold, Platinum, and Enterprise subscriptions. For more information, check [Upload custom plugins and bundles](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).

To learn more about the official and community-sourced plugins, refer to [{{es}} Plugins and Integrations](https://www.elastic.co/guide/en/elasticsearch/plugins/current/index.html).

Plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](../../../deploy-manage/deploy/elastic-cloud/ech-restrictions.md#ech-restrictions-plugins).



