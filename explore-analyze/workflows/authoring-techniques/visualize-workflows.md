---
navigation_title: Visualize a workflow
applies_to:
  stack: experimental 9.5+
  serverless: experimental
description: View a read-only graph of a workflow generated from its YAML to review triggers, steps, and branches in Kibana.
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

The graph view shows your workflow as a graph generated from its YAML. Use it to review the trigger, step order, and branching structure at a glance instead of parsing the YAML line by line. In this release, the graph view is read-only. You can inspect and navigate the workflow, but you cannot build or rewire it from the graph.

## Before you begin [workflows-visualize-before-you-begin]

- Workflows must be turned on, and your role must have the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.
- The graph view is off by default. In **Advanced Settings**, turn on the **Elastic Workflows: Experimental Features** (`workflows:experimentalFeatures`) advanced setting, then reload the page. The **YAML ↔ Graph** toggle appears in the editor's bottom bar.

## View a workflow as a graph [workflows-visualize-how-to]

1. Open a workflow in the [YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. In the bottom bar, select **Graph** to switch from YAML to the graph view. Select **YAML** to return to the editor.
3. Click a step or the trigger on the graph to open its details panel. The panel shows the name, type, and definition as read-only YAML.
4. From the details panel, select **Open in YAML editor** to jump to that step in the YAML. If you have execute privileges, you can also select **Run step** from the panel, or from the play control that appears when you hover a step on the graph.

The graph updates as you change the YAML. Selecting a step highlights it in both the graph and YAML views. Use the zoom controls on the canvas to zoom in, zoom out, reset zoom, or fit the workflow in view.

### What the graph shows [workflows-visualize-capabilities]

| Feature | What you see |
|---------|--------------|
| **Triggers and steps** | The graph starts with the workflow [trigger](/explore-analyze/workflows/triggers.md) and shows each [step](/explore-analyze/workflows/steps.md) in order. |
| **Branches left out of the YAML** | For an [`if`](/explore-analyze/workflows/steps/if.md) with only a true path, the graph still draws a labeled false path. For a [`switch`](/explore-analyze/workflows/steps/switch.md) with no `default`, it still draws a labeled default path. Those paths meet again at the next shared step, so missing branches are easier to spot. |
| **Parallel paths, loops, and nesting** | `parallel` steps appear as concurrent branches. Loops such as [`foreach`](/explore-analyze/workflows/steps/foreach.md) and [`while`](/explore-analyze/workflows/steps/while.md) appear as grouped containers, and nested [flow control](/explore-analyze/workflows/steps/flow-control-steps.md) stays readable on larger workflows. |
