---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Detect security events that match known threat indicators from threat intelligence feeds.
---

# Indicator match rules [indicator-match-rule-type]

## Overview

Indicator match rules continuously compare field values in your security event indices against field values in threat indicator indices. When a match is found, an alert is generated, enriched with metadata from the matched indicator. This makes indicator match rules the primary mechanism for operationalizing threat intelligence feeds within {{elastic-sec}}.

### Limitations

Indicator match rules provide a powerful capability to search your security data; however, their queries can consume significant deployment resources. When creating an indicator match rule, limit the time range of the indicator index query to the minimum period necessary for the desired rule coverage. For example, the default indicator index query `@timestamp > "now-30d/d"` searches specified indicator indices for indicators ingested during the past 30 days and rounds the query start time down to the nearest day (resolves to UTC `00:00:00`). Without this limitation, the rule includes all of the indicators in your indicator indices, which may extend the time it takes for the indicator index query to complete.

:::{admonition} Support restrictions
Indicator match rules have two additional constraints:

* **Cold and frozen tier data is not supported** - Data in these tiers must be older than the rule's query time range. If your data has unreliable timestamps, exclude cold and frozen tier data using a Query DSL filter.
* **Look-back time is limited to 24 hours** - Rules with an additional look-back time greater than 24 hours are not supported.
:::

### When to use an indicator match rule

Indicator match rules are the right fit when:

* You maintain an index of **known threat indicators** (IP addresses, domains, file hashes, URLs) and want to detect when any of them appear in your event data.
* You need to compare fields across **two separate indices** (source events and threat intelligence).
* You want alerts automatically **enriched** with indicator metadata, such as threat type, confidence, and source feed.

Indicator match rules are **not** the best fit when:

