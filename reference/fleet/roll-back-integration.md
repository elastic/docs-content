---
navigation_title: Roll back an integration
description: Roll back an Elastic Agent integration to the previously installed version, restoring the integration policies and configurations of the previous version.
applies_to:
  stack: ga 9.3
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Roll back an {{agent}} integration

::::{note}
This feature is available only for certain subscription levels. For more information, refer to [Elastic subscriptions]({{subscriptions}}).
::::

If you encounter issues after upgrading an integration, you can roll back the integration to the version installed before the upgrade. During the rollback action, the integration package and all associated integration policies and their configurations are automatically restored to the previously installed version.

Consider rolling back an integration if:

- The upgraded integration introduces breaking changes that affect your data collection.
- The new version causes unexpected behavior or errors in your environment.
- You need to revert to a previous version for compatibility reasons.

:::{note}
By default, the rollback action is available for 7 days following the integration upgrade. After the rollback window expires, you can no longer roll back the integration to the previously installed version.

You can [configure the rollback time-to-live (TTL)](#configure-rollback-ttl) in {{ech}} or self-managed deployments.
:::

## Requirements

To successfully roll back an integration, you must have access to all of its integration policies across **all spaces**. If you don't have access to the related spaces, the rollback action will be disabled.

## Roll back an integration

1. In {{kib}}, go to the **Integrations** page and open the **Installed integrations** tab.
2. Search for and select the integration you want to roll back to the previously installed version.
3. Click the **Settings** tab.
4. Click **Rollback <integration>**.

   If the button is disabled for an integration, this may be because:
   - The 7-day rollback window has expired.
   - You don't have access to all integration policies across all spaces.
   - No previous version is available to roll back to.
   - The integration was never upgraded.

5. In the confirmation window, click **Rollback integration** to confirm the action. A confirmation appears if the rollback is successful.

You can also roll back an integration from the **Installed integrations** tab of the **Integrations** page:

1. Search for the integration you want to roll back, then click the actions button at the end of its row.
2. Click **Rollback integration**, then confirm the action.

After the rollback of the integration is complete, the associated integration policies, their configurations and related assets are restored to the integration's previous version.

:::{note}
The automatic upgrade of rolled back integrations is disabled until the integrations are manually upgraded.
:::

## Configure the rollback TTL [configure-rollback-ttl]

The default duration of the rollback window is 7 days. To configure the rollback TTL duration, add the `xpack.fleet.integrationRollbackTTL` setting in the user settings of your {{ech}} deployment or in the `kibana.yml` configuration file of your self-managed deployment.

For example, to extend the rollback window to 14 days, set:

```yml
xpack.fleet.integrationRollbackTTL: 14d
```

For more information, refer to [{{fleet}} settings in {{kib}}](kibana://reference/configuration-reference/fleet-settings.md).