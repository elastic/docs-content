---
description: "Manage AlertZero in an Elastic Security space: change Worker settings, run Workers on demand, check their runs, recognize the indexes AlertZero adds, and turn AlertZero off."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Manage {{alertzero}}

After you [set up {{alertzero}}](set-up-alertzero.md), use these pages to manage it in each space:

- [](configure-worker-settings.md): Turn {{az-workers}} on or off, and change their {{az-autonomy}} and other settings.
- [](run-worker-on-demand.md): Run {{az-workers}} outside their schedule.
- [](view-execution-history.md): See every {{az-worker}} run, including failures.

To give people access to {{alertzero}}, refer to [](alertzero-privileges.md).

## Indexes that {{alertzero}} adds [alertzero-indexes]

{{alertzero}} adds two indexes, which you might notice in **Index Management**. {{alertzero}} creates and manages them, so you don't need to set them up.

- `ai-index-idx-security-investigations`: The detection gaps and forensics handoffs that {{az-workers}} pass to each other through [{{context-engine}}](/explore-analyze/ai-features/context-engine.md). Refer to [](watches-and-workers.md).
- `ai-index-idx-security-attack-fingerprints`: Lets the {{az-attack-discovery}} {{az-worker}} recognize an attack it already reported, so it adds the attack to the open {{az-investigation}} instead of opening a new one.

% After elastic/docs-content#9118 merges, link "Refer to" above to watches-and-workers.md#alertzero-context-engine.

## Turn off {{alertzero}} [alertzero-turn-off]

Turning off the advanced setting hides {{alertzero}} in the space, but its {{az-workers}} keep running. You can't reach the {{az-watch}} pages while the setting is off, so turn off the {{az-workers}} first:

1. Turn off each {{az-worker}} on its {{az-watch}} page. Refer to [](configure-worker-settings.md#alertzero-worker-on-off).
2. Turn off the **{{alertzero}}** advanced setting, in the same place where you [turned it on](set-up-alertzero.md#alertzero-turn-on).
