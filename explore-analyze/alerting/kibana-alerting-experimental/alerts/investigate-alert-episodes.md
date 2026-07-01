---
navigation_title: Investigate alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Investigate alert episodes in Kibana's experimental alerting system. Explore metric trends, lifecycle history, related episodes, metadata, actors, and assignment."
---

# Investigate alert episodes [investigate-alert-episodes]

In the {{alerting-v2-system}}, the episode detail page shows the full context of an alert episode, including its metric trend, lifecycle history, related episodes, triage actions, assignee, actors, source metadata, and severity.

## Metric trend [metric-trend]

For threshold-based rules, the episode detail page shows how the evaluated metric compared to the rule's threshold conditions over the episode's lifetime. Use it to understand how the condition developed: how far the metric exceeded the threshold, whether the breach was escalating or stabilizing, and how long it persisted.

When a rule includes multiple threshold conditions:

- Conditions that compare the **same metric** appear together, with each threshold represented separately.
- Conditions that compare **different metrics** appear in separate views, one per metric.

This section is only present for rules that use threshold comparisons. It doesn't appear for signal-mode rules or rules whose evaluation logic doesn't produce comparable metric output.

## Related episodes by series [related-episodes]

The detail page groups related episodes into two subsections to help you distinguish between a condition recurring on one entity and a rule firing across many:

- **Same alert series:** Episodes sharing the same `rule_id` and `group_hash`. These are recurrences of the same condition on the same series. A long list here suggests the underlying issue isn't being fully resolved.
- **Other series for this rule:** Episodes from the same rule with a different `group_hash`. These show how broadly the rule is firing across other entities or conditions.

## Source event metadata [source-event-metadata]

The metadata view surfaces field values from the source event that triggered the episode. Use it to inspect fields that aren't shown in the main detail view, such as resource identifiers or version information.

## Response history and actors [actors]

Actors are the users who acted on the episode and when each action happened. Use this to track response history and coordinate across a shared queue.

## Episode ownership and assignment [episode-assignment]

You can assign an episode to a user to indicate ownership. Only one user can hold the assignment at a time. Assigning replaces any existing assignee.

Use assignment to establish clear ownership during triage and prevent duplicate work when multiple people are reviewing the same queue.
