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

A skill is a reusable instruction set that gives [agents](agent-builder-agents.md) specialized expertise for a particular type of task. Instead of embedding the same detailed instructions in every agent that needs them, you author a skill once and assign it wherever it's needed. This keeps agent configurations clean and makes expertise easy to maintain and share across your team.

Tools are discrete operations the agent can invoke. Skills are higher-level capability packs that bundle tools, instructions, and context for a specific task domain. To learn more about tools, refer to [Tools](tools.md).

Skills differ from the agent's base system prompt: the system prompt is always in context, while skills are loaded selectively. An agent can have access to many skills without loading them all into the context window at once.

## How agents use skills

When an agent receives a message, it selects a skill if it determines that one of the available skills is relevant to the query based on the skill's name and description. If a skill activates, it provides:

- **Knowledge content**: domain-specific instructions written in Markdown that tell the agent how to approach the task.
- **Tools**: [Built-in tools](tools/builtin-tools-reference.md) or [custom tools](tools/custom-tools.md)  that the agent can call while the skill is active.

## Use cases

Use skills when you have domain-specific knowledge or procedures that multiple agents should follow consistently. Some examples:

- An {{product.security}} user asks about a suspicious host. The [`entity-analytics`](builtin-skills-reference.md#agent-builder-entity-analytics-skill) skill activates and guides the agent through finding the entity, analyzing its risk score, asset criticality, and behavioral history.
- An {{product.observability}} user asks why a service is slow or why an alert fired. The [`observability.investigation`](builtin-skills-reference.md#agent-builder-observability-investigation-skill) skill activates and diagnoses the issue across APM services and infrastructure.
- An {{product.elasticsearch}} user asks how to combine keyword and vector search for a product catalog. The [`search.hybrid-search`](builtin-skills-reference.md#agent-builder-search-hybrid-search-skill) skill activates and guides the agent through building a hybrid search solution.

## Built-in skills

{{agent-builder}} ships with built-in skills for common task domains. The skills available depend on your solution or serverless project type: some skills are available across all deployments, while others are specific to {{es}}, {{observability}}, or {{elastic-sec}}. Built-in skills are **read-only** and cannot be modified or deleted.

For the complete list, refer to [Built-in skills reference](builtin-skills-reference.md).

## Custom skills

You can extend the built-in catalog with your own custom skills. Custom skills are saved to your skill library, which you can manage from **Manage components > Skills**. Creating a skill adds it to the library, but it is not available to any agent until you add it from **Customize > Skills** on that agent. This separation means you can maintain a shared library of skills and choose which ones each agent has access to.

To learn how to create and manage custom skills, refer to [Custom skills](custom-skills.md).

## List skills using the API

To retrieve all available skills programmatically, use the [List skills](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-skills) API endpoint: `GET /api/agent_builder/skills`. For the full set of skills CRUD operations, refer to [Custom skills](custom-skills.md#skills-api).

## Next steps

- Review all built-in skills in the [Built-in skills reference](builtin-skills-reference.md).
- Learn how to create your own in [Custom skills](custom-skills.md).
- Write effective custom skill instructions with the [Skill creation guidelines](skill-creation-guidelines.md).
- Explore [Tools in {{agent-builder}}](tools.md) to understand how tools and skills relate.

## Related pages

- [Built-in tools reference](tools/builtin-tools-reference.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
