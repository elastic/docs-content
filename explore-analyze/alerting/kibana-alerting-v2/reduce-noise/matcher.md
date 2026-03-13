---
navigation_title: Matcher
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Use KQL matchers on Kibana alerting v2 notification policies to control which alerts trigger notifications based on severity, tags, or any field."
---

# Kibana alerting v2 matcher [matcher-v2]

Matchers are KQL expressions on notification policies that control which alerts trigger notifications. They filter the stream of alerts before grouping and throttling, ensuring that only relevant alerts reach their destinations.

## How matchers work

During the dispatcher's evaluation step, each alert episode is tested against the matcher of every relevant notification policy. The matcher is evaluated in-process (no {{es}} query required) and has access to:

- `data.*` — the alert event payload (fields from the ES|QL query)
- `rule_id` — the rule that produced the alert
- `group_hash` — the series identity
- `episode_id` — the current episode
- `episode_status` — `inactive`, `pending`, `active`, `recovering`
- `last_event_timestamp` — when the latest event was written

## Matcher syntax

Matchers use KQL syntax:

### Equality

```
severity: "critical"
```

### AND/OR logic

```
severity: "critical" AND tags: "production"
```

```
severity: "warning" OR severity: "medium"
```

### Membership

```
rule.name: ("cpu-alert" OR "memory-alert" OR "disk-alert")
```

### Prefix matching

```
service.name: "checkout*"
```

### Field existence

```
data.host.name: *
```

### Catch-all

An empty matcher (empty string or omitted) matches every alert from the linked rules. This is useful for default notification policies.

## Routing with matchers

Create multiple notification policies with different matchers to route alerts to different destinations:

- **Critical production alerts → PagerDuty**: `severity: "critical" AND tags: "production"`
- **Warning alerts → Slack**: `severity: "warning" OR severity: "medium"`
- **All remaining alerts → Email digest**: empty matcher (catch-all) with daily throttle

## When to use

- **Severity-based routing**: send critical alerts to PagerDuty, warnings to Slack.
- **Environment filtering**: only notify on production alerts, not staging.
- **Team routing**: route alerts tagged with specific service names to the responsible team's channel.
- **Exclusion**: exclude known-noisy rule names from a policy by using AND NOT logic.
