---
navigation_title: "Self-installation APM integration"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-self-integration.html
---



# Upgrade a self-installation of the APM integration to 8.x [apm-upgrade-8.0-self-integration]


This upgrade guide is for the Elastic APM integration. Only use this guide if both of the following are true:

* You have a self-installation of the {{stack}}, i.e. you’re not using {{ecloud}}.
* You have already switched to and are running {{fleet}} and the Elastic APM integration.


## Prerequisites [_prerequisites_9]

1. Prior to upgrading to version 9.0.0-beta1, {{es}}, and {{kib}} must be upgraded to version 7.17. To upgrade {{es}} and {{kib}}, see the [{{stack}} Installation and Upgrade Guide](https://www.elastic.co/guide/en/elastic-stack/7.17/upgrading-elastic-stack.html)
2. Review the [Elastic APM release notes](/release-notes/elastic-apm/release-notes.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/release-notes.md).


## Upgrade steps [_upgrade_steps_2]

1. Upgrade the {{stack}} to version 9.0.0-beta1.

    The {{stack}} ({{es}} and {{kib}}) must be upgraded before {{agent}}. See the [{{stack}} Installation and Upgrade Guide](../../../deploy-manage/upgrade/deployment-or-cluster.md) for guidance.

2. Upgrade {{agent}} to version 9.0.0-beta1. As a part of this process, the APM integration will automatically upgrade to version 9.0.0-beta1.

    1. In {{fleet}}, select **Agents**.
    2. Under **Agents**, click **Upgrade available** to see a list of agents that you can upgrade.
    3. Choose **Upgrade agent** from the **Actions** menu next to the agent you want to upgrade. The **Upgrade agent** option is grayed out when an upgrade is unavailable, or the {{kib}} version is lower than the agent version.

    For more details, or for bulk upgrade instructions, see [Upgrade {{agent}}](/reference/ingestion-tools/fleet/upgrade-elastic-agent.md)
