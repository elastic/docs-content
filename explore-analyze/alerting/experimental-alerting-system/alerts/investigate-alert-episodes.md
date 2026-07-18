---
navigation_title: Investigate alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Investigate alert episodes in Kibana's experimental alerting system. Understand what triggered an episode, assess metric behavior, find related episodes, review responders, and inspect underlying data."
---

# Investigate alert episodes in the {{alerting-v2-system}} [investigate-alert-episodes]

From the **Alerts** page, select an episode to open its detail page, which surfaces what triggered the episode, its severity, recurring patterns, and response history, so you can investigate and coordinate a response.

## Understand the trigger and scope [understand-trigger]

Each episode includes key context to answer the first questions in any investigation:

- **Grouping** - The value of the `BY` clause that identifies this episode's group, such as a hostname or service name. Use it to confirm which entity the rule is firing on.
- **Triggered** - When the episode opened.
- **Duration** - How long the episode has been active.
- **Assignee** - Who currently owns the episode, if anyone. To assign or reassign the episode, refer to [Triage alert episodes](triage-alert-episodes.md).

The **Rule overview** section shows the rule name, type, and status alongside a snippet of its {{esql}} query. Select **View rule details** to open the full rule configuration and confirm exactly what condition the rule evaluates.

## Assess the metric behavior [assess-metric-behavior]

Each episode shows a trend chart comparing the evaluated metric against the rule's threshold conditions over the episode's lifetime. Use it to understand how far the metric exceeded the threshold, whether the breach was escalating or stabilizing, and when it peaked.

When a rule includes multiple threshold conditions:

- Conditions that compare the **same metric** appear together, with each threshold represented separately.
- Conditions that compare **different metrics** appear in separate views, one for each metric.

This chart appears only for alert-mode rules whose query contains extractable threshold comparisons.

The episode timeline shows its full duration as a horizontal bar, from when it was triggered to its most recent evaluation or close time.

## Check for related or recurring episodes [related-episodes]

Related episodes from the same rule are grouped to help you answer whether this is an isolated incident or part of a larger pattern:

- **Same alert group** - Episodes for this rule that share the same group as the current episode (same `group_hash`). A long list here suggests the underlying condition isn't being fully resolved between episodes.
- **Other groups for this rule** - Episodes from the same rule firing on different entities (different `group_hash`). Use this to gauge how broadly the rule is triggering across your environment.

## Review who has responded [review-responders]

Each episode tracks who performed the most recent response action of each type, so you can avoid duplicating work or missing a step someone else already handled:

- **Acknowledged by** - The user who most recently acknowledged the episode.
- **Resolved by** - The user who most recently resolved the episode.
- **Snoozed by** - The user who snoozed the episode, shown together with the **Snoozed until** time.

These rows only appear when the episode is in the corresponding state. System-generated actions display as **System**.

## Inspect the underlying data [inspect-data]

Each episode includes a metadata view that surfaces the field values computed or retained by the rule's {{esql}} query. For example, a query using `STATS ... BY` stores aggregated values, not all fields from the underlying events. Use it to inspect rule-specific context such as resource identifiers or computed metrics. You can search by field name or value and toggle off null fields to focus on populated data.

<!-- TODO: Confirm how users access the full source document from here — is it via Open in Discover, direct query of the source index, or is there no direct path? Add guidance once confirmed. -->

## Access the response runbook [access-runbook]

If the rule has a runbook URL configured, you can access it directly from the episode to follow documented response procedures.
