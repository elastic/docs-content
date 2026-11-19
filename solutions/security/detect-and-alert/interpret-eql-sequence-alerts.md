---
applies_to:
  serverless:
    security: ga
  stack: ga
products:
  - id: security
  - id: cloud-serverless
description: Learn what an EQL sequence alert shows, where to find the details it leaves out, and how timestamps work so you can tell when the activity happened.
---

# Interpret EQL sequence alerts [security-interpret-eql-sequence-alerts]

Sequence rules can detect attacks that unfold in steps. A sequence rule is an [EQL rule](/solutions/security/detect-and-alert/eql.md) with a sequence query, which looks for events that happen in a set order. For example, a sequence rule can detect when the `msxsl.exe` program starts and then connects to an external address. Each event might be harmless on its own, but together they can be a sign of an attack.

A sequence alert summarizes the whole sequence, and the details of each event are in separate building block alerts. This page explains what each kind of alert shows, and how to tell when the activity happened.

## Sequence alert details [eql-sequence-alerts-details]

A sequence alert shows the values that every event in the sequence has in common, which identifies the host, user, or process that the activity involves. Values that differ between events, or that only some events have, appear in the building block alerts instead. For example:

* If every event happened on the same host, the sequence alert shows the host's name.
* If each event has a different command line, the sequence alert doesn't show a command line.
* If the query links events with `sequence by`, such as `sequence by process.entity_id`, every event has the same value for that field, so the sequence alert always shows it.

### Event details in building block alerts [eql-sequence-alerts-building-blocks]

The details of each event are in building block alerts. For each event in the sequence, the rule creates a building block alert that contains all the fields of that event. The Alerts table hides building block alerts by default. To view them, refer to [View the events in an EQL sequence](/solutions/security/detect-and-alert/manage-detection-alerts.md#eql-sequence-events).

Other rules can also create building block alerts. A [building block rule](/solutions/security/detect-and-alert/about-building-block-rules.md) marks every alert it creates as a building block alert, not only the alerts for events in a sequence.

The following example query detects `msxsl.exe` starting and then connecting to an external address from the same process:

```eql
sequence by process.entity_id
  [process where event.type == "start" and process.name == "msxsl.exe"]
  [network where event.type == "connection" and network.direction == "egress"]
```

When this query matches, the rule creates a sequence alert and two building block alerts, one for each event. The alerts contain values like these:

| Field | Building block alert (process start) | Building block alert (network connection) | Sequence alert |
|---|---|---|---|
| `host.name` | `win-01` | `win-01` | `win-01` |
| `process.entity_id` | `abc123` | `abc123` | `abc123` |
| `process.args` | `msxsl.exe`, `payload.xml`, `style.xsl` | Not present | Not present |
| `destination.ip` | Not present | `203.0.113.10` | Not present |

A sequence query can include a step that checks that an event didn't happen, written with `!`. What the rule creates for that step depends on your version:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The rule doesn't create a building block alert for that step, because no event matched it.
* {applies_to}`stack: ga 9.0-9.1` The rule creates an empty building block alert for that step. Because the empty alert has no values in common with the others, the sequence alert contains none of the events' fields.

## How timestamps work on EQL sequence alerts [eql-sequence-alerts-time]

The times on a sequence alert show when the rule detected the sequence, not when the events happened. To build an incident timeline or find when the activity happened, check the `kibana.alert.original_time` field on each building block alert, which shows when its event happened.

In the previous example, the alerts have these times:

| Alert | `kibana.alert.original_time` | `@timestamp` |
|---|---|---|
| Building block alert (process start) | Nov 12, 08:15:02 | Nov 16, 10:00:05 |
| Building block alert (network connection) | Nov 12, 08:15:04 | Nov 16, 10:00:05 |
| Sequence alert | Nov 16, 10:00:05 | Nov 16, 10:00:05 |

In the table, only the `kibana.alert.original_time` values on the building block alerts show when the events happened. The other times show when the rule created the alerts.

The rule detected this sequence four days after it happened. A gap like this can happen when events arrive late, for example because an agent was offline, and the rule uses a [timestamp override](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) such as `event.ingested` to find late events. A timestamp override doesn't change any of the times on the alerts. If you use the sequence alert's time as the time of the activity, you might search for related activity in the wrong time range.

## Next steps [eql-sequence-alerts-next-steps]

* To review the building block alerts for a sequence alert, refer to [View the events in an EQL sequence](/solutions/security/detect-and-alert/manage-detection-alerts.md#eql-sequence-events).
* To search alerts with queries, including building block alerts, refer to [Find the alerts for an EQL sequence](/solutions/security/detect-and-alert/query-alert-indices.md#find-eql-sequence-alerts).
* To write and tune sequence queries, refer to [Event correlation (EQL) rules](/solutions/security/detect-and-alert/eql.md).
