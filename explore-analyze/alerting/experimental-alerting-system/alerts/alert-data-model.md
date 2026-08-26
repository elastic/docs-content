---
navigation_title: Alert data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Signal and alert rule events share the .rule-events data stream and most fields. Alert events add episode.* lifecycle fields; triage actions go to .alert-actions."
---

# Alert data model in the {{alerting-v2-system}} [alert-data-model]

This page explains how Signal mode and Alert mode rule events relate, and where {{kib}} stores them.

## How rule mode determines what gets written [how-rule-mode-determines-output]

Every time a rule finds a match, it writes a [rule event](../rules/rule-event-field-reference.md) to `.rule-events`. Whether that event is a signal or an alert depends on the rule's mode. Both kinds share the same data stream and most of the same fields.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A `type: signal` rule event. A point-in-time record that the query matched. | Rules in Signal mode |
| Alert | A `type: alert` rule event with `episode.*` fields. Events that share `episode.id` form an alert episode. | Rules in Alert mode |

:::{note}
A rule in Signal mode only writes signals. It never opens alert episodes, so action policies have nothing to match against.
:::

## How {{kib}} records evaluation and triage data [how-kib-records-evaluation-triage-data]

Rule output is written to the following append-only data streams, both managed by {{kib}} through ILM and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one document per result row, per rule run, and never overwrites them. This stream holds both `type: signal` and `type: alert` rule events.
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve).

## Related pages

- [Rule events](../rules/rule-event-field-reference.md): What a rule event is and how Signal mode and Alert mode use those events.