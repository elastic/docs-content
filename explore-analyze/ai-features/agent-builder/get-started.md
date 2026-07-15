---
navigation_title: "Get started"
description: "Learn how to access Elastic Agent Builder, ingest data, and build skills for AI agents."
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

# Get started with {{agent-builder}}

To start using {{agent-builder}} you need to deploy {{es}} and {{kib}}.

If you don't already have an Elastic deployment, you can start a [free trial](https://cloud.elastic.co/registration) or refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type). 

::::{important}
This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons).
::::

:::::::{stepper}
::::::{step} Access {{agent-builder}}

:::::{applies-switch}

::::{applies-item} stack: ga 9.4+

On non-serverless deployments, {{agent-builder}} availability depends on the navigation mode of your {{kib}} space:

:::{dropdown} {{es}} solution view
{{agent-builder}} is enabled by default, replacing AI Assistant. You can access it from multiple entry points:
- Select the **Agent Builder** card on the {{es}} home page.
- Click **Agents** in the navigation menu.
- Click the **AI Agent** button in the top-right header to start a conversation from any page.
- Open the **Agent builder** API tutorial from the {{kib}} **Getting started** page, under **Explore the API**.
:::

:::{dropdown} {{product.observability}} and {{product.security}} solution views
{{agent-builder}} is enabled by default, replacing AI Assistant. You can access it from two entry points:
- Click **Agents** in the navigation menu.
- Click the **AI Agent** button in the top-right header to start a conversation from any page.
:::

:::{dropdown} Classic view
{{agent-builder}} appears in the side navigation under {{es}}. You can choose Agent Builder as your assistant through the initial selector or the [chat experience switch](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
:::

You can also search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

::::{applies-item} serverless: ga

{{agent-builder}} is the default chat experience in all serverless project types.

:::{dropdown} {{es-serverless}}

You can access {{agent-builder}} from multiple entry points in the UI:

- Select the **Elastic Agent** card on the {{es}} home page.
- Click **Agents** in the navigation menu.
- Click the **AI Agent** button in the top-right header to start a conversation from any page.
- Open the **Build a chat tool with Agent Builder** API tutorial from the {{kib}} **Getting started** page, under **Explore the API**.

:::

:::{dropdown} {{obs-serverless}} and {{sec-serverless}}
{{agent-builder}} is enabled by default, replacing AI Assistant. Click the **AI Agent** button in the top-right header to start a conversation from any page.
:::

You can also search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

:::::

:::::{dropdown} Previous versions
:applies_to: stack: preview =9.2, ga 9.3

On non-serverless deployments, {{agent-builder}} availability depends on the navigation mode of your {{kib}} space:

:::{dropdown} {{es}} solution view
{{agent-builder}} is enabled by default, replacing Search Assistant. You can access it from multiple entry points:
- Select the **Agent Builder** card on the {{es}} home page.
- Click **Agents** in the navigation menu.
- Click the **AI Agent** button in the top-right header to start a conversation from any page.
- Open the **Agent builder** API tutorial from the {{kib}} **Getting started** page, under **Explore the API**.
:::

:::{dropdown} {{product.observability}} and {{product.security}} solution views
You must [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable the feature. Once enabled, find **Agents** in the navigation menu.
:::

:::{dropdown} Classic view
{{agent-builder}} appears in the side navigation under {{es}}. You can choose Agent Builder as your assistant through the initial selector or the [chat experience switch](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
:::

You can also search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::::

::::::

:::{note}
To learn about required privileges for {{agent-builder}}, refer to [Permissions and access control](permissions.md).
:::

::::{step} Ingest data into Elasticsearch

If you already have data in {{es}}, skip ahead to [start a conversation](#start-a-conversation).

If you need to add data first, choose the path that fits:

:::{dropdown} Use sample data
If you're not ready to add your own data, you can:

- Load [sample data](/manage-data/ingest/sample-data.md) in {{kib}}.
- Generate synthetic financial data using [this Python tool](https://github.com/jeffvestal/synthetic-financial-data?tab=readme-ov-file#synthetic-financial-data-generator-). (This requires your [{{es}} URL and an API key](/solutions/elasticsearch-solution-project/search-connection-details.md)).
- Follow the [{{agent-builder}} API tutorial](agent-builder-api-tutorial.md), which includes sample book data.
:::

:::{dropdown} Bring your own data
If you already have data, you can:

- [Upload a file](/manage-data/ingest/upload-data-files.md) in the {{kib}} UI for quick testing.
- Learn about your [ingestion options](/manage-data/ingest.md) if you'd like to ingest larger datasets.
:::

::::

::::{step} Start a conversation

The **Agent Chat** UI provides a conversational interface where you can interact with agents and explore your data using natural language. The default `Elastic AI Agent` is ready to use immediately.

Use chat to ask questions, request data analysis, try [built-in skills](builtin-skills-reference.md), or [create dashboards and visualizations](agent-builder-dashboards-and-visualizations.md). You can also invoke a specific skill with a slash command, inspect the agent's reasoning and tool calls, and confirm any proposed write actions before changes are applied.

Learn more in [Agent Chat](chat.md).

::::

::::{step} Enable experimental features (optional)

Some {{agent-builder}} features are experimental and hidden by default. Turn on the `agentBuilder:experimentalFeatures` [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) in {{kib}} to try them before they're generally available.

This unlocks features such as [plugins](plugins.md), [connectors](connectors.md), and additional [built-in skills](builtin-skills-reference.md).

::::

::::{step} Configure model (optional)

On {{ech}} and {{serverless-full}}, {{agent-builder}} comes with preconfigured models ready to use. To review recommended models, switch models, or add your own, refer to [model selection and configuration](models.md).

::::

::::{step} Build skills, tools, and agents

After you test the default `Elastic AI Agent`, create a [custom skill](custom-skills.md) for a specific workflow. Skills package task-specific instructions, context, and the tools needed to complete the workflow.

Add [tools](tools.md) when the skill needs to retrieve data, run queries, call APIs, or take action. Create a [custom agent](custom-agents.md#create-a-new-agent) when you need a distinct persona, system prompt, model configuration, or set of enabled skills. You don't need a separate agent for every workflow: a single agent can use skill descriptions to choose the right skills and tools for the user's request. Note that custom agents don't include [Elastic capabilities](agent-builder-agents.md#elastic-capabilities) by default — enable the toggle to assign all Elastic-built tools, skills, and plugins automatically.

To build programmatically, try the [{{agent-builder}} API tutorial](agent-builder-api-tutorial.md) or explore the [Kibana APIs](programmatic-access.md).

::::

:::::::

:::{tip}
For solution-specific guidance, refer to [Agent Builder for {{observability}}](/solutions/observability/ai/agent-builder-observability.md) and [Agent Builder for {{elastic-sec}}](/solutions/security/ai/agent-builder/agent-builder.md).
:::
