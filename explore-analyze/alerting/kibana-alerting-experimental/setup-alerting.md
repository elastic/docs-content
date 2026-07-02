---
navigation_title: Set up
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Get the {{alerting-v2}} running in your space: enable the UI, confirm data streams, then understand spaces, API keys, and privileges."
---

# Set up the {{alerting-v2}} [alerting-setup]


Before you can create your first rule, the {{alerting-v2}} in {{kib}} must be enabled in your space and a few background systems need to be in place. 

Rules rely on two data streams to store their output, API keys to run with the right privileges, and space scoping to keep objects organized. Getting these right upfront means your rules will run cleanly and their output will be queryable from the start.

If you want to jump straight to creating a rule, go to [Quick start](quick-start-alerting.md). For privilege requirements, refer to [{{alerting-v2-cap}} privileges](alerting-privileges.md).

## Enable the {{alerting-v2}} [alerting-set-up]

To access the {{alerting-v2}}, a {{kib}} administrator must turn on the `alerting:v2:enabled` advanced setting. The steps differ by deployment type.

### Enable on {{stack}} [alerting-enable-stack]

1. Go to **Stack Management → Advanced Settings**.
2. Under **Global settings**, toggle on **alerting:v2:enabled**.

### Enable on {{serverless-short}} [alerting-enable-serverless]

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
The `/internal/kibana/global_settings` endpoint is an internal API and may change without notice. There is currently no public equivalent.
:::

When the `alerting:v2:enabled` setting is turned off, rule and dispatcher execution stops, the APIs and UIs are hidden, and existing rules and action policies are paused. Turning it back on resumes execution. Disabling does not delete any data.

## Where rule events are stored

The {{alerting-v2}} automatically create and manage two data streams when the first rule runs. You don't need to create them manually.

| Data stream | What it stores |
|---|---|
| `.rule-events` | A record for every rule evaluation. One document per result row, per run. Never updated in place. |
| `.alert-actions` | Records for acknowledge, snooze, deactivate, fire, suppress, and other audit and suppression tracking. |

Both data streams are hidden system data streams. To query them in Discover, prefix the name with `$`:

```esql
FROM $`.rule-events`
| WHERE rule.id == "<your-rule-id>"
| SORT @timestamp DESC
| LIMIT 10
```

After your first rule runs, use the query above in Discover to confirm documents are appearing. If nothing appears after a few seconds, check that the rule is enabled and that your ES|QL query returns results when run independently.

## Spaces [spaces-for-alerting]

Rules and action policies are space-scoped. Objects you create in one space are not visible in another. Alert events are stored globally, but the UI filters what you see by space.

## API keys [alerting-privileges]


Saving a rule or action policy automatically creates an API key that is used to run it. The key inherits the privileges of the user who saved the object. If those privileges change over time, update the key from the rule or policy management UI.

## Next steps

When you're ready to go further, these can be done in any order:

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
- **[Create a rule](rules/create-a-rule.md):** Write the {{esql}} query that defines what to detect, choose Signal or Alert mode, and configure grouping and thresholds in [Configure a rule](rules/configure-a-rule.md).
-->
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- **[Set up workflows](workflows-alerting.md):** Configure the automation objects that deliver messages — email, Slack, webhook, and so on. You need at least one workflow before action policies can send anything.
- **[Create action policies](action-policies/create-configure-action-policy.md):** Define who gets notified, how often, and under what conditions. Policies use KQL matchers to pick up the right episodes and route them to your workflows.
-->