---
navigation_title: Use the YAML editor
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Author, test, and run workflows in the Kibana YAML editor, and understand the difference between test runs and production runs.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Use the YAML editor [workflows-yaml-editor]

The YAML editor is the primary interface for creating and editing workflows. This page describes the editor's components and features, and explains how test runs and production runs differ. You can write YAML yourself, or start from a [natural language description](/explore-analyze/workflows/authoring-techniques/use-natural-language.md) and edit the generated definition here. To review a workflow as a read-only graph instead of YAML, refer to [](/explore-analyze/workflows/authoring-techniques/visualize-workflows.md).

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.

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
| **Editor pane** | The main area for writing and editing workflows. To learn more about the expected workflow structure, refer to [](/explore-analyze/workflows.md). |
| **Actions menu** | A quick-add menu for pre-formatted [triggers](/explore-analyze/workflows/triggers.md) and [step types](/explore-analyze/workflows/steps.md). Built-in triggers (`manual`, `scheduled`, and `alert`) appear at the top level. <br> {applies_to}`stack: ga 9.5+` Event-driven triggers are grouped by family when a family has more than one trigger, so related triggers such as the cases triggers appear together under a **Cases** group. |
| **Save button** | Saves the current workflow. |
| **Run button** | Manually runs the entire workflow or an individual step. <br> - Entire workflow: Click the **Run** icon {icon}`play` (next to **Save**).  <br> - Individual step: Select the step in the editor pane, then click the **Run** icon {icon}`play`.   |
| **Executions tab** | Shows [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md) and real-time logs. |
| **Validation logs** | Shows validation successes and failures. Some common validation errors include: <br> - Invalid YAML syntax because of incorrect indentation or formatting <br> - Missing a required field or property (for example, `name`, `type`) <br> - The step type is unknown or doesn't match a valid action <br> - Invalid template syntax because of malformed template expression.|

:::{tip}
When viewing step output in the executions panel, click the **Copy** icon next to a step name to copy its full output path to your clipboard. For example, clicking **Copy** on a step named `check_if_newer` copies `steps.check_if_newer.output.conditionResult`, which you can paste directly into your workflow YAML to reference that step's output.
:::

## Test runs and production runs [workflows-test-vs-production-runs]

Every workflow execution is either a test run or a production run. Understanding the difference helps you iterate safely during development without affecting real processes.

| | Test run {icon}`flask` | Production run {icon}`play` |
|---|---|---|
| **Purpose** | Try out a workflow or individual step while authoring | Run an enabled workflow for real |
| **How to start** | Click **Run** {icon}`play` in the workflow editor. Refer to [Provide data for a test run](#workflows-supply-test-input) for more information. | Click **Run** from the workflow list, or let a configured trigger fire. |
| **Scope** | Entire workflow or a single step | Entire workflow |
| **Execution history** | Saved with a flask ({icon}`flask`) badge so you can filter for test runs. Step-level test runs are not saved in history. ![Alt text](/explore-analyze/images/workflows-test-runs.png "=700x600") | Saved without a badge. Filter the executions list by **production** to see only these runs. ![Alt text](/explore-analyze/images/workflows-filter-prod-runs.png "=700x600") |
| **Template context** | `execution.isTestRun` resolves to `true`. | `execution.isTestRun` resolves to `false`. |

You can use the `execution.isTestRun` context variable in your workflow YAML to change behavior during testing. For example, you can choose to skip sending a real notification during a test run.

## Provide data for a test run [workflows-supply-test-input]

When you click **Run** {icon}`play` in the editor, the **Test workflow** dialog asks what data to run the workflow against. Which options appear depends on the workflow's triggers. Common options include:

- **Document**: Use a real document from {{es}}. Appears when the workflow has a [manual trigger](/explore-analyze/workflows/triggers/manual-triggers.md).
- **Manual**: Type your own JSON.
- **Historical**: Reuse the data from a previous run. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`

For [event-driven](/explore-analyze/workflows/triggers/event-driven-triggers.md) workflows, the dialog also includes an **Event** tab where you can pick a real event to test against. Refer to [Test a workflow with a real event](/explore-analyze/workflows/triggers/event-driven-triggers.md#event-driven-triggers-test). {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`

For [alert-triggered](/explore-analyze/workflows/triggers/alert-triggers.md) workflows, the dialog includes an **Alert** tab where you can pick a real alert to test against.

### Use a document from {{es}} [workflows-supply-test-input-document]

Select **Document**, then search for and pick a document from an {{es}} index. The workflow runs against that document's actual field values, which is useful for confirming your steps behave correctly with real data before you rely on a live trigger.

### Type your own JSON [workflows-supply-test-input-manual]

Select **Manual**, then enter JSON directly in the dialog. This is useful for testing a specific scenario, such as an edge case or a field value that's hard to find in your existing data.

### Reuse data from a previous run [workflows-supply-test-input-historical]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Select **Historical**, then, under **Select execution**, search or pick a previous run from the list. A time-range filter next to the picker defaults to the last week, so you can narrow a long execution history down to the runs you care about.

After a run from the editor finishes, click the **Run again** icon {icon}`refresh` next to **Done** in the execution panel. The **Test workflow** dialog opens on the **Historical** tab with that run selected. The time range uses the execution's start time as the end of the range and a start one week earlier, so the selected run stays in the list.

If you select a run from the **Executions** tab, click **Run** in the editor and select **Historical**.

If you change the time range so the selected execution falls outside it, the selection clears and **Run** stays unavailable until you pick another execution.

After you select an execution, click **Run** to start a test run using that execution's data.

Reusing data this way is useful when you want to reproduce an issue or validate a workflow change against real data from a prior run, without tracking down the original event or re-entering values by hand.
