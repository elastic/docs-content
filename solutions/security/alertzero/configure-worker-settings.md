---
description: "Turn an AlertZero Worker on or off, and set its autonomy and other settings."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Configure {{az-worker}} settings

Turn {{az-workers}} on or off, and change their settings.

## Before you begin [alertzero-configure-before]

- Changing {{az-workers}}, including turning them on or off, needs the `manage_security` cluster privilege. That privilege also lets a user manage users and roles across the cluster, so don't grant it only for {{alertzero}}. Refer to [](alertzero-privileges.md).
- Without `manage_security`, the {{az-watch}} pages are read-only. If you decide which {{az-workers}} run and how much they do without you, but don't have this privilege, ask an administrator to apply your choices.

## Turn {{az-workers}} on or off [alertzero-worker-on-off]

Before you turn off {{az-workers}}, check whether [other {{az-workers}} need them](requirements.md#alertzero-requirements-dependencies). If another {{az-worker}} needs the one you turn off, {{alertzero}} asks you to confirm first and shows a warning on both {{az-workers}}. It never turns {{az-workers}} on or off for you.

When you turn on the {{az-continuous-threat-hunt}} {{az-worker}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.

## Set {{az-autonomy}} levels [alertzero-worker-autonomy]
