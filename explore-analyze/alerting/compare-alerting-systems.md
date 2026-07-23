---
navigation_title: Compare alerting systems
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: elasticsearch
  - id: cloud-hosted
description: Compare Kibana alerting, the experimental ES|QL-based alerting system, and Watcher by use case and deployment type to select the right tool for your monitoring needs.
---

# Compare alerting systems [compare-alerting-systems]

Elastic offers three alerting systems, each suited to different use cases and workflows. For most new projects and projects on the most recent {{kib}} versions, the {{alerting-v2-system}} is the recommended system. Use this page to compare them by goal, feature, and availability.

## Select by use case

| Goal | Suggested system | Availability |
|---|---|---|
| Monitor metrics, logs, or uptime with ready-made rules and no query language | [{{kib}} alerting](alerts.md) | {applies_to}`stack: ga` {applies_to}`serverless: ga` |
| Use rules built for {{elastic-sec}}, {{observability}}, APM, or Maps | [{{kib}} alerting](alerts.md) | {applies_to}`stack: ga` {applies_to}`serverless: ga` |
| Write {{esql}} to define exactly what to detect and what data each alert episode carries | [{{alerting-v2-system-cap}}](system-overview.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Query alert history in Discover or build dashboards from alert data | [{{alerting-v2-system-cap}}](system-overview.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Manage notification routing, grouping, and throttling in one place, reusable across rules | [{{alerting-v2-system-cap}}](system-overview.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Build highly custom notification logic with reusable, configurable workflows | [{{alerting-v2-system-cap}}](system-overview.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Build highly custom logic with scripting and chained inputs | [Watcher](watcher.md) | {applies_to}`stack: ga` {applies_to}`serverless: unavailable` |

## Compare at a glance

| | {{kib}} alerting | {{alerting-v2-system-cap}} | Watcher |
|---|---|---|---|
| **Best for** | Teams using built-in rule types with form-based setup | Teams that need full control over detection and notification routing | Custom alerting logic requiring scripting |
| **Rule definition** | Select a rule type and fill in parameters | [Write an {{esql}} query](experimental-alerting-system/rules/configure-rule-query.md) or use a rule builder with form-based setup | Write a JSON watch definition |
| **Alert data** | In-place updates, limited query support | [Append-only events queryable with {{esql}} in Discover](experimental-alerting-system/alerts/query-alerts-and-signals-in-discover.md) | Watch history index |
| **Notifications** | Configured per action on each rule | [Centralized action policies](experimental-alerting-system/notifications-actions.md), reusable across rules; supports action-level throttling and conditions | Action-level throttling and conditions |
| **Noise reduction** | Snooze per rule or [per alert](alerts/view-alerts.md#snooze-alerts), maintenance windows | [Per-episode acknowledge or deactivate, per-series snooze, maintenance windows, match condition routing in action policies](experimental-alerting-system/action-policies/reduce-notification-noise.md) | Action conditions and throttling |
| **Available on {{serverless-full}}** | Yes | Yes, {applies_to}`serverless: experimental` | No |
| **Available on {{stack}}** | Yes | Yes, {applies_to}`stack: experimental 9.5+` | Yes |
