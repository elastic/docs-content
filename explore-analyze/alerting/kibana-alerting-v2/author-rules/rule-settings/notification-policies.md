---
navigation_title: Notification policies
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Notification policies control how and when Kibana alerting v2 alerts reach people and systems, including matching, grouping, throttling, and routing."
---

# Kibana alerting v2 notification policies [notification-policies-v2]

A notification policy defines how and when alerts reach people and systems. In Kibana alerting v2, notification policies are **global** saved objects: they are not attached to individual rules. Which rules a policy applies to is determined by **`rule_labels`** on the policy and by the episode matcher, not by references from the rule.

## Compare Kibana alerting v1 and v2 notification policies

| | Kibana alerting v1 | Kibana alerting v2 |
|---|---|---|
| **Scope** | Per-rule connectors and actions on the rule | **Global** notification policies. Rules do not reference specific policies |
| **Matching** | Rule execution drives connector runs | **`rule_labels`** scoping on the policy, then KQL episode matching |
| **Matcher context** | N/A (rule-centric) | Typed fields including `episode_status`, `rule.name`, `rule.labels`, and `data.*` |

## How notification policies apply to rules

Notification policies are **global**. Rules do not store or reference a list of notification policies.

- **Scoping** is expressed on the policy itself using **`rule_labels`**. Only episodes for rules whose labels satisfy the policy’s label selector are candidates for that policy.
- After label scoping, the policy’s **KQL episode matcher** runs against the typed matcher context (for example `episode_status`, `rule.name`, `rule.labels`, and fields under `data.*`).

## Learn more

- [Create and manage notification policies](notification-policies/create-manage-notification-policies.md)
- [How notification policies are evaluated](notification-policies/how-notification-policies-are-evaluated.md)
