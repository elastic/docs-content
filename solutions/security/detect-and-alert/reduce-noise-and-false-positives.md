---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: "Compare and choose the right mechanism to reduce alert noise: tuning, exceptions, suppression, or snoozing."
---

# Reduce noise and false positives

{{elastic-sec}} provides four distinct mechanisms for managing alert noise, each operating at a different point in the pipeline from raw events to analyst notification. Selecting the wrong tool for your situation reduces effectiveness and can obscure real threats. This page explains when to use each mechanism and how they work together.

## Select the right approach

Use the following table to identify which mechanism matches your situation. If multiple rows apply, refer to [Using them together](#using-them-together).

| Your situation | Use this | What it does |
|---|---|---|
| The rule fires on activity that isn't suspicious in any environment (for example, the query is too broad and catches normal admin behavior) | [Tune rule logic](/solutions/security/detect-and-alert/tune-detection-rules.md) | Refine the query, threshold, or schedule so the rule only matches what it should |
| The rule correctly identifies a pattern, but a specific known-safe case keeps firing in your environment (for example, an SCCM server triggers your remote service creation rule nightly) | [Exception](/solutions/security/detect-and-alert/rule-exceptions.md) | Permanently suppress alerts matching specific field values. The rule logic stays unchanged. |
| The rule generates many alerts for the same entity in a short window (for example, a compromised host triggers the same rule every 5 minutes for an hour) | [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md) | After the first alert for a given field value, suppress further alerts for a defined time window |
| You need to temporarily stop receiving notifications during scheduled maintenance or a known event | [Snooze actions](/solutions/security/detect-and-alert/snooze-rule-actions.md) | The rule runs and alerts are still created and stored. Only notifications (email, Slack, webhooks) are paused. |
| A specific known-safe process or user keeps appearing across many different rules (for example, your vulnerability scanner triggers dozens of rules) | [Shared exception list](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md) | Apply one exception list across multiple rules simultaneously, avoiding duplicate exceptions rule by rule |
| You're deploying a new rule and want to observe alert volume before enabling notifications | [Snooze actions](/solutions/security/detect-and-alert/snooze-rule-actions.md) | Enable the rule fully, review alerts in the UI, and only enable notifications once you're confident in the signal |

## How each mechanism works

Each mechanism intervenes at a different stage of the detection pipeline. They are listed here in pipeline order, from earliest to latest.

### Tune rule logic

Acts on: **the rule query, before events are evaluated**

*"The rule is catching the wrong things."*

Modify the rule query, threshold count, look-back window, or schedule to improve detection precision. Tuning is the only mechanism that improves the underlying signal rather than filtering output. Alerts are still created for events matching the revised logic, and change history requires version tracking. Tuning affects all environments using the rule.

Refer to [Tune detection rules](/solutions/security/detect-and-alert/tune-detection-rules.md) for detailed guidance.

### Rule exceptions

Acts on: **alert creation, after the rule evaluates but before the alert is written**

*"This specific case is acceptable in my environment."*

Permanently prevent alert creation for events matching defined field conditions. The rule logic stays unchanged. Exceptions are auditable and removable at any time. They can apply to a single rule or be shared across multiple rules through [shared exception lists](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md).

Refer to [Rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md) for detailed guidance.

### Alert suppression

Acts on: **alert deduplication, after the first alert is created**

*"I already know about this. Don't repeat it."*

After the first alert fires for a given field value (for example, a specific host or user), suppress subsequent duplicate alerts for a defined time window. Unlike exceptions, suppression is temporary and time-bounded. It acknowledges the signal is real but reduces repetitive noise. Configured per rule, grouped by field value.

Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/alert-suppression.md) for detailed guidance.

### Snooze rule actions

Acts on: **notifications, after alerts are created and stored**

*"Don't page anyone right now. I'll review later."*

Temporarily pause the rule's notification actions (emails, Slack messages, webhooks) without affecting rule execution or alert creation. Alerts generated during a snooze period are stored normally and visible in the Alerts UI. Snoozing expires automatically or can be canceled manually. For space-wide pausing, use a [maintenance window](/explore-analyze/alerts-cases/alerts/maintenance-windows.md).

Refer to [Snooze rule actions](/solutions/security/detect-and-alert/snooze-rule-actions.md) for detailed guidance.

## Key distinctions

|  | Tuning logic | Rule exceptions | Alert suppression | Snooze rule actions |
|---|---|---|---|---|
| Rule still runs | Yes | Yes | Yes | Yes |
| Alert written to index | Modified | No | First only | Yes |
| Analyst notified | For matches | No | First only | No |
| Alert visible in UI | For matches | No | First only | Yes, all alerts |
| Time-bounded | No | No, permanent | Yes, configurable window | Yes, configurable duration |
| Can span multiple rules | No | Yes, shared lists | No | No |

::::{important}
Exceptions and suppression have different forensic implications. Exceptions permanently prevent alert records from being created. If you later need to investigate whether a specific event occurred, the alert data won't be there. Suppression writes the first alert but drops subsequent ones. For high-value assets or regulated environments, prefer suppression over exceptions so there's always at least one alert record for any real detection event. Reserve exceptions for activity that is definitively never relevant.
::::

## Using them together [using-them-together]

These four mechanisms are not mutually exclusive. A well-tuned ruleset typically uses all of them simultaneously for different purposes. The following scenario illustrates how they layer on top of each other in practice.

**Scenario: A noisy lateral movement rule in a real environment**

| Situation | Action | Mechanism |
|---|---|---|
| The base query matches too broadly, catching any remote service creation including from `C:\Windows\` | Narrow the query to exclude standard install paths. The rule now only fires on services installed to non-standard locations. | Tune rule logic |
| The SCCM deployment server still triggers it every deployment cycle from a known management IP | Add an exception: `source.ip: "10.1.5.20" AND user.name: "svc-sccm"`. Those specific alerts are never created. | Exception |
| A compromised host generates 30 alerts in an hour. Analysts only need to know about the first one. | Enable alert suppression grouped by `host.id` with a 1-hour window. One alert per host per hour. | Suppression |
| Planned maintenance window tonight. Legitimate admin activity will trigger alerts, but no one should be paged. | Snooze rule actions for 4 hours. Alerts are created and stored. Notifications are paused. Review them in the morning. | Snooze actions |

::::{note}
Order of application matters. Tuning and exceptions are evaluated before an alert is created. Suppression deduplicates after creation. Snoozing acts after suppression, only on notifications. Applying them in the wrong conceptual order leads to gaps. For example, using suppression to handle what should be an exception means the first alert is still stored and may page someone, and the suppression window may expire before the condition is resolved.
::::
