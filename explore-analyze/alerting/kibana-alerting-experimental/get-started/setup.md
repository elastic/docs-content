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

- **Data in Elasticsearch**: Rules can only detect conditions in data that already exists. Make sure the indices or data streams your rules will query are populated before creating rules.
- **A space selected**: Rules, action policies, and the privileges that control them are all space-scoped. Decide which space you'll work in before setting things up.
- **Connectors configured** (required for notifications): Action policies send notifications through workflows, which require at least one [connector](/deploy-manage/manage-connectors.md), for example, Slack, email, or PagerDuty.
- **Enterprise license** (Stack deployments only, required for notifications): Workflows-based notifications require an Enterprise license. Rules and alert episodes work on any tier. {{serverless-short}} has no license restriction.

## Turn on the system [alerting-setup-turn-on]

The {{alerting-v2-system}} is controlled by the `alerting:v2:enabled` advanced setting in {{kib}}. This setting is off by default. Turn it on to make the UIs for {{alerting-v2-system}} features available in your space.

::::{tab-set}
:::{tab-item} {{stack}}
:sync: stack

**Requirement:** `kibana_admin` role or equivalent {{stack-manage-app}} access.

1. Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Global settings**, toggle on **alerting:v2:enabled**.
:::

:::{tab-item} {{serverless-short}}
:sync: serverless

**Requirement:** `admin` project role.

{{serverless-short}} has no Global Advanced Settings UI. Use Dev Tools to call the global settings API:

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

To turn off the {{alerting-v2-system}}, set `alerting:v2:enabled` to `false`:

- **{{stack}}:** Go to the same **Advanced Settings** page and toggle off **alerting:v2:enabled**.
- **{{serverless-short}}:** Call the global settings API with `"alerting:v2:enabled": false`.

When the setting is off:

- Rule and action policy execution stops.
- The APIs and UI are hidden.
- Existing rules and action policies are paused.

Turning the setting back on resumes execution. Turning it off does not delete any data. Your rules and action policies remain as {{kib}} saved objects, and existing documents in `.rule-events` and `.alert-actions` are preserved.

## Next steps

After turning on the system, configure role access so your team can use it:

- **[Configure access](configure-access.md):** Create or update a role with access to the {{alerting-v2-system}} features and the data streams they write to. Users need at minimum **Rules: All** to create rules. Granting **Alerts: Read** gives a role Kibana triage access and automatic Elasticsearch `read` access to `.rule-events` and `.alert-actions`, with no separate index privilege needed.