---
navigation_title: Event field reference
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Field reference for Kibana alerting v2 documents in .rule-events: shared fields for all events, episode fields only when type is alert, and .alert-actions."
---

# Kibana alerting v2 alert event field reference [alert-event-field-reference-v2]

{{kib}} alerting v2 writes one document per rule evaluation output to the **`.rule-events`** data stream. This page lists the fields stored in those documents.

**Signal vs alert:** When **`type`** is **`signal`**, only the [fields shared by all events](#fields-for-all-events) are populated. When **`type`** is **`alert`**, the document includes the same fields plus **`episode.*`** ([episode fields](#episode-fields-only-when-type-is-alert)). The **`episode`** object is the **only** extra field group on alert events compared to signal events. For the authoritative mapping and enums, see the Kibana resource definition ([`alert_events.ts`](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/alerting_v2/server/resources/alert_events.ts)).

## Fields for all events

These fields appear on both **`signal`** and **`alert`** documents.

| Field | Type | Required | Description |
|---|---|---|---|
| `@timestamp` | `date` | Yes | When this document was written to **`.rule-events`**. |
| `scheduled_timestamp` | `date` | No | Scheduled execution time for this rule run. |
| `rule.id` | `keyword` | Yes | Rule identifier. |
| `rule.version` | `long` | Yes | Rule version at the time this event was emitted. |
| `group_hash` | `keyword` | Yes | Series identity key for grouped evaluations. |
| `data` | `flattened` | Yes | Payload from the ES\|QL query output (shape depends on your rule). |
| `status` | `keyword` | Yes | One of: `breached`, `recovered`, `no_data`. |
| `source` | `keyword` | Yes | Origin of this event (product-specific identifier). |
| `type` | `keyword` | Yes | `signal` (detect mode) or `alert` (alert mode with lifecycle). |

## Episode fields (only when `type` is `alert`)

Present only when **`type`** is **`alert`**. Omit **`episode`** on **`signal`** events.

| Field | Type | Description |
|---|---|---|
| `episode.id` | `keyword` | Episode identifier for this series. |
| `episode.status` | `keyword` | One of: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | `long` | Count of consecutive evaluations in the current **`episode.status`**. Set when status is **`pending`** or **`recovering`**; not used for **`inactive`** or **`active`** in the stored mapping. |

There is **no** top-level or nested **`duration`** field on raw **`.rule-events`** documents in this schema. Duration for triage or reporting may come from [ES\|QL views](manage-alerts/explore-alerts-discover.md), the alert UI, or your own queries over timestamps and episode identifiers.

## Mapping notes (`.rule-events`)

- The data stream uses **`dynamic: false`**: only the mapped paths above are indexed at the top level. Rely on **`data`** (flattened) for arbitrary ES\|QL output; treat paths under **`data`** as defined by your rule until you confirm them in Discover or dashboards.
- The stream is versioned and managed by {{kib}} (including ILM). Do not change mappings on managed backing indices.

## Alert action records (`.alert-actions`)

User and system **alert actions** (for example acknowledge, snooze, tag) are stored in the **`.alert-actions`** data stream. Use these documents for auditing, MTTA-style metrics, and action history.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | `date` | When the action was recorded |
| `episode.id` | `keyword` | Target episode |
| `rule.id` | `keyword` | Rule that owns the episode |
| `action.type` | `keyword` | Action type, for example `acknowledge`, `snooze`, `tag`, `fire`, **`unmatched`** |

The **`unmatched`** value indicates that no notification policy matched the episode, so no workflow ran for it under those policies. Other action types reflect user or system operations (see [Alert actions](manage-alerts/investigate-respond/alert-actions.md)).
