---
navigation_title: Rules on alerts
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Write Kibana alerting v2 rules that query alert events for correlation, escalation, and noise reduction across multiple rules."
---

# Kibana alerting v2 rules on alerts [rules-on-alerts-v2]

Because Kibana alerting v2 alert events are stored as queryable data in standard {{es}} indices, you can write rules that use the alert events index as their data source. This enables correlation, escalation, and noise reduction patterns.
