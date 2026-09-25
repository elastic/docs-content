---
navigation_title: Set up
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Requirements for using the experimental alerting system in Kibana, including license, connectors, data, and space selection, plus how to turn the system on and off."
---

# Set up the {{alerting-v2-system}} [setup]

This page covers what you need before using the {{alerting-v2-system}}, and how to turn it on and off.

## Before you use the system [alerting-setup-requirements]

You'll need the following to create rules and send notifications.

- **Data in Elasticsearch**: Rules can only detect conditions in data that already exists. Make sure the indices or data streams your rules will query are populated before creating rules. Refer to [Ingest your data](/manage-data/ingest.md) for options.
- **A space selected**: Rules, [action policies](../action-policies/about-action-policies.md), and the privileges that control them are all space-scoped. Decide which space you'll work in before setting things up. Refer to [Manage spaces](/deploy-manage/manage-spaces.md) to create or switch spaces.
- **Connectors configured** (required for notifications): [Workflows](../workflows-alerting.md) send notifications and require at least one [connector](/deploy-manage/manage-connectors.md), for example, Slack, email, or PagerDuty. [Action policies](../action-policies/about-action-policies.md) invoke those workflows.
- **Enterprise license** (Stack deployments only, required for notifications): Workflows-based notifications require an Enterprise license. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

## Turn on the system [alerting-setup-turn-on]

The {{alerting-v2-system}} is controlled by the [`alerting:v2:enabled`](kibana://reference/advanced-settings.md#alerting-v2-enabled) advanced setting in {{kib}}. This is a global setting, so turning it on makes the {{alerting-v2-system}} available in every space, even though the rules and action policies you create in it are space-scoped.

1. Go to the **Advanced Settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Global Settings** tab, then turn on **Alerting V2**.
3. Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md) to confirm the {{alerting-v2-system}} is accessible in your space.

If the menu item doesn't appear immediately, refresh the page and search again. It might take a moment for the UI to reflect the updated setting.

## Turn off the system [alerting-setup-turn-off]

To turn off the {{alerting-v2-system}}, go to the **Advanced Settings** page, select the **Global Settings** tab, and turn off **Alerting V2**.

Turning off the setting does not delete any data. {{kib}} retains your rules and action policies as saved objects, and keeps existing documents in `.rule-events` and `.alert-actions`. Turning the setting back on restores the {{alerting-v2-system}} UI.

:::{important}
Turning off `alerting:v2:enabled` hides the {{alerting-v2-system}} UI but does not stop rules and action policies from running. To stop both entirely:

- **{{stack}}** - Set `xpack.alerting_v2.enabled: false` in [`kibana.yml`](/deploy-manage/deploy/self-managed/configure-kibana.md)
- **{{serverless-short}}** - On {{serverless-short}}, the {{alerting-v2-system}} is managed by Elastic. [Contact Elastic support](https://www.elastic.co/docs/troubleshoot) to turn it off.
:::

## Next steps [alerting-setup-next-steps]

After turning on the system:

- [Configure access](configure-access.md) to create or update a role with access to the {{alerting-v2-system}} features and the data streams they write to.
- [Create your first rule](create-your-first-rule.md) to load sample data, write a detection query, and observe the alert lifecycle.
