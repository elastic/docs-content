---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Overview and workflow for building custom detection rules tailored to your threat model.
---

# Create a detection rule

Build custom detection rules tailored to your environment and threat model. The pages in this section walk you through selecting a rule type, writing rule logic, and configuring rule settings.

**[Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md)**
:   Start here if you're not sure which rule type fits your use case. Compares all rule types side by side and explains how building block rules fit into detection chains.

**[Rule types](/solutions/security/detect-and-alert/rule-types.md)**
:   Go here once you've selected a rule type. Each rule type page covers when to use it, how to write effective queries, real-world examples, and the field configuration specific to that type.

**[Using the rule builder](/solutions/security/detect-and-alert/using-the-rule-builder.md)**
:   The step-by-step workflow for creating rules in the {{kib}} UI. Covers the creation steps and links to rule settings and rule type guides.

**[Using the API](/solutions/security/detect-and-alert/using-the-api.md)**
:   Relevant if you need to create or manage rules programmatically, integrate rule management into CI/CD pipelines, or bulk-import rules.

**[Set rule data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md)**
:   Relevant if you need to override the default index patterns for a specific rule, target a narrower set of indices, or exclude cold and frozen data tiers.

**[Write investigation guides](/solutions/security/detect-and-alert/write-investigation-guides.md)**
:   Use this when you want to add triage guidance to a rule. Covers Markdown syntax, Timeline query buttons, and Osquery integration for investigation guides.

**[Validate and test rules](/solutions/security/detect-and-alert/validate-and-test-rules.md)**
:   Relevant before enabling a new rule in production. Covers how to test rule logic against historical data and assess alert volume.
