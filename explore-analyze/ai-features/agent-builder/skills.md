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

A skill is a reusable capability pack that gives an [agent](agent-builder-agents.md) specialized expertise for a particular type of task. Each skill bundles three things:

- **Instructions**: domain-specific guidance written in Markdown that shapes how the agent approaches the task.
- **Tools**: [built-in](tools/builtin-tools-reference.md) or [custom](tools/custom-tools.md) tools the agent can call while the skill is active.
- **Context**: additional knowledge the skill can draw on, such as reference documents or runbooks.

This makes skills different from [tools](tools.md), which are discrete operations like running a query or retrieving a document. Skills sit one level higher, combining tools with the instructions and context needed to complete a workflow end to end.

Skills also differ from the agent's system prompt. The system prompt is always in context, while skills load selectively. An agent can have access to many skills without loading them all into the context window at once. You author a skill once and assign it to any agent that needs it, keeping agent configurations clean and making expertise easy to share across your team.

## How skills are invoked

Skills can be invoked in three ways:

**Automatic discovery (default)**
:   The agent receives a list of available skills with their names and descriptions. Based on the user's natural language input, it automatically selects and invokes the most relevant skill. No special syntax is needed.

**Slash commands**
:   Users can explicitly invoke a skill by typing `/` followed by the skill name and a prompt. This is useful when you know exactly which skill you need.

:::{image} images/skill-slash-command.png
:alt: Chat input showing a slash command that invokes the visualization-creation skill
:width: 550px
:screenshot:
:::

**Attachment-driven**
:   When a user attaches contextual data to a message (for example, an alert from the alert flyout), the agent can automatically invoke the relevant skill based on the attachment type.

## Use cases

Use skills when you have domain-specific knowledge or procedures that multiple agents should follow consistently. Some examples:

- An [{{product.security}}](/solutions/security/ai/agent-builder/agent-builder.md) user asks about a suspicious host. The [`entity-analytics`](builtin-skills-reference.md#agent-builder-entity-analytics-skill) skill activates and guides the agent through finding the entity, analyzing its risk score, asset criticality, and behavioral history.
- An [{{product.observability}}](/solutions/observability/ai/agent-builder-observability.md) user asks why a service is slow or why an alert fired. The [`observability.investigation`](builtin-skills-reference.md#agent-builder-observability-investigation-skill) skill activates and diagnoses the issue across APM services and infrastructure.
- An {{product.elasticsearch}} user asks how to combine keyword and vector search for a product catalog. The [`search.hybrid-search`](builtin-skills-reference.md#agent-builder-search-hybrid-search-skill) skill activates and guides the agent through building a hybrid search solution.

## Built-in skills

{{agent-builder}} ships with built-in skills for common task domains. The skills available depend on your solution or serverless project type: some skills are available across all deployments, while others are specific to {{es}}, {{observability}}, or {{elastic-sec}}. Built-in skills are **read-only** and cannot be modified or deleted.

For the complete list, refer to [Built-in skills reference](builtin-skills-reference.md).

## Custom skills

You can extend the built-in catalog with your own custom skills. Custom skills are saved to your skill library, which you can manage from **Manage components > Skills**. Creating a skill adds it to the library, but it is not available to any agent until you add it from **Customize > Skills** on that agent. This separation means you can maintain a shared library of skills and choose which ones each agent has access to.

To learn how to create and manage custom skills, refer to [Custom skills](custom-skills.md).

## List skills using the API

To retrieve all available skills programmatically, use the [List skills]({{kib-apis}}operation/operation-get-agent-builder-skills) API endpoint: `GET /api/agent_builder/skills`. For the full set of skills CRUD operations, refer to [Custom skills](custom-skills.md#skills-api).

## Next steps

- Review all built-in skills in the [Built-in skills reference](builtin-skills-reference.md).
- Learn how to create your own in [Custom skills](custom-skills.md).
- Write effective custom skill instructions with the [Skill creation guidelines](skill-creation-guidelines.md).
- Explore [Tools in {{agent-builder}}](tools.md) to understand how tools and skills relate.
- Bundle skills for distribution using [Plugins in {{agent-builder}}](plugins.md).

## Related pages

- [Built-in tools reference](tools/builtin-tools-reference.md)
- [{{agent-builder}} Kibana APIs](kibana-api.md)
