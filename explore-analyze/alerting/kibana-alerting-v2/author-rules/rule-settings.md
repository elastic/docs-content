---
navigation_title: Rule settings
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Overview of Kibana alerting v2 rule settings: schedule, thresholds, no-data handling, grouping, notification policies, and workflows."
---

# Kibana alerting v2 rule settings [rule-settings-v2]

Rule settings control how a Kibana alerting v2 rule evaluates data, manages alert lifecycle, and routes notifications. This page provides an overview of all configurable settings. Refer to the linked pages for detailed guidance on each.

## Schedule and lookback

The [schedule and lookback](rule-settings/schedule-and-lookback.md) settings control how often the rule runs and how far back it looks when evaluating data.

## Activation and recovery thresholds

[Activation and recovery thresholds](rule-settings/activation-and-recovery-thresholds.md) prevent transient conditions from creating actionable alerts and prevent rapid toggling between active and recovered states.

## No-data handling

[No-data handling](rule-settings/no-data-handling.md) controls what happens when the rule query returns no results.

## Grouping

[Grouping](rule-settings/grouping.md) splits alert event generation by one or more fields. Each unique combination produces its own alert series with independent lifecycle tracking.

## Notification policies

[Notification policies](rule-settings/notification-policies.md) are standalone entities that control how alerts reach people and systems.

## Workflows

[Workflows](rule-settings/workflows.md) are automated sequences of tasks. Rules can link to workflows directly for rule-triggered actions.
