---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to view, organize, and manage your workflows.
---

# Manage workflows [workflows-manage]

The **Workflows** page allows you to view and manage all your workflows. From the page, you can create, edit, duplicate, delete, and more with your workflows. To find the **Workflows** page, use the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](setup.md) for more information.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

:::{image} /explore-analyze/images/workflows-page.png
:alt: A view of Workflows editor
:screenshot:
:::

## Available actions [workflow-available-actions]

From the Workflows page, you can create new workflows, search and filter existing ones, manually trigger workflows, and more.

### Create a workflow [workflow-create]

Click **Create a new workflow** to open the YAML editor. Refer to [](/explore-analyze/workflows/author-workflows.md) to learn how to use the editor.

### Search and filter [workflow-search-filter]

Use the search bar to filter workflows by name, description, or tag. You can also use the **Enabled** filter to only show workflows that are turned on (enabled) or off (disabled), and the **Created By** filter to only show workflows created by the specified user.

### Run a workflow [workflow-run]

To instantly run a workflow, click the **Run** icon {icon}`play` for a workflow, or open the **All actions** menu ({icon}`boxes_vertical`) and click **Run**. The workflow manually runs regardless of its specified triggers. To learn about monitoring workflow runs, refer to [](/explore-analyze/workflows/monitor-troubleshoot.md).

### Edit a workflow [workflow-edit]

Click the **Edit** icon to open the workflow in the YAML editor. Alternatively, open the **All actions** menu ({icon}`boxes_vertical`), and click **Edit**.

### Turn a workflow on or off [workflow-enable-disable]

Use the **Enabled** toggle to control whether a workflow can run:

- **Enabled**: The workflow responds to its configured triggers.
- **Disabled**: The workflow won't run, even if it's triggered.