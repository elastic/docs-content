---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Create and configure detection rules tailored to your environment and threat model.
---

# Author rules [rules-ui-create]

Create detection rules tailored to your environment and threat model. Whether you're writing rules from scratch or customizing prebuilt rules, the pages in this section guide you through selecting a rule type, writing rule logic, and configuring settings.

**[Choose the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md)**
:   Start here if you're not sure which rule type fits your use case. Compares all rule types side by side.

**[Rule types](/solutions/security/detect-and-alert/rule-types.md)**
:   Detailed guidance for each rule type, including when to use it and field configuration specific to that type.

**[Using the UI](/solutions/security/detect-and-alert/using-the-rule-builder.md)**
:   Step-by-step workflow for creating rules in the {{elastic-sec}} UI.

**[Using the API](/solutions/security/detect-and-alert/using-the-api.md)**
:   Create or manage rules programmatically, integrate with CI/CD pipelines, or bulk-import rules.

**[Common rule settings](/solutions/security/detect-and-alert/common-rule-settings.md)**
:   Reference for all shared rule settings: severity, risk score, schedule, actions, and notification variables.

**[Set rule data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md)**
:   Override default index patterns, target specific indices, or exclude cold and frozen data tiers.

**[Write investigation guides](/solutions/security/detect-and-alert/write-investigation-guides.md)**
:   Add triage guidance to rules using Markdown, Timeline query buttons, and Osquery integration.

**[Validate and test rules](/solutions/security/detect-and-alert/validate-and-test-rules.md)**
:   Test rule logic against historical data and assess alert volume before enabling in production.