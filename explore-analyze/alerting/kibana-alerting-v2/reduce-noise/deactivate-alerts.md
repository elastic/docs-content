---
navigation_title: Deactivate alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Stop lifecycle processing and notifications for a Kibana alerting v2 alert episode while the rule continues detecting new episodes."
---

# Deactivate {{kib}} alerting v2 alerts [deactivate-alerts-v2]

**Deactivate** stops lifecycle processing and notifications for one **alert episode**. The rule continues to run and can open new **episodes** for other **series** (`group_hash`), but the **deactivated** episode is no longer tracked.
