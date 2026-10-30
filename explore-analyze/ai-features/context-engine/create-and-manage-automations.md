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

Use the guided route to have {{agent-builder}} propose and set up an automation for the AI index:

1. Open **Context**, then select the AI index.
2. In the **Automations** section, select **Add automation** → **Create with AI Agent**.
3. {{agent-builder}} opens in the side panel and sends **Suggest an automation for this AI index.**

    If this browser already has a conversation for this AI index in the current space, {{agent-builder}} reopens it. The browser remembers one conversation for each AI index in each space.

    To start over:

    1. Click **Open navigation menu** at the top of the panel.
    2. Click **New chat**.
    3. Select **Add automation** → **Create with AI Agent** again.

    If you send a message in the new chat, or select a different chat from that menu, that conversation is the one that reopens next time.

4. Review the generation strategy that {{agent-builder}} proposes and the evidence it cites from your data.

    For an AI index without automations, {{agent-builder}} chooses the strategy from the data. It asks you to choose in these cases:

    - The description covers more than one recurring entity, such as products and customers. It asks which entity to profile.
    - Two strategies fit about equally, or the data doesn't show what the AI index is for. It asks you to choose a strategy.

    For an AI index that already has automations, it asks what you want to achieve.
5. What happens next depends on the strategy:

    - **Index/Table Metadata, Bottom-Up, Cumulative / Wiki-style, and Targeted KI**: {{agent-builder}} installs a template and attaches the automation to the AI index. The install has no confirmation prompt. When one strategy clearly fits, it installs without asking you to approve it in chat.
    - **Other strategies**: {{agent-builder}} asks you to confirm a plan before it builds anything:

        1. Review the plan, which includes the strategy, sources, corpus filter, and expected cost. Ask for changes where necessary, then confirm.
        2. {{agent-builder}} builds and pilots the workflow, removes the temporary KIs that the pilot wrote, and summarizes the results. Review the summary.
        3. In the confirmation prompt, select **Save and attach**. If the workflow replaces an existing automation, select **Replace** instead.

6. Confirm the run:

    - For an Index/Table Metadata, Bottom-Up, or Cumulative / Wiki-style automation that would write more than five KIs, the first prompt is a pilot of five items. Select **Run pilot**. **Cancel** is the other button.
    - Otherwise, select **Run automation** or **Cancel**.
    - A Targeted KI automation is the exception. {{agent-builder}} runs it without this prompt.

    To run the automation later:

    - Ask {{agent-builder}} again.
    - In the **Automations** section of the AI index, from the actions menu ({icon}`ellipsis`) for the automation, select **Run** after the workflow is enabled.
    - [Run it from the Workflows UI](#run-schedule-and-monitor-an-automation).

    If the pilot writes a KI for each item, {{agent-builder}} estimates how long the full run takes. Select **Run automation**.

    If the pilot fails, or doesn't write a KI for each item, {{agent-builder}} reports the problem and stops. The pilot writes real KIs, which the full run replaces. If you cancel the full run, the pilot's KIs stay in the AI index.
7. The full run continues in the background. To check on it, ask {{agent-builder}} for a progress update.
8. Return to the AI index and confirm that the workflow appears in the **Automations** section.

<!--
:::{image} images/suggest-automation.png
:alt: AI index Automations section showing the Add automation menu with the Create with AI Agent option
:width: 700px
:screenshot:
:::
-->

When {{agent-builder}} builds a workflow for a strategy that has no template, it pilots the workflow and deletes the temporary KIs the pilot wrote before you save it. Focus your review on the source data it reads, what each KI represents, the claims and query guidance it generates, and the checks it performs before writing a KI. You do not need to understand every line of the generated YAML.

## Create an automation manually

Use the manual route when you intend to author the workflow yourself:

1. Open the AI index. In the **Automations** section, select **Add automation** → **Create workflow**.
2. {{context-engine}} creates and attaches a workflow with **Enabled** turned off, then opens it in the Workflows YAML editor.
3. Replace the generic starter workflow with the trigger and steps that generate the intended KIs.
4. Include the appropriate {{context-engine}} workflow steps to create, update, verify, or delete KIs.
5. Test the workflow, review its output, then save it.
6. Return to the AI index and confirm that the workflow appears in the **Automations** section.

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
2. In the **Automations** section, from the actions menu ({icon}`ellipsis`) for the automation, select **View** to inspect the workflow YAML without leaving the page.
3. To edit the workflow, from the actions menu, select **Open in Workflows**.
4. Make and test the required changes, then save the workflow.

Saving a workflow creates a versioned snapshot. For information about comparing or restoring versions, refer to [Workflow version history](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflows-version-history).

## Run, schedule, and monitor an automation

Operate an automation from the Workflows UI:

- [Run the workflow manually](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflow-run) to generate or refresh KIs immediately.
- Add a [scheduled trigger](/explore-analyze/workflows/triggers/scheduled-triggers.md) when its KIs must refresh automatically.
- [Monitor the execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-monitor-execution) and inspect the inputs, outputs, and errors for each step.
- Use the **Enabled** toggle to control whether the workflow responds to its configured triggers.

After a successful run, return to the AI index's **Knowledge Indicators** tab and confirm that the expected KIs were created or updated.

:::{tip}
To steer an {{agent-builder}} agent toward the generated KIs, open **Manage components → Agents**, create or edit an agent, and add the AI index in its settings. For the complete setup and testing flow, refer to [Use {{context-engine}} with {{agent-builder}}](use-context-engine-with-agent-builder.md).
:::

## Detach or delete an automation

Removing an automation from an AI index detaches its workflow. It does not delete the workflow itself.

Detach an automation as follows:

1. Open the AI index.
2. In the **Automations** section, from the actions menu ({icon}`ellipsis`) for the automation, select **Delete**.
3. In the confirmation dialog, select **Remove**. The change is saved immediately.
4. Confirm that the automation no longer appears in the AI index.

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
