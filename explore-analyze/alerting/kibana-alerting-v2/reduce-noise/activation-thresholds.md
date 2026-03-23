---
navigation_title: Activation thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Require consecutive breaches or a minimum duration before a Kibana alerting v2 alert episode becomes active, filtering out transient spikes."
---

# {{kib}} alerting v2 activation thresholds [activation-thresholds-v2]

**Activation thresholds** require a condition to be met a certain number of consecutive times or for a minimum duration before an **alert episode** transitions from `pending` to `active`.
