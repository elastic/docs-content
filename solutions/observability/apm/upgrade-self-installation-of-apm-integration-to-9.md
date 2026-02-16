---
navigation_title: Self-installation APM integration
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-self-integration.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Upgrade a self-installation of the APM integration to 9.0 [apm-upgrade-9.0-self-integration]

This upgrade guide is for the Elastic APM integration. Only use this guide if both of the following are true:

* You have a self-installation of the {{stack}}, i.e. you’re not using {{ecloud}}.
* You have already switched to and are running {{fleet}} and the Elastic APM integration.

## Prerequisites [_prerequisites_9]

1. Before you upgrade to version 9.0, you must upgrade {{es}} and {{kib}} to the latest patch version of 8.18. For more details, refer to the [{{stack}} Installation and Upgrade Guide](https://www.elastic.co/guide/en/elastic-stack/8.18/upgrading-elastic-stack.html).
2. Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md).
3. Review the [Elastic APM breaking changes](apm-server://release-notes/breaking-changes.md).

## Upgrade steps [_upgrade_steps_2]

1. Upgrade the {{stack}} to version 9.0.

    The {{stack}} ({{es}} and {{kib}}) must be upgraded before {{agent}}. refer to the [{{stack}} Installation and Upgrade Guide](/deploy-manage/upgrade/deployment-or-cluster.md) for guidance.

2. Upgrade {{agent}} to version 9.0 As a part of this process, the APM integration will automatically upgrade to version 9.0.

    1. In {{fleet}}, select **Agents**.
    2. Under **Agents**, click **Upgrade available** for a list of agents that you can upgrade.
    3. Choose **Upgrade agent** from the **Actions** menu next to the agent you want to upgrade. The **Upgrade agent** option is grayed out when an upgrade is unavailable, or the {{kib}} version is lower than the agent version.

    For more details, or for bulk upgrade instructions, refer to [Upgrade {{agent}}](/reference/fleet/upgrade-elastic-agent.md)

3. When upgrading from 8.18 to 9.0, if you have 7.x indices, you need to either set the indices to `readonly`, or if reindexing, add [ILM privileges](https://www.elastic.co/guide/en/apm/guide/7.17/privileges-to-setup-beats.html#_set_up_ilm) for `reindexed-v*-apm*` indices.