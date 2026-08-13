---
navigation_title: Provided with ECH
description: Enable official Elasticsearch plugins that Elastic Cloud Hosted provides and upgrades with your deployment.
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-adding-elastic-plugins.html
  - https://www.elastic.co/guide/en/cloud/current/ec-adding-elastic-plugins.html
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# Add plugins provided with {{ech}} [ec-adding-elastic-plugins]

You can use a variety of [official {{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md) that are compatible with your version of {{es}}. When you upgrade to a new {{es}} version, these plugins are upgraded with the rest of your deployment.

## Before you begin [ec_before_you_begin_6]

Some restrictions apply when adding plugins. For example, plugins are not supported for {{kib}}. To learn more, check [Restrictions for {{es}} and {{kib}} plugins](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-plugins).

## Enable plugins for a deployment

:::{include} /deploy-manage/deploy/elastic-cloud/_snippets/enable-extensions-on-deployment.md
:::
