---
navigation_title: Maintenance windows
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Schedule periods during which Kibana alerting v2 notifications are paused for planned deployments or recurring maintenance."
---

# {{kib}} alerting v2 maintenance windows [maintenance-windows-v2]

**{{maint-windows-cap}}** are scheduled periods during which notifications are paused. Rule evaluation continues and **alert episodes** can still be recorded in **`.rule-events`**; dispatch is what pauses. Use them for planned deployments, infrastructure changes, or recurring maintenance.
