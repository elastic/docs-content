---
navigation_title: Matchers
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Route only matching Kibana alerting v2 alerts to notification destinations using KQL matcher conditions on notification policies."
---

# Kibana alerting v2 notification matchers [matcher-v2]

Notification policy matchers are KQL expressions that determine which alerts a policy applies to. Only alerts matching the condition are routed to the policy's workflow destinations.
