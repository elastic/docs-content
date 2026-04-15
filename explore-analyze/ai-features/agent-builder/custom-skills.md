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

## Create a custom skill

Custom skills are saved to your skill library and can be assigned to any agent. You can create a skill from **Manage components > Skills**, or inline when adding skills to an agent from **Customize > Skills**.

:::{tip}
For guidance on writing effective descriptions and instructions, refer to [Skill creation guidelines](skill-creation-guidelines.md).
:::

:::::{stepper}
::::{step} Open the Create skill dialog

Go to **Manage components > Skills**, then select **Create a skill**.

::::

::::{step} Fill in the skill fields

Complete the fields in the **Create skill** dialog:

- **ID**: A unique identifier for the skill.
- **Name**: A human-readable name (64-character limit).
- **Description**: A short description of when the agent should use the skill (1024-character limit). This field is always included in the agent's context, so it should be specific and semantically distinct from other skill descriptions.
- **Instructions**: The skill content in Markdown. Include trigger conditions, step-by-step instructions, examples, and edge cases. Corresponds to `content` in the API.
- **Associated tools**: The tools the skill should have access to (up to 100). Available under **Advanced options** in the UI. Corresponds to `tool_ids` in the API.

:::{image} images/create-new-skill.png
:alt: Create skill dialog showing fields for ID, Name, Description, Instructions, and Associated tools
:width: 550px
:screenshot:
:::

::::

::::{step} Save the skill

Select **Save**. The skill is added to your library and becomes available to assign to any agent.

::::

:::::

### Use the API

You can also create and manage skills programmatically using the [Skills API](#skills-api). The API supports all the same fields as the UI, plus `referenced_content`: additional named content blocks the agent can read selectively.

## Add skills to an agent

To add skills to the selected agent, go to **Customize > Skills** and select **Add skills**. You have two options:

- **Import from skill library**: Add a previously created skill from **Manage components > Skills** to this agent.
- **Create a skill**: Create a new skill and add it to this agent in one step. The new skill is also saved to **Manage components > Skills**.

Built-in skill availability depends on your deployment type. Refer to [Built-in skills reference](builtin-skills-reference.md) for details.

## Skills API

Use the {{kib}} REST API to manage skills programmatically. For request examples, refer to [Skills APIs](kibana-api.md#skills-apis).

- [List skills](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-skills) `GET /api/agent_builder/skills`
- [Create a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-skills) `POST /api/agent_builder/skills`
- [Get a skill by ID](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-skills-skillid) `GET /api/agent_builder/skills/{skillId}`
- [Update a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-agent-builder-skills-skillid) `PUT /api/agent_builder/skills/{skillId}`
- [Delete a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-agent-builder-skills-skillid) `DELETE /api/agent_builder/skills/{skillId}`

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Built-in skills reference](builtin-skills-reference.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
