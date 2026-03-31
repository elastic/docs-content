---
navigation_title: Recovery thresholds
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Require sustained recovery before a Kibana alerting v2 alert episode returns to inactive, preventing rapid toggling between active and recovered."
---

# {{kib}} alerting v2 recovery thresholds [recovery-thresholds-v2]

**Recovery thresholds** require a condition to be absent for a certain number of consecutive evaluations or for a minimum duration before an **alert episode** transitions from `recovering` to `inactive`.
