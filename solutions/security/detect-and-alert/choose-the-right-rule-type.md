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

Unsure which rule type to use? This guide helps you decide. {{elastic-sec}} offers several detection rule types, each designed for a different kind of threat signal. Selecting the right type is important because it determines what the rule can detect, how it performs, and how its alerts behave.

## Rule type comparison [rule-types]

Use the following table to select the right rule type. The rows are ordered as a decision flow: start at the top and use the first rule type that fits your detection goal.

| Ask yourself | Rule type | Description |
|---|---|---|
| Is the threat a behavioral deviation I can't define with an exact pattern? | [{{ml-cap}}](/solutions/security/detect-and-alert/machine-learning.md) | Relies on {{ml}} anomaly detection jobs to model normal behavior and flag deviations. No query authoring required. |
| Do I need to compare events against a threat intelligence feed? | [Indicator match](/solutions/security/detect-and-alert/indicator-match.md) | Compares source event fields against threat intelligence indices. Alerts are enriched with indicator metadata. |
| Am I looking for a field value appearing for the first time? | [New terms](/solutions/security/detect-and-alert/new-terms.md) | Fires when a value (or combination of up to three values) has never appeared in a configurable history window. Surfaces novel activity. |
| Does detection require an ordered sequence of events or a missing event? | [Event correlation (EQL)](/solutions/security/detect-and-alert/eql.md) | Uses EQL to correlate events by shared fields across time. Detects multi-step attack chains and gaps in expected activity. |
| Should an alert fire when event volume crosses a threshold? | [Threshold](/solutions/security/detect-and-alert/threshold.md) | Fires when the number of matching events grouped by one or more fields meets or exceeds a threshold. Ideal for brute-force and volume-based patterns. |
| Do I need aggregation, transformation, or computed fields? | [{{esql}}](/solutions/security/detect-and-alert/esql.md) | Uses pipe-based {{esql}} queries to aggregate, transform, and filter data before alerting. Each result row becomes an alert. |
| None of the above? | [Custom query](/solutions/security/detect-and-alert/custom-query.md) | Matches events using KQL or Lucene. The most flexible and widely used type for known field values, patterns, or boolean conditions. |

<!-- BUILDING BLOCK SECTION - COMMENTED OUT FOR REVIEW
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
Add [rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications) to building block rules if you want notifications when building block alerts are generated, even though the alerts are hidden from the default Alerts view.
::::

### Viewing building block alerts

Building block alerts are excluded from the Overview and Alerts pages by default. To include them:

1. Navigate to the **Alerts** page.
2. Select **Additional filters** then **Include building block alerts**.

On a building block rule's details page, the rule's alerts are always displayed.

### Marking a rule as a building block

Select the **Building block** option in the rule's [advanced settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) when creating or editing any rule type.
END BUILDING BLOCK SECTION -->

