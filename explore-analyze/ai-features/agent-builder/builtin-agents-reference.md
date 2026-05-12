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

Built-in agents are pre-configured by Elastic with instructions and tools to handle common use cases.

## Elastic AI Agent

The **Elastic AI Agent** is the default general-purpose agent. It is designed to help with a wide range of tasks, from writing {{esql}} queries to exploring your data indices.

The Elastic AI Agent is a standard persisted agent that is space-aware. A separate instance is created automatically in each [{{kib}} space](/deploy-manage/manage-spaces.md) when first accessed, and each instance can be customized independently: change its instructions, assign [skills](builtin-skills-reference.md) and [tools](./tools/builtin-tools-reference.md), or clone it as a starting point for a new agent.

:::{note}
In 9.2  and 9.3, the Elastic AI Agent cannot be modified or deleted. To customize it, clone it and [create a custom agent](custom-agents.md#create-a-new-agent).
:::


## Built-in agents in previous versions

:::{important}
In {{stack}} 9.3, {{agent-builder}} included two specialized built-in agents for observability and security use cases. Both were removed in 9.4 in favor of equivalent capabilities exposed as skills on the [Elastic AI Agent](#elastic-ai-agent).
:::

### Observability Agent
```{applies_to}
stack: preview =9.3, removed 9.4+
serverless:
  observability: removed
```

A specialized agent for logs, metrics, and traces. It is designed to assist with infrastructure monitoring and application performance troubleshooting.


**Assigned tools:**
* All [**{{observability}} tools**](./tools/builtin-tools-reference.md#observability-tools)
* A subset of [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

### Threat Hunting Agent
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

## Related pages

- [Agents](agent-builder-agents.md)
- [Create a custom agent](custom-agents.md#create-a-new-agent)
- [Built-in tools reference](./tools/builtin-tools-reference.md)
