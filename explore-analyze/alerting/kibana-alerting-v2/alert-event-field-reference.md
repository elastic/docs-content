---
navigation_title: Fields for rule events and actions
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Fields in the {{kib}} alerting v2 `.rule-events` data stream for signals and alerts, episode fields on lifecycle alerts, and action records in `.alert-actions`."
---

# {{kib}} alerting v2 rule event and action field reference [alert-event-field-reference-v2]

This page is the field reference for {{kib}} alerting v2 data written to {{es}}. It covers names, types, required fields, and valid values. Use it when you author {{esql}} in Discover, build dashboards or reports, or integrate automation against alert and signal documents.

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle. Do not change mappings or index settings for these stream yourself.
:::

## Rule events index

All rules write their signal and alert events to the **rule events index**, implemented as the **`.rule-events`** data stream. Each document has a `type` of `signal` or `alert`.

- **`signal`:** Point-in-time facts you query or chain into other rules. For example, rows a follow-on rule reads from `.rule-events` to build a rule on alert data. These documents do not include `episode.*` fields.
- **`alert`:** Lifecycle-tracked episodes in the alert UI: inbox, episode details, and triage. For example, a breach that stays open as an episode until the condition clears. These documents include `episode.*` fields.

Both kinds share the same [base fields](#signal-and-alert-document-fields). Only `alert` documents add [`episode.*`](#episode-fields-for-alerts-with-lifecycle-tracking) fields.

### Signal and alert document fields

The following table lists each top-level field that appears on both `signal` and `alert` documents in **`.rule-events`**. [Episode fields for alerts with lifecycle tracking](#episode-fields-for-alerts-with-lifecycle-tracking) lists additional fields for `alert` rows only.

| Field | Type | Required | Description |
|---|---|---|---|
| `@timestamp` | `date` | Yes | When this document was written to `.rule-events`. |
| `scheduled_timestamp` | `date` | No | Scheduled execution time for this rule run. |
| `rule.id` | `keyword` | Yes | Rule identifier. |
| `rule.version` | `long` | Yes | Rule version at the time this event was emitted. |
| `group_hash` | `keyword` | Yes | Series identity key for grouped evaluations. |
| `data` | `flattened` | Yes | Payload from the {{esql}} query output. Shape depends on your rule. |
| `status` | `keyword` | Yes | One of: `breached`, `recovered`, `no_data`. |
| `source` | `keyword` | Yes | Origin of this event. Product-specific identifier. |
| `type` | `keyword` | Yes | `signal` or `alert`. Application field on each rule event document written by {{kib}}. |


:::{admonition} Fields not stored as a dedicated column
There is no top-level or nested `duration` field on **`.rule-events`** documents. For triage or reporting, derive duration from [{{esql}} views](manage-alerts/explore-alerts-discover.md), the alert UI, or your own queries over timestamps and episode identifiers.
:::

### Episode fields for alerts with lifecycle tracking

The table below describes `episode.*` fields on documents in **`.rule-events`** where `type` is `alert`, when {{kib}} is managing that alert’s lifecycle in the alert inbox and related views. `signal` documents do not include an `episode` section.

| Field | Type | Description |
|---|---|---|
| `episode.id` | `keyword` | Episode identifier for this series. |
| `episode.status` | `keyword` | One of: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | `long` | Count of consecutive evaluations in the current `episode.status`. This field is only set when `episode.status` is `pending` or `recovering`. |

## Alert actions index

When a user or the system records an action on an alert episode, {{kib}} writes a document to the **alert actions index**, implemented as the **`.alert-actions`** data stream. Each document is one action. The `action.type` field records what happened, for example acknowledge, snooze, tag, fire, or unmatched.

Use **`.alert-actions`** for triage history, metrics such as MTTA, and auditing. This stream does not store what your rule query returned on each run. That output exists only in **`.rule-events`**.

### Alert action document fields

The following table lists fields on each document in **`.alert-actions`**.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | `date` | When the action was recorded |
| `episode.id` | `keyword` | Target episode |
| `rule.id` | `keyword` | Rule that owns the episode |
| `action.type` | `keyword` | The action type, for example: <br>- **`acknowledge`:** User acknowledged the alert.<br>- **`snooze`:** Notifications snoozed for a period.<br>- **`tag`:** Tag applied to the alert.<br>- **`fire`:** Notification or escalation fired for the episode.<br>- **`unmatched`:** No notification policy matched the episode, so no workflow ran for it under those policies. <br><br> For the full set of action types and UI behavior, refer to [Alert actions](manage-alerts/investigate-respond/alert-actions.md). |

## Related documentation

- [Explore {{kib}} alerting v2 alerts and signals in Discover](manage-alerts/explore-alerts-discover.md): How rule event documents map to rows in Discover, how Detect and Alert mode relate to `type`, and how multiple rules share the `.rule-events` stream.
- [Where query output appears in each document](manage-alerts/explore-alerts-discover.md#where-query-output-appears-in-each-document): Top-level fields versus the `data` field when you query in Discover.
