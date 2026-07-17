---
navigation_title: Rule events
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How the experimental alerting system in Kibana writes rule events to .rule-events: signal and alert document types, shared base fields, episode fields, and the append-only data stream behavior."
---

# Rule events in {{alerting-v2-system}} [rule-reference]

This page explains the two types of documents the {{alerting-v2-system}} writes to `.rule-events` and how the data stream behaves, so you can write {{esql}} queries against `.rule-events` with confidence, for example, to replay an episode's history, investigate a signal, or build dashboards from rule output.

<!-- TODO: When PR #6527 merges, add a sentence here linking to the full field list:
For the full list of fields on each document type, refer to [Rule event field reference](../alerts/field-reference.md).
-->

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle through [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md). Older backing indices are deleted automatically when the retention window expires. Do not change mappings or index settings for these streams yourself.
:::

## Rule event documents

Each time a rule evaluates, {{kib}} writes one document per matched series to `.rule-events`. The `type` field determines the document kind:

- **`signal`** - A point-in-time record that the query matched. Useful for querying history or chaining into follow-on rules. Signal documents don't include `episode.*` fields.
- **`alert`** - A lifecycle-tracked episode visible in the alert inbox, episode details, and triage views. Alert documents include `episode.*` fields and represent a breach that stays open until the condition clears.

Both kinds share base fields. Only `alert` documents add episode fields that carry the lifecycle state for the matched series.

:::{note}
The `.rule-events` data stream is append-only. A new document is written on every rule evaluation. Existing documents are never updated. Each document is a snapshot of that moment. The `episode.status` field records the lifecycle stage the episode was in at that evaluation. To view the full history of an episode, query `.rule-events` filtered by `episode.id`, for example:

```esql
FROM .rule-events
| WHERE episode.id == "<episode-id>"
| SORT @timestamp ASC
```

<!-- TODO: When PR #6527 merges, add after the code block:
"For more query examples including lifecycle replay and incident tracing, refer to [Query alert history in Discover](../alerts/query-alerts-and-signals-in-discover.md)."
-->
:::

## Related pages

- [{{esql}} query](configure-rule-query.md): How the base query and alert condition shape what's written to `.rule-events`.
- [Rules](../rules.md): What rules do and how they fit into the broader {{alerting-v2-system}}.