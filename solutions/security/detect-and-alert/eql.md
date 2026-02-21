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

Event correlation rules use [Event Query Language (EQL)](elasticsearch://reference/query-languages/eql/eql-syntax.md) to detect ordered sequences of events, single events with complex conditions, or the absence of expected events. EQL is purpose-built for event-based data and excels at expressing time-ordered relationships that other query languages cannot.

### When to use an EQL rule

EQL rules are the right fit when:

* You need to detect a **sequence** of events that must occur in a specific order, such as a process creation followed by a network connection from the same process.
* You want to detect **missing events** in a sequence, for example, a login that is never followed by a logout within a time window.
* The detection logic involves correlating events by a **shared field** (such as `process.entity_id` or `host.id`) across time.
* You need richer event-level logic than KQL allows, such as filtering by event category within a sequence step.

EQL rules are **not** the best fit when:

* A single-event match is sufficient. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to count how often something happens. Use a [threshold rule](/solutions/security/detect-and-alert/threshold.md) instead.
* You need aggregation, transformations, or pipe-based processing. Use an [{{esql}} rule](/solutions/security/detect-and-alert/esql.md) instead.

### Data requirements

EQL rules require at least one {{es}} index pattern or [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md). The indexed data must include a timestamp field (defaults to `@timestamp`) and an event category field (defaults to `event.category`). Sequence queries also benefit from a tiebreaker field to resolve events that share the same timestamp.

## Writing effective EQL queries [craft-eql]

### Sequence queries

Sequence queries are the signature capability of EQL. A sequence defines two or more event conditions that must occur in order, optionally joined by a shared field:

```eql
sequence by process.entity_id
  [process where event.type in ("start", "process_started")
    and process.name == "msxsl.exe"]
  [network where event.type == "connection"
    and process.name == "msxsl.exe"
    and network.direction == "outgoing"]
```

| Clause | Purpose |
|---|---|
| `sequence by process.entity_id` | Correlates events that share the same process entity, ensuring the network event came from the same process instance that started. |
| First `[ ]` bracket | Matches the process-start event for `msxsl.exe`. |
| Second `[ ]` bracket | Matches an outbound network connection from the same `msxsl.exe` process. |

The rule generates a single alert when the full sequence is detected.

### Single-event queries

EQL also supports single-event queries when you need EQL-specific syntax features, such as function calls or the `wildcard` function:

```eql
process where event.type == "start"
  and process.name == "certutil.exe"
  and process.args : "-urlcache"
```

### Missing event detection

The `!` (missing events) syntax detects events that should have occurred but did not:

```eql
sequence by user.name with maxspan=1h
  [authentication where event.outcome == "success"]
  ![authentication where event.action == "logout"]
```

This detects a successful login that is never followed by a logout within one hour.

### Best practices

* **Use `by` clauses for precision.** Joining on a shared field like `process.entity_id` or `host.id` prevents unrelated events on different hosts from matching.
* **Set `maxspan` to limit time windows.** Without a `maxspan`, a sequence can match events that are days apart, generating noisy alerts.
* **Order conditions from most specific to least.** Put the rarest event first to reduce the number of partial sequences the engine must track.

::::{tip}
**See it in practice.** These prebuilt rules demonstrate different EQL patterns:

* **Suspicious MSXSL Process**: A two-step sequence correlating process creation with outbound network activity. Demonstrates the core sequence-by-entity pattern.
* **Potential Credential Access through Renamed COM+ Services DLL**: A single-event EQL query using `process.pe.original_file_name` to catch renamed binaries.
* **Startup Persistence through DLL Search Order Hijacking**: A sequence that links file creation in a specific directory to a subsequent process load, illustrating file-to-process correlation.
::::

## EQL field reference [eql-fields]

The following settings are specific to EQL rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

**Index patterns or {{data-source}}**
:   The {{es}} indices or {{data-source}} the rule searches when querying for events.

**EQL query**
:   The [EQL query](elasticsearch://reference/query-languages/eql/eql-syntax.md) that defines the detection logic. Can be a single-event query, a sequence, or a sequence with missing events. Documents or sequences matching this query generate alerts.

**EQL settings** (optional)
:   Additional fields used by [EQL search](/explore-analyze/query-filter/languages/eql.md#specify-a-timestamp-or-event-category-field):

    * **Event category field**: The field containing event {{classification}} (such as `process`, `file`, or `network`). Typically a [keyword family](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) field. Defaults to `event.category`.
    * **Tiebreaker field**: A secondary field for sorting events in ascending, lexicographic order when they share the same timestamp.
    * **Timestamp field**: The field containing the event timestamp, used for ordering sequence events. Defaults to `@timestamp`. This is different from the **Timestamp override** advanced setting, which controls the query time range.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
