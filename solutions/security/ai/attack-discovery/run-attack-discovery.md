---
navigation_title: Run Attack Discovery
description: "Choose how to run Attack Discovery based on your role: analyst triage, scheduled monitoring, automation, or chat investigation."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery [run-attack-discovery]

Attack Discovery turns related alerts into attack narratives you can triage. How you start a run depends on your workflow: a manual or scheduled run in the UI, an automated workflow, or an {{agent-builder}} conversation. Use the table to open the guide that matches what you want to do.

| Best for | Available in | Go to |
|---|---|---|
| SOC analysts who configure, manually run, and schedule Attack Discovery from the **Attacks** view. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Attacks view](/solutions/security/ai/attack-discovery/run-from-attacks-page.md) |
| Automation builders who include Attack Discovery as one step in a larger workflow. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md) |
| SOC analysts who ask {{agent-builder}} to investigate in chat. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Run from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md) |
| SOC analysts who need to manually generate discoveries or create a schedule from the Attack Discovery UI (the primary place to run Attack Discovery before {{stack}} 9.5). | {applies_to}`stack: ga 9.0-9.4` | [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) |

:::{note}
:applies_to: {"stack": "preview =9.4"}
In 9.4, schedules created on the **Attacks** page or the **Attack Discovery** page appear on both.
:::
