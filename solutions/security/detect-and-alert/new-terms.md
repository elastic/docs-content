---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create detection rules that alert when a field value appears for the first time in a history window.
---

# New terms rules [new-terms-rule-type]

## Overview

New terms rules detect the first appearance of a field value (or combination of field values) within a configurable history window. The rule compares each value it finds during its current execution against a historical baseline, and generates an alert only when the value has never appeared in that baseline period.

### When to use a new terms rule

New terms rules are the right fit when:

* You want to detect **first-seen activity**, such as a user logging in from a new country, a process executing for the first time on a host, or a new domain appearing in DNS logs.
* The threat signal is **novelty**, not a specific pattern or count.
* You want to combine up to three fields to detect **novel combinations**, such as a `host.ip` and `user.name` pair that has never been observed together before.

New terms rules are **not** the best fit when:

* You are looking for a known bad value. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to detect spikes in volume. Use a [threshold rule](/solutions/security/detect-and-alert/threshold.md) instead.
* You want statistical {{anomaly-detect}} without defining explicit fields. Use a [{{ml}} rule](/solutions/security/detect-and-alert/machine-learning.md) instead.

### Data requirements

New terms rules require at least one {{es}} index pattern or [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md) with a sufficient history of events. The history window must contain enough data to establish a reliable baseline. A window that is too short leads to excessive false positives as many values appear "new".

## Writing effective new terms rules [craft-new-terms]

### Selecting fields

Select the field whose novelty you want to detect. Fields with moderate cardinality work best:

* **Good candidates:** `source.geo.country_name`, `process.executable`, `dns.question.name`, `user.name`
* **Poor candidates:** High-cardinality fields like `event.id` or `_id` (nearly every value is unique, so nearly every event triggers an alert).

### Multi-field combinations

You can select up to three fields to detect novel combinations. For example, selecting `host.name` and `user.name` generates an alert when a user logs in to a host they have never used before, even if both the user and host are individually well-known.

::::{important}
Each unique combination of values is evaluated separately. A document with `host.name: ["host-1", "host-2"]` and `user.name: ["user-1", "user-2", "user-3"]` produces 6 (2x3) combinations. The rule evaluates a maximum of 100 unique combinations per document. Fields with large arrays of values may produce incorrect results.
::::

### Sizing the history window

The **History Window Size** determines how far back the rule looks to decide whether a term is new. The window must be larger than the rule interval plus any additional look-back time.

| Window size | Best for | Trade-off |
|---|---|---|
| 1-7 days | Fast-moving environments, high-volume data | More false positives from values that are infrequent |
| 7-30 days | General-purpose detection | Balanced coverage |
| 30-90 days | Detecting truly rare first appearances | Higher resource usage, slower execution |

### Best practices

* **Start with a longer history window and shorten it** as you understand your data's baseline patterns.
* **Pair with exceptions** to suppress known-benign first appearances, such as expected new employees or scheduled system changes.
* **Monitor rule execution time.** Large history windows on high-volume indices can increase execution time significantly.

::::{tip}
**See it in practice.** These prebuilt rules use new terms detection:

* **First Time Seen Commonly Exploited Remote Access Tool Execution.** Detects the first execution of a known remote access tool on any host, surfacing tools that may have been recently deployed by an adversary.
* **First Occurrence of User Agent For a GitHub Personal Access Token (PAT).** Detects a new user agent string associated with a GitHub PAT, which may indicate token compromise.
* **First Time Seen Google Workspace OAuth Login from Third-Party Application.** Detects novel third-party OAuth application logins, surfacing potential unauthorized integrations.
::::

## New terms field reference [new-terms-fields]

The following settings are specific to new terms rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

**Index patterns or {{data-source}}**
:   The {{es}} indices or {{data-source}} the rule searches.

**Custom query**
:   The KQL or Lucene query used to filter events before evaluating new terms. Only matching documents are checked for new field values.

**Fields**
:   The field (or up to three fields) to check for new terms. When multiple fields are selected, the rule detects novel combinations of their values.

**History Window Size**
:   The time range (in minutes, hours, or days) to search for historical occurrences of a term. A term is considered new only if it does not appear in the history window outside of the current rule interval and additional look-back time.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
