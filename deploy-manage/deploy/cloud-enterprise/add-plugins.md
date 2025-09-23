---
navigation_title: Add plugins and extensions
applies_to:
  deployment:
    ece:
---

# Add plugins and extensions in {{ece}} [ece-adding-plugins]

Plugins extend the core functionality of {{es}}. {{ece}} makes it easy to add plugins to your deployment by providing a number of plugins that work with your version of {{es}}. One advantage of these plugins is that you generally don’t have to worry about upgrading plugins when upgrading to a new {{es}} version, unless there are breaking changes. The plugins are upgraded along with the rest of your deployment.

::::{note}
This page refers to {{es}} plugins that come built-in with the {{ece}} platform. For details on adding other plugins, refer to [](./add-custom-bundles-plugins.md).
::::

Adding plugins to a deployment is as simple as selecting it from the list of available plugins, but different versions of {{es}} support different plugins. Plugins are available for different purposes, such as:

* National language support, phonetic analysis, and extended unicode support
* Ingesting attachments in common formats and ingesting information about the geographic location of IP addresses
* Adding new field datatypes to {{es}}

Additional plugins might be available. If a plugin is listed for your version of {{es}}, it can be used.

You can also [create](elasticsearch://extend/index.md) and add custom plugins.

To add plugins when creating a new deployment:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md) and select **Create deployment**.
2. Make your initial deployment selections, then select **Advanced settings**.
3. Beneath the {{es}} master node, expand the **Manage plugins and settings** caret.
4. Select the plugins you want.
5. Select **Create deployment**.

The deployment spins up with the plugins installed.

To add plugins to an existing deployment:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. Beneath the {{es}} master node, expand the **Manage plugins and settings** caret.
5. Select the plugins that you want.
6. Select **Save changes**.

There is no downtime when adding plugins to highly available deployments. The deployment is updated with new nodes that have the plugins installed.