---
navigation_title: How notification policies are evaluated
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "How the Kibana alerting v2 dispatcher processes alert episodes through a 10-step pipeline: suppressions, matchers, grouping, throttling, and dispatch."
---

# How Kibana alerting v2 notification policies are evaluated [how-notification-policies-evaluated-v2]

The dispatcher is the asynchronous component that bridges rule execution and notification delivery. It polls for new alert episodes and processes them through a 10-step pipeline.

The dispatcher runs every 10 seconds and processes up to 10,000 episodes per run.
