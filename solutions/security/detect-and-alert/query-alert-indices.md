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

### Correlate alerts in a threshold rule

Detects hosts triggering multiple alerts within a time window—useful for identifying systems under active attack.

Create a [threshold rule](/solutions/security/detect-and-alert/threshold.md) with:
- **Index pattern**: `.alerts-security.alerts-default`
- **Query**: `kibana.alert.workflow_status: "open"`
- **Group by**: `host.name`
- **Threshold**: Count ≥ 5 (or your preferred value)

This generates a new alert when the same host appears in 5 or more open alerts.

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


