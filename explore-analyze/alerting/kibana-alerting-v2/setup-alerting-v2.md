---
navigation_title: Set up
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "Get {{alerting-v2}} running in your space: enable the UI, confirm data streams, then understand spaces, API keys, and privileges."
---

# Set up {{alerting-v2}} [alerting-setup-v2]

$$$alerting-setup-v2$$$

This page covers what you need to do before authoring rules. You must first enabling {{alerting-v2}} and Workflows, understand where rule events (signals and alerts) are stored, and understand how spaces and API keys scope the objects you create.

If you want to jump straight to creating a rule, go to [Quick start](quick-start-alerting-v2.md). For privilege requirements, refer to [{{alerting-v2}} privileges](alerting-v2-privileges.md).

## Enable {{alerting-v2}} and Workflows [alerting-set-up-v2]

$$$alerting-set-up-v2$$$

- {{alerting-v2}} is available in {{serverless-short}} only. Enable it in **{{manage-app}} > Advanced Settings** by setting `alertingv2` to `true`. Once enabled, go to **{{manage-app}} > V2 Alerting Preview** to open the **Rules** page.

% Update these docs about enabling the advanced setting for v2 alerting. ^

- To use workflows to deliver notifications, also enable the Workflows UI in **{{manage-app}} > Advanced Settings** by setting `workflows:ui:enabled` to `true`.

## Where rule events are stored

{{alerting-v2}} automatically creates and manages two data streams when the first rule runs. You don't need to create them manually.

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

## Spaces [spaces-for-alerting-v2]

Rules and action policies are space-scoped. Objects you create in one space are not visible in another. Alert events are stored globally, but the UI filters what you see by space.

## API keys [alerting-privileges-v2]

$$$alerting-privileges-v2$$$

Saving a rule or action policy automatically creates an API key that is used to run it. The key inherits the privileges of the user who saved the object. If those privileges change over time, update the key from the rule or policy management UI.

## What's next

When you're ready to go further, these can be done in any order:

- **[Author rules](rules/author-rules-v2.md):** Write the {{esql}} query that defines what to detect, choose Detect or Alert mode, and configure grouping and thresholds in [Configure a rule](rules/configure-a-rule-v2.md).
- **[Set up workflows](workflows-alerting-v2.md):** Configure the automation objects that deliver messages — email, Slack, webhook, and so on. You need at least one workflow before action policies can send anything.
- **[Create action policies](notifications/create-configure-action-policy-v2.md):** Define who gets notified, how often, and under what conditions. Policies use KQL matchers to pick up the right episodes and route them to your workflows.