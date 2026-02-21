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

### When to use an indicator match rule

Indicator match rules are the right fit when:

* You maintain an index of **known threat indicators** (IP addresses, domains, file hashes, URLs) and want to detect when any of them appear in your event data.
* You need to compare fields across **two separate indices** (source events and threat intelligence).
* You want alerts automatically **enriched** with indicator metadata, such as threat type, confidence, and source feed.

Indicator match rules are **not** the best fit when:

* You are matching against values within the same index. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to detect event sequences or ordering. Use an [EQL rule](/solutions/security/detect-and-alert/eql.md) instead.
* Your indicators are in a flat file rather than an {{es}} index. First [upload them as a value list](#using-value-lists) or import them through the {{ml-app}} {{data-viz}}.

### Data requirements

Indicator match rules require:

* **Source event indices** containing the security events you want to scan.
* **Indicator indices** containing threat intelligence data. Data in these indices must be [ECS compatible](/reference/security/fields-and-object-schemas/siem-field-reference.md) and must contain a `@timestamp` field.

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

### Using value lists as indicator indices [using-value-lists]

You can use [value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md) as the indicator index. This is useful when you have a flat list of indicators (IPs, domains, hashes) that you want to match against without creating a full indicator index:

1. Upload a value list of indicators.
2. In the **Indicator index patterns** field, enter `.items-<{{kib}} space>` (the hidden index where value lists are stored).
3. In the **Indicator index query** field, enter `list_id : <your-list-name>`.
4. In **Indicator mapping**, set the **Indicator index field** to the list type (`keyword`, `text`, or `IP`).

### Best practices

* **Keep indicator indices current.** Stale indicators generate false positives and waste analyst time.
* **Use the Indicator prefix override** advanced setting if your indicator data uses a non-standard field structure (default is `threat.indicator`).
* **Create Timeline templates** before building indicator match rules. When investigating alerts in Timeline, query values are automatically replaced with corresponding alert field values.

::::{tip}
**See it in practice.** These prebuilt rules use indicator matching:

* **Threat Intel Indicator Match:** The foundational indicator match rule that compares source events against threat intelligence indices across multiple field types (IP, domain, hash).
* **Threat Intel Hash Indicator Match:** A focused variant matching file hashes (`file.hash.sha256`, `file.hash.md5`) against indicator indices for malware detection.
::::

## Indicator match field reference [indicator-match-fields]

The following settings are specific to indicator match rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

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
    * **MATCHES / DOES NOT MATCH**: {applies_to}`stack: ga 9.2` Whether the values should match or not match. At least one `MATCHES` entry is required.
    * **Indicator index field**: A field from your threat indicator index.

    Multiple mapping entries can be combined with `AND` and `OR` clauses. Only single-value fields are supported.

**Suppress alerts** (optional)
:   Reduce repeated or duplicate alerts. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
