---
applies_to:
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "How {{alerting-v2}} watches your data, turns conditions into signals and alerts, routes episodes through action policies and workflows, and where to go next in the docs."
---

# {{alerting-v2}} [alerting-overview-v2]

{{alerting-v2}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, such as when to open an issue, who should know, and how often to notify them. The system handles the rest.

## The core idea [kibana-alerting-v2-overview]

{{alerting-v2}} separates *detecting* a problem from *notifying* people about it. A rule watches your data and records what it finds. Separate action policies decide who hears about it and when. This lets you build and test detection logic before wiring up any notifications, and update notification routing without touching your rules.

## The four building blocks

## The four building blocks

{{alerting-v2}} is built around four objects — rules, alerts, action policies, and workflows — each with a distinct role.

### Rules
A rule defines what to watch for in your data and how often to check. Every rule runs in one of two modes:

- **Detect mode** — the rule records what it finds, but doesn't track whether the problem is ongoing or send any notifications. Use this for observation and investigation.
- **Alert mode** — the rule tracks problems over time and can trigger notifications when something needs attention.

Refer to [Rules](kibana-alerting-v2/rules-v2.md) to learn more.

### Alerts
When a rule runs in Alert mode, it creates an alert for each problem it detects. An alert isn't a single snapshot — it's an ongoing record that follows the problem through its full lifecycle, from when it first appeared to when it resolved. You triage and manage alerts in the Alerts UI. Refer to [Alerts](kibana-alerting-v2/alerts-v2.md) to learn more.

### Action policies
An action policy controls whether an alert should trigger a notification, and how often. You can set conditions to filter which alerts it applies to — for example, only critical severity alerts from a specific service. A single action policy can apply to alerts from any rule in your space. Refer to [Notifications](kibana-alerting-v2/notifications-v2.md) to learn more.

### Workflows
A workflow is what actually sends the message or runs the automation — for example, posting to Slack or sending an email. Action policies hand off to workflows for delivery. Without a workflow attached, no notification is sent. Refer to [Workflows for {{alerting-v2}}](kibana-alerting-v2/workflows-alerting-v2.md) to learn more.

## A quick example

An SRE team creates a rule that checks checkout service latency every five minutes. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode. An action policy with a `rule.labels: "checkout"` matcher picks it up, skips low-severity episodes, and sends a Slack message through an on-call workflow.

The engineer gets one message, investigates, fixes a slow query, and latency drops. The episode recovers automatically. No dashboard watching required.

## How the pieces fit together [how-pieces-fit-together]

$$$detection-and-notification-v2$$$
$$$runtime-execution-order$$$

What happens after a rule finds something depends entirely on the rule's mode.

### Alert mode

Use Alert mode when you want to track issues and be notified. The rule opens an episode when the condition is met and keeps it open until the condition clears.

```
Rule runs → finds something → writes an alert event
  → episode opens (pending → active)  → you get notified
  → condition clears (recovering → inactive) → you get notified again
  → action policy → workflow → notification
```

1. The rule evaluates {{esql}} on a schedule and writes an alert event to `.rule-events`.
2. The alert event joins an episode, which is tracked until the condition resolves.
3. Action policies match eligible episodes and decide whether outreach should run.
4. Matched policies invoke configured workflows, which deliver messages or run automation steps.
5. Notifications are the outcome (email, chat, webhook, and so on) when all prior steps pass.

### Detect mode

Use Detect mode when you want to record matches for querying and analysis without alerting anyone. The rule writes a signal and stops. An episode is not opened, and notifications are not sent.

```
Rule runs → finds something → writes a signal event
  → queryable in Discover
  → no episode, no action policy, no notification
```

$$$configuration-order$$$

## {{alerting-v2}} terms [key-concepts-glossary]

These terms appear throughout the {{alerting-v2}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   A set of rules that controls who gets notified, when, and how often. You configure a matcher to filter which alerts it applies to, how alerts should be grouped, and which workflow should send the message. One action policy can apply to alerts from multiple rules. To learn more, refer to [Notifications](kibana-alerting-v2/notifications-v2.md).

**Alert**
:   A rule event produced when a rule runs in Alert mode. Unlike a signal, an alert is tied to an ongoing episode and is part of the full story of that problem from when it started to when it resolved.

**Breach**
:   A single moment when a rule's query finds a match. One breach doesn't necessarily trigger a notification. You can configure a rule to require several consecutive breaches before it confirms the problem is real.

**Episode**
:   The complete record of one problem, from when it was first detected to when it recovered. An episode moves through states (pending, active, recovering, inactive) as the situation changes. This is what you see and act on in the Alerts UI. To learn more, refer to [Alerts](kibana-alerting-v2/alerts-v2.md).

**{{esql}}**
:   The query language every rule uses to search your data. To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   The message or action delivered when an alert matches an action policy and a workflow sends it. Examples include a Slack message, an email, or a webhook call. To learn more, refer to [How action policies are evaluated](kibana-alerting-v2/notifications-v2.md#how-action-policies-evaluated-v2).

**Rule**
:   The definition of what to watch for in your data, how often to check, and what counts as a problem. Rules run on a schedule. In Detect mode they produce signals. In Alert mode they track ongoing episodes. To learn more, refer to [Rules](kibana-alerting-v2/rules-v2.md).

**Rule event**
:   A record written to `.rule-events` every time a rule runs and its query finds a match. Every rule produces rule events. Whether the record is a signal or an alert depends on the mode the rule is running in.

**Severity**
:   A label you can attach to alerts to indicate how serious they are. Severity is available as a filter in action policies, so you can route critical alerts differently from low-priority ones. To learn more, refer to [Author rules](kibana-alerting-v2/rules/author-rules-v2.md#severity-levels).

**Signal**
:   A rule event produced when a rule runs in Detect mode. Signals are stored and queryable, but they don't open episodes or trigger notifications.

**Threshold**
:   The condition a rule uses to decide when something is worth alerting on. This includes both the query that detects the problem and settings that control how many times the condition must be met before an alert opens or closes. To learn more, refer to [Conditions and thresholds](kibana-alerting-v2/rules/author-rules-v2.md#conditions-and-thresholds).

**Workflow**
:   The automation that sends a message or runs an action when an action policy decides a notification should go out. Examples include posting to Slack, sending an email, or calling a webhook. To learn more, refer to [Workflows for {{alerting-v2}}](kibana-alerting-v2/workflows-alerting-v2.md).
