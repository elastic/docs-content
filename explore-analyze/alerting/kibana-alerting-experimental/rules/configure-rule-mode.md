---
navigation_title: Rule mode
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How rule mode determines whether detections produce signal documents or tracked alert episodes in the experimental alerting system, and when to use each."
---

# Rule mode in the {{alerting-v2-system}} [experimental-alerting-system-rule-mode]

Rule mode is a required setting for rules in the {{alerting-v2-system}}. It determines what the rule produces when the detection query finds a match. Rule mode is set by the rule creation method. Some [creation paths](create-a-rule.md) only support one mode.

| Mode | Behavior |
| --- | --- |
| Signal | Records each matching row as a signal document. No alert episodes, no notifications. |
| Alert | Creates an alert episode for each matching row. Episodes are tracked through lifecycle states, appear on the Alerts UI, and can be routed to notifications by action policies. |

## When to use each rule mode [rule-mode-when-to-use]

Signal mode is the right fit when:

* You are writing a new detection query and want to verify it produces the expected matches before notifying anyone.
* You need to build detection history in `.rule-events` without generating alert noise or triggering notifications.

Signal mode is **not** the right fit when:

* You need to track how long a condition has been active or how it transitions between states. Signal mode does not create episodes or lifecycle state.
* You need notifications when a condition fires. Switch to Alert mode and attach an action policy.

Alert mode is the right fit when:

* The rule is production-ready and each breach should be tracked as a distinct alert episode that opens, can escalate, and closes when the condition clears.
* Alert episodes from the rule should be available for be triage, acknowledgment, or escalation.
* You want to attach action policies to route notifications when alert episodes open, escalate, or recover.

Alert mode is **not** the right fit when:

* The rule's query is still being tuned and generating alerts would create noise for on-call teams. Use Signal mode to validate first, then switch.

## Examples

### Build detection history before enabling alerts

You're writing a new detection query and want to verify it produces the results you expect before anyone gets paged. Create the rule in Signal mode so matches are recorded in `.rule-events` and you can inspect them in Discover without opening any alert episodes or triggering notifications. Once the matches look correct, edit the rule and switch it to Alert mode.

### Route critical episodes to an on-call workflow

You have a checkout service error rate rule and want on-call engineers notified when it fires. Create the rule in Alert mode so each breach opens a tracked episode that action policies can route to a notification channel. The rule's episodes appear on the Alerts UI and are visible to any action policy whose KQL matcher matches the episode fields.
