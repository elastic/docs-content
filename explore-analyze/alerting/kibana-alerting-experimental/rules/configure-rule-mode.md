---
navigation_title: Rule mode
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Choose between Signal and Alert mode for rules in Kibana's experimental alerting system."
---

# Rule mode in the {{alerting-v2-system}} [rule-mode]

Rule mode is a required setting for rules in the {{alerting-v2-system}}. Rule mode set by the rule creation method and some creation paths only support one mode. Refer to [Create a rule](create-a-rule.md) for available options.

| Mode | Behavior | Best for |
| --- | --- | --- |
| Signal | Records each matching row as a signal document. No alert episodes, no notifications. | Testing a new query, building detection history, or observing matches without notifying anyone. |
| Alert | Creates an alert episode for each matching row. Episodes are tracked through lifecycle states, appear on the **Alerts** page, and can be routed to notifications by action policies. | Production rules where breaches should be tracked, escalated, or routed to a notification channel. |

## Examples

### Build detection history before enabling alerts

You're writing a new detection query and want to verify it produces the results you expect before anyone gets paged. Create the rule in Signal mode so matches are recorded in `.rule-events` and you can inspect them in Discover without opening any alert episodes or triggering notifications. Once the matches look correct, edit the rule and switch it to Alert mode.

### Route critical episodes to an on-call workflow

You have a checkout service error rate rule and want on-call engineers notified when it fires. Create the rule in Alert mode so each breach opens a tracked episode that action policies can route to a notification channel. The rule's episodes appear on the **Alerts** page and are visible to any action policy whose KQL matcher matches the episode fields.
