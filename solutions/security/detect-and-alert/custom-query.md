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

Custom query rules search your {{es}} indices using a KQL or Lucene query and generate an alert whenever one or more documents match. 

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

Custom query rules require at least one {{es}} index pattern or [data view](/solutions/security/get-started/data-views-elastic-security.md) that contains the events you want to match. The indices must be accessible to the user who creates or last edits the rule, because the rule executes with that user's [API key privileges](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept).

<!-- CRAFT LAYER - COMMENTED OUT FOR REVIEW
## Writing effective queries [craft-custom-query]

### Query language

Custom query rules accept either **KQL** (Kibana Query Language) or **Lucene** syntax. KQL is the default selection. Use Lucene when you need regular expressions, fuzzy matching, or other features KQL does not support.

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
END CRAFT LAYER -->

## Annotated examples [custom-query-examples]

The following examples use the [detections API](/solutions/security/detect-and-alert/using-the-api.md) request format to show how custom query rules are defined. Each example is followed by a breakdown of the custom query-specific fields. For common fields like `name`, `severity`, and `interval`, refer to the [detections API documentation]({{kib-apis}}group/endpoint-detection-engine-rules-api).

### Basic KQL query [custom-query-example-kql]

This rule detects SSH logins by `root` or `admin` users, which may indicate unauthorized access or a policy violation.

```json
{
  "type": "query",
  "language": "kuery",
  "name": "SSH login by privileged user",
  "description": "Detects SSH login events by root or admin users.",
  "query": "event.category: \"authentication\" and event.action: \"ssh_login\" and (user.name: \"root\" or user.name: \"admin\")",
  "index": ["filebeat-*", "logs-system.*"],
  "severity": "high",
  "risk_score": 73,
  "tags": ["SSH", "Authentication", "Privilege Escalation"],
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `type` | `"query"` | Identifies this as a custom query rule. |
| `language` | `"kuery"` | Uses KQL syntax. The other accepted value is `"lucene"`. |
| `query` | `event.category: "authentication" and ...` | Matches authentication events where the `event.action` is `ssh_login` and the user is `root` or `admin`. The `and`/`or` operators combine conditions in KQL. |
| `index` | `["filebeat-*", "logs-system.*"]` | Searches Filebeat and Elastic Agent system integration indices. Must match the indices where SSH events are ingested. |
| `severity` / `risk_score` | `"high"` / `73` | Reflects the security impact. Root SSH logins are high-severity in most environments. |
| `interval` / `from` | `"5m"` / `"now-6m"` | Runs every 5 minutes and looks back 6 minutes, creating a 1-minute overlap so short ingestion delays don't cause missed events. |

### Lucene query with regular expressions [custom-query-example-lucene]

This rule detects PowerShell execution with Base64-encoded commands, a technique commonly used to obfuscate malicious scripts. The regular expression requires Lucene syntax because KQL does not support regex matching.

```json
{
  "type": "query",
  "language": "lucene",
  "name": "Suspicious PowerShell encoded command",
  "description": "Detects PowerShell invocations that use the -EncodedCommand parameter.",
  "query": "process.name:powershell.exe AND process.args:/.*\\-(e|ec|en|enc|enco|encod|encode|encoded|encodedc|encodedco|encodedcom|encodedcomm|encodedcomma|encodedcomman|encodedcommand) .+/",
  "index": ["winlogbeat-*", "logs-endpoint.events.*"],
  "severity": "medium",
  "risk_score": 47,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `language` | `"lucene"` | Required for the `/.../` regex syntax in the `query`. KQL does not support regular expressions. |
| `query` | `process.name:powershell.exe AND process.args:/.../` | Uses a Lucene regex to match any truncation of the `-EncodedCommand` flag. PowerShell allows partial parameter names, so the regex covers all variants. The `AND` operator is uppercase in Lucene, unlike KQL's lowercase `and`. |
| `index` | `["winlogbeat-*", "logs-endpoint.events.*"]` | Covers Windows event logs (Winlogbeat) and Elastic Defend endpoint events. |

### KQL query with alert suppression [custom-query-example-suppression]

This rule detects failed login attempts and uses [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md) to group repeated failures by user and host, reducing alert noise during brute-force attacks.

```json
{
  "type": "query",
  "language": "kuery",
  "name": "Repeated failed login attempts",
  "description": "Detects failed authentication events grouped by user and host.",
  "query": "event.category: \"authentication\" and event.outcome: \"failure\"",
  "index": ["filebeat-*", "logs-system.*", "winlogbeat-*"],
  "severity": "medium",
  "risk_score": 47,
  "interval": "5m",
  "from": "now-6m",
  "alert_suppression": {
    "group_by": ["user.name", "host.name"],
    "duration": { "value": 5, "unit": "m" },
    "missing_fields_strategy": "suppress"
  }
}
```

| Field | Value | Purpose |
|---|---|---|
| `alert_suppression.group_by` | `["user.name", "host.name"]` | Groups matching events by user and host. All events with the same `user.name` and `host.name` within the suppression window produce a single alert instead of one per event. Accepts up to 3 fields. |
| `alert_suppression.duration` | `{ "value": 5, "unit": "m" }` | Sets the suppression window to 5 minutes. Accepted units are `s` (seconds), `m` (minutes), and `h` (hours). |
| `alert_suppression.missing_fields_strategy` | `"suppress"` | When a suppression field is missing from a document, the event is still suppressed into a single alert. Use `"doNotSuppress"` to create individual alerts for documents missing the field. |

## Custom query rule field reference [custom-query-fields]

The following settings appear in the **Define rule** section when creating a custom query rule. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/common-rule-settings.md).

**Index patterns or data view**
:   The {{es}} indices or data view the rule queries when searching for events. Index patterns are prepopulated with the indices configured in the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) advanced setting. Alternatively, select a data view from the drop-down to use its associated index patterns and [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md).

**Custom query**
:   The KQL or Lucene query that defines the main detection logic. Other fields such as filters or exceptions can be used to narrow the scope of the query.

**Saved query** (optional)
:   A {{kib}} saved query to use as the rule's detection logic. When loaded dynamically, the rule inherits changes to the saved query automatically. When loaded as a one-time copy, the query is embedded in the rule and can be edited independently.

**Timeline query** (optional)
:   Import a query from a saved Timeline to use as the rule's detection logic. The imported query populates the **Custom query** field.

**Suppress alerts by** (optional)
:   Reduce alert fatigue by consolidating multiple instances of the same event into a single alert. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).