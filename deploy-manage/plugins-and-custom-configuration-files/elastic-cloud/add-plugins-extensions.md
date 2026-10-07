---
navigation_title: In ECH
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

# Add plugins and bundles in {{ech}} [ec-adding-plugins]

On {{ech}}, you extend the core functionality of {{es}} in two ways: you enable one of the plugins that {{ecloud}} provides, or you supply the file yourself. Anything you supply yourself is called an *extension* in the {{ecloud}} console and API, and comes in two forms: a custom *plugin*, which adds code to {{es}}, or a *bundle*, which packages custom configuration files that {{es}} reads at runtime, such as synonym dictionaries, SAML metadata, or certificates.

Refer to [](/deploy-manage/plugins-and-custom-configuration-files.md) for options that apply to other deployment types.

## Add plugins

You can add {{es}} plugins to a deployment in one of two ways, depending on whether Elastic Cloud provides the plugin or you supply it yourself:

* [Provided with {{ech}}](add-plugins-provided-with-ech.md): {{ecloud}} hosts compatible official plugins for your {{es}} version and upgrades them with your deployment, except when there are breaking changes. You enable the plugins per deployment. To learn about official and community plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).

* [Custom plugins](upload-custom-plugins-bundles.md): When you need a community or third-party plugin, an official plugin that is not provided with {{ech}}, or [one you write yourself](elasticsearch://extend/index.md), you upload it as an extension. Uploading custom plugins requires a Gold, Platinum, or Enterprise subscription.

Plugins are not supported for {{kib}} in {{ech}} deployments. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins).

## Add configuration bundles

Bundles use the same extensions workflow as custom plugins: you upload a ZIP file, choose the bundle type, and then enable the extension on your deployment. The difference happens at runtime, when plugins are installed into {{es}} and bundles are extracted as files on disk.

For example, you can upload an Identity Provider metadata file used when you [secure your clusters with SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md).

Unlike custom plugins, bundles can be uploaded on all subscription levels, including Standard. To prepare, upload, and enable a bundle, refer to [Upload custom plugins and bundles](upload-custom-plugins-bundles.md).

## Manage through the API

To create, update, enable, or delete extensions programmatically, refer to [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md).
