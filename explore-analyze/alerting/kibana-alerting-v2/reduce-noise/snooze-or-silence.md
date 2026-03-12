---
navigation_title: Snooze or silence alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Temporarily suppress Kibana alerting v2 notifications using snooze (per series), silence (attribute-based), or acknowledge (per episode)."
---

# Snooze or silence Kibana alerting v2 alerts [snooze-silence-v2]

Snooze and silence are manual suppression mechanisms that temporarily prevent notifications without affecting alert detection or lifecycle tracking. Alerts continue to fire and are recorded — only notifications are suppressed.

## Snooze

**Scope**: per series (rule + group key)

Snooze suppresses notifications for a specific alert series for a configured duration. This is the most common manual suppression action.

### How snooze works

1. You snooze an alert series from the alert inbox, flyout, or rule details.
2. Choose a duration (for example, 3 minutes, 1 hour, 8 hours, 1 day) or set a specific end time.
3. During the snooze window, the dispatcher records `suppress` with reason `snooze` for all episodes in that series.
4. When the snooze expires, notifications resume automatically.

### Per-series scope

In Kibana alerting v2, snooze is per series, not per rule. If a rule monitors 100 hosts and you snooze `host-a`, notifications continue for the other 99 hosts.

This is a significant improvement over Kibana alerting v1, where snooze applies to the entire rule.

### When to use snooze

- You are investigating a known issue and do not want to be interrupted.
- A deployment is in progress and you expect temporary alert activity.
- You need to suppress noise for a specific entity without affecting others.

## Silence

**Scope**: attribute-based (labels, tags, or alert fields)

Silence suppresses notifications based on matching conditions rather than targeting a specific series. Any alert whose attributes match the silence condition is suppressed.

### When to use silence

- You want to suppress all alerts from a specific environment (for example, `env: staging`).
- You want to suppress all alerts with a specific tag during a known event.
- You need broader suppression than per-series snooze provides.

## Acknowledge

**Scope**: per episode

Acknowledge is related to snooze and silence but works differently. It suppresses notifications for a specific episode (not the series or attribute-based). When a new episode starts for the same series, notifications resume.

### When to use acknowledge

- You have seen the alert and do not need further notifications for this specific incident.
- You want the alert to remain visible in the inbox but without generating more notifications.
- You need per-incident suppression that does not affect future incidents.

## Comparison

| Mechanism | Scope | Duration | Auto-expires |
|---|---|---|---|
| **Snooze** | Per series | Time-bound | Yes |
| **Silence** | Attribute-based | Until removed | No |
| **Acknowledge** | Per episode | Until unacknowledged or new episode | No |
