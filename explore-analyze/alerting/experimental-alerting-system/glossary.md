---
navigation_title: Glossary
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: Definitions of key terms used throughout the experimental Kibana alerting system documentation.
---

# {{alerting-v2-system-cap}} glossary [glossary]

These terms appear throughout the {{alerting-v2-system}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   A configuration that controls which alert episodes invoke a workflow and how often. A single action policy can apply to one rule, several rules, or all rules in the space. To learn more, refer to [Notifications and actions](notifications-actions.md).

**Alert episode**
:   The complete record of one problem, from first detection to recovery, moving through states (pending, active, recovering, inactive). An episode is the grouping of [rule events](rules/rule-event-field-reference.md) that share an `episode.id`. To learn more, refer to [Alerts](alerts.md).

**Breach**
:   A single instance when a rule's query finds a match, which may or may not open an alert episode depending on how the rule is configured. To learn more, refer to [{{esql}} query](rules/configure-rule-query.md).

**Dispatcher**
:   The background process that evaluates action policies against active alert episodes on a short interval (around 5 seconds), independent of the rule schedule. To learn more, refer to [Reduce notification noise](action-policies/reduce-notification-noise.md).

**{{esql}}**
:   The query language every rule uses to search your data. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action a workflow sends (such as a Slack message, an email, or a webhook call) when an alert episode matches an action policy or a lifecycle trigger fires. To learn more, refer to [How action policies are evaluated](action-policies/about-action-policies.md#how-action-policies-evaluated).

**Rule**
:   The definition of what to watch for in your data, how often to check, and what counts as a match. A rule runs on a schedule. {{kib}} writes [rule events](rules/rule-event-field-reference.md) when the query finds a match. The rule's configuration determines whether those events are grouped into alert episodes. To learn more, refer to [Rules](rules.md).

**Rule event**
:   A record {{kib}} writes to `.rule-events` when a rule finds a match: one event per matching row, per run. {{kib}} never overwrites these events. Events that are part of an alert episode have `type: alert` and `episode.*` fields. The UI and the `type` field call other events **signals** (`type: signal`). To learn more, refer to [Rule events](rules/rule-event-field-reference.md).

**Severity**
:   A label attached to alert episodes to indicate urgency. Severity is available as a filter in action policies so critical episodes can be routed differently from low-priority ones. To learn more, refer to [Configure rule severity](rules/configure-rule-severity.md).

**Signal**
:   A [rule event](rules/rule-event-field-reference.md) with `type: signal`. These events stay in `.rule-events` and are queryable in Discover. Action policies evaluate alert episodes only, so a signal never reaches a policy or a workflow. To learn more, refer to [Query signals](alerts/query-signals.md) and [Rule mode](rules/configure-rule-mode.md).

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on, including how many times the condition must be met before an alert episode opens or closes. To learn more, refer to [Alert delay](rules/configure-rule-alert-delay.md) and [Recovery condition](rules/configure-rule-recovery.md).

**Workflow**
:   The automation that sends a message or runs an action (such as posting to Slack, sending an email, or calling a webhook) when an action policy or an alert episode lifecycle trigger invokes it. To learn more, refer to [Connect workflows](workflows-alerting.md).