* You need to join data from multiple sources with transformations, aggregations, or complex filtering. Use an [{{esql}} rule](/solutions/security/detect-and-alert/esql.md) with [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) for more flexible cross-index queries.
* You need to detect event sequences or ordering. Use an [EQL rule](/solutions/security/detect-and-alert/eql.md) instead.
* Your indicators are in a flat file rather than an {{es}} index. First [upload them as a value list](#using-value-lists) or import them through the {{ml-app}} {{data-viz}}.

### Data requirements

Indicator match rules require:

* **Source event indices** containing the security events you want to scan.
* **Indicator indices** containing threat intelligence data. Data in these indices must be [ECS compatible](/reference/security/fields-and-object-schemas/siem-field-reference.md) and must contain a `@timestamp` field.

## Using value lists as indicator indices [using-value-lists]

You can use [value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md) as the indicator index. This is useful when you have a flat list of indicators (IPs, domains, hashes) that you want to match against without creating a full indicator index:

1. Upload a value list of indicators.
2. In the **Indicator index patterns** field, enter `.items-<{{kib}} space>` (the hidden index where value lists are stored).
3. In the **Indicator index query** field, enter `list_id : <your-list-name>`.
4. In **Indicator mapping**, set the **Indicator index field** to the list type (`keyword`, `text`, or `IP`).

<!-- CRAFT LAYER - COMMENTED OUT FOR REVIEW
## Writing effective indicator match rules [craft-indicator-match]

### Designing threat mappings

Threat mappings define which fields to compare between your source events and indicator indices. Good mappings are:

* **Specific:** Use the most specific fields available when mapping. For example, map `destination.ip` to `threat.indicator.ip` rather than a generic text field.
* **Combined with `AND`:** Join multiple mapping entries to increase precision. Requiring both `source.ip` and `destination.port` to match narrows results to truly relevant hits.
* **Scoped with `DOES NOT MATCH`:** {applies_to}`stack: ga 9.2` After defining matching conditions, add `DOES NOT MATCH` entries to exclude known-safe values. At least one `MATCHES` entry is required.

### Indicator index query

The default indicator index query `@timestamp > "now-30d/d"` limits matches to indicators ingested in the past 30 days. Adjust this window based on your threat intelligence freshness requirements:

* **Shorter window (7-14 days):** Reduces stale matches but may miss long-lived indicators.
* **Longer window (60-90 days):** Catches more indicators but increases the volume of matches and rule execution time.

### Best practices

* **Keep indicator indices current.** Stale indicators generate false positives and waste analyst time.
* **Use the Indicator prefix override** advanced setting if your indicator data uses a non-standard field structure (default is `threat.indicator`).
* **Create Timeline templates** before building indicator match rules. When investigating alerts in Timeline, query values are automatically replaced with corresponding alert field values.

::::{tip}
**See it in practice.** These prebuilt rules use indicator matching:

* **Threat Intel Indicator Match:** The foundational indicator match rule that compares source events against threat intelligence indices across multiple field types (IP, domain, hash).
* **Threat Intel Hash Indicator Match:** A focused variant matching file hashes (`file.hash.sha256`, `file.hash.md5`) against indicator indices for malware detection.
::::
END CRAFT LAYER -->

## Annotated examples [indicator-match-examples]

The following examples use the [detections API](/solutions/security/detect-and-alert/using-the-api.md) request format to show how indicator match rules are defined. Each example is followed by a field-by-field breakdown.

### IP-based indicator match [indicator-match-example-ip]

This rule matches outbound network connections against a threat intelligence feed of known malicious IP addresses.

```json
{
  "type": "threat_match",
  "language": "kuery",
  "name": "Network connection to known malicious IP",
  "description": "Matches outbound network events against a threat intelligence feed of malicious IPs.",
  "query": "event.category: \"network\" and network.direction: \"egress\"",
  "index": ["packetbeat-*", "filebeat-*", "logs-endpoint.events.*"],
  "threat_index": ["filebeat-threatintel-*"],
  "threat_query": "@timestamp >= \"now-30d\"",
  "threat_mapping": [
    {
      "entries": [
        {
          "field": "destination.ip",
          "type": "mapping",
          "value": "threat.indicator.ip"
        }
      ]
    }
  ],
  "threat_indicator_path": "threat.indicator",
  "severity": "critical",
  "risk_score": 99,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `type` | `"threat_match"` | Identifies this as an indicator match rule. |
| `query` | `event.category: "network" and network.direction: "egress"` | Filters source events to outbound network connections. Only these events are compared against indicators. Uses `"kuery"` or `"lucene"`, the same query languages available in custom query rules. |
| `threat_index` | `["filebeat-threatintel-*"]` | The index patterns containing threat intelligence indicators. |
| `threat_query` | `@timestamp >= "now-30d"` | Limits indicator matches to indicators ingested in the past 30 days. Shorter windows reduce stale matches but may miss long-lived indicators. Longer windows increase coverage at the cost of execution time. |
| `threat_mapping` | `[{ "entries": [{ "field": ..., "type": "mapping", "value": ... }] }]` | Maps `destination.ip` from source events to `threat.indicator.ip` in the indicator index. When values match, an alert is generated and enriched with indicator metadata. |
| `threat_indicator_path` | `"threat.indicator"` | The field path prefix for indicator data in the indicator index. Defaults to `threat.indicator`. Override when your indicator data uses a different field structure. |

### File hash match with AND logic and performance tuning [indicator-match-example-hash]

This rule matches file creation events against threat intelligence by both SHA-256 hash and file name, requiring both fields to match. Performance tuning fields control parallelism and batch size.

```json
{
  "type": "threat_match",
  "language": "kuery",
  "name": "Known malware file hash detected",
  "description": "Matches file creation events against threat intelligence by SHA-256 hash and file name.",
  "query": "event.category: \"file\" and event.type: \"creation\"",
  "index": ["logs-endpoint.events.*", "winlogbeat-*"],
  "threat_index": ["filebeat-threatintel-*"],
  "threat_query": "@timestamp >= \"now-30d\"",
  "threat_mapping": [
    {
      "entries": [
        {
          "field": "file.hash.sha256",
          "type": "mapping",
          "value": "threat.indicator.file.hash.sha256"
        },
        {
          "field": "file.name",
          "type": "mapping",
          "value": "threat.indicator.file.name"
        }
      ]
    }
  ],
  "concurrent_searches": 5,
  "items_per_search": 500,
  "severity": "critical",
  "risk_score": 99,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `threat_mapping[0].entries` | Two entries in one object | Multiple entries within a single `entries` object are combined with AND logic, so both the SHA-256 hash and file name must match. Separate `entries` objects (sibling array items) use OR logic. |
| `concurrent_searches` | `5` | The number of indicator searches to run in parallel. Increasing this value can speed up rule execution for large indicator indices at the cost of higher resource usage. |
| `items_per_search` | `500` | The number of indicators to include in each search request. Larger batches reduce the total number of searches but increase per-search memory usage. |

## Indicator match field reference [indicator-match-fields]

The following settings are specific to indicator match rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/common-rule-settings.md).

**Source**
:   The index patterns or {{data-source}} that store your source event documents. Prepopulated with indices from the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) advanced setting.

**Custom query**
:   The query and filters used to retrieve source event documents. Field values in matching documents are compared against indicator values according to the threat mapping. Defaults to `*:*` (all documents).

**Indicator index patterns**
:   The index patterns that store threat indicator documents. Prepopulated with indices from the [`securitySolution:defaultThreatIndex`](/solutions/security/get-started/configure-advanced-settings.md#update-threat-intel-indices) advanced setting.

**Indicator index query**
:   The query used to retrieve indicator documents. Defaults to `@timestamp > "now-30d/d"`, which searches for indicators ingested in the past 30 days.

**Indicator mapping**
:   Threat mapping conditions that compare values in source event fields with values in indicator fields. Configure:

    * **Field**: A field from your source event indices.
    * {applies_to}`stack: ga 9.2` **MATCHES / DOES NOT MATCH**: Whether the values should match or not match. At least one `MATCHES` entry is required.

       :::{note}
       Define matching (`MATCHES`) conditions first, then narrow down your results by adding `DOES NOT MATCH` conditions to exclude field values you want to ignore. Mapping entries that only use `DOES NOT MATCH` are not supported. At least one entry must have a `MATCHES` condition.
       :::

    * **Indicator index field**: A field from your threat indicator index.

    Multiple mapping entries can be combined with `AND` and `OR` clauses. Only single-value fields are supported.

**Suppress alerts** (optional)
:   Reduce repeated or duplicate alerts. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/prebuilt-rule-components.md#rule-prerequisites).
