---
applies_to:
  serverless:
    security: ga
  stack: ga
products:
  - id: security
  - id: cloud-serverless
description: Triage Event correlation (EQL) alerts in Elastic Security. Check what an EQL alert shows, review each event in its building block alerts, and find when the activity happened.
---

# Triage EQL alerts [security-triage-eql-alerts]

[Event correlation (EQL) rules](/solutions/security/detect-and-alert/eql.md) can detect attacks that unfold in steps when they use a sequence query, which looks for events that happen in a set order. For example, an EQL rule can detect when the `msxsl.exe` program starts and then connects to an external address. Each event might be harmless on its own, but together they can be a sign of an attack.

When a sequence matches, the rule creates an EQL alert that summarizes the whole sequence, and a building block alert for each event. To triage an EQL alert, check what the alert shows, review each event in its building block alerts, and find when the activity happened.

## Check what the EQL alert shows [eql-sequence-alerts-details]

An EQL alert shows the values that every event in the sequence has in common, which identifies the host, user, or process that the activity involves. Values that differ between events, or that only some events have, appear in the building block alerts instead. For example:

* If every event happened on the same host, the EQL alert shows the host's name.
* If each event has a different command line, the EQL alert doesn't show a command line.
* If the query links events with `sequence by`, such as `sequence by process.entity_id`, every event has the same value for that field, so the EQL alert always shows it.

Other rules can also create [building block alerts](/solutions/security/detect-and-alert/about-building-block-rules.md). If you select **Mark all generated alerts as "building block" alerts** for a rule, every alert that the rule creates is a building block alert, not only the alerts for events in a sequence.

The following example query detects `msxsl.exe` starting and then connecting to an external address from the same process:

```eql
sequence by process.entity_id
  [process where event.type == "start" and process.name == "msxsl.exe"]
  [network where event.type == "connection" and network.direction == "egress"]
```

When this query matches, the rule creates an EQL alert and two building block alerts, one for each event. The alerts contain values like these:

| Field | Building block alert (process start) | Building block alert (network connection) | EQL alert |
|---|---|---|---|
| `host.name` | `win-01` | `win-01` | `win-01` |
| `process.entity_id` | `abc123` | `abc123` | `abc123` |
| `process.args` | `msxsl.exe`, `payload.xml`, `style.xsl` | Not present | Not present |
| `destination.ip` | Not present | `203.0.113.10` | Not present |

A sequence query can include a step that checks that an event didn't happen, written with `!`. What the rule creates for that step depends on your version:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The rule doesn't create a building block alert for that step, because no event matched it.
* {applies_to}`stack: ga 9.0-9.1` The rule creates an empty building block alert for that step. Because the empty alert has no values in common with the others, the EQL alert contains none of the events' fields.

## Review each event in the sequence [eql-sequence-events]

To see what happened at each step of the sequence, review the EQL alert's building block alerts:

| Method | How to do it |
|--------|--------------|
| Timeline | Select {icon}`timeline` **Investigate in timeline** for the EQL alert. Timeline shows the EQL alert and its building block alerts. If the rule uses a Timeline template, Timeline uses the template's query instead. |
| Alerts table | Select **Additional filters** → **Include building block alerts**, then filter by the EQL alert's group ID, for example `kibana.alert.group.id: "<group-id>"`. |

On each building block alert, `kibana.alert.group.index` shows the event's position in the sequence, starting from `0`.

## Find when the activity happened [eql-sequence-alerts-time]

The times on an EQL alert show when the rule detected the sequence, not when the events happened. To build an incident timeline or find when the activity happened, check the `kibana.alert.original_time` field on each building block alert, which shows when its event happened.

In the previous example, the alerts have these times:

| Alert | `kibana.alert.original_time` | `@timestamp` |
|---|---|---|
| Building block alert (process start) | Nov 12, 08:15:02 | Nov 16, 10:00:05 |
| Building block alert (network connection) | Nov 12, 08:15:04 | Nov 16, 10:00:05 |
| EQL alert | Nov 16, 10:00:05 | Nov 16, 10:00:05 |

In the table, only the `kibana.alert.original_time` values on the building block alerts show when the events happened. The other times show when the rule created the alerts.

The rule detected this sequence four days after it happened. A gap like this can happen when events arrive late, for example because an agent was offline, and the rule uses a [timestamp override](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) such as `event.ingested` to find late events. A timestamp override doesn't change any of the times on the alerts. If you use the EQL alert's time as the time of the activity, you might search for related activity in the wrong time range.
