---
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

# Choose an alerting system [choose-an-alerting-system]

Elastic offers multiple alerting systems. For most new projects, the {{alerting-v2-system}} is the recommended starting point. Pick the system that fits how you want to define rules and route notifications.

## Select by use case

| Goal | Suggested system | Availability |
|---|---|---|
| Monitor metrics, logs, or uptime with ready-made rules and no query language | [{{kib}} alerting](alerts.md) | {applies_to}`stack: ga` {applies_to}`serverless: ga` |
| Use rules built for Security, Observability, APM, or Maps | [{{kib}} alerting](alerts.md) | {applies_to}`stack: ga` {applies_to}`serverless: ga` |
| Write {{esql}} to define exactly what to detect and what data each alert episode carries | [{{alerting-v2-system-cap}}](kibana-alerting-experimental.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Query alert history in Discover or build dashboards from alert data | [{{alerting-v2-system-cap}}](kibana-alerting-experimental.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Manage notification routing, grouping, and throttling in one place, reusable across rules | [{{alerting-v2-system-cap}}](kibana-alerting-experimental.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Build highly custom notification logic with reusable, configurable workflows | [{{alerting-v2-system-cap}}](kibana-alerting-experimental.md) | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` |
| Build highly custom logic with scripting and chained inputs | [Watcher](watcher.md) | {applies_to}`stack: ga` {applies_to}`serverless: unavailable` |

## Compare at a glance

| | {{kib}} alerting | {{alerting-v2-system-cap}} | Watcher |
|---|---|---|---|
| **Best for** | Teams using built-in rule types with form-based setup | Teams that need full control over detection and notification routing | Custom alerting logic requiring scripting |
| **Rule definition** | Select a rule type and fill in parameters | Write an {{esql}} query or use a rule builder with form-based setup | Write a JSON watch definition |
| **Alert data** | In-place updates, limited query support | Append-only events queryable with {{esql}} in Discover | Watch history index |
| **Notifications** | Configured per action on each rule | Centralized action policies, reusable across rules; supports action-level throttling and conditions | Action-level throttling and conditions |
| **Noise reduction** | Snooze per rule, maintenance windows | Per-episode acknowledge or deactivate, per-series snooze, maintenance windows, match condition routing in action policies | Action conditions and throttling |
| **Available on {{serverless-full}}** | Yes | Yes, {applies_to}`serverless: experimental` | No |
| **Available on {{stack}}** | Yes | Yes, {applies_to}`stack: experimental 9.5+` | Yes |

<!--
TODO: Once PRs #6523, #6525, and #6527 are merged, add cross-links to the experimental system cells in the comparison table above. The cells currently describe the system but don't link anywhere. Suggested targets:

| Row                        | Link target                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Alert data (experimental)  | kibana-alerting-experimental/alerts/query-alerts-and-signals-in-discover.md (PR #6527) |
| Notifications (experimental) | kibana-alerting-experimental/notifications-actions.md or action-policies/about-action-policies.md (PR #6525) |
| Noise reduction (experimental) | kibana-alerting-experimental/action-policies/reduce-notification-noise.md (PR #6525) |
| Rule definition (experimental) | kibana-alerting-experimental/rules/configure-rule-query.md (PR #6523) |

Also add links to the experimental system rows in the "Select by use case" table once the relevant pages are available.
-->
