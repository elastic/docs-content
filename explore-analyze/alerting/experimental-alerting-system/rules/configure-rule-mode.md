---
navigation_title: Rule mode
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How rule mode determines whether matching rows are written as signal events or as alert events that form tracked episodes in the experimental alerting system, and when to use each."
---

# Rule mode in the {{alerting-v2-system}} [rule-mode]

Rule mode is a required setting for rules in the {{alerting-v2-system}}. It determines whether {{kib}} records each [rule event](rule-event-field-reference.md) as a signal or tracks it as an alert episode. Rule mode is set by the rule creation method. Some [creation paths](create-a-rule.md) only support one mode.

| Mode | `kind` value | Behavior |
| --- | --- | --- |
| Signal | `signal` | {{kib}} writes a rule event with `type: signal` for each matching row. No alert episodes, no notifications. |
| Alert | `alert` | {{kib}} writes a rule event with `type: alert` and `episode.*` fields for each matching row. Events that share an `episode.id` form an alert episode. Episodes are tracked through lifecycle states, appear on the **Alerts** page, and can be routed to notifications by action policies. |

Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts** to view and triage alert episodes.

If you're editing YAML directly, rule mode maps to the `kind` field on the rule. That `kind` field isn't the same as the `type` field on rule events: `kind` configures the rule, and `type` records what {{kib}} wrote for that run.

## When to use each rule mode [rule-mode-when-to-use]

Signal mode is the right fit when:

* You are writing a new detection query and want to verify it produces the expected matches before notifying anyone.
* You need to build detection history in `.rule-events` without generating alert noise or triggering notifications.

Signal mode is **not** the right fit when:

* You need to track how long a condition has been active or how it transitions between states. Signal mode does not create episodes or lifecycle state.
* You need notifications when a condition fires. Switch to Alert mode and attach an action policy.

Alert mode is the right fit when:

* The rule is production-ready and each breach should be tracked as a distinct alert episode that opens, can escalate, and closes when the condition clears.
* Alert episodes from the rule should be available for triage, acknowledgment, or escalation.
* You want to attach action policies to route notifications when alert episodes open, escalate, or recover.

Alert mode is **not** the right fit when:

* The rule's query is still being tuned and generating alert episodes would create noise for on-call teams. Use Signal mode to validate first, then switch.

## Examples

### Build detection history before enabling alert episodes

You're writing a new detection query and want to verify it produces the results you expect before anyone gets paged. Create the rule in Signal mode so matches are recorded in `.rule-events` and you can inspect them in Discover without opening any alert episodes or triggering notifications. Once the matches look correct, edit the rule and switch it to Alert mode.

### Route critical episodes to an on-call workflow

You have a checkout service error rate rule and want on-call engineers notified when it fires. Create the rule in Alert mode so each breach opens a tracked episode that action policies can route to a notification channel. The rule's episodes appear on the **Alerts** page and are visible to any action policy whose KQL matcher matches the episode fields.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Create a rule](create-a-rule.md): Compare rule creation paths and choose the one that fits your workflow.
- [Query signals](../alerts/query-signals.md): Query Signal mode output in Discover, build dashboards, and correlate signals with Alert mode rules.
- [Rule events](rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how `type` relates to rule `kind`.
- [Rule event data model](../alerts/rule-event-data-model.md): Shared `.rule-events` schema for Signal-mode and Alert-mode events.
