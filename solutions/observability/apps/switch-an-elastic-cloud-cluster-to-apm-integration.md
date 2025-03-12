---
navigation_title: "Switch an {{ecloud}} cluster"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-integration-upgrade-steps-ess.html
---



# Switch an Elastic Cloud cluster to the APM integration [apm-integration-upgrade-steps-ess]


1. [Upgrade the {{stack}}](#apm-integration-upgrade-ess-1)
2. [Switch to {{agent}}](#apm-integration-upgrade-ess-2)
3. [Configure the APM integration](#apm-integration-upgrade-ess-3)
4. [Scale APM and {{fleet}}](#apm-integration-upgrade-ess-4)


## Upgrade the {{stack}} [apm-integration-upgrade-ess-1]

Use the {{ecloud}} Console to upgrade the {{stack}} to version 9.0.0-beta1. See the [Upgrade guide](../../../deploy-manage/upgrade/deployment-or-cluster.md) for details.


## Switch to {{agent}} [apm-integration-upgrade-ess-2]

APM data collection will be interrupted while the migration is in progress. The process of migrating should only take a few minutes.

With a Superuser account, complete the following steps:

1. In {{kib}}, go to the **Applications** app and click **Settings** → **Schema**.

    :::{image} ../../../images/observability-schema-agent.png
    :alt: switch to {{agent}}
    :::

2. Click **Switch to {{agent}}**. Make a note of the `apm-server.yml` user settings that are incompatible with {{agent}}. Check the confirmation box and click **Switch to {{agent}}**.

    :::{image} ../../../images/observability-agent-settings-migration.png
    :alt: {{agent}} settings migration
    :::


{{ecloud}} will now create a {{fleet}} Server instance to contain the new APM integration, and then will shut down the old APM server instance. Within minutes your data should begin appearing in the Applications UI again.


## Configure the APM integration [apm-integration-upgrade-ess-3]

You can now update settings that were removed during the upgrade. See [Configure APM Server](configure-apm-server.md) for a reference of all available settings.

In {{kib}}, navigate to **Management** > **Fleet**. Select the **Elastic Cloud Agent Policy**. Next to the **Elastic APM** integration, select **Actions** > **Edit integration**.


## Scale APM and {{fleet}} [apm-integration-upgrade-ess-4]

Certain {{es}} output configuration options are not available with the APM integration. To ensure data is not lost, you can scale APM and {{fleet}} up and out. APM’s capacity to process events increases with the instance memory size.

Go to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), select your deployment and click **Edit**. Here you can edit the number and size of each availability zone.

:::{image} ../../../images/observability-scale-apm.png
:alt: scale APM
:::

Congratulations -- you now have the latest and greatest in Elastic APM!
