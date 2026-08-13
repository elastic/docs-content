---
navigation_title: Provided with ECE
description: Enable built-in Elasticsearch plugins on Elastic Cloud Enterprise deployments without managing upgrades yourself.
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-plugins.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
  - id: elasticsearch
---

# Add plugins provided with {{ece}} [ece-adding-plugins]

You can use a variety of {{es}} plugins that are compatible with your version of {{es}}. When you upgrade to a new {{es}} version, these plugins are upgraded with the rest of your deployment, unless there are breaking changes.

Different versions of {{es}} support different plugins. If a plugin is listed for your version, you can enable it on the deployment.

## Add plugins when creating a new {{ece}} deployment

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md) and select **Create deployment**.
2. Make your initial deployment selections, then select **Advanced settings**.
3. Beneath the {{es}} master node, expand the **Manage plugins and settings** caret.
4. Select the plugins you want.
5. Select **Create deployment**.

The deployment spins up with the plugins installed.

## Add plugins to an existing {{ece}} deployment

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. Beneath the {{es}} master node, expand the **Manage plugins and settings** caret.
5. Select the plugins that you want.
6. Select **Save changes**.

There is no downtime when adding plugins to highly available deployments. The deployment is updated with new nodes that have the plugins installed.
