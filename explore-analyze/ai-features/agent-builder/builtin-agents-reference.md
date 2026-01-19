---
description: Reference of all built-in agents available in Elastic Agent Builder
navigation_title: "Built-in agents reference"
applies_to:
  stack: preview =9.2, ga 9.3
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} built-in agents reference

This page lists the built-in agents available in {{agent-builder}}. Built-in agents are pre-configured by Elastic with specific instructions and tools to handle common use cases. 

You cannot modify or delete built-in agents. To customize one, you can clone it and [create a custom agent](agent-builder-agents.md#create-a-new-agent-in-the-gui).

## Availability

The availability of specific agents depends on your solution view or serverless project type.

:::{note}
{{product.observability}} and {{product.security}} users must opt-in to use {{agent-builder}}. To learn more, refer to [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
:::

## Elastic AI Agent
```{applies_to}
stack: preview =9.2, ga 9.3
serverless: ga
```

The **Elastic AI Agent** is the default general-purpose agent for {{es}}. It is designed to help with a wide range of tasks, from writing {{esql}} queries to exploring your data indices.


**Assigned Tools:**
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

## {{observability}} Agent
```{applies_to}
stack: preview =9.3
  serverless:
    observability: preview
```

A specialized agent for logs, metrics, and traces. It is designed to assist with infrastructure monitoring and application performance troubleshooting.


**Assigned Tools:**
* All [**{{observability}} tools**](./tools/builtin-tools-reference.md#observability-tools)
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

## Threat Hunting Agent
```{applies_to}
stack: preview =9.3
  serverless:
    security: preview
```

A specialized agent for security alert analysis tasks, including alert investigation and security documentation. It helps analysts triage alerts and understand complex security events.


**Assigned Tools:**
* All [**Security tools**](./tools/builtin-tools-reference.md#security-tools)
* All [**Platform core tools**](./tools/builtin-tools-reference.md#platform-core-tools)

## Related pages

- [Create a new agent](agent-builder-agents.md#create-a-new-agent-in-the-gui)
- [{{agent-builder}}](../elastic-agent-builder.md)
- [{{agent-builder}} built-in tools reference](./tools/builtin-tools-reference.md)