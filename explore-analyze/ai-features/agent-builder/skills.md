---
navigation_title: "Skills"
description: "Learn how Agent Builder skills extend agents with specialized knowledge and tools for specific task domains."
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

# Skills in {{agent-builder}}

Skills are reusable instruction sets that give [agents](agent-builder-agents.md) specialized expertise for a particular type of task. Instead of embedding the same detailed instructions in every agent that needs them, you author a skill once and assign it wherever it's needed. This keeps agent configurations clean and makes expertise shareable across your team.

Tools are discrete operations the agent can invoke. Skills are higher-level capability packs that bundle tools, instructions, and context for a specific task domain. To learn more about tools, refer to [Tools](tools.md).

Skills differ from the agent's base system prompt: the system prompt is always in context, while skills are loaded selectively. An agent can have access to many skills without loading all of them into the context window at once.

## How agents use skills

When an agent receives a message, it selects a skill if it determines that one of the available skills is relevant to the query based on the skill's name and description. If a skill activates, it provides:

- **Knowledge content**: domain-specific instructions written in Markdown that tell the agent how to approach the task.
- **Tools**: [Built-in tools](tools/builtin-tools-reference.md) or [custom tools](tools/custom-tools.md)  that the agent can call while the skill is active.

## Use cases

Use skills when you have domain-specific knowledge or procedures that multiple agents should follow consistently. Some examples:

- A {{product.security}} user asks to investigate a security alert. The [`alert-analysis`](builtin-skills-reference.md#agent-builder-alert-analysis-skill) skill activates and guides the agent through fetching the alert, finding related alerts by shared entity fields, correlating with threat intelligence, and assessing risk scores.
- A {{product.observability}} user asks why a service is slow. The [`observability.rca`](builtin-skills-reference.md#agent-builder-observability-rca-skill) skill activates and runs structured root cause analysis across logs, traces, and metrics.
- An {{product.elasticsearch}} user asks what data is in a given index. The [`data-exploration`](builtin-skills-reference.md#agent-builder-data-exploration-skill) skill activates and guides the agent to inspect the index schema and summarize the data.

## Built-in skills

{{agent-builder}} ships with built-in skills for common task domains. The skills available depend on your solution or serverless project type: some skills are available across all deployments, while others are specific to {{es}}, {{observability}}, or {{elastic-sec}}. Built-in skills are **read-only** and cannot be modified or deleted.

For the complete list, refer to [Built-in skills reference](builtin-skills-reference.md).

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

You can also create and manage skills programmatically using the [Skills API](kibana-api.md#skills-apis). The API supports all the same fields as the UI, plus `referenced_content`: additional named content blocks the agent can read selectively.

## Add skills to an agent

To add skills to the selected agent, go to **Customize > Skills** and select **Add skills**. You have two options:

- **Import from skill library**: Add a previously created skill from **Manage components > Skills** to this agent.
- **Create a skill**: Create a new skill and add it to this agent in one step. The new skill is also saved to **Manage components > Skills**.

% TODO: Confirm whether all built-in skills are assignable to custom agents, or some are solution-scoped.

## Skills API

Use the {{kib}} REST API to manage skills programmatically. For request examples, refer to [Skills APIs](kibana-api.md#skills-apis).

- [List skills](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-skills) `GET /api/agent_builder/skills`
- [Create a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-skills) `POST /api/agent_builder/skills`
- [Get a skill by ID](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-skills-skillid) `GET /api/agent_builder/skills/{skillId}`
- [Update a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-agent-builder-skills-skillid) `PUT /api/agent_builder/skills/{skillId}`
- [Delete a skill](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-agent-builder-skills-skillid) `DELETE /api/agent_builder/skills/{skillId}`

## Next steps

- Review all built-in skills in the [Built-in skills reference](builtin-skills-reference.md).
- Learn how to write effective custom skill instructions in [Skill creation guidelines](skill-creation-guidelines.md).
- Explore [Tools in {{agent-builder}}](tools.md) to understand how tools and skills relate.

## Related pages

- [Built-in skills reference](builtin-skills-reference.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [Built-in tools reference](tools/builtin-tools-reference.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
