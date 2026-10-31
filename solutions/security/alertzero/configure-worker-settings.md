---
description: "Turn an AlertZero Worker on or off, and set its autonomy and other settings."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Configure Worker settings

Turn a Worker on or off, and change its settings.

## Turn a {{az-worker}} on or off [alertzero-worker-on-off]

Before you turn off a {{az-worker}}, check whether [another {{az-worker}} needs it](requirements.md#alertzero-requirements-dependencies). When you turn off a {{az-worker}} that another one needs, {{alertzero}} asks you to confirm first and shows a warning on both {{az-workers}}. It never turns {{az-workers}} on or off for you.

When you turn on the {{az-continuous-threat-hunt}} {{az-worker}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.

## Set a Worker's autonomy [alertzero-worker-autonomy]
