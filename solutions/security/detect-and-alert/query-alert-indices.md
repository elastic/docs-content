---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/query-alert-indices.html
  - https://www.elastic.co/guide/en/serverless/current/security-query-alert-indices.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Query alert indices when building rule queries, dashboards, or visualizations in Elastic Security.
---

# Query alert indices [security-query-alert-indices]

You can query {{elastic-sec}} alert indices to build custom dashboards, create detection rules that correlate alerts, or export alert data for external analysis. This page explains how to query alert data correctly and provides examples for common use cases.

::::{important}
Do not modify alert index mappings. System indices contain internal configuration data—changing mappings can cause rule execution and alert indexing failures. To add custom fields to alert documents, use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead.
::::


## Alert index alias [alert-index-aliases]

Query the `.alerts-security.alerts-<space-id>` index alias, where `<space-id>` is your {{kib}} space (for example, `default`). Do not add a dash or wildcard after the space ID.

| Scope | Index pattern |
|-------|---------------|
| Single space | `.alerts-security.alerts-default` |
| All spaces | `.alerts-security.alerts-*` |

## Alert indices (internal) [alert-indices]

Alert events are stored in hidden {{es}} indices. You should query the alias (described above) rather than these internal indices directly—the alias automatically points to the correct underlying indices as they roll over.

| Type | Example | Description |
|------|---------|-------------|
| Alias (recommended) | `.alerts-security.alerts-default` | Points to all alert indices for the space. Use this for queries. |
| Internal index | `.internal.alerts-security.alerts-default-000001` | First internal index for the default space. |
| Internal index | `.internal.alerts-security.alerts-default-000002` | Second internal index (created after rollover). |

The `NNNNNN` suffix increments over time as indices roll over (starting from `000001`). New alerts are written to the latest index, but the alias spans all of them.

## Example queries [example_queries]

The following examples show common ways to query alert data. Adapt them to your space ID and field values as needed.

### Count alerts by rule name (ES|QL)

Returns the top 10 rules generating the most open alerts. Use this to identify noisy rules or prioritize tuning efforts.

```esql
FROM .alerts-security.alerts-default   // Query the alert index for the default space
| WHERE kibana.alert.workflow_status == "open"   // Filter to untriaged alerts
| STATS count = COUNT(*) BY kibana.alert.rule.name   // Group and count by rule
| SORT count DESC   // Most alerts first
| LIMIT 10   // Top 10 only
```

### Find high-severity open alerts (KQL)

Returns critical alerts that haven't been triaged. Use this in Discover, dashboards, or as a filter on the Alerts page.

```text
kibana.alert.severity: "critical" AND kibana.alert.workflow_status: "open"
```

- `kibana.alert.severity`: Filters by severity level (`low`, `medium`, `high`, `critical`)
- `kibana.alert.workflow_status`: Filters by triage state (`open`, `acknowledged`, `closed`)

### Find alerts for a specific host (KQL)

Returns all active alerts for a specific host. Useful when investigating a potentially compromised system.

```text
host.name: "web-server-01" AND kibana.alert.status: "active"
```

- `host.name`: The hostname from the original event
- `kibana.alert.status`: System status (`active` means the alert condition is ongoing)

### Find the alerts for an EQL sequence (KQL) [find-eql-sequence-alerts]

