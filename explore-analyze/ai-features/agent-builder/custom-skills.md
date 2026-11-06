---
navigation_title: "Custom skills"
description: "Learn how to create and manage custom skills in Agent Builder."
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

# Create and manage custom skills

Custom skills let you package domain-specific knowledge and tools into reusable instruction sets that can be assigned to any [agent](agent-builder-agents.md). For an overview of how skills work, refer to [Skills in {{agent-builder}}](skills.md).

## When to create a custom skill

Create a custom skill when you have domain-specific knowledge or procedures that are not covered by the [built-in skills](builtin-skills-reference.md). Custom skills are particularly useful when you need to:

- **Standardize a workflow**: Encode a repeatable process (such as a triage runbook or an onboarding checklist) so that every agent follows the same steps.
- **Share expertise across agents**: Write instructions once and assign them to multiple agents instead of duplicating the same guidance in each agent's system prompt.
- **Scope tools to a task**: Bundle specific tools with the instructions that explain how and when to use them, so the agent only has access to relevant tools for the task at hand.
- **Keep agent prompts clean**: Move detailed, task-specific instructions out of the system prompt and into a skill that loads only when needed.

## Create a custom skill [create-a-custom-skill]

You can create a custom skill in three ways:

- Use the {{agent-builder}} UI.
- Use the {{kib}} REST API.
- Ask an agent to create it from Agent Chat.

### Create a skill in the UI [create-a-skill-in-the-ui]

Follow these steps to create a custom skill and add it to your skill library. Once saved, you need to add the skill to an agent before the agent can use it.

You can create a skill from **Manage components → Skills**, or inline when adding skills to an agent from **Customize → Skills**.

:::{tip}
For guidance on writing effective descriptions and instructions, refer to [Skill creation guidelines](skill-creation-guidelines.md).
:::

:::::{stepper}
::::{step} Open the create skill form

Go to **Manage components → Skills**, then select **New skill**. This opens the **Create a new skill** page.

From an agent's **Customize → Skills** page, select **Add skill**, then **Create a skill**. That opens the **Create skill** flyout.

:::{image} images/create-new-skill.png
:alt: Create skill flyout with ID, Name, Description, Instructions, and Associated tools under Advanced options
:width: 550px
:screenshot:
:applies_to: { stack: ga 9.4-9.5 }
:::

::::

::::{step} Fill in the skill fields

Complete the fields in the form:

