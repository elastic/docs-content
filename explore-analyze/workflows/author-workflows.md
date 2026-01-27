---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Reference guide for the workflow YAML editor interface.
---

# Author workflows [workflows-yaml-editor]

The YAML editor is the primary interface for creating and editing workflows. This page describes the editor's components and features.

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](setup.md) to learn more.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::


:::{image} /explore-analyze/images/workflows-editor.png
:alt: A view of Workflows editor
:screenshot:
:::

## Editor layout [workflows-editor-layout]

The editor layout is composed of the following elements:

| Component | Description |
|-----------|-------------|
| **Editor pane** | The main area for writing and editing workflows. To learn more about the expected workflow structure, refer to [](/explore-analyze/workflows.md) |
| **Actions menu** | A quick-add menu for pre-formatted [triggers](triggers.md) and [step types](steps.md).  |
| **Save button** | Saves the current workflow. |
| **Run button** | Manually runs the entire workflow or an individual step. <br> - Entire workflow: Click the **Run** icon {icon}`play` (next to **Save**).  <br> - Individual step: Select the step in the editor pane, then click the **Run** icon {icon}`play`.   |
| **Executions tab** | Shows [execution history](monitor-troubleshoot.md) and real-time logs. |
| **Validation logs** | Shows validation successes and failures. Some common validation errors include: <br> - Invalid YAML syntax because of incorrect indentation or formatting <br> - Missing a required field or property (for example, `name`, `type`) <br> - The step type is unknown or doesn't match a valid action <br> - Invalid template syntax because of malformed template expression|