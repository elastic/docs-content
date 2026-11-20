---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create detection rules using Event Query Language (EQL) to detect event sequences and correlations.
---

# Event correlation (EQL) rules [eql-rule-type]

## Overview

Event correlation rules use [Event Query Language (EQL)](/explore-analyze/query-filter/languages/eql.md) to detect ordered sequences of events, single events that match complex conditions, or sequences in which an expected event doesn't happen.

When the rule detects the full sequence, it creates an EQL alert and a building block alert for each event in the sequence. To learn what each alert contains and how to triage them, refer to [](/solutions/security/detect-and-alert/triage-eql-alerts.md).

### When to use an EQL rule

EQL rules are the right fit when:

* You need to detect a sequence of events that must occur in a specific order, such as a process creation followed by a network connection from the same process.
* You want to detect missing events in a sequence, for example, a login without a matching logout within a time window.
* The detection logic involves correlating events by a shared field (such as `process.entity_id` or `host.id`) across time.
* You need richer event-level logic than KQL allows, such as filtering by event category within a sequence step.
* You need to detect an ordered sequence of alerts from other rules, rather than raw events. To learn how one rule can search the alerts that other rules create, refer to [](/solutions/security/detect-and-alert/about-building-block-rules.md#security-building-block-rules-set-up-rules-that-run-on-alert-indices).

EQL rules aren't the best fit when:

* A single-event match is sufficient. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to count how often something happens. Use a [threshold rule](/solutions/security/detect-and-alert/threshold.md) instead.
* You need aggregation, transformations, or pipe-based processing. Use an [{{esql}} rule](/solutions/security/detect-and-alert/esql.md) instead.

### Data requirements

EQL rules require at least one {{es}} index pattern or [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md). The data must include a timestamp field and an event category field. To learn how EQL uses these fields and their defaults, refer to [Required fields](/explore-analyze/query-filter/languages/eql.md#eql-required-fields).

## Writing effective EQL queries [craft-eql]

An EQL rule can use a single-event query, a sequence query, or a sequence with missing events. To learn the syntax for each, including `by`, `maxspan`, and missing events (`!`), refer to [Search for a sequence of events](/explore-analyze/query-filter/languages/eql.md#eql-search-sequence) and the [EQL syntax reference](elasticsearch://reference/query-languages/eql/eql-syntax.md), which also covers conditions and functions. 

To practice building a sequence query against sample attack data before you turn it into a rule, refer to [](/explore-analyze/query-filter/languages/example-detect-threats-with-eql.md).

<!-- CRAFT LAYER - COMMENTED OUT FOR REVIEW
### Best practices

* **Join on a field that identifies one entity.** For process activity, use `process.entity_id` instead of `process.pid`, because operating systems reuse process IDs. Joining on a shared field like `host.id` also prevents unrelated events on different hosts from matching.
* **Set `maxspan` to limit time windows.** Without a `maxspan`, events anywhere in the rule's look-back window can match, which can create noisy alerts.

::::{tip}
**See it in practice.** These prebuilt rules demonstrate different EQL patterns:

* **Suspicious MSXSL Process**: A two-step sequence correlating process creation with outbound network activity. Demonstrates the core sequence-by-entity pattern.
* **Potential Credential Access through Renamed COM+ Services DLL**: A single-event EQL query using `process.pe.original_file_name` to catch renamed binaries.
* **Startup Persistence through DLL Search Order Hijacking**: A sequence that links file creation in a specific directory to a subsequent process load, illustrating file-to-process correlation.
::::
END CRAFT LAYER -->

## Annotated examples [eql-examples]

The following examples use the [detections API](/solutions/security/detect-and-alert/using-the-api.md) request format to show how EQL rules are defined. Each example is followed by a breakdown of the EQL-specific fields. For common fields like `name`, `severity`, and `interval`, refer to the [detections API documentation]({{kib-apis}}group/endpoint-detection-engine-rules-api).

### Sequence query with shared field [eql-example-sequence]

This rule detects when `msxsl.exe` starts and then makes an outbound network connection from the same process instance, a known living-off-the-land binary (LOLBin) technique.

```json
{
  "type": "eql",
  "language": "eql",
  "name": "MSXSL network connection after process start",
  "description": "Detects msxsl.exe starting and making an outbound network connection.",
  "query": "sequence by process.entity_id [process where event.type == \"start\" and process.name == \"msxsl.exe\"] [network where event.type == \"connection\" and network.direction == \"egress\"]",
  "index": ["winlogbeat-*", "logs-endpoint.events.*"],
  "severity": "high",
  "risk_score": 73,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `type` / `language` | `"eql"` / `"eql"` | Both must be `"eql"`. Unlike custom query rules, the `language` field is fixed and not interchangeable. |
| `query` | `sequence by process.entity_id [process where ...] [network where ...]` | A two-step sequence. The `by process.entity_id` clause ensures both events came from the same process instance. The first bracket matches a process-start event for `msxsl.exe`, and the second matches an outbound network connection from that same process. |
| `index` | `["winlogbeat-*", "logs-endpoint.events.*"]` | Covers {{winlogbeat}} and {{elastic-defend}} indices. Both must contain process and network events for the sequence to match. |

### Single-event query with EQL settings [eql-example-single]

This rule detects `certutil.exe` being used to download files and demonstrates the EQL-specific settings fields.

```json
{
  "type": "eql",
  "language": "eql",
  "name": "File download via certutil",
  "description": "Detects certutil.exe being used to download files, a common LOLBin technique.",
  "query": "process where event.type == \"start\" and process.name == \"certutil.exe\" and process.args : \"-urlcache\"",
  "index": ["winlogbeat-*", "logs-endpoint.events.*"],
  "event_category_override": "event.category",
  "tiebreaker_field": "event.sequence",
  "timestamp_field": "@timestamp",
  "severity": "medium",
  "risk_score": 47,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `query` | `process where event.type == "start" and ... and process.args : "-urlcache"` | A single-event EQL query. The `:` operator performs a wildcard match on `process.args`, unlike the strict `==` equality used for other fields. |
| `event_category_override` | `"event.category"` | Specifies which field contains the event {{classification}} (such as `process`, `file`, `network`). Defaults to `event.category`. Override this when your data uses a different field name. |
| `tiebreaker_field` | `"event.sequence"` | A secondary sort field for events that share the same timestamp. Ensures deterministic event ordering in sequence queries. |
| `timestamp_field` | `"@timestamp"` | The field used for ordering events in sequences. Defaults to `@timestamp`. Different from the `timestamp_override` advanced setting, which controls the query time range. |

## EQL rule field reference [eql-fields]

The following settings appear in the **Define rule** section when creating an EQL rule. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/common-rule-settings.md).

**Index patterns or {{data-source}}**
:   The {{es}} indices or {{data-source}} the rule searches when querying for events.

**EQL query**
:   The [EQL query](elasticsearch://reference/query-languages/eql/eql-syntax.md) that defines the detection logic. Can be a single-event query, a sequence, or a sequence with missing events. Documents or sequences matching this query generate alerts.

**EQL settings** (optional)
:   Additional fields used by [EQL search](/explore-analyze/query-filter/languages/eql.md#specify-a-timestamp-or-event-category-field):

    * **Event category field**: The field containing event {{classification}} (such as `process`, `file`, or `network`). Typically a [keyword family](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) field. Defaults to `event.category`.
    * **Tiebreaker field**: A secondary field for sorting events in ascending, lexicographic order when they share the same timestamp. To learn how EQL uses this field, refer to [Specify a sort tiebreaker](/explore-analyze/query-filter/languages/eql.md#eql-search-specify-a-sort-tiebreaker).
    * **Timestamp field**: The field containing the event timestamp, used for ordering sequence events. Defaults to `@timestamp`. This is different from the **Timestamp override** advanced setting, which controls the query time range.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).
