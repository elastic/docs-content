---
navigation_title: "Built-in agents"
description: "Reference of the pre-configured AI agents available in Elastic Agent Builder, including their specialized capabilities and assigned tools."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} built-in agents reference

Built-in agents are pre-configured by Elastic with specific instructions and tools to handle common use cases.

## Availability

The [Elastic AI Agent](#elastic-ai-agent) is created automatically in each [{{kib}} space](/deploy-manage/manage-spaces.md) when first accessed, and is only available in the space where it was created.

## Elastic AI Agent

The **Elastic AI Agent** is the default general-purpose agent for {{es}}. It is designed to help with a wide range of tasks, from writing {{esql}} queries to exploring your data indices.

It is a standard persisted agent that is space-aware, so you can customize it independently for each space: change its instructions, adjust which tools it has access to, or clone it as a starting point for a new agent.

:::{note}
:applies_to: { "stack": "preview =9.2, ga =9.3" }
In {{stack}} 9.2 (preview) and 9.3 (GA), the Elastic AI Agent cannot be modified or deleted. To customize it, clone it and [create a custom agent](custom-agents.md#create-a-new-agent).
:::

**Default assigned tools:**
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

::::{dropdown} Previous versions

:::{note}
:applies_to: { "stack": "preview =9.2, ga =9.3" }
{{product.observability}} and {{product.security}} users must opt-in to use {{agent-builder}}. To learn more, refer to [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
:::

## Observability Agent
```{applies_to}
stack: preview =9.3, removed 9.4+
serverless:
  observability: removed
```

A specialized agent for logs, metrics, and traces. It is designed to assist with infrastructure monitoring and application performance troubleshooting.


**Assigned tools:**
* All [**{{observability}} tools**](./tools/builtin-tools-reference.md#observability-tools)
* A subset of [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

## Threat Hunting Agent
```{applies_to}
stack: preview =9.3, removed 9.4+
serverless:
  security: removed
```

A specialized agent for security alert analysis tasks, including alert investigation and {{elastic-sec}} documentation. It helps analysts triage alerts and understand complex security events. For more information and example use-cases, refer to [](/solutions/security/ai/agent-builder/agent-builder.md).

**Assigned tools:**
* All [**Security tools**](./tools/builtin-tools-reference.md#security-tools)
* A subset of [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

The standalone **Threat Hunting Agent** is removed in 9.4. Threat hunting workflows now use the [Elastic AI Agent](#elastic-ai-agent) with the [`threat-hunting`](builtin-skills-reference.md#agent-builder-threat-hunting-skill) skill enabled, which provides the same capabilities without switching between separate built-in agents. For Security-specific context, refer to [](/solutions/security/ai/agent-builder/skills-model.md).

**Migration path:** Enable the [`threat-hunting`](builtin-skills-reference.md#agent-builder-threat-hunting-skill) skill on the Elastic AI Agent in place of that standalone agent. The skill ships with the same tool set and query templates previously bundled into the agent, plus platform core tools for generating and running {{esql}} queries. For use cases and example prompts, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md#threat-hunting).

::::

## Related pages

- [Agents](agent-builder-agents.md)
- [Create a custom agent](custom-agents.md#create-a-new-agent)
- [Built-in tools reference](./tools/builtin-tools-reference.md)
