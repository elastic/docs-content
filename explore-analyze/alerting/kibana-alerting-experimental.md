---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "How the {{alerting-v2}} watch your data, turn conditions into signals and alerts, route episodes through action policies and workflows, and where to go next in the docs."
---

# {{alerting-v2-cap}} overview [alerting-overview]

The {{alerting-v2}} in Kibana are marked **Experimental** in the UI and are subject to change before general availability. They include alerts, alert episodes, rules, notification policies, workflows, and connectors. For the existing Kibana alerting system, see [Kibana alerting](alerts.md).

The {{alerting-v2}} watch your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, such as when to open an issue, who should know, and how often to notify them. The system handles the rest.

## The core idea [kibana-alerting-v2-overview]

The {{alerting-v2}} separate *detecting* a problem from *notifying* people about it. A rule watches your data and records what it finds. Separate action policies decide who hears about it and when. This lets you build and test detection logic before wiring up any notifications, and update notification routing without touching your rules.

## The four building blocks

The {{alerting-v2}} are built around four objects, rules, alerts, action policies, and workflows, each with a distinct role.

### Rules
A rule defines what to watch for in your data and how often to check. Every rule runs in one of two modes:

- **Detect mode** - The rule records what it finds, but doesn't track whether the problem is ongoing or send any notifications. Use this for observation and investigation.
- **Alert mode** - The rule tracks problems over time and can trigger notifications when something needs attention.

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
Refer to [Rules](kibana-alerting-experimental/rules.md) to learn more.
-->

### Alerts
In Alert mode, a rule tracks each problem over time. Rather than starting a new alert on every run, the rule keeps updating the same alert until the problem clears. You see one lifecycle for that problem, from when it started to when it resolved, instead of a separate alert per check. You triage and manage them on the **Alerts** page.
<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
Refer to [Alerts](kibana-alerting-experimental/alerts.md) to learn more.
-->

<!-- TODO: Clarify and address Tia's suggestion to use alert episodes and rule_events instead -->

### Action policies
An action policy controls whether an alert should trigger an action, and how often. You can set conditions to filter which alerts it applies to, for example, only critical severity alerts from a specific service. A single action policy can apply to alerts from any rule in your space.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
Refer to [Notifications](kibana-alerting-experimental/notifications.md) to learn more.
-->

### Workflows
A workflow is what actually sends the message or runs the automation, for example, posting to Slack or sending an email. Action policies hand off to workflows for delivery. Without a workflow attached, no notification is sent.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
Refer to [Workflows for the {{alerting-v2}}](kibana-alerting-experimental/workflows-alerting.md) to learn more.
-->

## How the pieces fit together [how-pieces-fit-together]


What happens after a rule finds something depends entirely on the rule's mode.

### Alert mode

Use Alert mode when you want to track issues and be notified. The rule opens an episode when the condition is met and keeps it open until the condition clears.

```
Rule runs → finds something → writes a rule event
  → episode opens (pending → active)  → you get notified
  → condition clears (recovering → inactive) → you get notified again
  → action policy → workflow → notification
```

1. The rule evaluates {{esql}} on a schedule and writes a rule event to `.rule-events`.
2. The rule event joins an episode, which is tracked until the condition resolves.
3. Action policies match eligible episodes and decide whether outreach should run.
4. Matched policies invoke configured workflows, which deliver messages or run automation steps.
5. Notifications are the outcome (email, chat, webhook, and so on) when all prior steps pass.

#### Example: Rule runs in Alert mode

An SRE team creates a rule in Alert mode that checks checkout service latency every five minutes. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode. An action policy with a `rule.labels: "checkout"` matcher picks it up, skips low-severity episodes, and sends a Slack message through an on-call workflow.

The on-call engineer gets one message, investigates, fixes a slow query, and latency drops. The episode recovers automatically. No dashboard watching required.

:::{image} ../images/rule-alert-mode-diagram.png
:alt: Diagram of Alert mode flow. A rule runs ES|QL on a schedule. When it finds a match, it writes an alert event tied to an ongoing episode. The episode moves through pending, active, recovering, and inactive states. An action policy matches eligible episodes and routes them to a workflow, which delivers a notification.
:::

### Detect mode

Use Detect mode when you want to record matches for querying and analysis without alerting anyone. The rule writes a signal and stops. An episode is not opened, and notifications are not sent.

