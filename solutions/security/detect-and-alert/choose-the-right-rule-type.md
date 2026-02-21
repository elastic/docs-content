---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/about-rules.html
  - https://www.elastic.co/guide/en/serverless/current/security-about-rules.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Compare detection rule types and select the best fit for your threat detection use case.
---

# Choose the right rule type [security-about-rules]

{{elastic-sec}} offers several detection rule types, each designed for a different kind of threat signal. Selecting the right type is the single most important decision when creating a rule, because it determines what the rule can detect, how it performs, and how its alerts behave.

## Rule type comparison [rule-types]

Use the following table to narrow your selection based on what you want to detect:

| If you want to detect... | Use this rule type | Learn more |
|---|---|---|
| A known field value, pattern, or boolean condition | [**Custom query**](/solutions/security/detect-and-alert/custom-query.md) | Matches events using KQL or Lucene. The most flexible and widely used type. |
| An ordered sequence of events or a missing event | [**Event correlation (EQL)**](/solutions/security/detect-and-alert/eql.md) | Uses EQL to correlate events by shared fields across time. Detects multi-step attack chains and gaps in expected activity. |
| A field value count exceeding a boundary | [**Threshold**](/solutions/security/detect-and-alert/threshold.md) | Fires when the number of matching events grouped by one or more fields meets or exceeds a threshold. Ideal for brute-force and volume-based patterns. |
| Events matching a known threat indicator | [**Indicator match**](/solutions/security/detect-and-alert/indicator-match.md) | Compares source event fields against threat intelligence indices. Alerts are enriched with indicator metadata. |
| A field value appearing for the first time | [**New terms**](/solutions/security/detect-and-alert/new-terms.md) | Fires when a value (or combination of up to three values) has never appeared in a configurable history window. Surfaces novel activity. |
| Aggregated, transformed, or computed conditions | [**{{esql}}**](/solutions/security/detect-and-alert/esql.md) | Uses pipe-based {{esql}} queries to aggregate, transform, and filter data before alerting. Each result row becomes an alert. |
| Behavioral anomalies without a fixed pattern | [**{{ml-cap}}**](/solutions/security/detect-and-alert/machine-learning.md) | Relies on {{ml}} anomaly detection jobs to model normal behavior and flag deviations. No query authoring required. |

## Decision flowchart

Ask these questions in order to identify the right rule type:

1. **Can you describe the exact pattern?** If not, and the threat is a behavioral deviation from normal, use a **{{ml}}** rule.
2. **Does the detection require comparing events against an external threat feed?** If yes, use an **indicator match** rule.
3. **Is the signal the first-ever appearance of a value?** If yes, use a **new terms** rule.
4. **Does the detection require a sequence of events in a specific order, or detecting a missing event?** If yes, use an **EQL** rule.
5. **Does the detection require counting events and firing when a volume threshold is crossed?** If yes, use a **threshold** rule.
6. **Do you need aggregation, transformation, or computed fields within the query?** If yes, use an **{{esql}}** rule.
7. **None of the above?** Use a **custom query** rule.

## Building block rules and detection chains [about-building-block-rules]

Any rule type can be designated as a **building block** rule. Building block rules generate alerts that are hidden from the Alerts page by default. They serve as intermediate signals that feed into higher-level detection logic.

### When to use building blocks

Building block rules are useful when:

* An individual event is too low-risk to warrant analyst attention, but a combination of such events is significant.
* You want to create a **detection chain**: a set of building block rules whose hidden alerts become the input for a downstream rule that produces a visible, high-confidence alert.
* You need a persistent record of low-severity signals for threat hunting or retrospective analysis without cluttering the Alerts page.

### How detection chains work

A detection chain typically has two layers:

1. **Building block rules** query source event indices and produce hidden alerts. These alerts are written to the `.alerts-security.alerts-<kibana space>` index.
2. **A downstream rule** queries the alert index (`.alerts-security.alerts-*`) instead of source event indices. It correlates or aggregates the building block alerts and produces a visible alert when the combined pattern meets its criteria.

For example, you might create three building block rules:

* One that detects a suspicious registry modification.
* One that detects a new scheduled task creation.
* One that detects an outbound connection to a rare domain.

Each of these individually produces low-confidence alerts. A downstream EQL sequence rule can then query the alert index to detect all three occurring on the same host within a short time window, producing a single high-confidence alert for a likely intrusion chain.

::::{tip}
Add [rule actions](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-notifications) to building block rules if you want notifications when building block alerts are generated, even though the alerts are hidden from the default Alerts view.
::::

### Viewing building block alerts

Building block alerts are excluded from the Overview and Alerts pages by default. To include them:

1. Navigate to the **Alerts** page.
2. Select **Additional filters** then **Include building block alerts**.

On a building block rule's details page, the rule's alerts are always displayed.

### Marking a rule as a building block

Select the **Building block** option in the rule's [advanced settings](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-ui-advanced-params) when creating or editing any rule type.

## Shared concepts [shared-rule-concepts]

The following concepts apply to all rule types. For the full settings reference, see [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

### Data sources [views-index-patterns]

When you create a rule, you must specify either {{es}} index patterns or a {{data-source}} as the data source (except for {{ml}} rules, which do not use queries). If you select a {{data-source}}, you can use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) associated with that {{data-source}} in your rule query.

::::{note}
To access {{data-source}}s in {{stack}}, you must have the [required permissions](/explore-analyze/find-and-organize/data-views.md#data-views-read-only-access). In {{serverless-short}}, you must have the appropriate [predefined Security user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges.
::::

::::{important}
System indices, such as the alert indices, contain important configuration and internal data. Do not change their mappings. Changes can lead to rule execution and alert indexing failures. Use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead to add fields to existing alert and event documents.
::::

### Authorization [alerting-authorization-model]

Rules are authorized using an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user to edit the rule. When you create or modify a rule, an API key is generated that captures a snapshot of your privileges. This API key is used for all background tasks, including detection checks and action execution.

::::{important}
If a user without the required privileges (such as index privileges) updates a rule, the rule stops functioning. Ensure that only users with appropriate access edit rules.
::::

### Exceptions [about-exceptions]

You can [add exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md) to rules to prevent them from generating alerts even when their criteria are met. This is useful for reducing noise from trusted processes, internal IP addresses, or known-benign activity.

::::{note}
Exceptions are supported for custom query, {{ml}}, event correlation, and indicator match rule types.
::::

### Notifications [about-notifications]

For both prebuilt and custom rules, you can send notifications when alerts are created. Notifications can be sent through {{jira}}, Microsoft Teams, PagerDuty, Slack, and other connectors. Configure actions when you [create or edit a rule](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-notifications).
