---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Learn where detection alerts are stored and how alert documents are structured.
---

# Alert storage and schema [alert-storage-and-schema]

Detection alerts are stored in hidden {{es}} indices, separate from your source event data. This page explains the index structure and the fields that make up an alert document.


## Index aliases [alert-index-aliases]

Query alerts using the index alias, not the underlying indices directly:

| Scope | Alias |
|-------|-------|
| Single space | `.alerts-security.alerts-<space-id>` (for example, `.alerts-security.alerts-default`) |
| All spaces | `.alerts-security.alerts-*` |

:::{important}
Do not add a dash or wildcard after the space ID when querying a single space.
:::


## Backing indices [backing-indices]

An index alias like `.alerts-security.alerts-default` doesn't store data itself. It points to one or more real {{es}} indices — called backing indices — where the alert documents actually live.

As alert volume grows, {{es}} creates new backing indices automatically through a process called [rollover](/manage-data/lifecycle/index-lifecycle-management/rollover.md). Each backing index has a name like `.internal.alerts-security.alerts-<space-id>-NNNNNN` (for example, `.internal.alerts-security.alerts-default-000001`), where the numeric suffix increments with each rollover. New alerts are always written to the latest backing index, but when you query the alias, the results span all of them. You don't need to know which backing index holds a particular alert.

::::{important}
Do not modify alert index mappings. These are system indices that contain internal configuration data. Changes can cause rule execution and alert indexing failures. To add custom fields, use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead.
::::


## Retention and rollover [alert-retention]

```{applies_to}
stack: ga
```

Alert indices use an {{ilm}} ({{ilm-init}}) policy that rolls over after 30 days or when the primary shard reaches 50 GB. There is no delete phase by default, which means alerts accumulate indefinitely unless you add one.

To manage alert index size, you can add a delete phase to the {{ilm-init}} policy attached to the alert indices. For example, you could configure the policy to delete alert indices that are older than 180 days. You can also reduce the rate of alert creation by narrowing rule queries, adding [exceptions](/solutions/security/detect-and-alert/rule-exceptions.md), or enabling [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).


## Legacy index alias [legacy-index-alias]

For backward compatibility, {{elastic-sec}} also maintains a `.siem-signals-<space-id>` alias. New integrations should use `.alerts-security.alerts-<space-id>`.


## Index mappings [alert-index-mappings]

Alert index mappings define which fields an alert document can contain and how {{es}} indexes them (as a keyword, date, float, and so on). These mappings are system-managed — you do not create or edit them. {{elastic-sec}} builds them automatically from three component templates, each contributing a different layer of fields.

When the detection engine initializes for a {{kib}} space, it composes these three component templates into a single index template (for example, `.alerts-security.alerts-default-index-template`). That index template controls the mappings for all alert indices in that space.

The result is that every detection alert document can contain fields from all three layers. For example, a single alert might include `host.name` (from ECS), `kibana.alert.uuid` (from the technical template), and `kibana.alert.risk_score` (from the Security template) — all in one document.

**ECS component template**
:   Provides standard {{product.ecs}} field mappings. These are the same fields you find in event indices (`logs-*`, `filebeat-*`), so alert documents share a common schema with the source events that triggered them.

    Example fields: `host.name` (keyword), `user.name` (keyword), `process.pid` (long), `source.ip` (ip), `@timestamp` (date)

**Technical component template**
:   Provides fields that the {{kib}} alerting framework uses for all rule types — not just security detection rules. These fields track alert identity, rule ownership, and execution metadata.

    Example fields: `kibana.alert.uuid` (keyword), `kibana.alert.status` (keyword), `kibana.alert.rule.uuid` (keyword), `kibana.alert.rule.execution.uuid` (keyword), `kibana.space_ids` (keyword)

