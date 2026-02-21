---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create rules using KQL or Lucene queries to detect known field values and patterns.
---

# Custom query rules [custom-query-rule-type]

## Overview

Custom query rules search your {{es}} indices using a KQL or Lucene query and generate an alert whenever one or more documents match. They are the most flexible and widely used rule type in {{elastic-sec}}.

### When to use a custom query rule

Custom query rules are the right fit when:

* You need to detect known indicators, field values, or simple boolean conditions, such as a specific process name, a registry path, or a combination of event fields.
* The detection logic can be expressed as a single query without requiring event ordering, aggregation, or comparison against external threat feeds.
* You want to reuse an existing {{kib}} saved query or Timeline query as the basis for a detection.

Custom query rules are **not** the best fit when you need to:

* Detect **sequences** of events in a specific order. Use an [event correlation (EQL) rule](/solutions/security/detect-and-alert/eql.md) instead.
* Fire only when a field value **exceeds a count**. Use a [threshold rule](/solutions/security/detect-and-alert/threshold.md) instead.
* Match events against an **external indicator feed**. Use an [indicator match rule](/solutions/security/detect-and-alert/indicator-match.md) instead.
* Detect a **field value that has never appeared before**. Use a [new terms rule](/solutions/security/detect-and-alert/new-terms.md) instead.

### Data requirements

Custom query rules require at least one {{es}} index pattern or [data view](/solutions/security/get-started/data-views-elastic-security.md) that contains the events you want to match. The indices must be accessible to the user who creates or last edits the rule, because the rule executes with that user's [API key privileges](/solutions/security/detect-and-alert/choose-the-right-rule-type.md#alerting-authorization-model).

## Writing effective queries [craft-custom-query]

### Query language

Custom query rules accept either **KQL** (Kibana Query Language) or **Lucene** syntax. KQL is the default and is generally easier to read. Use Lucene when you need regular expressions, fuzzy matching, or other features KQL does not support.

### Building the query

A good custom query is precise enough to surface true positives without excessive noise. Follow these guidelines:

* **Start narrow, then widen.** Begin with the most specific field-value pairs that identify the behavior, then relax constraints only if you miss true positives.
* **Anchor on stable fields.** Prefer fields that adversaries cannot easily change, such as `event.action`, `process.pe.original_file_name`, or `file.path`, over fields like `process.name` that can be trivially renamed.
* **Combine conditions with `and`.** Joining multiple conditions reduces false positives. For example, matching on both `process.name` and `process.args` is more precise than matching on either alone.
* **Use `or` for variant coverage.** If the same behavior can appear with different field values (for example, multiple process names), group them with `or` or use a wildcard.

### Using saved queries and Timeline queries

You can populate a custom query rule from a {{kib}} saved query or a saved Timeline:

* **Saved query (dynamic):** Select **Load saved query dynamically on each rule execution** to link the rule to the saved query. The rule always uses the current version of the saved query. You cannot edit the rule's query directly while this option is active.
* **Saved query (one-time):** Deselect the dynamic option to copy the saved query into the rule. The rule's query becomes independent, and future changes to the saved query are not inherited.
* **Timeline query:** Click **Import query from saved Timeline** to copy a Timeline's query into the rule.

### Annotated example

The following query (adapted from the prebuilt rule *Volume Shadow Copy Deleted or Resized via VssAdmin*) detects when the `vssadmin delete shadows` Windows command is executed:

```
event.action:"Process Create (rule: ProcessCreate)" and process.name:"vssadmin.exe" and process.args:("delete" and "shadows")
```

| Clause | Purpose |
|---|---|
| `event.action:"Process Create (rule: ProcessCreate)"` | Anchors the query to process-creation events reported by Sysmon, filtering out unrelated event types. |
| `process.name:"vssadmin.exe"` | Narrows to the specific binary. |
| `process.args:("delete" and "shadows")` | Requires both arguments to be present, distinguishing destructive shadow-copy deletion from benign `vssadmin` usage such as `list shadows`. |

**Index patterns:** `winlogbeat-*` (Winlogbeat ships Windows event logs to {{elastic-sec}}).

::::{tip}
**See it in practice.** These prebuilt rules use custom queries and illustrate different detection patterns:

* **Volume Shadow Copy Deleted or Resized via VssAdmin.** Matches a specific process with targeted arguments. A focused, low-noise pattern.
* **Clearing Windows Event Logs.** Uses `or` to cover multiple utilities (`wevtutil`, `powershell`) that can clear event logs. Demonstrates variant coverage.
* **Potential Process Injection via PowerShell.** Combines `process.name` with `powershell.file.script_block_text` field matching to detect in-memory injection techniques. An example of pairing process metadata with deeper content inspection.
::::

## Custom query field reference [custom-query-fields]

The following settings are specific to custom query rules. For settings shared across all rule types (severity, risk score, schedule, actions, and so on), refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

**Index patterns or data view**
:   The {{es}} indices or data view the rule queries when searching for events. Index patterns are prepopulated with the indices configured in the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) advanced setting. Alternatively, select a data view from the drop-down to use its associated index patterns and [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md).

**Custom query**
:   The KQL or Lucene query that defines the detection logic. Documents matching this query generate alerts. Use the filter bar to add structured filters alongside the query text.

**Saved query** (optional)
:   A {{kib}} saved query to use as the rule's detection logic. When loaded dynamically, the rule inherits changes to the saved query automatically. When loaded as a one-time copy, the query is embedded in the rule and can be edited independently.

**Timeline query** (optional)
:   Import a query from a saved Timeline to use as the rule's detection logic. The imported query populates the **Custom query** field.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution. It helps other users understand the rule's data dependencies.

**Related integrations** (optional)
:   Associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
