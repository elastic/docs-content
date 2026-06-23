---
navigation_title: Using the YAML editor
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Define rules as YAML in Kibana's experimental alerting system for version control, infrastructure-as-code, and bulk provisioning of detection logic."
---

# Create rules using the YAML editor in {{alerting-v2-system}} [create-rules-yaml]


The YAML editor is part of the {{alerting-v2-system}} in {{kib}}. It lets you define rules as text documents rather than filling in a form. 

This page covers when to use the YAML editor instead of the rule builder, and how to get started. For the full list of supported fields and accepted values, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

Use the YAML editor when you want to version-control rule definitions alongside your other configuration, manage rules through infrastructure-as-code tooling, copy or adapt a rule quickly without re-entering settings by hand, or provision many rules at once. If you're creating a rule from scratch and want guidance through each setting, the [rule builder](create-rule-from-rule-builder.md) is the better starting point. If you have a query already working in Discover, you can [create a rule directly from there](create-rule-from-discover.md).

## YAML-only mode when editing rules [yaml-only-edit]

When you reopen a rule for editing, the form/YAML toggle is disabled if the rule's YAML configuration contains settings the form cannot represent. The rule opens in YAML-only mode. This prevents the form from silently dropping fields it doesn't know how to display on save. The YAML editor remains fully functional, and all fields round-trip without loss.

The following configurations force YAML-only mode when editing:

| Configuration | Why the form can't represent it |
| --- | --- |
| `query.format: standalone` with `kind: alert` | The form is built around the composed query format (base query plus condition blocks). Standalone format rules cannot be loaded into the form editor. |
| `recovery_strategy: no_breach` or `recovery_strategy: none` | The form only supports custom recovery queries. The no-breach and none strategies have no form equivalent. |
| `no_data_strategy` (any active value) | The form has no controls for no-data handling. |
| `query.no_data` block | The form has no UI for inline no-data query definitions. |

If the toggle is disabled and you want to use the form, you must remove the non-representable configuration from the YAML before saving, then reopen the rule.

<!-- TODO: Verify field names against the shipped M2 YAML schema. Issue #7092 references `recovery_strategy`, `no_data_strategy`, and `query.no_data`, which differ from the currently documented `recovery_policy.type` and `no_data.behavior` in yaml-rule-schema-reference.md. Confirm whether these are updated M2 field names or whether the issue uses conceptual rather than schema-level names, and update the table and yaml-rule-schema-reference.md accordingly. -->

<!--[CONTENT NEEDED: UI. This page needs a procedure once the YAML editor UI is finalized: how to open it, how to paste or edit a definition, and how to save. Hold until the editor workflow is confirmed.]
-->
