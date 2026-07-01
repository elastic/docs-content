---
navigation_title: Investigate alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Investigate alert episodes in Kibana's experimental alerting system. Explore lifecycle history, related episodes, metadata, actors, and assignment."
---

# Investigate alert episodes [investigate-alert-episodes]

In the {{alerting-v2-system}}, the episode detail page shows the full context of an alert episode, including its lifecycle history, related episodes, triage actions, assignee, actors, and source metadata.

## Related episodes by series [related-episodes]

Related episodes are grouped into two subsections to help you distinguish between a condition recurring on one entity and a rule firing across many:

- **Same alert series:** Episodes sharing the same `rule_id` and `group_hash`. These are recurrences of the same condition on the same series. A long list here suggests the underlying issue is not being fully resolved.
- **Other series for this rule:** Episodes from the same rule with a different `group_hash`. These show how broadly the rule is firing across other entities or conditions.

## Source event metadata [source-event-metadata]

The metadata view surfaces field values from the source event that triggered the episode. Use it to inspect fields that are not shown in the main detail view, such as resource identifiers or version information.

## Response history and actors [actors]

Actors are the users who have taken actions on the episode and when each action was taken. Use this to track response history and coordinate across a shared queue.

## Episode ownership and assignment [episode-assignment]

An episode can be assigned to a user to indicate ownership. Only one user can be assigned at a time. Assigning replaces any existing assignee.

Use assignment to establish clear ownership during triage and prevent duplicate work when multiple people are reviewing the same queue.
