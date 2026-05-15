---
navigation_title: Using the YAML editor
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Define rules as YAML in the experimental alerting features for version control, infrastructure-as-code, and bulk provisioning."
---

# Create rules using the YAML editor [create-rules-yaml]


The YAML editor is part of the experimental alerting features in Kibana. It lets you define rules as text documents rather than filling in a form. Use it when you want to version-control rule definitions alongside your other configuration, manage rules through infrastructure-as-code tooling, copy or adapt a rule quickly without re-entering settings by hand, or provision many rules at once.

If you're creating a rule from scratch and want guidance through each setting, the [rule builder](create-rule-from-rule-builder.md) is the better starting point. If you have a query already working in Discover, you can [create a rule directly from there](create-rule-from-discover.md).

For the full list of supported YAML fields and their accepted values, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

<!--[CONTENT NEEDED: UI. This page needs a procedure once the YAML editor UI is finalized: how to open it, how to paste or edit a definition, and how to save. Hold until the editor workflow is confirmed.]
-->