**Security mappings component template**
:   Provides fields specific to {{elastic-sec}} detection alerts. These cover severity, risk scoring, alert lineage, suppression, and rule parameters. This is the layer that makes detection alerts different from alerts created by other {{kib}} rule types (like Observability threshold rules).

    Example fields: `kibana.alert.severity` (keyword), `kibana.alert.risk_score` (float), `kibana.alert.ancestors` (object), `kibana.alert.suppression.docs_count` (long), `kibana.alert.rule.parameters.query` (flattened)

### Mapping limits

| Setting | Value |
|---------|-------|
| `index.mapping.total_fields.limit` | 1700 |
| `number_of_shards` | 1 |

The 1700-field limit accommodates all ECS, technical, and Security-specific fields. If you need additional fields, use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) rather than modifying the index mappings.

::::{important}
Do not modify alert index mappings or component templates. These are system-managed resources — changes can cause rule execution failures, alert indexing errors, or data loss during upgrades. {{elastic-sec}} may update these templates between versions.
::::


## Alert document structure [alert-document-structure]

Alert documents combine fields from three sources, corresponding to the component templates described above.

### ECS fields

{{product.ecs}} fields are copied from the source event that triggered the alert. These include fields like `host.*`, `user.*`, `process.*`, `source.*`, `destination.*`, and `network.*`. The specific fields present depend on the source event and the rule type.

### Detection engine fields

The detection engine adds `kibana.alert.*` fields that describe the alert itself:

| Field | Type | Description |
|-------|------|-------------|
| `kibana.alert.uuid` | keyword | Unique identifier for the alert |
| `kibana.alert.rule.name` | keyword | Name of the rule that created the alert |
| `kibana.alert.rule.uuid` | keyword | Unique identifier for the rule |
| `kibana.alert.rule.type` | keyword | Rule type (for example, `query`, `eql`, `threshold`) |
| `kibana.alert.severity` | keyword | Alert severity: `low`, `medium`, `high`, or `critical` |
| `kibana.alert.risk_score` | float | Numeric risk score (0–100) |
| `kibana.alert.original_time` | date | The `@timestamp` from the source event |
| `kibana.alert.workflow_status` | keyword | Triage status: `open`, `acknowledged`, or `closed` |
| `kibana.alert.workflow_tags` | keyword | Tags applied during triage |
| `kibana.alert.workflow_assignee_ids` | keyword | Users assigned to investigate the alert |
| `kibana.alert.reason` | keyword | Human-readable explanation of why the alert was created |
| `kibana.alert.status` | keyword | System status: `active` or `recovered` |
| `kibana.alert.building_block_type` | keyword | Present on [building block alerts](/solutions/security/detect-and-alert/how-alerts-are-generated.md#building-block-alerts) |
| `kibana.alert.suppression.docs_count` | long | Number of suppressed events (when [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md) is active) |
| `kibana.alert.suppression.terms.field` | keyword | Fields used for suppression grouping |
| `kibana.alert.suppression.terms.value` | keyword | Values in the suppression fields |
| `kibana.alert.suppression.start` | date | Start of the suppression time window |
| `kibana.alert.suppression.end` | date | End of the suppression time window |
| `kibana.alert.depth` | long | Nesting depth of the alert (used for building block chains) |
| `kibana.alert.ancestors` | object | Lineage information linking the alert to its source documents |
| `kibana.alert.rule.parameters.*` | flattened | Rule configuration parameters (query, index patterns, threat mappings) |

For the complete field list, refer to the [Alert schema](/reference/security/fields-and-object-schemas/alert-schema.md) reference.

### Event categorization

Every detection alert has `event.kind` set to `signal`. This is the key field that identifies a document as a detection alert rather than a raw event or [external alert](/solutions/security/detect-and-alert/detection-vs-external-alerts.md).


## Querying alert documents [querying-alert-documents]

When retrieving alert data programmatically, use the `fields` option in the [search API](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) rather than relying on `_source`. This approach handles field resolution across the component template layers correctly and avoids issues with flattened or multi-valued fields.

For query examples and best practices, refer to [Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md).
