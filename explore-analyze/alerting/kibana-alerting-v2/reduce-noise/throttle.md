---
navigation_title: Throttling
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Limit Kibana alerting v2 notification frequency by setting a minimum interval between notifications for the same group."
---

# {{kib}} alerting v2 throttle [throttle-v2]

**Throttling** sets a minimum interval between notifications for the same **notification group**. It reduces notification volume without changing rule evaluation or **alert episode** lifecycle state.