```
Rule runs → finds something → writes a signal event
  → queryable in Discover
  → no episode, no action policy, no notification
```

#### Example: Rule runs in Detect mode

A security team wants to track when a rarely-used admin API endpoint is called. Individual calls are not inherently suspicious, so they do not want a notification every time the rule fires. The pattern only becomes meaningful in context. They create a rule in Detect mode that checks for requests to the endpoint every hour.

The rule writes a signal each time it finds a match. No episodes are opened and no notifications go out.

:::{image} ../images/rule-detect-mode-diagram.png
:alt: Diagram of Detect mode flow. A rule runs ES|QL on a schedule. When it finds a match, it writes a signal event to .rule-events. The signal is available for querying in Discover, dashboards, and ES|QL.
:::

Later, an on-call alert fires for unusual privilege escalation on the same host. During the investigation, the team queries `.rule-events` in Discover and finds that the admin API endpoint was called three times in the hour before the escalation. The Detect mode signals did not surface the incident. The Alert mode rule did. But without the signals already in the index, the admin API activity would have been invisible during the post-incident review.


## {{alerting-v2}} terms [key-concepts-glossary]

These terms appear throughout the {{alerting-v2}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   How you control who gets notified, when, and how often. You configure a matcher to filter which alerts it applies to, how episodes batch into notifications, and which workflow should send the message. One action policy can apply to alerts from multiple rules.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Notifications](kibana-alerting-experimental/notifications.md).
-->

**Alert**
:   A rule event produced when a rule runs in Alert mode. Unlike a signal, an alert is tied to an ongoing episode and is part of the full story of that problem from when it started to when it resolved.

**Breach**
:   A single moment when a rule's query finds a match. One breach doesn't necessarily trigger a notification. You can configure a rule to require several consecutive breaches before it confirms the problem is real.

**Dispatcher**
:   The background process in {{kib}} that runs the notification pipeline. On a short interval (around 10 seconds), it evaluates each enabled action policy against active episodes and sends notifications. The dispatcher runs on its own cadence, separate from the rule schedule.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Notification gating](kibana-alerting-experimental/notifications/notification-gating.md).
-->

**Episode**
:   The complete record of one problem, from when it was first detected to when it recovered. An episode moves through states (pending, active, recovering, inactive) as the situation changes. This is what you see and act on in the Alerts UI.
<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
    To learn more, refer to [Alerts](kibana-alerting-experimental/alerts.md).
-->

**{{esql}}**
:   The query language every rule uses to search your data. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action delivered when an alert matches an action policy and a workflow sends it. Examples include a Slack message, an email, or a webhook call.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [How action policies are evaluated](kibana-alerting-experimental/notifications.md#how-action-policies-evaluated).
-->

**Rule**
:   The definition of what to watch for in your data, how often to check, and what counts as a problem. Rules run on a schedule. In Detect mode they produce signals. In Alert mode they track ongoing episodes.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Rules](kibana-alerting-experimental/rules.md).
-->

**Rule event**
:   A record written to `.rule-events` every time a rule runs and its query finds a match. Every rule produces rule events. Whether the record is a signal or an alert depends on the mode the rule is running in.

**Severity**
:   A label you can attach to alerts to indicate how serious they are. Severity is available as a filter in action policies, so you can route critical alerts differently from low-priority ones.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Author rules](kibana-alerting-experimental/rules/author-rules.md#severity-levels).
-->

**Signal**
:   A rule event produced when a rule runs in Detect mode. Signals are stored and queryable, but they don't open episodes or trigger notifications.

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on. This includes both the query that detects the problem and settings that control how many times the condition must be met before an alert opens or closes.
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
    To learn more, refer to [Conditions and thresholds](kibana-alerting-experimental/rules/author-rules.md#conditions-and-thresholds).
-->

**Workflow**
:   The automation that sends a message or runs an action when an action policy decides a notification should go out. Examples include posting to Slack, sending an email, or calling a webhook.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
    To learn more, refer to [Workflows for the {{alerting-v2}}](kibana-alerting-experimental/workflows-alerting.md).
-->

::::{note}
The {{alerting-v2}} are sometimes referred to as "alerting v2" or "the new alerting system" in internal documentation and community discussions. This documentation uses "{{alerting-v2}}" as the primary term.
::::