- {applies_to}`stack: ga 9.4-9.5` **ID**: Unique identifier for the skill. Use lowercase letters, numbers, hyphens, and underscores. Start and end with a lowercase letter or a number. The limit is 64 characters. The create form shows this field. The edit form shows it read-only.
- {applies_to}`stack: ga 9.4-9.5` **Name**: Display name. Use letters, numbers, spaces, hyphens, and underscores. Start and end with a letter or a number. The limit is 64 characters.
- {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` **Name**: Identifier for the skill. Use lowercase letters, numbers, hyphens, and underscores. Start and end with a lowercase letter or a number. The limit is 64 characters. As you type, the field lowercases text and replaces each space with a hyphen. The **Create a new skill** page and the **Create skill** flyout save this value as both the skill ID and the skill name. You can't change the name in the UI after you save the skill. The skills library and skill details show the name. Create and update messages from these forms show the name. Delete messages use the ID. For a skill created in this form, the ID and the name are the same value.
- **Description**: Short description of when the agent should use the skill (1,024-character limit). The agent uses the description to choose when to load the skill, so make it specific and distinct from other skill descriptions. Corresponds to `description` in the API.
- **Instructions**: Skill content in Markdown. Include trigger conditions, step-by-step instructions, examples, and edge cases. Corresponds to `content` in the API.
- **Files**: Optional Markdown the agent can read when it uses the skill, such as a runbook, playbook, or other reference material. On the **Create a new skill** page this is the **Files** section. In the **Create skill** flyout it appears above **Advanced options**. Select **Add file** to add one. The limit is 100 files. Corresponds to [`referenced_content`]({{kib-apis}}operation/operation-post-agent-builder-skills#operation-post-agent-builder-skills-body-application-json-referenced_content) in the API.
- **Associated tools**: Tools the skill can use. The limit is 5. On the **Create a new skill** page this is its own section. In the **Create skill** flyout, open **Advanced options** to select the tools. Corresponds to `tool_ids` in the API.

::::

::::{step} Save the skill

Select **Save**. The skill is added to your library and becomes available to assign to any agent.

::::

::::{step} Add the skill to an agent

Custom skills in your library are not available to your agents until you add them. On the agent, go to **Customize → Skills**.

- If the agent already has skills, select **Add skill**.
- {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` If the agent has no skills yet, select **Add skills**. That opens the library panel.

From **Add skill** you can:

- **Import from skill library**: Open the **Add skill from library** panel. Turn on the switch next to a skill to add it to this agent.
- **Create a skill**: Open the **Create skill** flyout, save the skill, and add it to this agent. The skill is also saved to your library.

Built-in skill availability depends on your deployment type. Refer to [Built-in skills reference](builtin-skills-reference.md) for details.

::::

::::{step} Test the skill

Send the agent realistic queries that should trigger the skill. Check that the agent selects the skill when expected, follows your instructions correctly, and handles the edge cases you documented. Revise the description or instructions based on what you observe.

For guidance on writing effective instructions, refer to [Skill creation guidelines](skill-creation-guidelines.md).

::::

:::::

### Create a skill with the API [skills-api]

Create and manage skills programmatically using the {{kib}} REST API. You can set the description, instructions (`content`), associated tools (`tool_ids`), and [`referenced_content`]({{kib-apis}}operation/operation-post-agent-builder-skills#operation-post-agent-builder-skills-body-application-json-referenced_content) the same way you do in the UI. For request examples, refer to [Skills APIs](kibana-api.md#skills-apis).

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` A create request still requires separate `id` and `name` fields. The **Create a new skill** page and the **Create skill** flyout send the **Name** value for both. With the API, `name` can differ from `id`. Use letters, numbers, spaces, hyphens, and underscores, start and end with a letter or a number, and stay within 64 characters. `id` uses lowercase letters, numbers, hyphens, and underscores, starts and ends with a lowercase letter or a number, and has the same 64-character limit. Get, update, and delete requests use `id` in the path. An update can change `name` and cannot change `id`. Skills created earlier keep their stored `id` and `name`. When those values differ, the skills library and skill details show `name`.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Agent Chat **Create skill** posts the `id` and `name` stored on the draft. That path does not copy the form behavior of sending one **Name** value for both fields.

- [List skills]({{kib-apis}}operation/operation-get-agent-builder-skills) `GET /api/agent_builder/skills`
- [Create a skill]({{kib-apis}}operation/operation-post-agent-builder-skills) `POST /api/agent_builder/skills`
- [Get a skill by ID]({{kib-apis}}operation/operation-get-agent-builder-skills-skillid) `GET /api/agent_builder/skills/{skillId}`
- [Update a skill]({{kib-apis}}operation/operation-put-agent-builder-skills-skillid) `PUT /api/agent_builder/skills/{skillId}`
- [Delete a skill]({{kib-apis}}operation/operation-delete-agent-builder-skills-skillid) `DELETE /api/agent_builder/skills/{skillId}`

### Create a skill from Agent Chat [create-a-skill-from-chat]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Open a conversation with any agent and ask it to create a skill. For example, "Create a skill that handles production alerts using our incident runbook." The agent presents the generated skill as a draft.

Review the description, instructions, associated tools, and references, and ask the agent to edit anything that needs changing. When the draft is ready, select **Create skill**. The skill is not added to your library until you select **Create skill**.

:::{image} images/create-skill-from-chat.png
:screenshot:
:alt: Skill draft in Agent Chat showing its description, instructions preview, associated tool references, and a Create skill button
:width: 750px
:::

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Built-in skills reference](builtin-skills-reference.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
