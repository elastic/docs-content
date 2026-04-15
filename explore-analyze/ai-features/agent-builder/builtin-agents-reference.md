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

::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

Built-in agents cannot be modified or deleted. To customize one, you can clone it and [create a custom agent](custom-agents.md#create-a-new-agent).

The **Elastic AI Agent** is not a built-in agent in this version. It is a standard persisted default agent that is space-aware and editable. Refer to [Elastic AI Agent](#elastic-ai-agent) for details.

::::

::::{applies-item} { stack: preview =9.2, ga 9.3 }

:::{tip}
You cannot modify or delete built-in agents. To customize one, you can clone it and [create a custom agent](custom-agents.md#create-a-new-agent).
:::

::::

::::

## Availability

The availability of specific agents depends on your solution view or serverless project type.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

Built-in agents are space-agnostic: they are available across all [{{kib}} spaces](/deploy-manage/manage-spaces.md). The default [Elastic AI Agent](#elastic-ai-agent) is an exception: it is created automatically per space and is only available in the space where it was created.

:::

:::{applies-item} { stack: preview =9.2, ga 9.3 }

Built-in agents are space-agnostic: they are available across all [{{kib}} spaces](/deploy-manage/manage-spaces.md).

:::

::::

:::{note}
{{product.observability}} and {{product.security}} users must opt-in to use {{agent-builder}}. To learn more, refer to [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
:::

## Elastic AI Agent
```{applies_to}
stack: preview =9.2, ga 9.3+
serverless: ga
```

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

The **Elastic AI Agent** is the default general-purpose agent for {{es}}. Unlike the other built-in agents, it is a standard persisted agent that is automatically created in each [{{kib}} space](/deploy-manage/manage-spaces.md) when first accessed.

Because the default agent is space-aware, you can customize it independently for each space. You can change its instructions, adjust which tools it has access to, or clone it as a starting point for a new agent.

In {{elastic-sec}}, you enable [Security skills](/solutions/security/ai/agent-builder/skills-model.md) for domain workflows (for example, threat hunting or alert triage) instead of using a separate built-in security agent.

**Default assigned tools:**
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

:::

:::{applies-item} { stack: preview =9.2, ga 9.3 }

The **Elastic AI Agent** is the default general-purpose agent for {{es}}. It is designed to help with a wide range of tasks, from writing {{esql}} queries to exploring your data indices.

**Assigned tools:**
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

:::

::::

## Observability Agent
```{applies_to}
stack: preview 9.3
serverless:
  observability: preview
```

A specialized agent for logs, metrics, and traces. It is designed to assist with infrastructure monitoring and application performance troubleshooting.


**Assigned tools:**
* All [**{{observability}} tools**](./tools/builtin-tools-reference.md#observability-tools)
* A subset of [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

## Threat Hunting Agent [threat-hunting-agent]

::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

:::{warning}
The standalone Threat Hunting Agent is deprecated in {{stack}} 9.4. Use the [Elastic AI Agent](#elastic-ai-agent) with the Threat Hunting skill enabled for the same workflows. Refer to [Elastic AI Agent, skills, and tools in {{elastic-sec}}](/solutions/security/ai/agent-builder/skills-model.md).
:::

::::

::::{applies-item} { stack: preview =9.2, ga 9.3 }

```{applies_to}
stack: preview 9.3
serverless:
  security: preview
```

A specialized agent for security alert analysis tasks, including alert investigation and {{elastic-sec}} documentation. It helps analysts triage alerts and understand complex security events. For more information and example use cases, refer to [Agent Builder for {{elastic-sec}}](/solutions/security/ai/agent-builder/agent-builder.md).

**Assigned tools:**
* All [**Security tools**](./tools/builtin-tools-reference.md#security-tools)
* A subset of [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

::::

::::

## Related pages

- [Agents](agent-builder-agents.md)
- [Create a custom agent](custom-agents.md#create-a-new-agent)
- [Built-in tools reference](./tools/builtin-tools-reference.md)
