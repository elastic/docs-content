---
navigation_title: Using the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create ES|QL rules, AI-assisted rules, and Threshold Alert rules in Kibana's experimental alerting system using the rule builder flyout."
---

# Create rules in the {{alerting-v2-system}} [create-rules-rule-builder]

The rule builder is part of the {{alerting-v2-system}} in {{kib}}. This page covers the three creation paths available from the rules list, how the Threshold Alert builder works including alert delay and recovery conditions, and how to switch between form and YAML editing modes. For descriptions of what each setting does, refer to [Configure a rule](configure-a-rule.md).

## Creation paths [rule-creation-paths]

All rules are created through a flyout that opens from the **Create rule** button in the rules list. Three options are available:

- **Create ES|QL rule**: Write the detection query as {{esql}} directly, with a live preview of results. A YAML editor is also available within this path. Use this when you want full control over the query. If you already have a query working in Discover, you can [start from there instead](create-rule-from-discover.md) to skip re-entering it.
- **Create with AI Agent**: Describe what you want to detect in plain language. The AI agent generates a rule definition and walks you through reviewing and saving it. Use this when you know the problem but aren't sure how to write the {{esql}}.
- **Start from a rule builder**: Choose a structured rule type and fill in a guided form. The builder generates the {{esql}} query automatically. Use this when you want to create a standard rule type without writing {{esql}} by hand. Refer to [Threshold Alert](#threshold-alert) for the available type.

## Threshold Alert

Threshold Alert is the rule type available under **Start from a rule builder**. Use it to monitor one or more metrics and alert when they cross a threshold, with multi-condition support and custom aggregations.

You define the rule by filling in structured fields for the data source, aggregation, filters, and alert conditions. The builder generates the {{esql}} query automatically from those inputs. Rules created through the builder can be reopened and edited in builder mode as long as the underlying {{esql}} hasn't been edited directly.

Use the **Create ES|QL rule** path when the detection logic requires more than a single metric threshold, such as multi-window burn rates or cross-series correlation.

### Alert delay [threshold-builder-alert-delay]

When the rule is in Alert mode, the threshold builder includes an alert delay field that controls when the rule opens an alert episode after the threshold is first breached. Three modes are available: immediate activation on the first breach, activation after a set number of consecutive breaches, or activation after the condition has persisted for a specified duration. For a description of each mode and guidance on when to use it, refer to [Activation thresholds](configure-a-rule.md#activation-recovery-thresholds).

The alert delay field is only shown for Alert-mode rules. Signal-mode rules don't maintain alert episode lifecycle tracking, so activation thresholds don't apply.

### Recovery conditions [threshold-builder-recovery]

When you define alert conditions in the Threshold Alert builder, the builder automatically derives corresponding recovery conditions by flipping the comparators. For example, a `greater than` alert condition produces a `less than or equal to` recovery condition. You can customize the derived conditions or leave the defaults as generated. Recovery conditions are preserved correctly when you reopen an existing rule in builder mode for editing.

## ES|QL rule: form and YAML editing [rule-builder-form-yaml]

The **Create ES|QL rule** path supports both a step-by-step form and a YAML editing mode. When creating a new rule, you can switch between them at any point. Edits in YAML mode are preserved when you return to the form view. To discard YAML edits and return to the prior form state, use the **Cancel YAML** option.

When editing an existing rule, the form/YAML toggle is disabled if the rule's YAML configuration contains settings the form cannot represent. In that case, the rule opens in YAML-only mode to prevent the form from silently dropping fields on save. The YAML editor remains fully functional. For the list of configurations that trigger this restriction, refer to [YAML-only mode when editing rules](create-rule-with-yaml.md#yaml-only-edit).

Use YAML mode when you want to fine-tune the raw rule definition, copy a configuration from an existing rule, or work faster than filling in individual form fields allows. The YAML editor isn't available within the Threshold Alert builder or other rule builder types.

For a list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

<!--[CONTENT NEEDED: UI. This page needs step-by-step procedures once the creation flows are finalized: how to open each path, how to fill in settings, how to preview, and how to save. Navigation paths, button labels, and form field arrangement should all be verified against the shipped UI before publishing.]
-->
