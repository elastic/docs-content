---
navigation_title: How it works
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: A detailed walkthrough of how a rule's configuration determines whether matches are grouped into an alert episode or left as signals, and how those paths drive action policies and notifications.
---

# How the {{alerting-v2-system}} works [how-it-works]

This page walks through what happens at each step after a rule runs on its schedule. Both paths begin the same way: {{kib}} writes a [rule event](rules/rule-event-field-reference.md) for each matching row. The walkthroughs below use Signal mode and Alert mode. Use this page to understand how the different components of the {{alerting-v2-system}} interact.

## Rule runs in Alert mode [how-alert-mode-works]

In Alert mode, {{kib}} writes each match as a rule event (`type: alert`) with `episode.*` fields. Events that share an `episode.id` form an alert episode, which persists and tracks the problem until the condition clears. Each new event can advance the episode's lifecycle state. An action policy sits between the episode and a workflow, deciding whether and when to invoke it.

| Step | Actor | Action |
|------|-------|--------|
| 1 | Rule | Runs on schedule and evaluates {{esql}} against your data |
| 2 | {{kib}} | Query returns results → Writes one rule event per matching row to `.rule-events` (`type: alert`) |
| 3 | {{kib}} | Tracks the event as an alert episode. Events that share an `episode.id` form the episode. The episode opens in `pending` and advances to `active` once the activation threshold is met |
| 4 | Action policy | Evaluates the episode against its conditions (checks for episode eligibility, match conditions, and frequency) |
| 5 | Action policy | If conditions are met, invokes a workflow |
| 6 | Workflow | Sends notification or runs automation |
| 7 | {{kib}} | Condition clears → Writes a new rule event → Episode moves to `recovering` → `inactive` |
| 8 | Action policy | Evaluates recovery event and invokes a workflow if conditions are met |
| 9 | Workflow | Sends the recovery notification |

:::{note}
Steps 4–6 and 8–9 run on a separate background process that polls roughly every 5 seconds. Action policy evaluation is not triggered synchronously by the rule's own execution. There is always at least one dispatcher polling cycle between a rule run and any resulting notification.
:::

### Example: Latency monitoring in Alert mode

An SRE team wants to know when checkout service latency degrades, and notify the on-call team when it does. The team creates a rule in Alert mode:

1. The rule runs an {{esql}} query every five minutes, checking p95 checkout service latency.
2. When p95 exceeds 2 seconds for more than one consecutive check, those events form an alert episode.
3. An action policy with a `rule.tags: "checkout"` matcher skips low-severity episodes and invokes an on-call workflow that sends a Slack message.

The engineer investigates, fixes a slow query, and the alert episode recovers automatically.

## Rule runs in Signal mode [how-signal-mode-works]

In Signal mode, each time the rule runs on its schedule and its query returns results, {{kib}} writes a rule event (`type: signal`) to `.rule-events`. That event is the signal. Signals accumulate over time and are immediately queryable in Discover for incident investigation, or as inputs to a follow-on rule that groups matches into an episode. For query examples, dashboards, and correlation patterns, refer to [Query signals](alerts/query-signals.md).

| Step | Actor | Action |
|------|-------|--------|
| 1 | Rule | Runs on schedule and evaluates {{esql}} against your data |
| 2 | {{kib}} | Query returns results → Writes one rule event per matching row to `.rule-events` (`type: signal`) |
| 3 | {{kib}} | Records the event as a signal. The event is immediately queryable in Discover, dashboards, and {{esql}} |

### Example: Tracking administrator API calls in Signal mode

A security team wants to track calls to a rarely-used administrator API endpoint, but individual calls aren't suspicious enough to page anyone. To start collecting data without generating noise, the team creates a rule in Signal mode:

1. The rule runs an {{esql}} query on a schedule, checking for calls to the administrator API endpoint.
2. Each time the query returns results, {{kib}} writes a rule event (`type: signal`) to `.rule-events`.
3. The signals accumulate silently and are immediately queryable in Discover.

After a few weeks, the accumulated signals become useful in two ways. The team can write a follow-on rule that groups matches into an episode and combines admin API calls with other signals (such as a spike in error rates) to catch correlated activity that neither signal would surface on its own. When an outage happens, the team can query the signal history as evidence directly in Discover, without reconstructing the original query or worrying that the source data has become stale.

## Related pages

- [Get started](get-started.md): Enable the {{alerting-v2-system}} and create your first rule.
- [Rules](rules.md): What rules do, what they don't control, and how to choose a creation path.
- [Rule events](rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how those events relate to signals and alert episodes.
- [Query signals](alerts/query-signals.md): Query signals in Discover and use them as input to a rule that opens an episode.
- [Notifications and actions](notifications-actions.md): Set up workflows and action policies to notify your team when an alert episode matches.