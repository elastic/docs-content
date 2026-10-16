---
navigation_title: Configure a rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Overview of configurable rule settings, including mode, query, schedule, recovery, no-data handling, grouping, and related options."
---

# Configure a rule in the {{alerting-v2-system}} [rule-settings]

Rules in the {{alerting-v2-system}} have required settings and several optional ones. Start with the required settings, then add optional settings after you've validated the detection logic, for example by previewing results in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox) when writing {{esql}} directly. The following table links to a dedicated page for each setting, with field descriptions, accepted values, and when to configure it.

| Setting | Description | Required |
| --- | --- | --- |
| [Rule mode](configure-rule-mode.md) | Controls whether matching rows are grouped into an alert or remain available for later analysis. | Required |
| [{{esql}} query](configure-rule-query.md) | The detection logic and the parameters available in query expressions. | Required |
| [Schedule and lookback](configure-rule-schedule.md) | How often the rule evaluates and how far back the query looks. Schedule is required; lookback is optional but strongly recommended. | Strongly recommended |
| [Severity](configure-rule-severity.md) | Assign severity levels to alerts using a `severity` column in query output. | Optional |
| [Grouping](configure-rule-grouping.md) | Track multiple subjects (hosts, services, users) as independent alert series in one rule. | Optional |
| [Alert delay](configure-rule-alert-delay.md) | Reduce noise with delay modes for opening alerts. Only when matches are grouped into an alert. | Optional |
| [Recovery condition](configure-rule-recovery.md) | Whether an alert closes automatically, and how much confirmation it needs before it does. Only when matches are grouped into an alert. | {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Required <br><br> {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Optional |
| [No-data handling](configure-no-data-handling.md) | What the rule records when the base query returns no results. Only when matches are grouped into an alert. | {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Required <br><br> {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Optional |
| [Tags, runbooks, and dashboards](configure-rule-artifacts.md) | Labels, investigation guides, and linked dashboards attached to the rule. Tags and runbooks apply only when matches are grouped into an alert. Dashboards apply to any rule. | Optional |
