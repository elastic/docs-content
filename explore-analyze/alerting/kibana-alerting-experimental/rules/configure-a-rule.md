---
navigation_title: Configure a rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure rules in the experimental alerting system: mode, ES|QL query, grouping, schedule, activation and recovery thresholds, no-data handling, tags, and evaluation."
---

# Configure a rule in the {{alerting-v2-system}} [rule-settings]

Rules in the {{alerting-v2-system}} have three required settings and several optional ones. The table below lists each setting, what it controls, and whether it is required to save a rule.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
For notification routing, refer to [Notifications](../notifications.md).
-->

| Setting | Description | Required |
| --- | --- | --- |
| [Rule mode](configure-rule-mode.md) | Signal or Alert. Controls whether matching rows generate signal documents or tracked alert episodes. | Required |
| [ES\|QL query](configure-rule-query.md) | The detection logic and the parameters available in query expressions. | Required |
| [Schedule and lookback](configure-rule-schedule.md) | How often the rule evaluates and how far back the query looks. | Required |
| [Severity](configure-rule-severity.md) | Assign severity levels to alert episodes using a `severity` column in query output. | Optional |
| [Grouping](configure-rule-grouping.md) | Track multiple subjects (hosts, services, users) as independent alert series in one rule. | Optional |
| [Activation and recovery thresholds](configure-rule-thresholds.md) | Reduce noise with delay modes for opening and closing alert episodes. (Alert mode only) | Optional |
| [No-data handling](configure-no-data-handling.md) | What the rule records when the base query returns no results. | Optional |
| [Tags and runbooks](configure-rule-tags.md) | Free-form labels and investigation guides attached to the rule. (Alert mode only) | Optional |
