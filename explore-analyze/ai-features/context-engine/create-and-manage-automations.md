---
navigation_title: "Manage automations"
description: Create, inspect, run, schedule, update, and remove the workflow automations that generate Knowledge Indicators.
type: how-to
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Create and manage AI index automations

:::{include} _snippets/hidden-docs-notice.md
:::

Automations generate and refresh Knowledge Indicators (KIs) from an AI index's sources. {{context-engine}} runs each automation as an [Elastic workflow](/explore-analyze/workflows.md). You can have {{agent-builder}} propose and pilot one, author one in the Workflows UI, or manage workflows and their AI index associations programmatically.

## Before you begin

You need a custom AI index with at least one source, the **All** privilege for the **Context Engine** feature, and permission to create and manage workflows. To use the guided route, you also need access to {{agent-builder}} and permission to run workflows.

Decide what each KI should represent before creating an automation. Refer to [Select a generation strategy](build-and-maintain-ai-index.md#select-a-generation-strategy) and [Design useful Knowledge Indicators](build-and-maintain-ai-index.md#design-useful-knowledge-indicators).

## Create an automation with Agent Builder

Use the guided route to have {{agent-builder}} propose, pilot, and save a workflow for the AI index:

1. Open **Context**, then select the AI index.
2. In **Automations**, select **Suggest automation**.
3. {{agent-builder}} opens a new conversation and sends a request to suggest an automation for the AI index.
4. Review the proposed generation strategy, source coverage, KI content, and verification plan.
5. Ask for changes where necessary, then confirm that {{agent-builder}} should build and pilot the workflow.
6. Review the pilot summary and temporary KI output.
7. Tell {{agent-builder}} to save the automation.
8. Return to the AI index and confirm that the saved workflow appears in **Automations**.

<!--
:::{image} images/suggest-automation.png
:alt: AI index Automations section showing the Suggest automation action
:width: 700px
:screenshot:
:::
-->

The pilot can create and delete temporary KIs while testing the workflow. Focus your review on the source data it reads, what each KI represents, the claims and query guidance it generates, and the checks it performs before writing a KI. You do not need to understand every line of the generated YAML.

## Create an automation manually

Use the manual route when you intend to author the workflow yourself:

1. Open the AI index and select **Create automation**.
2. {{context-engine}} creates and attaches a workflow with **Enabled** turned off, then opens it in the Workflows YAML editor.
3. Replace the generic starter workflow with the trigger and steps that generate the intended KIs.
4. Include the appropriate {{context-engine}} workflow steps to create, update, verify, or delete KIs.
5. Test the workflow, review its output, then save it.
6. Return to the AI index and confirm that the workflow appears in **Automations**.

For YAML editing and test runs, refer to [Use the YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).

<!--
:::{image} images/workflow-automation-yaml-editor.png
:alt: Workflows YAML editor showing a newly created Context Engine automation
:width: 700px
:screenshot:
:::
-->

## Inspect or edit an automation

The AI index lists each attached workflow and whether it is enabled.

To inspect or edit one:

1. Open the AI index.
2. In **Automations**, use the preview action to inspect the workflow YAML without leaving the page.
3. Select **Edit workflow** to open it in the Workflows editor.
4. Make and test the required changes, then save the workflow.

Saving a workflow creates a versioned snapshot. For information about comparing or restoring versions, refer to [Workflow version history](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflows-version-history).

## Run, schedule, and monitor an automation

Operate an automation from the Workflows UI:

- [Run the workflow manually](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflow-run) to generate or refresh KIs immediately.
- Add a [scheduled trigger](/explore-analyze/workflows/triggers/scheduled-triggers.md) when its KIs must refresh automatically.
- [Monitor the execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-monitor-execution) and inspect the inputs, outputs, and errors for each step.
- Use the **Enabled** toggle to control whether the workflow responds to its configured triggers.

After a successful run, return to the AI index's **Knowledge Indicators** tab and confirm that the expected KIs were created or updated.

## Detach or delete an automation

Removing an automation from an AI index detaches its workflow. It does not delete the workflow itself.

Detach an automation as follows:

1. Open the AI index.
2. In **Automations**, select **Edit**.
3. Remove the automation, then select **Save**.
4. Confirm that it no longer appears in the AI index.

To delete the detached workflow, delete it separately from the Workflows UI. You can also choose to delete attached automations when you [delete the AI index](create-and-manage-ai-indices.md#delete-an-ai-index).

## Manage automations with the APIs

Use the Workflows APIs together with the {{context-engine}} APIs when you need to provision or operate automations programmatically:

1. Create the workflow with the [create workflow API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-workflows-workflow), or modify an existing workflow with the [update workflow API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-workflows-workflow-id). Use the [get workflow API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-workflows-workflow-id) to retrieve its current definition before changing it.
2. Attach the workflow by adding its ID to the AI index's `automations` array with the [create or update AI index API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-context-engine-ai-index-aiindexid):

    ```json
    {
      "automations": [
        {
          "type": "workflow",
          "value": "my-workflow-id"
        }
      ]
    }
    ```

3. Run it with the [run workflow API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-workflows-workflow-id-run), or enable its configured trigger. Use the [get workflow executions API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-workflows-workflow-workflowid-executions) to inspect its runs.
4. To detach it, remove its entry from the AI index's `automations` array. To remove the workflow itself, use the [delete workflow API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-workflows-workflow-id) separately.

Updating an AI index replaces its complete record. For an example that preserves the other fields, refer to [Update an AI index with the API](create-and-manage-ai-indices.md#update-ai-index-api).