Returns an Event correlation (EQL) alert and its building block alerts, which hold the details of each event in the sequence. Use this to see what happened at each step and when. On the Alerts page, [include building block alerts](/solutions/security/detect-and-alert/about-building-block-rules.md#security-building-block-rules-view-building-block-alerts-in-the-ui) to see the results.

```text
kibana.alert.group.id: "<group-id>"
```

- `kibana.alert.group.id`: The ID that an EQL alert and its building block alerts share
- `kibana.alert.original_time`: On each building block alert, when its event happened

To learn what each of these alerts tells you, refer to [](/solutions/security/detect-and-alert/triage-eql-alerts.md).

## Correlate alerts in detection rules [rules-that-search-alerts]

A detection rule can search the alert index instead of your event data, and create an alert when several alerts happen together. For example, it can alert when one host has [building block alerts](/solutions/security/detect-and-alert/about-building-block-rules.md) from several rules, so analysts triage one alert instead of an alert for each behavior. In the rule's index patterns, enter the [alert index alias](#alert-index-aliases) for your space. For an {{esql}} rule, use the alias in the query's `FROM` command instead.

When you write the rule, check these points:

* Match only the alerts that you want to combine. The alert index holds every alert in the space, including the correlation rule's own alerts. Match the rules by `kibana.alert.rule.name`, or by `kibana.alert.rule.rule_id` if someone might rename them.
* Leave **Mark all generated alerts as "building block" alerts** cleared for the correlation rule, so that analysts see its alerts.
* Set **Runs every** and **Additional look-back time** so that together they cover how far apart the alerts can happen. An alert's `@timestamp` shows when its rule created it. If you set a [timestamp override](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) such as `event.ingested`, the rule uses the time from each alert's source event instead, so add look-back time to cover how long the other rules take to create their alerts.
* Before you enable the rule, [preview it](/solutions/security/detect-and-alert/validate-and-test-rules.md#validate-historical-data) over a time range in which the other rules created alerts.

### Correlate alerts in a threshold rule

Detects hosts triggering multiple alerts within a time window—useful for identifying systems under active attack.

Create a [threshold rule](/solutions/security/detect-and-alert/threshold.md) with:
- **Index pattern**: `.alerts-security.alerts-default`
- **Query**: `kibana.alert.workflow_status: "open"`
- **Group by**: `host.name`
- **Threshold**: Count ≥ 5 (or your preferred value)

This generates a new alert when the same host appears in 5 or more open alerts.

### Correlate building block alerts in a threshold rule [correlate-building-block-alerts]

Detects hosts that have building block alerts from three rules, each of which detects one behavior. Use this pattern when the order of the behaviors doesn't matter.

Create a [threshold rule](/solutions/security/detect-and-alert/threshold.md) with:
- **Index pattern**: `.alerts-security.alerts-default`
- **Custom query**: `kibana.alert.rule.name : ("Registry modification" or "Scheduled task created" or "Rare domain connection")`
- **Group by**: `host.name`
- **Threshold**: `3`
- **Count**: `kibana.alert.rule.name`, with **Unique values** set to `3`
- **Runs every**: 10 minutes, with 50 minutes of **Additional look-back time**

This creates an alert for each host that has building block alerts from all three rules within an hour.

### Correlate alerts in a specific order (EQL) [correlate-alerts-in-order]

Detects the same three behaviors only when they happen in order on one host. Create an [Event correlation (EQL) rule](/solutions/security/detect-and-alert/eql.md) that searches the alert index alias, with this query:

```eql
sequence by host.name with maxspan=1h
  [any where kibana.alert.rule.name == "Registry modification"]
  [any where kibana.alert.rule.name == "Scheduled task created"]
  [any where kibana.alert.rule.name == "Rare domain connection"]
```

In **EQL settings**, set **Timestamp field** to `kibana.alert.original_time` so that the sequence follows the order in which the events happened, not the order in which the rules created their alerts.

## Common alert fields [common-alert-fields]

These fields are frequently used in alert queries. For a complete list of alert fields, refer to the [Alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).

| Field | Description |
|-------|-------------|
| `kibana.alert.rule.name` | Name of the rule that generated the alert |
| `kibana.alert.severity` | Alert severity: `low`, `medium`, `high`, or `critical` |
| `kibana.alert.risk_score` | Numeric risk score (0–100) |
| `kibana.alert.workflow_status` | Triage status: `open`, `acknowledged`, or `closed` |
| `kibana.alert.status` | System status: `active` or `recovered` |
| `@timestamp` | When the alert was created |
| `host.name` | Host associated with the alert |
| `user.name` | User associated with the alert |


