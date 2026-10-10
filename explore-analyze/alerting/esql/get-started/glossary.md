---
navigation_title: Glossary
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Definitions of key terms used throughout the documentation, such as alert, action policy, and rule event.
---

# Glossary [glossary]

These terms appear throughout the {{alerting-v2-system}} documentation.

**Action policy**
:   A configuration that controls which alerts invoke a workflow and how often. A single action policy can apply to alerts from one rule, several rules, or every rule in the space. To learn more, refer to [Notifications and actions](../notifications-actions.md).

**Alert**
:   The complete record of one problem, from first detection to recovery, moving through states (pending, active, recovering, inactive). An alert is the grouping of [rule events](../rules/rule-event-field-reference.md) that share `episode.id`. {applies_to}`stack: experimental =9.5` In {{stack}} 9.5, the UI calls an alert an **alert episode**. To learn more, refer to [Alerts](../alerts.md).

**Breach**
:   A matching row from a rule run. {{kib}} writes each breach as a [rule event](../rules/rule-event-field-reference.md). To learn more, refer to [{{esql}} query](../rules/configure-rule-query.md).

**Dispatcher**
:   The background process that evaluates action policies against eligible alerts on a short interval (around 5 seconds), independent of the rule schedule. To learn more, refer to [Reduce notification noise](../action-policies/reduce-notification-noise.md).

**{{esql}}**
:   The language the system uses to evaluate your data. Some creation paths generate the query for you. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action a workflow sends (such as a Slack message, an email, or a webhook call) when an alert matches an action policy or a lifecycle trigger fires. To learn more, refer to [How the dispatcher evaluates action policies](../action-policies/about-action-policies.md#how-action-policies-evaluated).

**Rule**
:   The definition of what to watch for in your data, what counts as a match, and how often to check. The rule's [mode](../rules/configure-rule-mode.md) determines whether its matches open alerts. To learn more, refer to [Rules](../rules.md).

**Rule event**
:   A record {{kib}} writes to `.rule-events` for each matching row in a rule run. {{kib}} never overwrites these events. Events with `type: alert` belong to an [alert](../alerts.md), and events with `type: signal` are signals. To learn more, refer to [Rule events](../rules/rule-event-field-reference.md).

**Severity**
:   A label stored on rule events when the query emits a recognized value. Action policies use it only for alerts, so critical alerts can be routed differently from low-priority ones. To learn more, refer to [Configure rule severity](../rules/configure-rule-severity.md).

**Signal**
:   A [rule event](../rules/rule-event-field-reference.md) with `type: signal`, kept in `.rule-events` for later analysis. Signals don't appear on the **Alerts** page and don't start workflows. To learn more, refer to [Query rule events](../alerts/query-signals.md) and [Rule mode](../rules/configure-rule-mode.md).

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on, including how many times the condition must be met before an alert opens or closes. To learn more, refer to [Alert delay](../rules/configure-rule-alert-delay.md) and [Recovery condition](../rules/configure-rule-recovery.md).

**Workflow**
:   The automation that sends a message or runs an action (such as posting to Slack, sending an email, or calling a webhook) when an action policy or an alert lifecycle trigger invokes it. To learn more, refer to [Connect workflows](../workflows-alerting.md).
