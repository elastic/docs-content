---
navigation_title: "Get started"
description: "Learn how to enable Elastic Agent Builder, ingest data, and start chatting with AI agents."
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

To start using {{agent-builder}} you need an {{es}} deployment. If you don't already have an {{es}} deployment, refer to [](/solutions/search/get-started.md).

For {{ech}} deployments, make sure you are using the solution navigation instead of classic navigation. You can set up a new [space](/deploy-manage/manage-spaces.md) to use the solution nav.

::::{admonition}
This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

::::::{stepper}
:::::{step} Enable {{agent-builder}}

::::{applies-switch}

:::{applies-item} { "serverless": "ga", "elasticsearch" }

{{agent-builder}} is enabled by default in serverless {{es}} projects. You can access it from multiple entry points in the UI:

- Select the **Agent Builder** card on the {{es}} home page.
- Click **Agents** in the navigation menu.
- Click the **AI Agent** button in the top-right header to start a conversation from any page.
- Open the **Agent builder** API tutorial from the {{kib}} **Getting started** page, under **Explore the API**.

You can also search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

:::{applies-item} { "serverless": "preview", "observability" }

In {{product.observability}} projects, you must [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable the feature.

Once enabled, find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

:::{applies-item} { "serverless": "preview", "security" }

In {{product.security}} projects, you must [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable the feature.

Once enabled, find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

:::{applies-item} stack: preview =9.2, ga 9.3+

On non-serverless deployments, {{agent-builder}} availability depends on the navigation mode of your {{kib}} space:

- **{{es}} solution view**: {{agent-builder}} is enabled by default, replacing Search Assistant. You can access it from multiple entry points:
    - Select the **Agent Builder** card on the {{es}} home page.
    - Click **Agents** in the navigation menu.
    - Click the **AI Agent** button in the top-right header to start a conversation from any page.
    - Open the **Agent builder** API tutorial from the {{kib}} **Getting started** page, under **Explore the API**.
- **{{product.observability}} and {{product.security}} solution views**: You must [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable the feature. Once enabled, find **Agents** in the navigation menu.
- **Classic view**: {{agent-builder}} appears in the side navigation under {{es}}. You can choose Agent Builder as your assistant through the initial selector or the [chat experience switch](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).

You can also search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

::::

:::{note}
To learn about required privileges for {{agent-builder}}, refer to [Permissions and access control](permissions.md).
:::

:::::

::::{step} Ingest data into Elasticsearch

If you already have data in {{es}}, skip ahead to [start a conversation](#start-a-conversation).

If you need to add data first, choose the path that fits:

### Use sample data

If you're not ready to add your own data, you can:

- Load [sample data](/manage-data/ingest/sample-data.md) in {{kib}}.
- Generate synthetic financial data using [this Python tool](https://github.com/jeffvestal/synthetic-financial-data?tab=readme-ov-file#synthetic-financial-data-generator-). (This requires your [{{es}} URL and an API key](/solutions/elasticsearch-solution-project/search-connection-details.md)).
- Follow the [{{agent-builder}} API tutorial](agent-builder-api-tutorial.md), which includes sample book data.

### Bring your own data

If you have data you want agents to work with:

- [Upload a file](/manage-data/ingest/upload-data-files.md) through {{kib}}.
- For search-specific guidance, refer to [](/solutions/search/ingest-for-search.md).
- For a broader overview, refer to [](/manage-data/ingest.md).

::::

::::{step} Start a conversation

The **Agent Chat** UI provides a conversational interface where you can interact with agents and explore your data using natural language. The default `Elastic AI Agent` is ready to use immediately.

Learn more in [Agent Chat](chat.md).

::::

::::{step} Configure model (optional)

On {{ech}} and {{serverless-full}}, {{agent-builder}} comes with preconfigured models ready to use. To switch models or add your own, refer to [model selection and configuration](models.md).

::::

::::{step} Begin building agents and tools

Once you've tested [built-in agents](builtin-agents-reference.md) with [built-in Elastic tools](tools.md), you can begin [building your own agents](custom-agents.md#create-a-new-agent) with custom instructions and [creating your own tools](tools/custom-tools.md#create-custom-tools-in-the-ui) to assign them. You can also clone the default `Elastic AI Agent` as a starting point for a custom agent.

To build agents and tools programmatically, try the [{{agent-builder}} API tutorial](agent-builder-api-tutorial.md) or explore the [Kibana APIs](programmatic-access.md).

::::

::::::
