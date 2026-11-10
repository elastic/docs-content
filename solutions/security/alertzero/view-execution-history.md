---
description: "See every AlertZero Worker run, including failures."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# View execution history

Each time a {{az-worker}} runs, {{kib}} records the run. Use the execution history to check that a {{az-worker}} is running on schedule, to see what a run did, and to find out why a run failed. The history includes scheduled runs and runs that you [start yourself](run-worker-on-demand.md).

## Before you begin [view-execution-history-before-you-begin]

* Turn on the [**Show managed workflows**](kibana://reference/advanced-settings.md#kibana-workflows-settings) advanced setting. Because each {{az-worker}} is a [managed workflow](/explore-analyze/workflows/managed-workflows.md), you can't see its runs while managed workflows are hidden. Refer to [](/explore-analyze/workflows/get-started/setup.md#workflows-managed-visibility).
* Make sure your role includes the privilege to read the executions of managed workflows. Refer to [](alertzero-privileges.md#alertzero-admin-access).

## View a Worker's runs [view-execution-history-steps]

1. Find **{{az-watches}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the {{az-watch}} that contains the {{az-worker}}.
3. In the {{az-worker}}'s settings, select **View executions**. The {{az-worker}}'s execution history opens in the workflow editor.
4. Select a run to see its logs, including what each step did.

If a run fails, open it and find the step with the error indicator to see what went wrong. For troubleshooting steps, refer to [](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).

To see what a run produced, such as {{az-proposed-actions}}, refer to [](work-in-alertzero.md).

:::{note}
Runs that you start from the workflow editor are test runs. They're saved with a flask {icon}`flask` badge, so you can tell them apart from scheduled runs and from runs that you start from the workflow list. Refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-test-vs-production-runs).
:::
