---
navigation_title: How it works
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: A detailed walkthrough of how Alert mode and Signal mode rules process data, produce rule events, and drive alert episodes, action policies, and notifications in the experimental alerting system.
---

# How the {{alerting-v2-system}} works [experimental-alerting-system-how-it-works]

This page walks through what happens at each step after a rule runs, and broken down by mode. Use it to understand how the different components of the {{alerting-v2-system}} interact.

## Rule runs in Alert mode [experimental-alerting-system-how-alert-mode-works]

In Alert mode, the rule doesn't just record that a condition was found. It opens an alert episode that persists and tracks the problem until the condition clears. Each time the rule runs, it writes a rule event that can advance the episode's lifecycle state. An action policy sits between the episode and your team, deciding whether and when to trigger a workflow.

| Step | Actor | Action |
|------|-------|--------|
| 1 | Rule | Runs on schedule and evaluates {{esql}} against your data |
| 2 | Rule | Query returns results → A rule event is written to `.rule-events` |
| 3 | System | Creates an alert episode and sets its initial state to `pending`; episode advances to `active` once the activation threshold is met |
| 4 | Action policy | Evaluates the episode against its conditions (checks for episode eligibility, match conditions, and frequency) |
| 5 | Action policy | If conditions are met, triggers a workflow |
| 6 | Workflow | Sends notification or runs automation |
| 7 | Rule | Condition clears → New rule event written → Episode moves to `recovering` → `inactive` |
| 8 | Action policy | Evaluates recovery event and triggers a workflow if conditions are met |
| 9 | Workflow | Sends the recovery notification |

:::{note}
Steps 4–6 and 8–9 run on a separate background process that polls roughly every 5 seconds. Action policy evaluation is not triggered synchronously by the rule's own execution. There is always at least one dispatcher polling cycle between a rule run and any resulting notification.
:::

### Example: Latency monitoring in Alert mode

An SRE team wants to know when checkout service latency degrades, and notify the on-call team when it does. The team creates an Alert mode rule:

1. The rule runs an {{esql}} query every five minutes, checking p95 checkout service latency.
2. When p95 exceeds 2 seconds for more than one consecutive check, the rule opens an alert episode.
3. An action policy with a `rule.tags: "checkout"` matcher skips low-severity episodes and sends a Slack message through an on-call workflow.

The engineer investigates, fixes a slow query, and the alert episode recovers automatically.

## Rule runs in Signal mode [experimental-alerting-system-how-signal-mode-works]

In Signal mode, the rule acts purely as a data producer. Each time the rule runs and its query returns results, it writes a rule event to `.rule-events` and stops. Signals accumulate over time and are immediately queryable in Discover for incident investigation, or as inputs to Alert mode rules that detect correlated activity across multiple signals.

| Step | Actor | Action |
|------|-------|--------|
| 1 | Rule | Runs on schedule and evaluates {{esql}} against your data |
| 2 | Rule | Query returns results → Writes a rule event (signal) to `.rule-events` |
| 3 | System | Signal is immediately queryable in Discover, dashboards, and {{esql}} |

No alert episode is opened. No action policy evaluates the result. No notification is sent.

### Example: Tracking administrator API calls in Signal mode

A security team wants to track calls to a rarely-used administrator API endpoint, but individual calls aren't suspicious enough to page anyone. To start collecting data without generating noise, the team creates a Signal mode rule:

1. The rule runs an {{esql}} query on a schedule, checking for calls to the administrator API endpoint.
2. Each time the query returns results, the rule writes a signal to `.rule-events`.
3. The signals accumulate silently and are immediately queryable in Discover.

After a few weeks, the accumulated signals become useful in two ways. The team can write an Alert mode rule that combines admin API calls with other signals (such as a spike in error rates) to catch correlated activity that neither signal would surface on its own. When an outage happens, the team can query the signal history as evidence directly in Discover, without reconstructing the original query or worrying that the source data has become stale.