---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/building-block-rule.html
  - https://www.elastic.co/guide/en/serverless/current/security-building-block-rules.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Create rules that generate hidden alerts used as building blocks for downstream detection rules.
---

# About building block rules [security-building-block-rules]

A building block rule creates alerts that the Alerts table hides by default. Use building block rules for activity that isn't worth triaging on its own but matters in combination with other activity. For example, you can create several building block rules that each detect one low-risk behavior, and then create a rule that alerts when several of those behaviors happen on the same host.

Rule actions still run for building block rules, so you can get [notifications](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications) when they create alerts.

## Create a building block rule [security-building-block-rules-create]

When you create or edit a rule of any type, open **Advanced settings** in the **About rule** step, and then select **Mark all generated alerts as "building block" alerts**.

## Use building block alerts in another rule [security-building-block-rules-set-up-rules-that-run-on-alert-indices]

To detect a combination of building block alerts, create a rule that searches the alerts index instead of your event indices. Select **Index Patterns** as the rule's **Source**, and enter the index pattern for alert indices (`.alerts-security.alerts-*`):

:::{image} /solutions/images/security-alert-indices-ui.png
:alt: Rule Source setting with Index Patterns selected and the .alerts-security.alerts-* index pattern entered
:screenshot:
:::

In the rule's query, match the building block alerts you want to combine, for example by their `kibana.alert.rule.name` value. For more ways to query alerts, refer to [Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md).
