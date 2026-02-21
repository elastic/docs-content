---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create detection rules using Elasticsearch Query Language (ESQL) with aggregation and pipeline processing.
---

# {{esql}} rules [esql-rule-type]

## Overview

{{esql}} rules use [{{es}} Query Language ({{esql}})](elasticsearch://reference/query-languages/esql.md) to query source events and aggregate or transform data using a pipeline syntax. Query results are returned as a table where each row becomes an alert. {{esql}} rules combine the flexibility of a full query pipeline with the detection capabilities of {{elastic-sec}}.

### When to use an {{esql}} rule

{{esql}} rules are the right fit when:

* You need **aggregation, transformation, or enrichment** within the query itself, such as computing statistics, renaming fields, or filtering on calculated values.
* The detection logic requires **pipe-based processing** that KQL and EQL cannot express, such as `STATS...BY` followed by `WHERE` to filter aggregated results.
* You want to create **new computed fields** (using `EVAL`) and alert on values derived from source data rather than raw field values.

{{esql}} rules are **not** the best fit when:

* A field-value match is sufficient. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to detect ordered event sequences. Use an [EQL rule](/solutions/security/detect-and-alert/eql.md) instead.
* You want {{anomaly-detect}} without explicit query logic. Use a [{{ml}} rule](/solutions/security/detect-and-alert/machine-learning.md) instead.

### Data requirements

{{esql}} rules query {{es}} indices directly using the `FROM` command. The indices must be accessible to the user who creates or last edits the rule.

## Writing effective {{esql}} queries [craft-esql]

### Query types

{{esql}} rule queries fall into two categories that affect how alerts are generated:

#### Aggregating queries

Aggregating queries use [`STATS...BY`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md) to group and count events. Alerts contain **only** the fields returned by the query plus any new fields created during execution.

```esql
FROM logs-*
| STATS host_count = COUNT(host.name) BY host.name
| SORT host_count DESC
| WHERE host_count > 20
```

This query counts events per host and alerts on hosts with more than 20 events. Use the `BY` clause with fields you want available for searching and filtering in the Alerts table.

::::{note}
Aggregating queries may create duplicate alerts when events in the additional look-back time are counted in both the current and previous rule execution.
::::

#### Non-aggregating queries

Non-aggregating queries do not use `STATS...BY`. Alerts contain the returned source event fields, any new fields, and all other fields from the source document.

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process" AND event.id == "8a4f500d"
| LIMIT 10
```

Adding `METADATA _id, _index, _version` enables [alert deduplication](#alert-deduplication). Without it, the same source event can generate duplicate alerts across executions.

### Alert deduplication [alert-deduplication]

For non-aggregating queries, add `METADATA _id, _index, _version` after the `FROM` command to enable deduplication:

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process"
| LIMIT 50
```

Ensure you do not `DROP` or filter out `_id`, `_index`, or `_version` in subsequent pipeline steps, or deduplication fails silently.

### Query design guidelines

* **`LIMIT` and Max alerts per run interact.** The rule uses the lower of the two values. If `LIMIT` is 200 but **Max alerts per run** is 100, only 100 alerts are created.
* **Include fields you need in `BY` clauses.** For aggregating queries, only the `BY` fields appear in alerts. Fields not included are unavailable for filtering or investigation.
* **Sort non-aggregating results by `@timestamp` ascending** when using alert suppression. This ensures proper suppression when the alert count exceeds **Max alerts per run**.

### Limitations

If your {{esql}} query creates new fields that are not part of the ECS schema, they are not mapped to the alerts index. You cannot search for or filter them in the Alerts table. As a workaround, create [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md).

### Custom highlighted fields

When configuring an {{esql}} rule's **Custom highlighted fields** (in [advanced settings](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-ui-advanced-params)), you can specify any fields that the query returns. This ensures returned fields are visible in the alert details flyout during investigation.

::::{tip}
**See it in practice.** These patterns demonstrate {{esql}} detection use cases:

* **High event count per host.** An aggregating query that groups by `host.name` and fires when a host exceeds a threshold count. Useful for detecting noisy hosts or denial-of-service patterns.
* **Process execution with computed risk.** A non-aggregating query with `EVAL` that computes a custom risk score from multiple fields, alerting only when the computed score exceeds a threshold.
::::

## {{esql}} field reference [esql-fields]

The following settings are specific to {{esql}} rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

**{{esql}} query**
:   The [{{esql}} query](elasticsearch://reference/query-languages/esql.md) that defines the detection logic. Can be aggregating (with `STATS...BY`) or non-aggregating. Each row in the query result becomes an alert.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
