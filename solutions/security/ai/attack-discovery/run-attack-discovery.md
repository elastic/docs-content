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

Pick the path that fits how you work, your version, and your deployment. Every option uses the same analysis steps. Every option also requires a [configured LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

| When to use this | Available in | Go to |
|---|---|---|
| Choose which alerts to analyze, then run Attack Discovery immediately or on a schedule. The **Attacks** view isn't available in [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) projects. | {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | [Run from the Attacks view](/solutions/security/ai/attack-discovery/run-from-attacks-page.md) |
| Include Attack Discovery as one step in a larger workflow. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md) |
| Ask {{agent-builder}} to investigate in chat. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md) |
| Work from the standalone Attack Discovery experience. In {{serverless-short}}, only EASE projects include this page. | {applies_to}`serverless: ga` {applies_to}`stack: deprecated =9.5, ga 9.0-9.4` | [Run from the Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) |
