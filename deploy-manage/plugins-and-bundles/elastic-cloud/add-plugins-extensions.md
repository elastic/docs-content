---
navigation_title: "Extend {{ech}}"
description: Extend Elasticsearch on Elastic Cloud Hosted with provided plugins, custom plugins, or configuration bundles.
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-adding-plugins.html
  - https://www.elastic.co/guide/en/cloud/current/ec-adding-plugins.html
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# Add plugins and extensions in {{ech}} [ec-adding-plugins]

On {{ech}}, you extend the core functionality of {{es}} with plugins or bundles. In the {{ecloud}} console and API, both are referred to as *extensions*.

For options that apply to other deployment types, refer to [](/deploy-manage/plugins-and-bundles.md).

## Add {{es}} plugins

Plugins are software packages that you install in {{es}} to extend its core functionality to include additional analyzers, discovery providers, or ingest processors. Availability depends on your {{es}} version. Common categories include:

* Discovery plugins, such as the cloud AWS plugin that allows discovering nodes on EC2 instances.
* Analysis plugins, to provide analyzers targeted at languages other than English.
* Scripting plugins, to provide additional scripting languages.

You can add plugins to a deployment in one of two ways, depending on whether Elastic Cloud provides the plugin or you supply it yourself:

* [Provided with {{ech}}](add-plugins-provided-with-ech.md): {{ecloud}} hosts compatible official plugins for your {{es}} version and upgrades them with your deployment, except when there are breaking changes. You enable the plugins per deployment. To learn about official and community plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).

* [Custom plugins](upload-custom-plugins-bundles.md): When you need a community or third-party plugin, an official plugin that is not [provided with {{ech}}](add-plugins-provided-with-ech.md), or [one you write yourself](elasticsearch://extend/index.md), you upload a custom plugin. Uploading custom plugins requires a Gold, Platinum, or Enterprise subscription.

Plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins).

## Add configuration bundles

:::{include} /deploy-manage/plugins-and-bundles/_snippets/what-are-bundles.md
:::

For example, you can upload an Identity Provider metadata file used when you [secure your clusters with SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md).

Bundles use the same extensions workflow as custom plugins where you upload a ZIP file, choose the bundle type, and then enable the extension on your deployment. The difference happens at runtime: plugins are installed into {{es}} while bundles are extracted as files on disk.

All subscription levels, including Standard, can upload scripts and dictionaries. To prepare, upload, and enable a bundle, refer to [Upload custom plugins and bundles](upload-custom-plugins-bundles.md).

## Manage through the API

To create, update, enable, or delete extensions programmatically, refer to [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).
