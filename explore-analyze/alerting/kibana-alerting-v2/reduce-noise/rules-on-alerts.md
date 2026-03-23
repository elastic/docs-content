---
navigation_title: Rules on alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Replace many individual Kibana alerting v2 notifications with a single meaningful one using rules that correlate across alert event data."
---

# {{kib}} alerting v2 rules on alerts [reduce-noise-rules-on-alerts-v2]

Follow-on **rules on alert data** reduce noise by running another rule against **`.rule-events`** (or related indices) so many low-level **episodes** can roll up into one higher-level notification.

Refer to [Author rules: rules on alert data](../author-rules/rules-on-alerts.md) for detailed configuration guidance.
