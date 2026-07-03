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

# {{alerting-v2-system-cap}} glossary [alerting-v2-glossary]

These terms appear throughout the {{alerting-v2-system}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   A configuration that controls whether and how often an alert episode triggers a notification, including which alerts qualify and how to avoid sending too many notifications. A single action policy can apply to one rule, several rules, or all rules in the space.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Notifications and actions](notifications-actions.md).
-->

**Alert episode**
:   The complete record of one problem tracked in Alert mode, from first detection to recovery, moving through states (pending, active, recovering, inactive).

**Breach**
:   A single instance when a rule's query finds a match, which may or may not open an alert episode depending on how the rule is configured.

**Dispatcher**
:   The background process that evaluates action policies against active alert episodes on a short interval (around 5 seconds), independent of the rule schedule.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Reduce notification noise](action-policies/reduce-notification-noise.md).
-->

**{{esql}}**
:   The query language every rule uses to search your data. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action delivered when an alert episode matches an action policy and a workflow sends it, such as a Slack message, an email, or a webhook call.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [How action policies are evaluated](notifications-actions.md#how-action-policies-evaluated).
-->

**Rule**
:   The definition of what to watch for in your data, how often to check, and what counts as a match; runs on a schedule and produces signals (Signal mode) or tracks alert episodes (Alert mode).
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Rules](rules.md).
-->

**Rule event**
:   A record written to `.rule-events` every time a rule runs and its query finds a match; in Signal mode it is a signal, in Alert mode it belongs to an alert episode.

**Severity**
:   A label attached to alert episodes to indicate urgency; available as a filter in action policies so critical episodes can be routed differently from low-priority ones.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Configure rule severity](rules/configure-rule-severity.md).
-->

**Signal**
:   A rule event recorded in Signal mode; stored and queryable in Discover but doesn't open an alert episode or trigger notifications.

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on, including how many times the condition must be met before an alert episode opens or closes.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Activation and recovery thresholds](rules/configure-rule-thresholds.md).
-->

**Workflow**
:   The automation that sends a message or runs an action when an action policy decides a notification should go out, such as posting to Slack, sending an email, or calling a webhook.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Connect workflows](workflows-alerting.md).
-->
