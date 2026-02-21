---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Technical reference for detection rule settings, alert schema, and querying alert indices.
---

# Settings, fields, and indices

Look up rule configuration settings, alert field definitions, and patterns for querying alert indices directly. These pages are designed for reference, not reading end to end.

**[Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md)**
:   Use this when you need to look up a specific rule setting, understand what a field does, or check valid values and defaults. Covers all shared settings (severity, risk score, schedule, actions, response actions, and notification variables) that apply across rule types. For rule-type-specific fields, refer to the individual [rule type](/solutions/security/detect-and-alert/rule-types.md) pages.

**[Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md)**
:   Relevant if you're building custom dashboards, visualizations, or SOAR integrations that query the `.alerts-security.alerts-*` index directly. Explains how to query alert indices safely, which fields are available, and links to the full [alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).
