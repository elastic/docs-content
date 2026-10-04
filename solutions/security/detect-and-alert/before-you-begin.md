---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Prerequisites and initial setup tasks before creating and running detection rules.
---

# Before you begin

Before you can create and run detection rules, turn on detections and make sure your users have the privileges they need. If you're new to {{elastic-sec}} detections, check out [Detection rule concepts](/solutions/security/detect-and-alert/detection-rule-concepts.md) for an overview of how rules work.

## One-time setup

These tasks are typically completed once when you first configure detection capabilities:

- [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md): Enable the Detections feature for your deployment type. On {{serverless-short}}, detections are on by default.
- [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md): Give users the cluster, index, and {{kib}} privileges they need for detection features. This page is part of [Access control](/solutions/security/manage/access-control.md), where you can return to it as your team changes.

## Related configuration

[Advanced data source configuration](/solutions/security/detect-and-alert/advanced-data-source-configuration.md) covers {{ccs}} setup, data tier exclusions, and index mode settings. Revisit it when you add clusters, change data retention policies, or onboard data sources that use different index configurations.