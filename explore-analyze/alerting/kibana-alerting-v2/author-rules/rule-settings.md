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

- **Execution interval** (`schedule.every`) — how often the rule evaluates, for example every 1 minute or 5 minutes.
- **Lookback window** (`schedule.lookback`) — the time range for the ES|QL query, for example the last 15 minutes of data.

## Activation and recovery thresholds

[Activation and recovery thresholds](rule-settings/activation-and-recovery-thresholds.md) prevent transient conditions from creating actionable alerts and prevent rapid toggling between active and recovered states.

- **Activation threshold** — consecutive breaches or minimum duration before `pending` → `active`.
- **Recovery threshold** — consecutive recoveries or minimum duration before `recovering` → `inactive`.

## No-data handling

[No-data handling](rule-settings/no-data-handling.md) controls what happens when the rule query returns no results:

- **`no_data`** — record a no-data event.
- **`last_status`** — carry forward the previous status.
- **`recover`** — treat as recovery.

## Grouping

[Grouping](rule-settings/grouping.md) splits alert event generation by one or more fields. Each unique combination produces its own alert series with independent lifecycle tracking.

## Notification policies

[Notification policies](rule-settings/notification-policies.md) are standalone entities that control how alerts reach people and systems. Link one or more policies to a rule to enable matching, grouping, throttling, and routing to workflow destinations.

## Workflows

[Workflows](rule-settings/workflows.md) are automated sequences of tasks. Rules can link to workflows directly for rule-triggered actions, or workflows can be referenced as destinations in notification policies.

## Additional settings

These settings are configured in the rule form or YAML:

| Setting | Description |
|---|---|
| **Tags** | Free-form labels for filtering rules and matching in notification policies |
| **Investigation guide** | Runbook or investigation document attached to the rule |
| **Investigation dashboards** | Linked dashboards for alert investigation context |
| **Severity levels** | User-defined severity conditions within a rule |
