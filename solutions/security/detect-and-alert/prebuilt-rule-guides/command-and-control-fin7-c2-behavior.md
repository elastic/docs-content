---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Possible FIN7 DGA Command and Control Behavior" prebuilt detection rule.'
---

# Possible FIN7 DGA Command and Control Behavior

## Triage and analysis

In the event this rule identifies benign domains in your environment, the `destination.domain` field in the rule can be modified to include those domains. Example: `...AND NOT destination.domain:(zoom.us OR benign.domain1 OR benign.domain2)`.
