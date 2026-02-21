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

Before you can create and run detection rules, confirm that your environment meets the infrastructure requirements and that your users have the necessary privileges. Some tasks only need to be done once during initial setup, while others should be revisited as your environment evolves.

## One-time setup

These tasks are typically completed once when you first configure detection capabilities:

- [**Turn on detections**](/solutions/security/detect-and-alert/requirements-privileges.md): Enable the Detections feature for your deployment type. On {{serverless-short}}, detections are on by default.
- [**Detections privileges**](/solutions/security/detect-and-alert/detections-privileges.md): Understand the cluster, index, and {{kib}} privileges required for detection features, and review predefined roles and the authorization model.

## Revisit as your environment changes

These tasks may need to be updated over time as you onboard new data sources, add users, or expand your detection coverage:

- **User roles and privileges**: As your team grows or responsibilities shift, review and update role assignments to ensure analysts have the access they need. Refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md).
- [**Advanced data source configuration**](/solutions/security/detect-and-alert/advanced-data-source-configuration.md): Revisit {{ccs}} setup, data tier exclusions, and index mode settings when you add new clusters, change data retention policies, or onboard data sources that use different index configurations.
