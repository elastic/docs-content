---
navigation_title: AI onboarding
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: cloud-serverless
  - id: elasticsearch
  - id: kibana
---

# AI onboarding in {{es}} projects

**AI onboarding** is a skill you can invoke in your IDE, CLI, or directly within your Elastic deployment using [](/explore-analyze/ai-features/elastic-agent-builder.md). This skill enables an AI agent to guide you from an initial idea for your use case to a working search experience, using natural language.

The agent asks what you’re building, understands your data, recommends the right approach, and generates a working implementation. This helps you get started immediately without reading documentation or creating templates.
Along the way, it explains key {{es}} concepts such as indices, mappings, and queries, so you learn while building.

AI onboarding helps you:

- **Get to value faster**: go from idea to a working search experience in minutes, not days
- **Build the right solution**: receive recommendations tailored to your use case and data
- **Learn by doing**: understand {{es}} concepts as part of the workflow
- **Avoid common pitfalls**: the assistant explains decisions and validates key steps

AI onboarding uses a guided, conversational flow that adapts to your use case.
It starts by understanding your intent, then analyzes your data and requirements.
Based on this, it recommends an appropriate search approach and guides you through implementation, including mappings, indexing, and queries.

## Get started with AI onboarding

When you start a new {{es}} project, the **Getting started** page opens. To access it later, use the **Getting started** menu.

:::{image} /solutions/images/ai-onboarding-paths.png
:alt: AI onboarding paths
:screenshot:
:::

You can choose between two onboarding paths:

### Use your IDE or CLI

Install Elastic onboarding skills in your preferred coding assistant (for example, Cursor or Claude Code):

1. Click **Copy prompt**.
2. Copy the generated prompt.

  :::{image} /solutions/images/ai-onboarding-copy-prompt.png
  :alt: AI onboarding prompt
  :screenshot:
  :::
3. Paste the prompt into your coding agent to install the onboarding skills.

Once installed, your coding agent can guide you through the onboarding flow.

### Use Elastic AI Agent

You can start onboarding directly in Elastic using the [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) chat. From the {{es}} getting started page in the UI:

1. Click **Open Elastic AI Agent**.
2. A chat interface opens.

  :::{image} /solutions/images/ai-onboarding-chat.png
  :alt: AI onboarding chat
  :screenshot:
  :::
3. Describe what you want to build.

The agent asks about your use case and data, recommends an appropriate search approach, guides you through mappings and setup, and generates a working implementation.

You can also [invoke the onboarding skill directly](/explore-analyze/ai-features/agent-builder/skills.md#how-skills-are-invoked):

:::{image} /solutions/images/ai-onboarding-skill.png
:alt: Invoke the AI onboarding skill directly
:screenshot:
:::
