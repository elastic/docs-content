---
navigation_title: Event field reference
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Field reference for Kibana alerting v2 alert event documents in .alerts-events-*, including common fields, alert-only fields, and the index mapping."
---

# Kibana alerting v2 alert event field reference [alert-event-field-reference-v2]

Kibana alerting v2 rules write alert event documents to the `.alerts-events-*` data stream. This page describes the fields in each document.

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
