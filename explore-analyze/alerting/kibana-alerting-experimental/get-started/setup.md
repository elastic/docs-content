---
navigation_title: Set up
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Enable and disable the experimental alerting system in Kibana: turn on the alerting:v2:enabled advanced setting, confirm the system is accessible, and understand what happens when the setting is turned off."
---

# Set up the {{alerting-v2-system}} [alerting-setup]

This page explains how to enable the {{alerting-v2-system}} in your space, confirm it's accessible, and turn it off when needed. Enabling and turning off the system requires a {{kib}} administrator. Confirming accessibility can be done by any user with space access.

## Turn on the system [alerting-setup-turn-on]

The {{alerting-v2-system}} is controlled by the `alerting:v2:enabled` advanced setting in {{kib}}. This setting is off by default. Turn it on to make the UIs for {{alerting-v2-system}} features available in your space.

::::{tab-set}
:::{tab-item} {{stack}}
:sync: stack

**Requirement:** Turning on this setting requires the `kibana_admin` role or equivalent {{stack-manage-app}} access.

**Steps:**

1. Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Global settings**, toggle on **alerting:v2:enabled**.
:::

:::{tab-item} {{serverless-short}}
:sync: serverless

**Requirement:** Turning on this setting requires the `admin` project role.

**Steps:**

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

- **[Configure access](configure-access.md):** Create or update a role with access to the {{alerting-v2-system}} features and the data streams they write to. Users need at minimum **Rules: All** to create rules and `read` index access on `.rule-events` to query rule output in Discover.

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
- **[Create a rule](../rules/create-a-rule.md):** Write the {{esql}} query that defines what to detect, choose Signal or Alert mode, and configure grouping and thresholds in [Configure a rule](../rules/configure-a-rule.md).
-->
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- **[Set up workflows](../workflows-alerting.md):** Configure the automation objects that deliver messages — email, Slack, webhook, and so on. You need at least one workflow before action policies can send anything.
- **[Create action policies](../action-policies/create-configure-action-policy.md):** Define who gets notified, how often, and under what conditions. Policies use KQL matchers to pick up the right episodes and route them to your workflows.
-->
