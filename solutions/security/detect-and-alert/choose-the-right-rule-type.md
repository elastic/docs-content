---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/about-rules.html
  - https://www.elastic.co/guide/en/serverless/current/security-about-rules.html
  - https://www.elastic.co/guide/en/security/current/building-block-rule.html
  - https://www.elastic.co/guide/en/serverless/current/security-building-block-rules.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Compare detection rule types, select the best fit for your threat detection use case, and decide when to make a rule a building block rule.
---

# Choose the right rule type [security-about-rules]

Unsure which rule type to use? This guide helps you decide. {{elastic-sec}} offers several detection rule types, each designed for a different kind of threat signal. Selecting the right type is important because it determines what the rule can detect, how it performs, and how its alerts behave.

## Rule type comparison [rule-types]

Use the following table to select the right rule type. The rows are ordered as a decision flow: start at the top and use the first rule type that fits your detection goal.

| Ask yourself | Rule type | Description |
|---|---|---|
| Is the threat a behavioral deviation I can't define with an exact pattern? | [{{ml-cap}}](/solutions/security/detect-and-alert/machine-learning.md) | Relies on {{ml}} anomaly detection jobs to model normal behavior and flag deviations. No query authoring required, but you must create or select anomaly jobs. |
| Do I need to compare events against a threat intelligence feed? | [Indicator match](/solutions/security/detect-and-alert/indicator-match.md) | Compares source event fields against threat intelligence indices. Alerts are enriched with indicator metadata. |
| Am I looking for a field value appearing for the first time? | [New terms](/solutions/security/detect-and-alert/new-terms.md) | Fires when a value (or combination of up to three values) has never appeared in a configurable history window. Surfaces novel activity. |
| Does detection require an ordered sequence of events or a missing event? | [Event correlation (EQL)](/solutions/security/detect-and-alert/eql.md) | Uses EQL to correlate events by shared fields across time. Detects multi-step attack chains and gaps in expected activity. |
| Should an alert fire when event volume crosses a threshold? | [Threshold](/solutions/security/detect-and-alert/threshold.md) | Fires when the number of matching events grouped by one or more fields meets or exceeds a threshold. Ideal for brute-force and volume-based patterns. |
| Do I need aggregation, transformation, or computed fields? | [{{esql}}](/solutions/security/detect-and-alert/esql.md) | Uses pipe-based {{esql}} queries to aggregate, transform, and filter data before alerting. Each result row becomes an alert. |
| None of the above? | [Custom query](/solutions/security/detect-and-alert/custom-query.md) | Matches events using KQL or Lucene. The most flexible and widely used type for known field values, patterns, or boolean conditions. |

Any of these rule types can also be a building block rule, whose alerts feed other rules instead of the alert queue. To decide whether to make a rule a building block rule, refer to [Building block rules and detection chains](#about-building-block-rules).

## Building block rules and detection chains [about-building-block-rules]

Some activity is too common to investigate on its own, but it points to an attack when several pieces of it happen together. To detect that pattern without adding noise to the alert queue, make the rules that find each piece building block rules. Then create a correlation rule that searches their alerts and creates one alert when the pieces add up.

Any rule type can be a building block rule. Its alerts go to the same alerts index as all other alerts, but the **Alerts** page and the Overview page don't show them by default.

### When to make a rule a building block rule [when-to-use-building-block-rules]

Make a rule a building block rule when its alerts are useful as evidence but don't need an analyst's attention on their own. Building block rules fit these cases.

* Each matching event is low risk, but several together are significant.
* You want a record of low-severity activity for threat hunting or later investigation, without adding it to the Alerts table.
* You want the activity to raise [entity risk scores](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md), which include building block alerts.

Elastic prebuilt rules also include building block rules, tagged `Rule Type: BBR`. To decide when to turn them on, refer to [Choosing which rules to enable](/solutions/security/detect-and-alert/install-prebuilt-rules.md#choosing-rules-to-enable).

### How a detection chain works [how-detection-chains-work]

A detection chain has two layers. Building block rules search your source events and create hidden alerts. A correlation rule then searches those alerts instead of source events. When the building block alerts fit the pattern it looks for, such as several on the same host within a short time, the correlation rule creates an alert that analysts see.

For example, an intrusion often leaves several traces that are common on their own, such as a change to a startup registry key, a new scheduled task, and an outbound connection to a rare domain. You can create a building block rule for each trace. An [EQL](/solutions/security/detect-and-alert/eql.md) sequence rule that searches the alerts can then detect all three on the same host within an hour and create one alert for an analyst to investigate.

Elastic prebuilt rules use the same approach. To see working examples, filter the Rules table by the `Rule Type: Higher-Order Rule` tag, which Elastic adds to its prebuilt rules that search alerts.

### Set up a detection chain [set-up-detection-chain]

1. For each rule that detects one piece of the pattern, open the rule's [advanced settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) and select **Mark all generated alerts as "building block" alerts**. You can turn on this setting when you create or edit a rule of any type.
2. Create the correlation rule. In the **Define rule** step, set **Source** to **Index Patterns**, then enter the alerts index pattern, `.alerts-security.alerts-*`.

    :::{image} /solutions/images/security-alert-indices-ui.png
    :alt: The Source setting set to Index Patterns, with the alerts index pattern entered
    :screenshot:
    :::

    To search the alerts from one {{kib}} space only, enter that space's alias instead, such as `.alerts-security.alerts-default`. Refer to [Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md#alert-index-aliases).
3. Write the correlation rule's query so it matches only the alerts you want to correlate. For example, filter by `kibana.alert.rule.name`, or by a tag that you add to each building block rule. To match only building block alerts, filter on `kibana.alert.building_block_type`, which other alerts don't have.

    Without a filter like this, the correlation rule can also match its own alerts and those of other correlation rules. Elastic prebuilt correlation rules, for example, exclude alerts from rules tagged `Rule Type: Higher-Order Rule`.

To get notified when a building block rule creates alerts, add [rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications) to it. The alerts stay hidden on the **Alerts** page, but the actions still run.

### View building block alerts [view-building-block-alerts]

To check what your building block rules found, or to investigate the alerts behind a correlation rule's alert, include building block alerts in the Alerts table.

1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Alerts table toolbar, select **Additional filters** → **Include building block alerts**.

A building block rule's details page already includes them, so you can find that rule's alerts there without changing the filter.

