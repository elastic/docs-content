---
navigation_title: "Disabled pre-execution workflow"
description: 'Troubleshooting guide for the Agent Builder error "Workflow is disabled and cannot be executed", returned when an agent or space still uses that workflow.'
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

[Pre-execution workflows](../agents-and-workflows.md#pre-execution-workflows) run after each user message, before the agent makes any calls to the large language model (LLM) in response. Disabling a workflow doesn't remove it from the agent or the space setting that uses it, so the agent keeps trying to run it.

## Symptoms

- Every message to an agent fails before the agent responds. You get no partial answer.
- The conversation shows a **Workflow Failed** error like this one:

  ```console-response
  The workflow "<workflow_id>" execution failed: Workflow '<workflow_id>' is disabled and cannot be executed.
  ```

## Diagnosis

You can assign a pre-execution workflow in two places: on an individual agent, and on the space. An agent runs the workflows from both, so check each one. If every agent in the space fails, the space setting is the likely source.

1. **Check the agent.** Run the following request from [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md) and check `configuration.workflow_ids`:

   ```console
   GET kbn:/api/agent_builder/agents/<agent_id>
   ```

   You can also check in the UI. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list, select the failing agent, then go to **Settings** → **Pre-execution workflow**.

   On serverless, and on 9.5.3 and later, a disabled workflow appears in the **Workflows** selector as `<workflow name> (disabled)`.

   On 9.4.x, and on 9.5.0 through 9.5.2, disabled workflows don't appear in the selector, so it can look empty even though the API response lists a workflow ID. Use the API response to identify the workflow.

2. **Check the space setting.** Check this if the agent's `configuration.workflow_ids` is empty, or if every agent in the space fails. Run the following request and look for `agentBuilder:prePromptWorkflowIds`:

   ```console
   GET kbn:/api/kibana/settings
   ```

   The response lists only settings that someone has explicitly set. If the key is absent, no space workflows are assigned.

## Resolution

Remove the workflow from the setting that uses it. To keep using the workflow, re-enable it instead.

:::{note}
Removing a workflow from an agent requires a role that grants wildcard (`*`) {{kib}} privileges, such as the built-in `superuser` role. You can't grant this from the {{kib}} role management UI. Without it, the **Workflows** selector is read-only in the UI, and the API returns a `400` error with the message `Only administrators can configure pre-execution workflows.`

Changing the space setting requires the `manage_advanced_settings` privilege instead, which you can grant through the **Advanced Settings** [feature privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
:::

### Remove the workflow from an agent [remove-from-agent]

1. Open the agent's **Settings** → **Pre-execution workflow** section.
2. Clear the disabled workflow from the **Workflows** selector, then save the agent.

   On 9.4.x, and on 9.5.0 through 9.5.2, the disabled workflow doesn't appear in the selector. Re-enable the workflow, clear it from the selector, save the agent, then disable the workflow again.

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

### Remove the workflow from the space setting [remove-from-space]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

1. Go to **{{stack-manage-app}}** → **AI** → [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).
2. In the **Agent Builder** section, find **Pre-execution workflow**.
3. Clear the workflow from the **Workflows** selector.
4. Select **Save changes**.

Agents run the space workflows whenever Elastic Workflows is turned on, even when the **Agent Builder** section is hidden. If the section doesn't appear, or if the disabled workflow isn't listed in the selector, clear the setting through the API instead. The setting is hidden from the **Advanced Settings** page, so the API is the only way to change it outside of **GenAI Settings**. The following request clears every pre-execution workflow assigned to the space:

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

- Before you disable a workflow, remove it from any agent and from the space setting that uses it. Disabling it alone breaks those agents.
- Before you turn off the `agentBuilder:experimentalFeatures` advanced setting, clear the space setting. Assigned workflows keep running, but the **Agent Builder** section you'd use to change them disappears.

## Resources

- [Pre-execution workflows](../agents-and-workflows.md#pre-execution-workflows)
- [Assign workflows to every agent in a space](../agents-and-workflows.md#assign-pre-execution-workflows-to-a-space)
- [Turn a workflow on or off](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflow-enable-disable)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
