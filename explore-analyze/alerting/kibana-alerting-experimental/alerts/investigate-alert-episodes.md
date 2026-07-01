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
