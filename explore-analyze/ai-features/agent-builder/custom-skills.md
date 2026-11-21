---
navigation_title: "Custom skills"
description: "Learn how to create, edit, and manage custom skills in Agent Builder."
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

You can create a skill from **Manage components** → **Skills**, or inline when adding skills to an agent from **Customize** → **Skills**.

:::{tip}
For guidance on writing effective descriptions and instructions, refer to [Skill creation guidelines](skill-creation-guidelines.md).
:::

:::::{stepper}
::::{step} Open the Create skill dialog

Go to **Manage components** → **Skills**, then select **Create a skill**. The following screenshot shows the dialog:

:::{image} images/create-new-skill.png
:alt: Create skill dialog showing fields for ID, Name, Description, Instructions, and Associated tools
:width: 550px
:screenshot:
:::

::::

::::{step} Fill in the skill fields

Complete the fields in the **Create skill** dialog:

- **ID**: A unique identifier for the skill.
- **Name**: A human-readable name (64-character limit).
- **Description**: A short description of when the agent should use the skill (1024-character limit). This field is always included in the agent's context, so it should be specific and semantically distinct from other skill descriptions.
- **Instructions**: The skill content in Markdown. Include trigger conditions, step-by-step instructions, examples, and edge cases. Corresponds to `content` in the API.
- **Referenced content** {applies_to}`stack: ga 9.5+`: Named content blocks that give the agent supplementary knowledge such as runbooks, playbooks, or reference material it can read selectively when the skill is triggered. Available under **Advanced options** in the UI. Corresponds to [`referenced_content`]({{kib-apis}}operation/operation-post-agent-builder-skills#operation-post-agent-builder-skills-body-application-json-referenced_content) in the API.
- **Associated tools**: The tools the skill should have access to (up to 100). Available under **Advanced options** in the UI. Corresponds to `tool_ids` in the API.

::::

::::{step} Save the skill

Select **Save**. The skill is added to your library and becomes available to assign to any agent.

::::

::::{step} Add the skill to an agent

Custom skills in your library are not available to your agents until you explicitly add them. To add a skill, go to **Customize** → **Skills** on the agent you want to configure and select **Add skills**. From here you can:

- **Import from skill library**: Select an existing skill from **Manage components** → **Skills**. After importing, make sure the skill is turned on in the agent's skill list.
- **Create a skill**: Build a new skill and add it to this agent in one step. The skill is enabled for the agent automatically and also saved to your library.

Built-in skill availability depends on your deployment type. Refer to [Built-in skills reference](builtin-skills-reference.md) for details.

::::

::::{step} Test the skill

Send the agent realistic queries that should trigger the skill. Check that the agent selects the skill when expected, follows your instructions correctly, and handles the edge cases you documented. Revise the description or instructions based on what you observe.

For guidance on writing effective instructions, refer to [Skill creation guidelines](skill-creation-guidelines.md).

::::

:::::

### Create a skill with the API [skills-api]

Create and manage skills programmatically using the {{kib}} REST API. The API supports all the same fields as the UI, including [`referenced_content`]({{kib-apis}}operation/operation-post-agent-builder-skills#operation-post-agent-builder-skills-body-application-json-referenced_content) for additional named content blocks the agent can read selectively. For request examples, refer to [Skills APIs](kibana-api.md#skills-apis).

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

Open a conversation with an agent that has [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) turned on, or that has the `skill-management` skill assigned, and ask it to create a skill. For example, "Create a skill that handles production alerts using our incident runbook." The agent asks clarifying questions when it needs more information, then presents the generated skill as a draft.

Review the description, instructions, associated tools, and references, and ask the agent to edit anything that needs changing. When the draft is ready, select **Create skill**. The skill is not added to your library until you select **Create skill**.

The following screenshot shows a skill draft in Agent Chat:

:::{image} images/create-skill-from-chat.png
:screenshot:
:alt: Skill draft in Agent Chat showing its description, instructions preview, associated tool references, and a Create skill button
:width: 750px
:::

To edit a skill that is already in your library, refer to [Edit a custom skill from Agent Chat](#edit-a-skill-from-chat).

## Edit a custom skill from Agent Chat [edit-a-skill-from-chat]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Ask an agent to view or edit a custom skill that is already in your library. The agent shows the skill as a card in the conversation, so you can review and save changes without leaving the chat. You can't edit built-in skills or skills provided by plugins from chat.

Before you start:

- Use an agent that has [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) turned on (the default Elastic AI Agent does) or that has the `skill-management` skill assigned.
- To save changes, you need the **Create and edit skills** privilege in the current space, the same privilege required to update a skill from **Manage components** → **Skills**. Refer to [{{agent-builder}} privileges](permissions.md#kib-privileges).

To view or edit a custom skill:

1. In an Agent Chat conversation, ask the agent to view or edit the skill by name or ID. For example, "Add a rate-limiting section to the incident-triage skill."
1. Review the skill card. Select **Preview** ([where to find it](#skill-card-preview)) to read the full instructions, or **Edit in Management** to open the saved skill in a new tab.
1. To change the skill, describe the change in the conversation. The agent shows an updated card with a **Draft** badge, a **Latest** badge, and **Save changes**.
1. (Optional) To compare the draft with the instructions that were loaded into the conversation, turn on **Show diff**.
1. Select **Save changes**. The card then shows a **Saved** badge and **Edit in Management**.

The following screenshot shows an edited skill draft with **Show diff** turned on. It shows the layout in stack 9.5 and 9.6. In stack 9.7+ and serverless, refer to [Where to find Preview](#skill-card-preview):

:::{image} images/edit-skill-from-chat.png
:screenshot:
:alt: Skill card in Agent Chat showing Draft and Latest badges, Preview and Save changes buttons, and a diff of the added instructions
:width: 750px
:::

### Where to find Preview [skill-card-preview]

::::{applies-switch}

:::{applies-item} { stack: ga 9.7+, serverless: ga }
**Preview** is in the **More actions** menu next to the primary button (**Save changes** or **Edit in Management**). On an older card in the same conversation, **Preview** is the main button.
:::

:::{applies-item} { stack: ga 9.5-9.6 }
**Preview** is a standalone button on the card.
:::

::::

### What to know before you save [skill-card-behavior]

Your library isn't updated until you save. **Save changes** replaces the saved skill's name, description, instructions, tools, and references with the draft on the card. This overwrites any changes made in **Manage components** → **Skills** or through the API since the agent loaded the skill. There is no conflict warning.

Which buttons you see depends on the card:

- **Show diff** appears only for an unsaved draft whose instructions differ from the loaded instructions. It compares instructions only, so a change to just the description, tools, or references shows no **Show diff**. After you save and then ask for another change, **Show diff** still compares against the instructions first loaded, so your earlier saved changes also appear as additions.
- **Save changes** and **Edit in Management** appear only on the newest version of a draft, which the **Latest** badge marks. If you ask the agent to load the skill again, it creates a separate card, and an earlier unsaved draft card keeps its own **Save changes**. Saving an older draft overwrites the library with that draft.

Without the **Create and edit skills** privilege, **Save changes** is disabled. You can still view the skill and ask the agent to draft changes, but you can't save them.

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Built-in skills reference](builtin-skills-reference.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
