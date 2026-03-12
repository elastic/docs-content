---
navigation_title: Notification policies
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Notification policies control how and when Kibana alerting v2 alerts reach people and systems — matching, grouping, throttling, and routing."
---

# Kibana alerting v2 notification policies [notification-policies-v2]

A notification policy defines how and when alerts reach people and systems. It is the boundary between an alert firing and a notification being sent, answering the question: "Is this alert worth notifying someone about?"

Notification policies are standalone, reusable entities. One policy can apply across multiple rules. This is a fundamental shift from Kibana alerting v1, where notification behavior is embedded inside each rule's action configuration.

## What a notification policy controls

| Capability | Description |
|---|---|
| **Matching** | KQL conditions that determine which alerts the policy applies to. Match by severity, rule name, tags, grouping key values, or any alert field |
| **Grouping** | Batch related alerts into a single notification. Group by host, rule, severity, or custom fields |
| **Frequency** | How often notifications are sent: immediate (per alert), throttled (at most once per interval), or periodic digest |
| **Suppression** | Suppress notifications during maintenance windows |
| **Destinations** | One or more workflow destinations (Slack, PagerDuty, email, or custom workflows) |

## Notification policies vs. rule actions

| Aspect | Kibana alerting v1 | Kibana alerting v2 notification policies |
|---|---|---|
| Where configured | On each rule, per action | Standalone entity, linked to rules |
| Scope | Single rule | Can span multiple rules |
| Throttling | Per action frequency | Per notification group |
| Matching | `run when` filter per action | KQL matcher across all alert fields |
| Grouping | Limited | Full field-based grouping |
| Reusability | Duplicate configuration per rule | Define once, link to many rules |

## How to link policies to rules

You link notification policies to rules during rule creation or editing:

1. In the rule form, go to the **Notification policies** section.
2. Select one or more existing policies, or click **Create policy** to create a new one.
3. Save the rule.

You can also link rules from the policy side: open a notification policy and assign rules to it.

A rule can reference multiple notification policies. Each policy evaluates independently, so a single alert can trigger notifications through different channels with different grouping and throttling.

## Learn more

- [Create and manage notification policies](notification-policies/create-manage-notification-policies.md) — how to create, edit, and manage policies.
- [How notification policies are evaluated](notification-policies/how-notification-policies-are-evaluated.md) — the 10-step dispatcher pipeline that processes alerts through policies.
