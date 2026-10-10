---
navigation_title: How it works
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: A detailed walkthrough of how a rule's configuration determines whether matches open an alert or remain available for later analysis, and how those paths drive action policies and workflows.
---

# How the system works [how-it-works]

Each time a {{alerting-v2-system}} rule runs, {{kib}} writes a [rule event](../rules/rule-event-field-reference.md) for each matching row. The rule's [mode](../rules/configure-rule-mode.md) determines what happens next. The events either belong to an [alert](../alerts.md) that can send notifications, or stay available for later analysis.

## Rule opens an alert [how-alert-mode-works]

In this path, each rule event (`type: alert`) carries `episode.*` fields, and events that share `episode.id` belong to the same alert:

| Step | Actor | Action |
|------|-------|--------|
| 1 | Rule | Runs on schedule and evaluates {{esql}} against your data |
| 2 | {{kib}} | Query returns results → Writes one rule event per matching row to `.rule-events` (`type: alert`) |
| 3 | {{kib}} | Opens an alert in `pending` and advances it to `active` once the activation threshold is met |
| 4 | Dispatcher | Evaluates the alert against each action policy's conditions (eligibility, scope, and frequency) |
| 5 | Dispatcher | If conditions are met, invokes a workflow |
| 6 | Workflow | Sends notification or runs automation |
| 7 | {{kib}} | Condition clears → Writes a new rule event → The alert moves to `recovering` → `inactive` |
| 8 | Dispatcher | Evaluates the recovery event and invokes a workflow if conditions are met |
| 9 | Workflow | Sends the recovery notification |

Steps 4–6 and 8–9 run in a separate background process, the dispatcher, which polls about every 5 seconds. At least one polling cycle passes between a rule run and any notification it causes.

For a minute-by-minute example of an alert moving through these states, refer to [Alert lifecycle states](../alerts.md#alert-episode-lifecycle).

## Rule writes events for later analysis [how-signal-mode-works]

In this path, each rule event (`type: signal`) stays in `.rule-events`. These events don't appear on the **Alerts** page and aren't evaluated by action policies or lifecycle triggers. They're immediately queryable in Discover, and they can feed a follow-on rule that opens an alert. For query examples, dashboards, and correlation patterns, refer to [Query rule events](../alerts/query-signals.md).

### Example: Tracking administrator API calls

A security team wants to track calls to a rarely used administrator API endpoint, but individual calls aren't suspicious enough to page anyone. The team creates a rule that records each call as a rule event without opening an alert.

After a few weeks, the accumulated events become useful in two ways. The team can write a follow-on rule that opens an alert and combines admin API calls with other events (such as a spike in error rates) to catch correlated activity that neither source would surface on its own. When an outage happens, the team can query that history as evidence directly in Discover, without reconstructing the original query or worrying that the source data has become stale.

## Related pages

- [Set up {{alerting-v2-system}}](../setup.md): Check the requirements and turn the system on or off.
- [Create your first rule](create-your-first-rule.md): Load sample data, create a rule, and observe the alert lifecycle.
- [Rules](../rules.md): What rules detect, how action policies invoke workflows, and how to select a creation path.
- [Notifications and actions](../notifications-actions.md): Set up action policies that invoke workflows for the alerts they apply to.
