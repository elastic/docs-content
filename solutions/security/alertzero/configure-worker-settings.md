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

Turn a {{az-worker}} on or off, and change its settings.

## Before you begin [alertzero-configure-before]

- Changing a {{az-worker}}, including turning it on or off, needs the `manage_security` cluster privilege. That privilege also lets a user manage users and roles across the cluster, so don't grant it only for {{alertzero}}. Refer to [](alertzero-privileges.md).
- Without `manage_security`, the {{az-watch}} pages are read-only. If you decide which {{az-workers}} run and how much they do without you, but don't have this privilege, ask an administrator to apply your choices.

## Turn a {{az-worker}} on or off [alertzero-worker-on-off]

Before you turn off a {{az-worker}}, check whether [another {{az-worker}} needs it](requirements.md#alertzero-requirements-dependencies). When you turn off a {{az-worker}} that another one needs, {{alertzero}} asks you to confirm first and shows a warning on both {{az-workers}}. It never turns {{az-workers}} on or off for you.

When you turn on the {{az-continuous-threat-hunt}} {{az-worker}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.

## Set a {{az-worker}}'s {{az-autonomy}} [alertzero-worker-autonomy]
