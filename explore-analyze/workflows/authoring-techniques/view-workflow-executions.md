---
navigation_title: View workflow executions
type: how-to
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Browse and filter workflow executions across your Kibana space using the global Executions view.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

% Ask Tin (#1453): Should the badge say preview or experimental?
% Code leans preview (same pattern as the Template Library "tech preview"). Drafted as preview.

# View workflow executions across your space [workflows-view-executions]

Use the global **Executions** view to monitor ongoing and past workflow runs across your space. You don't need to open each workflow's editor. This page explains how to turn the view on, browse and filter executions, and open execution details.

The global **Executions** view complements the per-workflow [Executions tab](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md), which shows real-time logs and history for a single workflow.

## Before you begin [workflows-view-executions-before-you-begin]

- Workflows must be available in your deployment, and your role must have the privileges to access them. Refer to [](/explore-analyze/workflows/get-started/setup.md).
- You need the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions).
- The global **Executions** view is in technical preview and is turned off by default. To turn it on, you need a role that can change global {{kib}} settings (for example, `kibana_admin` on {{stack}}, or the `admin` project role on {{serverless-short}}).

## Enable the Executions view [workflows-enable-executions-view]

% Checked in Kibana: Turn this on with the global setting
% `workflowsManagement:globalExecutionsView:enabled` (off by default). It does not appear in
% Advanced Settings — use the API steps below. Do not document a kibana.yml flag (old leftover).
% Ask Tin: Will users get a visible Advanced Settings toggle later? Will Cloud turn this on by
% default in 9.5?

A global setting, `workflowsManagement:globalExecutionsView:enabled`, controls access to the page. You won't find this setting in **Advanced Settings**. Turn it on with the Kibana global settings API, then reload the page.

1. Open **Dev Tools**.
2. Send the following request:

   ```json
   POST kbn:/api/kibana/global_settings
   {
     "changes": {
       "workflowsManagement:globalExecutionsView:enabled": true
     }
   }
   ```

3. Reload {{kib}} so navigation and routing pick up the change.

**Checkpoint:** The **Executions** page opens.

To turn the view off later, set the same key to `false` and reload.

## Open the Executions page [workflows-open-executions-page]

% Checked in Kibana: There is no Workflows / Executions / Library sub-nav yet. Side nav can show
% Workflows and Template Library; Executions is not in that menu. Best path today is the URL
% `/app/workflows/executions`. Update this section if the nav changes.

Go to `/app/workflows/executions`.

**Checkpoint:** The page title is **Executions**, and the description reads that you can browse and filter workflow executions across your space.

## Browse and filter executions [workflows-browse-filter-executions]

The **Executions** page lists workflow runs in your current space. By default it shows the last 24 hours, sorted by start time (newest first).

1. Use the search bar to query with KQL, and adjust the time range as needed.
2. Filter by **Status**, **Workflow**, **Executed by**, and **Trigger**.
3. Optionally change visible columns. Default columns include workflow, status, execution ID, trigger, and executed by.

**Checkpoint:** The table updates to match your filters and time range.

## Inspect an execution [workflows-inspect-execution]

1. Select a row in the executions table.
2. Review the **Execution details** flyout for summary fields such as execution ID, workflow, status, start and finish times, trigger, and executed by.
3. Expand **Raw document** when you need the full JSON for the run.

For step-level logs, input and output, and failure diagnosis on a specific workflow, open that workflow and use the [Executions tab](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).

% Follow-up (#1454): Live step colors on the diagram belong on the visualize-workflows page, not
% here. Add a link after that page ships.

## Related [workflows-view-executions-related]

- [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md): Track a single workflow's runs and troubleshoot failures from the editor.
- [Manage and organize workflows](/explore-analyze/workflows/authoring-techniques/manage-workflows.md): Find and run workflows from the Workflows page.
- [Troubleshoot workflows](/explore-analyze/workflows/authoring-techniques/troubleshooting.md): Resolve common authoring and runtime issues.
- [Set up Workflows](/explore-analyze/workflows/get-started/setup.md): Privileges and access requirements.
