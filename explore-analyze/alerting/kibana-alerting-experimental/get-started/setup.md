---
navigation_title: Set up
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "What you need before using the experimental alerting system in Kibana: license requirements, connectors, data, and space selection. Also covers how to turn the system on and off using the alerting:v2:enabled advanced setting."
---

# Set up the {{alerting-v2-system}} [alerting-setup]

This page covers what you need before using the {{alerting-v2-system}}, and how to turn it on and off in your space.

## Requirements [alerting-setup-requirements]

- **Data in Elasticsearch**: Rules can only detect conditions in data that already exists. Make sure the indices or data streams your rules will query are populated before creating rules. Refer to [Ingest your data](/manage-data/ingest.md) for options.
- **A space selected**: Rules, action policies, and the privileges that control them are all space-scoped. Decide which space you'll work in before setting things up. Refer to [Manage spaces](/deploy-manage/manage-spaces.md) to create or switch spaces.
- **Connectors configured** (required for notifications): Action policies send notifications through workflows, which require at least one [connector](/deploy-manage/manage-connectors.md), for example, Slack, email, or PagerDuty.
- **Enterprise license** (Stack deployments only, required for notifications): Workflows-based notifications require an Enterprise license. Rules and alert episodes work on any tier. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers. {applies_to}`stack: ga 9.5+`

## Turn on the system [alerting-setup-turn-on]

The {{alerting-v2-system}} is controlled by the `alerting:v2:enabled` advanced setting in {{kib}}. This setting is off by default. Turn it on to make the UIs for {{alerting-v2-system}} features available in your space.

::::{applies-switch}
:::{applies-item} stack: experimental 9.5+

**Role requirements**

You must have the `kibana_admin` role or equivalent {{stack-manage-app}} access to turn on the `alerting:v2:enabled` advanced setting.

**Steps**

1. Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Global settings**, toggle on **alerting:v2:enabled**.
:::

:::{applies-item} serverless:

**Role requirements**

You must have the `admin` project role to turn on the `alerting:v2:enabled` advanced setting. 

**Step**

{{serverless-short}} has no Global Advanced Settings UI, so use Dev Tools to call the global settings API:

```json
POST kbn:/internal/kibana/global_settings
{
  "changes": {
    "alerting:v2:enabled": true
  }
}
```

:::{note}
The `/internal/kibana/global_settings` endpoint is an internal API and might change without notice. There is currently no public equivalent.
:::
:::
::::

### Confirm the UI is accessible [alerting-setup-confirm]

After turning on the setting, verify the {{alerting-v2-system}} is accessible in your space:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and enter `Alerting v2 preview`.
2. Select the menu item from the results.

If the menu item doesn't appear immediately, refresh the page and search again. It might take a moment for the UI to reflect the updated setting.

## Turn off the system [alerting-setup-turn-off]

To turn off the {{alerting-v2-system}}, set `alerting:v2:enabled` to `false`.

::::{applies-switch}
:::{applies-item} stack: experimental 9.5+

Go to the **Advanced Settings** page and toggle off **alerting:v2:enabled**.
:::

:::{applies-item} serverless:

Use Dev Tools to call the global settings API:

```json
POST kbn:/internal/kibana/global_settings
{
  "changes": {
    "alerting:v2:enabled": false
  }
}
```
:::
::::

Turning off the setting does not delete any data. {{kib}} retains your rules and action policies as saved objects, and keeps existing documents in `.rule-events` and `.alert-actions`. Turning the setting back on restores the {{alerting-v2-system}} UI.

:::{important}
Turning off `alerting:v2:enabled` hides the {{alerting-v2-system}} UI but does not stop rules and action policies from running. To stop both entirely:

- **{{stack}}** - Set `xpack.alerting_v2.enabled: false` in [`kibana.yml`](/deploy-manage/deploy/self-managed/configure-kibana.md)
- **{{serverless-short}}** - On {{serverless-short}}, the {{alerting-v2-system}} is managed by Elastic. [Contact Elastic support](https://www.elastic.co/docs/troubleshoot) to turn it off.
:::

## Next steps

After turning on the system, [configure access](configure-access.md) to create or update a role with access to the {{alerting-v2-system}} features and the data streams they write to.