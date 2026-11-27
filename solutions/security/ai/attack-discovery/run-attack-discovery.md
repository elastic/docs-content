---
navigation_title: Run Attack Discovery
description: "Choose how to run Attack Discovery: from the Attacks view, a workflow, Agent Builder chat, or the Attack Discovery page."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery [run-attack-discovery]

Pick the path that fits how you work and the {{stack}} version you have. Every option uses the same analysis steps. Every option also requires a [configured LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

| When to use this | Available in | Go to |
|---|---|---|
| Choose which alerts to analyze, then run Attack Discovery immediately or on a schedule. | {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | [Run from the Attacks view](/solutions/security/ai/attack-discovery/run-from-attacks-page.md) |
| Include Attack Discovery as one step in a larger workflow. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md) |
| Ask {{agent-builder}} to investigate in chat. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md) |
| Work from the standalone Attack Discovery page. This is the main path in {{stack}} 9.4 and earlier, and on the Elastic AI SOC Engine (EASE) tier. | {applies_to}`stack: ga` {applies_to}`serverless: ga` | [Run from the Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) |

:::{note}
:applies_to: {"stack": "ga 9.5+", "serverless": {"security": "ga"}}
By default, the **Attacks** view replaces the Attack Discovery page. On the EASE tier, the **Attacks** view is unavailable, so use the [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) instead. Elsewhere, you can keep using the Attack Discovery page by turning off the [`securitySolution:enableAlertsAndAttacksAlignment`](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting.
:::
