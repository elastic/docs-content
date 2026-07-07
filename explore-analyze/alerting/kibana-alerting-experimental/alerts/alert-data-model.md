---
navigation_title: Alert data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Alert history in Kibana's experimental alerting system lives in two append-only streams, .rule-events for evaluations and .alert-actions for triage. Signals and alerts differ by rule mode."
---

# Alert data model in the {{alerting-v2-system}} [alert-data-model]

This page explains the foundational data model of the {{alerting-v2-system}}. It explains what the system writes, where it writes it, and why those choices affect what you can do with the data.

## How rule mode determines what gets written [signals-vs-alerts]

Every time a rule finds a match, it writes a document to `.rule-events`. Whether that document is a signal or an alert depends on the rule's mode.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A point-in-time record that the query matched (`type: signal`). | Rules in Detect mode |
| Alert | A lifecycle-tracked episode with `type: alert` and `episode.*` fields. | Rules in Alert mode |

:::{note}
A rule in Detect mode only writes signals. It never opens alert episodes, so action policies have nothing to match against.
:::

## How {{kib}} records evaluation and triage data [where-alert-data-is-stored]

Rule output is written to the following append-only data streams, both managed by {{kib}} through ILM and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one document for each rule evaluation and never overwrites them.
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve).