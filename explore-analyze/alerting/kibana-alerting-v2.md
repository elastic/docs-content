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

{{alerting-v2}} is built around four objects (rules, alerts, action policies, and workflows), each with a distinct role in the detection and notification pipeline.

### Rules
A rule says *what to watch* and *how often*. It holds an {{esql}} query, a schedule and lookback window, and in Alert mode, thresholds that control when an issue becomes active or recovers. Rules run in either Detect mode (records signals only, no episodes or notifications) or Alert mode (tracks episodes and enables policy matching). Refer to [Rules](kibana-alerting-v2/rules.md) to learn more.

### Alerts
When a rule runs in Alert mode, it maintains an alert episode for each tracked series: a record that something is wrong, with lifecycle states (pending, active, recovering) and the history of what happened. These live in Discover and the Alerts UI. Refer to [Alerts](kibana-alerting-v2/alerts.md) to learn more.

### Action policies
An action policy decides whether an episode should produce outreach and how often. It's a global object within the space (not attached to any one rule) that uses optional KQL matchers to pick up episodes from any rule. Multiple policies can match the same episode and each runs independently. Refer to [Notifications](kibana-alerting-v2/notifications.md) to learn more.

### Workflows
A workflow is what actually sends the message or runs the automation. Action policies point at workflows as destinations. If no workflow is attached and reachable, nothing is delivered. Refer to [Workflows for {{alerting-v2}}](kibana-alerting-v2/workflows-alerting-v2.md) to learn more.

## A quick example

An SRE team creates a rule that checks checkout service latency every five minutes. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode. An action policy with a `rule.labels: "checkout"` matcher picks it up, skips low-severity episodes, and sends a Slack message through an on-call workflow.

The engineer gets one message, investigates, fixes a slow query, and latency drops. The episode recovers automatically. No dashboard watching required.

## How the pieces fit together [how-pieces-fit-together]

$$$detection-and-notification-v2$$$
$$$runtime-execution-order$$$

At runtime the chain runs left to right:

```
Rule → Alert → Action Policy → Workflow → Notification
```

1. A rule evaluates {{esql}} on a schedule and writes signal or alert events.
2. In Alert mode, alert episodes track the ongoing issue from first breach through recovery.
3. Action policies match eligible episodes and decide whether outreach should run.
4. Matched policies invoke configured workflows, which deliver messages or run automation steps.
5. Notifications are the outcome (email, chat, webhook, and so on) when all prior steps pass.

$$$configuration-order$$$

## {{alerting-v2}} terms [key-concepts-glossary]

These terms appear throughout the {{alerting-v2}} docs. If a term is unclear while reading, check its definition here before going further.

**Action policy**
:   A global saved object in a space that decides whether and how often outreach runs for matching episodes. Holds the matcher, grouping, throttle, and workflow destinations. To learn more, refer to [Notifications](kibana-alerting-v2/notifications.md).

**Alert**
:   A document written to `.rule-events` when a rule in Alert mode matches. Alert documents have `type: alert` and include `episode.*` fields that tie them to the ongoing episode for that series.

**Breach**
:   A single evaluation where the rule's {{esql}} query (and optional alert condition) returned a match. One breach writes one document to `.rule-events`. Multiple consecutive breaches might be required before an episode becomes active, depending on the rule's activation thresholds.

**Episode**
:   In Alert mode, a lifecycle-tracked record that spans one full breach-to-recovery arc for a rule series. An episode moves through states (pending, active, recovering, inactive) and is what action policies match against and operators triage in the Alerts UI. To learn more, refer to [Alerts](kibana-alerting-v2/alerts.md).

**{{esql}}**
:   The query language every rule uses. Data sources are declared in the query itself (for example `FROM`). To learn more, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql.md).

**Notification**
:   A delivery produced when an episode passes through a matching action policy and its workflow destinations. To learn more, refer to [How action policies are evaluated](kibana-alerting-v2/notifications.md#how-action-policies-evaluated-v2).

**Rule**
:   An {{esql}} query plus a schedule and related settings. The entry point for detection. To learn more, refer to [Rules](kibana-alerting-v2/rules.md).

**Severity**
:   Carried by convention under `data.*` and available as a policy KQL field. To learn more, refer to [Author rules](kibana-alerting-v2/rules/author-rules.md#severity-levels).

**Signal**
:   A point-in-time record written to `.rule-events` when a rule in Detect mode matches. Signals have `type: signal` and no `episode.*` fields. They are queryable in Discover but do not open episodes or trigger notifications.

**Threshold**
:   Breach logic expressed in {{esql}}, combined with activation and recovery settings on the rule. To learn more, refer to [Conditions and thresholds](kibana-alerting-v2/rules/author-rules.md#conditions-and-thresholds).

**Workflow**
:   The automation object action policies invoke to deliver messages or run steps such as email, Slack, or webhooks. To learn more, refer to [Workflows for {{alerting-v2}}](kibana-alerting-v2/workflows-alerting-v2.md).
