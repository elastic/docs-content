---
navigation_title: Before you begin
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
description: Concept overview, access requirements, and setup to complete before authoring Kibana alerting v2 rules.
---

# Before you begin with Kibana alerting v2 [alerting-before-you-begin-v2]

These pages cover what to understand and configure before you create Kibana alerting v2 rules. Unlike [Author rules](author-rules.md), which focuses on building and changing rules, the topics below prepare your environment and permissions.

For a first-time path, work through them in the order listed. If you already handled setup or access, open the page that matches what you need.

**[Kibana alerting v2 concepts](before-you-begin/how-v2-alerting-works.md)**
:   How v2 runs end to end: Detect and Alert modes, what happens on each rule run, why detection and notification are separate layers, and definitions for terms you will see in the product (for example signals, alerts, series, episodes, notification policies, workflows, and the dispatcher).

**[Kibana alerting v2 privileges](before-you-begin/alerting-privileges.md)**
:   {{es}} index-level access and {{kib}} feature privileges for managing rules, notification policies, and alert-related data.

**[Set up Kibana alerting v2](before-you-begin/set-up.md)**
:   Prerequisites, turning the feature on, related data streams, and checks that alerting v2 is ready to use.
