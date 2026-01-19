---
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

Unlike custom agents, you cannot modify or delete these agents. However, they serve as excellent examples for [building your own custom agents](agent-builder-agents.md#create-a-new-agent-in-the-gui).

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

**Availability:**
* **All views:** Available in {{es}}, {{observability}}, Security, and Classic views.

**Assigned Tools:**
* All **Platform core tools** (e.g., `list_indices`, `execute_esql`, `get_document_by_id`)
* `product_documentation`

## {{observability}} Agent
```{applies_to}
stack: preview =9.3
```

A specialized agent for logs, metrics, and traces. It is designed to assist with infrastructure monitoring and application performance troubleshooting.

**Availability:**
* **Observability** view
* **Classic** view

**Assigned Tools:**
* All **{{observability}} tools** (e.g., `observability.get_alerts`, `observability.get_services`, `observability.get_log_change_points`)
* All **Platform core tools**

## Threat Hunting Agent
```{applies_to}
stack: preview =9.3
```

A specialized agent for security alert analysis tasks, including alert investigation and security documentation. It helps analysts triage alerts and understand complex security events.

**Availability:**
* **Security** view
* **Classic** view

**Assigned Tools:**
* All **Security tools** (e.g., `security.alerts`, `security.entity_risk_score`, `security.attack_discovery_search`)
* All **Platform core tools**

## Related pages

- [Create a new agent](agent-builder-agents.md#create-a-new-agent-in-the-gui)