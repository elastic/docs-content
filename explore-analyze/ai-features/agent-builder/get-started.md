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

{{agent-builder}} is enabled by default in serverless {{es}} projects.

Find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

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

- **{{es}} solution view**: {{agent-builder}} is enabled by default and appears in the side navigation. It replaces Search Assistant.
- **{{product.observability}} and {{product.security}} solution views**: You must [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable the feature.
- **Classic view**: {{agent-builder}} appears in the side navigation under {{es}}. You can choose Agent Builder as your assistant through the initial selector or the [chat experience switch](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).

Find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

::::

:::{note}
To learn about required privileges for {{agent-builder}}, refer to [Permissions and access control](permissions.md).
:::

:::::

::::{step} Ingest data into Elasticsearch

Before you begin with agents, you need some data in {{es}}. Otherwise, you will be chatting to the underlying LLM without any retrieval-augmented context.

To learn about adding data for search use cases, go to [](/solutions/search/ingest-for-search.md).
For a broader overview of ingestion options, go to [](/manage-data/ingest.md).

:::{tip}
If you're not ready to add your own data, you can:
- Use the Elastic [sample data](/manage-data/ingest/sample-data.md).
- Generate synthetic financial data using [this Python tool](https://github.com/jeffvestal/synthetic-financial-data?tab=readme-ov-file#synthetic-financial-data-generator-).  (This requires your [{{es}} URL and an API key](/solutions/elasticsearch-solution-project/search-connection-details.md)).

% TODO: we can link to a an agent builder tutorial if we add one in the docs
:::

::::

::::{step} Start a conversation

The **Agent Chat** UI provides a conversational interface where you can interact with agents and explore your data using natural language. {{agent-builder}} includes a default agent named `Elastic AI Agent` with access to all built-in tools, so you can begin chatting immediately.

Learn more in [Agent Chat](chat.md).

::::

::::{step} Configure model (optional)

On {{ech}} and {{serverless-full}}, {{agent-builder}} comes with preconfigured models ready to use. To switch models or add your own, refer to [model selection and configuration](models.md).

::::

::::{step} Begin building agents and tools

Once you've tested [built-in agents](builtin-agents-reference.md) with [built-in Elastic tools](tools.md), you can begin [building your own agents](custom-agents.md#create-a-new-agent) with custom instructions and [creating your own tools](tools/custom-tools.md#create-custom-tools-in-the-ui) to assign them.

::::

::::::
