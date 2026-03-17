---
navigation_title: Recovery thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Require sustained recovery before a Kibana alerting v2 alert deactivates, preventing rapid toggling between active and recovered."
---

# Kibana alerting v2 recovery thresholds [recovery-thresholds-v2]

Recovery thresholds require a condition to be absent for a certain number of consecutive evaluations or for a minimum duration before an alert transitions from `recovering` to `inactive`.
