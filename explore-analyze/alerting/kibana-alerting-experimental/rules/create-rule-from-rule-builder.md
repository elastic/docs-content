---
navigation_title: Using the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create a rule with the interactive rule builder in the {{alerting-v2}}: when to use it, creation paths, and Form/YAML switching."
---

# Create rules using the rule builder in {{alerting-v2}} [create-rules-rule-builder]

The rule builder is part of the {{alerting-v2}} in {{kib}}. It is the right starting point when you're creating a rule from scratch and want inline guidance through each setting. For a full description of what each setting does, refer to [Configure a rule](configure-a-rule.md).

If you already have a working query in Discover, you can [create a rule directly from there](create-rule-from-discover.md) without re-entering it. If you're managing rules as code or need to version-control rule definitions, use the [YAML editor](create-rule-with-yaml.md) instead.

## Creation paths [rule-creation-paths]

All rules are created through a flyout. The flyout opens from the rules list. When no rules exist yet, a panel offering three options displays:

- **From scratch**: Opens the rule form directly. Use this when you know what you want to detect and want full control over the definition.
- **From recommended rules**: Starts from a curated template. Use this when you want a pre-built starting point that you can review and adapt to your environment.
- **With AI agent**: Opens Agent Builder with a rule management skill pre-loaded. Describe the problem you want to detect in plain language. The agent generates a rule definition and walks you through saving it. Use this when you know the problem but aren't sure how to express it as an {{esql}} query.

Once rules exist, the **Create rule** button also gives you access to the AI agent path directly from the rules list.

## Form and YAML editing [rule-builder-form-yaml]

The rule creation flyout supports both a step-by-step form and a YAML editing mode. You can switch between them at any point. Edits in YAML mode are preserved when you return to the form view. To discard YAML edits and return to the prior form state, use the **Cancel YAML** option.

Use YAML mode when you want to fine-tune the raw rule definition, copy a configuration from an existing rule, or work faster than filling in individual form fields allows. Use the form when you want inline validation and contextual guidance for each setting.

For a list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

<!--[CONTENT NEEDED: UI. This page needs a step-by-step procedure once the rule builder UI is finalized: how to open it, how to fill in settings, how to preview, and how to save. Navigation paths, button labels, and form field arrangement should all be verified against the shipped UI before publishing. Hold until the rule builder workflow is confirmed.]
-->
