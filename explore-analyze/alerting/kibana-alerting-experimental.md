---
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: The experimental Kibana alerting system uses ES|QL rules to detect conditions, track problems as alert episodes, and route notifications through reusable action policies.
---

# {{alerting-v2-system-cap}} overview [alerting-overview]

The {{alerting-v2-system}} in {{kib}} is marked **Experimental** in the UI and is subject to change before general availability. It includes rules, alert episodes, action policies, workflows, and connectors. For the existing {{kib}} alerting system, refer to [{{kib}} alerting](alerts.md).

The {{alerting-v2-system}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, such as when to open an issue, who should know, and how often to notify them. The system handles the rest.

## The core idea [kibana-alerting-v2-overview]

The {{alerting-v2-system}} separates *detecting* a problem from *acting* on it. Rules focus purely on what to watch for in your data. Action policies handle who gets notified, when, and how, independently of any rule. You can build and test detection logic before wiring up any notifications, and update notification routing across all rules in one place without editing the rules themselves.

## The four building blocks

The {{alerting-v2-system}} is built around four objects: rules, alert episodes, action policies, and workflows, each with a distinct role.

### Rules

A rule defines what to watch for in your data and how often to check. Every rule runs in one of two modes: alert or signal.

- **Alert**: Opens an alert episode when the rule finds a match, keeps it open until the condition clears, and can notify your team or trigger automated actions when the state changes. Use this when you want the system to track an issue and tell someone about it.
- **Signal**: Records each match as a data point with no ongoing tracking and no notifications. Use this when you want to capture activity for later querying and investigation.

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
Refer to [Rules](kibana-alerting-experimental/rules.md) to learn more.
-->

### Alert episodes
In Alert mode, the rule opens one alert episode per problem and keeps it open until the condition clears. The alert episode moves through states (pending, active, recovering, inactive) giving you one lifecycle to triage rather than a separate item per rule check. You manage alert episodes on the **Alerts** page.
<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
Refer to [Alert episodes](kibana-alerting-experimental/alerts.md) to learn more.
-->

### Action policies
An action policy is the gating layer between an alert episode and a workflow. It decides whether and when to invoke a workflow by evaluating suppression, match conditions, and frequency. You can set conditions to filter which alert episodes it applies to, for example, only critical severity alert episodes from a specific service. Global action policies apply to alert episodes from any rule in the space. Per-rule action policies scope to a single rule for more targeted routing.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
Refer to [Notifications and actions](kibana-alerting-experimental/notifications-actions.md) to learn more.
-->

### Workflows
A workflow is what actually sends the message or runs the automation, for example, posting to Slack or sending an email. Action policies hand off to workflows for delivery. Without a workflow attached, no notification is sent.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
Refer to [Workflows for the {{alerting-v2-system}}](kibana-alerting-experimental/workflows-alerting.md) to learn more.
-->

## How the pieces fit together [how-pieces-fit-together]


What happens after a rule finds something depends entirely on the rule's mode.

### Alert mode

Use Alert mode when you want to track issues and be notified. The rule opens an alert episode when the condition is met and keeps it open until the condition clears.

```
Rule runs → the rule's conditions are met → writes a rule event
  → alert episode (pending → active)
      → [dispatcher] → action policy → workflow → notification
  → condition clears (recovering → inactive)
      → [dispatcher] → action policy → workflow → notification
```

1. The rule evaluates {{esql}} on a schedule and writes a rule event to `.rule-events`.
2. The rule event opens or updates an alert episode, which is tracked until the condition resolves.
3. The dispatcher runs on a short interval, independently of the rule schedule, and picks up active alert episodes.
4. For each active alert episode, the dispatcher evaluates all enabled action policies. Each policy runs the episode through a sequence of gates: suppression, match conditions, and frequency.
5. For policies where the episode clears all gates, the dispatcher invokes the configured workflows.
6. Workflows deliver the notification or run the automation (email, chat, webhook, and so on).

#### Example: Rule runs in Alert mode

An SRE team creates a rule in Alert mode that checks checkout service latency every five minutes. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode. An action policy with a `rule.tags: "checkout"` matcher picks it up, skips low-severity alert episodes, and sends a Slack message through an on-call workflow.

The on-call engineer gets one message, investigates, fixes a slow query, and latency drops. The alert episode recovers automatically. No dashboard watching required.

:::{image} ../images/rule-alert-mode-diagram.png
:alt: Diagram of Alert mode flow. A rule runs ES|QL on a schedule. When it finds a match, it writes a rule event tied to an ongoing alert episode. The alert episode moves through pending, active, recovering, and inactive states. An action policy matches eligible alert episodes and routes them to a workflow, which delivers a notification.
:::

### Signal mode

Use Signal mode when you want to record matches for querying and analysis without alerting anyone. The rule writes a signal and stops. An alert episode is not opened, and notifications are not sent.

```
Rule runs → the rule's conditions are met → writes a signal
  → queryable in Discover
  → no alert episode, no action policy, no notification
```

1. The rule evaluates {{esql}} on a schedule and writes a rule event (signal) to `.rule-events`.
2. The signal is available for querying in Discover, dashboards, and ES|QL.
3. No alert episode is opened. No action policy is evaluated. No notification is sent.

#### Example: Rule runs in Signal mode

A security team wants to track when a rarely-used admin API endpoint is called. Individual calls are not inherently suspicious, so they do not want a notification every time the rule fires. The pattern only becomes meaningful in context. They create a rule in Signal mode that checks for requests to the endpoint every hour.

The rule writes a signal each time it finds a match. No alert episodes are opened and no notifications go out.

:::{image} ../images/rule-detect-mode-diagram.png
:alt: Diagram of Signal mode flow. A rule runs ES|QL on a schedule. When it finds a match, it writes a signal to .rule-events. The signal is available for querying in Discover, dashboards, and ES|QL.
:::

Later, an on-call alert fires for unusual privilege escalation on the same host. During the investigation, the team queries `.rule-events` in Discover and finds that the admin API endpoint was called three times in the hour before the escalation. The Signal mode rule events did not surface the incident. The Alert mode rule did. But without the signals already in the index, the admin API activity would have been invisible during the post-incident review.


## {{alerting-v2-system-cap}} glossary [key-concepts-glossary]

These terms appear throughout the {{alerting-v2-system}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   The gating layer between an alert episode and a workflow. You configure suppression rules, match conditions to filter which alert episodes it applies to, frequency settings to control batching and cooldown, and which workflow should send the message. Global action policies apply to alert episodes from any rule in the space. Per-rule action policies scope to a single rule.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Notifications and actions](kibana-alerting-experimental/notifications-actions.md).
-->

**Alert episode**
:   The complete record of one problem tracked in Alert mode, from when it was first detected to when it recovered. An alert episode moves through states (pending, active, recovering, inactive) as the situation changes. This is what you see and act on on the **Alerts** page.

**Breach**
:   A single moment when a rule's query finds a match. One breach doesn't necessarily trigger a notification. You can configure a rule to require several consecutive breaches before it confirms the problem is real.

**Dispatcher**
:   The background process in {{kib}} that runs the notification pipeline. On a short interval (around 5 seconds), it evaluates each enabled action policy against active alert episodes and sends notifications. The dispatcher runs on its own cadence, separate from the rule schedule.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Reduce notification noise](kibana-alerting-experimental/action-policies/reduce-notification-noise.md).
-->

