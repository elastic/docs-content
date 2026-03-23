---
navigation_title: Event field reference
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Field reference for Kibana alerting v2 alert event documents in .rule-events, including common fields, alert-only fields, and the index mapping."
---

# Kibana alerting v2 alert event field reference [alert-event-field-reference-v2]

Kibana alerting v2 rules write alert event documents to the **`.rule-events`** data stream. This page describes the fields in each document.

## Common fields

| Field | Type | Description |
|---|---|---|
| `@timestamp` | `date` | When this alert event document was written |
| `scheduled_timestamp` | `date` | The scheduled execution timestamp for the rule run |
| `rule.id` | `keyword` | The rule identifier |
| `rule.version` | `long` | The rule version at the time this event was emitted |
| `group_hash` | `keyword` | Series identity key |
| `data` | `flattened` | Event payload containing the ES\|QL query output |
| `status` | `keyword` | Event status: `breached`, `recovered`, or `no_data` |
| `source` | `keyword` | Source of this event |
| `type` | `keyword` | Event type: `signal` or `alert` |

## Alert-only fields

| Field | Type | Description |
|---|---|---|
| `episode.id` | `keyword` | The episode identifier |
| `episode.status` | `keyword` | Current episode state: `inactive`, `pending`, `active`, or `recovering` |
| `episode.status_count` | `long` | Count of consecutive evaluations in the current status |

::::{note}
**SME follow-up:** Whether **`duration`** appears on the raw alert event document in **`.rule-events`** (versus only in aggregated or episode views) is not finalized in this reference. Confirm with engineering before documenting `duration` in the raw event table.
::::

## Index mapping (`.rule-events`)

The **`.rule-events`** data stream uses mappings defined by the alerting v2 storage layer. Treat `data` as **flattened** for arbitrary query output; avoid relying on undocumented subfields until they are listed in product reference material.

## Alert action records (`.alert-actions`)

User and system **alert actions** (for example acknowledge, snooze, tag) are stored in the **`.alert-actions`** data stream. Use these documents for auditing, MTTA-style metrics, and action history.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | `date` | When the action was recorded |
| `episode.id` | `keyword` | Target episode |
| `rule.id` | `keyword` | Rule that owns the episode |
| `action.type` | `keyword` | Action type, for example `acknowledge`, `snooze`, `tag`, `fire`, **`unmatched`** |

The **`unmatched`** value indicates a dispatcher outcome where the episode did not match any notification policy. Other action types reflect user or system operations (see [Alert actions](manage-alerts/investigate-respond/alert-actions.md)).
