---
description: "What you can and can't configure in AlertZero."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Manage AlertZero

Learn what you can and can't configure in AlertZero.

## Turn off {{alertzero}} [alertzero-turn-off]

Turning off the advanced setting hides {{alertzero}} in the space, but its {{az-workers}} keep running. You can't reach the {{az-watch}} pages while the setting is off, so turn off the {{az-workers}} first:

1. Turn off each {{az-worker}} on its {{az-watch}} page. Refer to [](configure-worker-settings.md#alertzero-worker-on-off).
2. Turn off the **{{alertzero}}** advanced setting, in the same place where you [turned it on](set-up-alertzero.md#alertzero-turn-on).
