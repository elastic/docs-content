---
navigation_title: "Disabled pre-execution workflow"
description: "Resolve the Agent Builder error \"Workflow is disabled and cannot be executed\", caused by an agent or space that still references a disabled pre-execution workflow."
type: troubleshooting
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Agent messages fail when a pre-execution workflow is disabled in {{agent-builder}}

[Pre-execution workflows](../agents-and-workflows.md#pre-execution-workflows) run after each user message, before the agent makes any LLM calls in response. Disabling a workflow doesn't detach it from the agent or the space-level setting that references it, so the agent keeps trying to run it.

## Symptoms

* Every message to an agent fails before the agent responds. The agent never reaches the LLM, so you get no partial answer.
* The conversation shows a **Workflow Failed** error like this one:

  ```console-response
  The workflow "<workflow_id>" execution failed: Workflow '<workflow_id>' is disabled and cannot be executed.
  ```

* Depending on which setting holds the reference, either one agent fails or every agent in the space fails.

## Diagnosis

Two settings can assign a pre-execution workflow, and the agent runs the workflows from both. Find out which one references the disabled workflow.

1. **Check the agent.** Run the following request from [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md) and check `configuration.workflow_ids`:

   ```console
   GET kbn:/api/agent_builder/agents/<agent_id>
   ```

   You can also check in the UI. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list, select the failing agent, then go to **Settings** → **Pre-execution workflow**.

   On serverless, and on 9.5.3 and later, a disabled workflow appears in the **Workflows** selector as `<workflow name> (disabled)`.

   On 9.4.x, and on 9.5.0 through 9.5.2, disabled workflows don't appear in the selector, so it can look empty even though the API response lists a workflow ID. Use the API response to identify the workflow.

2. **Check the space-level setting.** Check this if the agent's `configuration.workflow_ids` is empty, or if every agent in the space fails. Run the following request and look for `agentBuilder:prePromptWorkflowIds`:

   ```console
   GET kbn:/api/kibana/settings
   ```

   The response lists only settings that someone has explicitly set. If the key is absent, no space-level workflows are assigned.

## Resolution

Remove the workflow from the setting that references it. To keep using the workflow, re-enable it instead.

:::{note}
Only users with wildcard {{kib}} application privileges, such as `superuser`, can change an agent's pre-execution workflows. There's no separate privilege you can grant for it. Other users get an `Only administrators can configure pre-execution workflows.` error from the API, and the **Workflows** selector is disabled for them in the UI. Changing the space-level setting is different: it requires the `manage_advanced_settings` privilege, which you can grant through the **Advanced Settings** feature privilege.
:::

### Remove the workflow from an agent [remove-from-agent]

1. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list, select the agent, then go to **Settings** → **Pre-execution workflow**.
2. Clear the disabled workflow from the **Workflows** selector, then save the agent.

   On 9.4.x, and on 9.5.0 through 9.5.2, disabled workflows don't appear in the selector. Re-enable the workflow, clear it from the selector, save the agent, then disable the workflow again. The 9.4.x releases don't receive the change that keeps disabled workflows visible.

You can also update the agent through the API. The following request clears every pre-execution workflow from the agent:

```console
PUT kbn:/api/agent_builder/agents/<agent_id>
{
  "configuration": {
    "workflow_ids": []
  }
}
```

The update replaces only the keys you send, so the agent keeps its instructions, tools, skills, and other settings. To keep the agent's other pre-execution workflows, list their IDs instead of sending an empty array.

### Remove the workflow from the space-level setting [remove-from-space]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

1. Go to **{{stack-manage-app}}** → **AI** → **GenAI Settings**.
2. In the **Agent Builder** section, find **Pre-execution workflow**.
3. Clear the workflow from the **Workflows** selector.
4. Select **Save changes**.

Agents run the space-level workflows whenever Elastic Workflows is turned on, even when the **Agent Builder** section is hidden. If the section doesn't appear, or if the disabled workflow isn't listed in the selector, clear the setting through the API instead. The setting is hidden from the **Advanced Settings** page, so the API is the only way to change it outside of **GenAI Settings**. The following request clears every space-level pre-execution workflow:

```console
POST kbn:/api/kibana/settings
{
  "changes": {
    "agentBuilder:prePromptWorkflowIds": []
  }
}
```

To keep the other workflows, list their IDs instead of sending an empty array. This request applies to the current space, so run it in each space that needs it.

## Best practices

* Before you disable a workflow, remove it from any agent and from the space-level setting that references it. Disabling alone breaks those agents.

## Resources

* [Pre-execution workflows](../agents-and-workflows.md#pre-execution-workflows)
* [Turn a workflow on or off](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflow-enable-disable)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
