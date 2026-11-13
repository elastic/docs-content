---
navigation_title: Visualize a workflow
applies_to:
  serverless: ga
  stack: ga 9.6+, experimental =9.5
description: View a read-only graph of a workflow generated from its YAML to review triggers, steps, branches, and run results in Kibana.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
type: how-to
---

# Visualize a workflow [workflows-visualize]

The graph view shows your workflow as a graph generated from its YAML. Use it to check the trigger, the order of steps, and every branch at a glance instead of reading the YAML line by line. The graph view is read-only. You can inspect steps and run them from the graph, but you make changes in the YAML editor.

## Before you begin [workflows-visualize-before-you-begin]

- Workflows must be turned on, and your role must have the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.
- {applies_to}`stack: experimental =9.5` Turn on the graph view in the space where you want to use it. In **Advanced Settings**, turn on **Elastic Workflows: Experimental Features** (`workflows:experimentalFeatures`), save your changes, and reload {{kib}}. This setting also moves **Run workflow** and the editor tools into the editor's bottom bar. In later versions, the graph view is available without this setting.

## View a workflow as a graph [workflows-visualize-how-to]

1. Open a workflow in the [YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. If the editor's bottom bar is collapsed, hover over it to expand it. Then select **Graph**. To return to the YAML, select **YAML**.
3. Select a step or the trigger to open its details panel. The panel shows the name, type, and definition as read-only YAML.
4. To change the step, select **Open in YAML editor**. The editor switches to YAML and scrolls to that step.

If your role can run workflows, you can also run a single step from the graph. Select **Run step** {icon}`play` in the details panel, or hover over the step on the graph and select {icon}`play`. You can't run a trigger on its own.

The graph updates as you edit the YAML. If the YAML has errors, the graph keeps showing the last valid version until you fix them.

To move around a large workflow, use the zoom controls on the canvas to zoom in, zoom out, reset the zoom, or fit the whole workflow in view. To lay out the graph horizontally instead of vertically, open **Settings** in the bottom bar and set **Direction** to **Horizontal**.

## Check a run on the graph [workflows-visualize-runs]

To see how a run moved through the workflow, open the **Executions** tab, select a run, and then select **Graph** in the bottom bar. The graph colors each step by its status, so you can see which steps succeeded, which failed, and which are still running. The graph updates while the run is in progress. To learn more about runs, refer to [](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).

## What the graph shows [workflows-visualize-capabilities]

| Element | What you see |
|---------|--------------|
| **Triggers and steps** | The graph starts with the workflow [trigger](/explore-analyze/workflows/triggers.md) and shows each [step](/explore-analyze/workflows/steps.md) in order. Step names appear in title case, so a step named `send_slack_message` appears as "Send Slack Message". |
| **Missing branches** | For an [`if`](/explore-analyze/workflows/steps/if.md) with only a true path, the graph still draws a labeled false path. For a [`switch`](/explore-analyze/workflows/steps/switch.md) with no `default`, it still draws a labeled default path. Those paths meet again at the next shared step, so missing branches are easier to spot. |
| **Parallel branches** | For a [`parallel`](/explore-analyze/workflows/steps/parallel.md) step with a fixed set of `branches`, each branch appears as its own path, labeled with the branch name. A `parallel` step that fans out over a list appears as a single step. |
| **Loops** | [`foreach`](/explore-analyze/workflows/steps/foreach.md) and [`while`](/explore-analyze/workflows/steps/while.md) loops appear as containers that hold the steps they repeat. Containers can nest inside each other. |
| **Retries** | A step with [retries](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md#workflows-on-failure-retry) configured shows a badge with its maximum number of attempts. |