**{{esql}}**
:   The query language every rule uses to search your data. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action delivered when an alert episode matches an action policy and a workflow sends it. Examples include a Slack message, an email, or a webhook call.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [How action policies are evaluated](kibana-alerting-experimental/notifications-actions.md#how-action-policies-evaluated).
-->

**Rule**
:   The definition of what to watch for in your data, how often to check, and what counts as a problem. Rules run on a schedule. In Signal mode they produce signals. In Alert mode they track ongoing alert episodes.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Rules](kibana-alerting-experimental/rules.md).
-->

**Rule event**
:   A record written to `.rule-events` every time a rule runs and its query finds a match. Every rule produces rule events. In Signal mode the record is a signal. In Alert mode it belongs to an alert episode.

**Severity**
:   A label you can attach to alert episodes to indicate how serious they are. Severity is available as a filter in action policies, so you can route critical alert episodes differently from low-priority ones.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Author rules](kibana-alerting-experimental/rules/author-rules.md#severity-levels).
-->

**Signal**
:   A rule event recorded when a rule runs in Signal mode. Signals are stored and queryable, but they don't open alert episodes or trigger notifications.

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on. This includes both the query that detects the problem and settings that control how many times the condition must be met before an alert episode opens or closes.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Conditions and thresholds](kibana-alerting-experimental/rules/author-rules.md#conditions-and-thresholds).
-->

**Workflow**
:   The automation that sends a message or runs an action when an action policy decides a notification should go out. Examples include posting to Slack, sending an email, or calling a webhook.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Workflows for the {{alerting-v2-system}}](kibana-alerting-experimental/workflows-alerting.md).
-->

## Next steps

To understand how the {{alerting-v2-system}} fits into {{kib}}'s alerting options, refer to [Alerting](../alerting.md) or [Choose an alerting system](choose-an-alerting-system.md).