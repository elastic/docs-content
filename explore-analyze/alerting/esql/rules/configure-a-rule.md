---
navigation_title: Configure a rule
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Overview of configurable rule settings: required settings (mode, query, schedule) and optional settings (severity, grouping, alert delay, recovery, no-data, artifacts)."
---

# Configure a rule [rule-settings]

{{alerting-v2-system-cap}} rules have required settings and several optional ones. Start with the required settings, then add optional settings after you've validated the detection logic, for example by previewing results in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox) when writing {{esql}} directly. The following table links to a dedicated page for each setting, with field descriptions, accepted values, and when to configure it.

| Setting | Description | Required |
| --- | --- | --- |
| [Rule mode](configure-rule-mode.md) | Controls whether matching rows are grouped into an alert or remain available for later analysis. | Required |
| [{{esql}} query](configure-rule-query.md) | The detection logic and the parameters available in query expressions. | Required |
| [Schedule and lookback](configure-rule-schedule.md) | How often the rule evaluates and how far back the query looks. Schedule is required; lookback is optional but strongly recommended. | Strongly recommended |
| [Severity](configure-rule-severity.md) | Assign severity levels to alerts using a `severity` column in query output. | Optional |
| [Grouping](configure-rule-grouping.md) | Track multiple subjects (hosts, services, users) as independent alert series in one rule. | Optional |
| [Alert delay](configure-rule-alert-delay.md) | Reduce noise with delay modes for opening alerts. Only when matches are grouped into an alert. | Optional |
| [Recovery condition](configure-rule-recovery.md) | Whether an alert closes automatically, and how much confirmation it needs before it does. Only when matches are grouped into an alert. | Optional |
| [No-data handling](configure-no-data-handling.md) | What the rule records when the base query returns no results. Only when matches are grouped into an alert. | Optional |
| [Tags, runbooks, and dashboards](configure-rule-artifacts.md) | Labels, investigation guides, and linked dashboards attached to the rule. Tags and runbooks apply only when matches are grouped into an alert. Dashboards apply to any rule. | Optional |
| [Routing tags](../action-policies/create-configure-action-policy.md#add-routing-tags) {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` | Tags that link the rule's alerts to action policies with the same tag. Only when matches are grouped into an alert. | Optional |
