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

The {{alerting-v2-system}} in {{kib}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, such as when to open an issue, who should know, and how often to notify them. The system handles the rest.

::::{note}
In the generally available {{kib}} alerting system, the term *alert* refers to a tracked occurrence of a rule condition. In the {{alerting-v2-system}}, the equivalent concept is called an *alert episode*. The two terms describe similar ideas in different systems and are not interchangeable.
::::

## The core idea [kibana-alerting-v2-overview]

The {{alerting-v2-system}} separates *detecting* a problem from *acting* on it:

- **Detecting** - Rules focus purely on what to watch for in your data and on collecting breach and recovery events.
- **Acting** - Action policies handle who gets notified, when, and how, independently of any rule.

You can build and test detection logic before wiring up any notifications, and update notification routing across all rules in one place without editing the rules themselves.

## The four building blocks

The {{alerting-v2-system}} is built around four objects: rules, alert episodes, action policies, and workflows, each with a distinct role.

### Rules

A rule defines what to watch for in your data and how often to check. Every rule runs in one of two modes: alert or signal.

- **Alert** - Opens an alert episode when the rule finds a match, keeps it open until the condition clears, and can notify your team or trigger automated actions when the state changes. Use this when you want the system to track an issue and tell someone about it.
- **Signal** - Records each match as a data point with no ongoing tracking and no notifications. Use this when you want to capture activity for later querying and investigation.

<!-- TODO: When PR #6523 (rules) merges, uncomment the link below and trim this sub-section to 1–2 anchor sentences + the link.
Refer to [Rules](kibana-alerting-experimental/rules.md) to learn more.
-->

### Alert episodes

In Alert mode, the rule opens one alert episode per problem and keeps it open until the condition clears. The alert episode moves through states (pending, active, recovering, inactive) giving you one lifecycle to triage rather than a separate item per rule check.

<!-- TODO: When PR #6527 (alerts) merges, uncomment the link below and trim this sub-section to 1–2 anchor sentences + the link.
Refer to [Alert episodes](kibana-alerting-experimental/alerts.md) to learn more.
-->

### Action policies

An action policy is the gating layer between an alert episode and a workflow. It decides whether and when to invoke a workflow by evaluating suppression, match conditions, and frequency. Policy configuration determines the scope. A policy can apply to alert episodes from a specific rule, multiple rules, or all rules in the space.

<!-- TODO: When PR #6525 (workflows/notifications) merges, uncomment the link below and trim this sub-section to 1–2 anchor sentences + the link.
Refer to [Notifications and actions](kibana-alerting-experimental/notifications-actions.md) to learn more.
-->

### Workflows

A workflow is what actually sends the message or runs the automation, for example, posting to Slack, sending an email, calling a webhook. The {{alerting-v2-system}} invokes workflows through action policies that you configure to trigger on a schedule or on a state change on an alert episode.

<!-- TODO: When PR #6525 (workflows/notifications) merges, uncomment the link below and trim this sub-section to 1–2 anchor sentences + the link.
Refer to [Connect workflows](kibana-alerting-experimental/workflows-alerting.md) to learn more.
-->

## How the pieces fit together [how-pieces-fit-together]

What happens after a rule finds something depends entirely on the rule's mode.

### Alert mode

Use Alert mode when you want to track issues and be notified. An alert episode groups the rule events produced by a rule. Each episode has a lifecycle that starts with the first matching rule event and advances through states as new events are written.

```
Rule runs → conditions met → writes rule event to .rule-events
  → alert episode groups rule events (pending → active)
      → [dispatcher] → action policy → workflow → notification
  → condition clears → new rule event written (recovering → inactive)
      → [dispatcher] → action policy → workflow → notification
```

The rule evaluates {{esql}} on a schedule and writes each result as a rule event to `.rule-events`. These events are grouped into an alert episode, and each new event can advance the episode's lifecycle state. You configure action policies to specify exactly which episodes trigger workflows, how often, and whether matching episodes are dispatched as a group or as individual workflows. When the condition clears, a new rule event moves the episode to recovering and recovery notifications fire through the same pipeline.

::::{dropdown} Example: Rule runs in Alert mode
An SRE team wants to know when checkout service latency degrades, and notify the on-call team when it does. The team creates an Alert mode rule:

1. The rule runs an {{esql}} query every five minutes, checking p95 checkout service latency.
2. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode.
3. An action policy with a `rule.tags: "checkout"` matcher skips low-severity episodes and sends a Slack message through an on-call workflow.

The engineer investigates, fixes a slow query, and the alert episode recovers automatically.

<!-- TODO: Update diagram to reflect that alert episodes group rule events and lifecycle state evolves as new rule events are written.
:::{image} ../images/rule-alert-mode-diagram.png
:alt: Diagram of Alert mode flow. 
:::
-->
::::

### Signal mode

Use Signal mode when you want to record matches for querying and analysis without alerting anyone. The rule writes a signal and stops — no alert episode is opened and no notifications are sent.

```
Rule runs → the rule's conditions are met → writes a signal
  → queryable in Discover
  → no alert episode, no action policy, no notification
```

The rule evaluates {{esql}} on a schedule and writes a rule event (signal) to `.rule-events`. The signal is immediately available for querying in Discover, dashboards, and {{esql}}.

::::{dropdown} Example: Rule runs in Signal mode
A security team wants to track calls to a rarely-used admin API endpoint, but individual calls aren't suspicious enough to page anyone. To start collecting data without generating noise, the team creates a Signal mode rule:

1. The rule runs an {{esql}} query on a schedule, checking for calls to the admin API endpoint.
2. Each time the condition is met, the rule writes a signal to `.rule-events`.
3. The signals accumulate silently and are immediately queryable in Discover.

After running the Signal mode rule for a few weeks, the team has two new capabilities. First, they can create an Alert mode rule that references the presence of admin API calls alongside other signals (such as a spike in error rates) to detect correlated activity that neither signal would surface alone. Second, when investigating an outage, the team can explore the accumulated signal data as evidence without reconstructing the original query or worrying about whether the source data was cleared by retention policies. The signals are already there, timestamped and queryable.

<!-- TODO: Update diagram to reflect that signal mode writes rule events to .rule-events (not "signals") and that these events are immediately queryable in Discover, dashboards, and ES|QL.
:::{image} ../images/rule-detect-mode-diagram.png
:alt: Diagram of Signal mode flow. A rule runs ES|QL on a schedule. When it finds a match, it writes a signal to .rule-events. The signal is available for querying in Discover, dashboards, and ES|QL.
:::
-->
::::

## Next steps

<!-- TODO: When PRs #6523, #6525, and #6527 merge, replace the paragraph below with these three forward-facing tracks and remove the choose-an-alerting-system link (it points here, not forward):
- **Rules**: Refer to [Rules](kibana-alerting-experimental/rules.md) to learn how to create and configure detection rules.
- **Alerts**: Refer to [Alerts](kibana-alerting-experimental/alerts.md) to learn how alert episodes work and how to triage them.
- **Notifications**: Refer to [Notifications and actions](kibana-alerting-experimental/notifications-actions.md) to learn how action policies and workflows route notifications.
-->

To understand how the {{alerting-v2-system}} fits into {{kib}}'s alerting options, refer to [Alerting](../alerting.md) or [Choose an alerting system](choose-an-alerting-system.md).
