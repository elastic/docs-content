---
navigation_title: Matchers
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Route only matching {{alerting-v2}} alert episodes to notification destinations using KQL matcher conditions on action policies."
---

# {{alerting-v2}} notification matchers [matcher-v2]

**Action policy matchers** are KQL expressions that determine which **alert episodes** a policy applies to. Only **episodes** that match the condition (after **rule_labels** scoping) are routed to the policy's workflow destinations.
