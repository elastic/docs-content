---
description: "Manage AlertZero in an Elastic Security space. Configure and manually run Workers, check their runs, and turn AlertZero off."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Manage {{alertzero}}

Control how {{alertzero}} runs in a space. You can change what its {{az-workers}} do, check how their runs went, and turn {{alertzero}} off when you no longer need it.

To enable {{az-workers}} or turn them off, set their {{az-autonomy}}, or change how often they run, refer to [](configure-worker-settings.md). You can also [manually run a {{az-worker}}](run-worker-on-demand.md) instead of waiting for its schedule, and [check each {{az-worker}}'s execution history](view-execution-history.md) to find runs that failed.

## Turn off {{alertzero}} [alertzero-turn-off]

If you turn off {{alertzero}} while its {{az-workers}} are enabled, the {{az-workers}} keep running, and you can no longer reach the {{az-watch}} pages where you turn them off. Turn off the {{az-workers}} first.

1. Turn off each {{az-worker}} on its {{az-watch}} page. Refer to [](configure-worker-settings.md).
2. Find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. In the **Security Solution** section, turn off the **{{alertzero}}** setting.
4. Select **Save changes**, then select **Reload page**.

% After elastic/docs-content#9118 merges, link the Configure Workers reference in step 1 to configure-worker-settings.md#alertzero-worker-on-off.
