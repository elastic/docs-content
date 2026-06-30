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

Rule configuration is part of the {{alerting-v2-system}} in {{kib}}. The {{esql}} query defines what a rule detects. The settings below determine whether it behaves correctly in production. For query authoring, refer to [Author rules](author-rules.md).
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
For notification routing, refer to [Notifications](../notifications.md).
-->

| Setting | Description |
| --- | --- |
| [Rule mode](configure-rule-mode.md) | Can be Signal or Alert mode. Controls whether matching rows generate signal documents or tracked alert episodes. |
| [ES\|QL query](configure-rule-query.md) | The detection logic and the parameters available in query expressions. |
| [Severity](configure-rule-severity.md) | Assign severity levels to alert episodes using a `severity` column in query output. |
| [Grouping](configure-rule-grouping.md) | Track multiple subjects (hosts, services, users) as independent alert series in one rule. |
| [Schedule and lookback](configure-rule-schedule.md) | How often the rule evaluates and how far back the query looks. |
| [Activation and recovery thresholds](configure-rule-thresholds.md) | Reduce noise with delay modes for opening and closing alert episodes. (Alert mode only) |
| [No-data handling](configure-no-data-handling.md) | What the rule records when the base query returns no results. |
| [Tags and runbooks](configure-rule-tags.md) | Free-form labels and investigation guides attached to the rule. (Alert mode only) |
