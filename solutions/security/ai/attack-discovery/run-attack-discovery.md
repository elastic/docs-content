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

Attack Discovery uses a [large language model (LLM)](/explore-analyze/ai-features/llm-guides/llm-connectors.md) to find related alerts that might be part of the same attack. You can start a run on demand, set up a recurring schedule, add a run to a workflow, or ask {{agent-builder}} to run it in chat. Where you start a run depends on your subscription, version, and deployment:

| When to use this | Run from | {{stack}} Enterprise | {{serverless-short}} Complete |
|---|---|:---:|:---:|
| Select which alerts to analyze, then run Attack Discovery immediately or on a schedule. | [**Attacks** view](/solutions/security/ai/attack-discovery/run-from-attacks-page.md) | ✓ (9.4+) | ✓ |
| Include Attack Discovery as one step in a larger workflow. | [A workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md) | ✓ (9.5+) | ✓ |
| Ask {{agent-builder}} to investigate in chat. | [{{agent-builder}} chat](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md) | ✓ (9.5+) | ✓ |
| Run Attack Discovery on demand or on a schedule. | [**Attack Discovery** page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) | ✓ (9.0–9.5 only) | — |

:::{note}
Attack Discovery isn't available with a {{stack}} Basic, Gold, or Platinum subscription, or in {{serverless-short}} Security Analytics Essentials projects.
:::

:::{dropdown} Run Attack Discovery in Elastic AI SOC Engine (EASE) projects
[EASE](/solutions/security/ai/ease/ease-intro.md) projects don't have the **Attacks** view. In an EASE project, you can run Attack Discovery from the [**Attack Discovery** page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) and [a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md).
:::
