---
navigation_title: Visualize a workflow
applies_to:
  stack: experimental 9.5+
  serverless: experimental
description: View a read-only diagram of a workflow generated from its YAML to review triggers, steps, and branches in Kibana.
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

The diagram view shows your workflow as a visual graph generated from its YAML. Use it to review the trigger, step order, and branching structure at a glance instead of parsing the YAML line by line. In this release, the diagram is read-only. You can inspect and navigate the workflow, but you cannot build or rewire it from the graph.

## Before you begin [workflows-visualize-before-you-begin]

- Workflows must be turned on, and your role must have the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.
- Turn on the advanced setting that displays the diagram view. Refer to [Enable the diagram view](#workflows-visualize-enable) for more information.

## Enable the diagram view [workflows-visualize-enable]

The diagram view is off by default. Turn on the **Elastic Workflows: Experimental Features** advanced setting (`workflows:experimentalFeatures`) to use it.

1. Go to the **Advanced Settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `workflows:experimentalFeatures` (or **Elastic Workflows: Experimental Features**).
3. Toggle the setting on, then save your changes and reload the page.

Reload the YAML editor. The **YAML ↔ Graph** toggle will appear in the editor's bottom bar.

## View a workflow as a diagram [workflows-visualize-how-to]

1. Open a workflow in the [YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. In the bottom bar, select **Graph** to switch from YAML to the diagram. Select **YAML** to return to the editor.
3. Click a step or the trigger on the diagram to open its details panel. The panel shows the name, type, and definition as read-only YAML.
4. From the details panel, select **Open in YAML editor** to jump to that step in the YAML. If you have execute privileges, you can also select **Run step** from the panel, or from the play control that appears when you hover a step on the diagram.

The diagram updates as you change the YAML. Selecting a step highlights it in both the Graph and YAML views. You should see the trigger and each step on the diagram. Conditional and parallel steps appear as separate branches. Use the zoom controls on the canvas to zoom in, zoom out, reset zoom, or fit the workflow in view.

## What the diagram shows [workflows-visualize-capabilities]

| Feature | What you see |
|---------|--------------|
| **Triggers and steps** | The graph starts with the workflow [trigger](/explore-analyze/workflows/triggers.md) and shows each [step](/explore-analyze/workflows/steps.md) in order. |
| **Branches left out of the YAML** | For an [`if`](/explore-analyze/workflows/steps/if.md) with only a true path, the diagram still draws a labeled false path. For a [`switch`](/explore-analyze/workflows/steps/switch.md) with no `default`, it still draws a labeled default path. Those paths meet again at the next shared step, so missing branches are easier to spot. |
| **Parallel paths, loops, and nesting** | `parallel` steps appear as concurrent branches. Loops such as [`foreach`](/explore-analyze/workflows/steps/foreach.md) and [`while`](/explore-analyze/workflows/steps/while.md) appear as grouped containers, and nested [flow control](/explore-analyze/workflows/steps/flow-control-steps.md) stays readable on larger workflows. |

<!-- TODO post-9.5: examples, layouts, full overlay, cross-surface -->
