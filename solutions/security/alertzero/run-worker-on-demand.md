---
description: "Run an AlertZero Worker outside its schedule."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Run a {{az-worker}} on demand

A {{az-worker}} normally runs on its own schedule. You can also start a run yourself, for example to see the effect of a settings change without waiting for the next scheduled run. You start the run from the **Workflows** page, because each {{az-worker}} is a [managed workflow](/explore-analyze/workflows/managed-workflows.md).

## Before you begin [run-worker-on-demand-before-you-begin]

* Turn the {{az-worker}} on. A {{az-worker}} that's turned off can't be run. Refer to [](configure-worker-settings.md#configure-worker-settings-enabled).
* Turn on the [**Show managed workflows**](kibana://reference/advanced-settings.md#kibana-workflows-settings) advanced setting. Managed workflows are hidden by default, and the **Workflows** page can't show a {{az-worker}} while they're hidden. Refer to [](/explore-analyze/workflows/get-started/setup.md#workflows-managed-visibility).
* Make sure your role includes the privilege to run workflows. Refer to [](alertzero-privileges.md#alertzero-admin-access).

## What to expect from an on-demand run [run-worker-on-demand-expect]

A run that you start from the workflow list is an extra run, in addition to the scheduled ones. The {{az-worker}} still runs on its schedule, and the extra run produces the same kinds of results as a scheduled run, such as {{az-proposed-actions}} and {{az-investigations}}.

A run that you start uses the same {{az-autonomy}} level as a scheduled run, with one exception: the {{az-endpoint-analysis}} {{az-worker}}. When you run it yourself, it always uses **{{az-manual}}** {{az-autonomy}}, even if you set it to **{{az-supervised}}**. Any containment {{az-proposed-actions}} that it creates wait for your approval.

## Run a Worker [run-worker-on-demand-steps]

1. Find **Workflows** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **View**, then select **Managed** so that managed workflows appear in the list.
3. In the workflow list, find the {{az-worker}}.
4. In the {{az-worker}}'s row, select **Run** {icon}`play`.

To check the result of the run, refer to [](view-execution-history.md).

:::{important}
Start the run from the workflow list, not from the workflow editor that **View executions** opens. A run that you start in the editor is a test run, which is meant for trying out a workflow while you author it, not for production runs. For more information, refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-test-vs-production-runs).
:::
