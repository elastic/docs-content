---
navigation_title: Manage and organize workflows
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Find, edit, duplicate, enable, disable, run, and review version history for workflows from the Workflows page in Kibana.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Manage and organize workflows [workflows-manage]

The **Workflows** page allows you to view and manage all your workflows. From the page, you can create, edit, duplicate, delete, and more with your workflows. To find the **Workflows** page, use the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

## Available actions [workflow-available-actions]

From the Workflows page, you can create new workflows, search and filter existing ones, manually trigger workflows, and more.

### Create a workflow [workflow-create]

Click **Create workflow** to open the YAML editor with the AI chat sidebar. You can [describe the workflow in natural language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md), write [YAML](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) by hand, or move between the two.

### Search and filter [workflow-search-filter]

Use the search bar to filter workflows by name, description, or tag. You can also use the **Enabled** filter to only show workflows that are turned on (enabled) or off (disabled), and the **Created By** filter to only show workflows created by the specified user.

### Run a workflow [workflow-run]

To instantly run a workflow, click the **Run** icon {icon}`play` for a workflow, or open the **All actions** menu ({icon}`boxes_vertical`) and click **Run**. The workflow manually runs regardless of its specified triggers. To learn about monitoring workflow runs, refer to [](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).

### Edit a workflow [workflow-edit]

Click the **Edit** icon to open the workflow in the YAML editor. Alternatively, open the **All actions** menu ({icon}`boxes_vertical`), and click **Edit**.

### Turn a workflow on or off [workflow-enable-disable]

Use the **Enabled** toggle to control whether a workflow can run:

- **Enabled**: The workflow responds to its configured triggers.
- **Disabled**: The workflow won't run, even if it's triggered.

## Version history [workflows-version-history]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Every time you save a workflow, Elastic records a new **workflow version**: a numbered snapshot of the full definition, who saved it, and when. Use version history to review teammate edits, inspect what changed after a refactor, or roll back to a known-good definition.

Versions are kept indefinitely by default.

### Open the history timeline [workflows-version-history-open]

1. Open a workflow in the editor.
2. In the workflow header, open the **More** menu {icon}`boxes_vertical` and select **History**.

The timeline lists committed versions newest first. Each entry shows:

- A version badge (`v1`, `v2`, `v3`, and so on)
- **Current version** on the latest committed version (when you have no unsaved edits)
- Who saved the version and when
- A change summary grouped by **Steps**, **Triggers**, and **Settings** (for example, steps added or removed), so you can scan changes without reading the full YAML

### Compare versions [workflows-version-history-compare]

Select a version in the timeline to preview its YAML in the editor:

- **Single-version view**: The full YAML for that version
- **Compare view**: A line-by-line diff against the previous version, or against another version you choose with **Compare to this version**. Added and removed lines are highlighted in the YAML, and a counter at the bottom of the editor shows how many changes the version contains. Use the arrows beside it to step through the changes one at a time.

  :::{tip}
  To flag validation errors, select the settings icon {icon}`controls` at the bottom right of the YAML preview, then turn on validation error highlighting.
  :::

If you have unsaved edits, they appear at the top of the timeline as **Unsaved changes**. Select that row to compare your draft against the last committed version before you save.

### Restore a previous version [workflows-version-history-restore]

1. Select a version in the timeline or use **Restore this version** on a timeline row.
2. Review the preview or diff.
3. Select **Restore**, then confirm.

Restoring creates a **new** version at the top of the timeline with a comment such as **Restored from v3**. History is preserved; restore is not a destructive revert.

You cannot restore **Managed** workflows. Restore requires the Workflows **Update** privilege; viewing history requires **Read**. Refer to [](/explore-analyze/workflows/get-started/setup.md#workflows-role-access).

### Execution and version linkage [workflows-version-history-executions]

Each workflow execution is linked to the workflow version that was active when it ran. Open an execution from the **Executions** tab to see which version was used for that run. Refer to [](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).
