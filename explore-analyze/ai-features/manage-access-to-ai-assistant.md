---
applies_to:
  stack: ga 9.2+
  serverless: ga
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Manage access to AI features

The **GenAI Settings** and **Feature Settings** pages let you control the list of models available for each AI feature, turn on token usage tracking, install documentation, and more.

## Requirements

- To access **GenAI Settings**, you need the `Actions and connectors: all` or `Actions and connectors: read` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). 
- To access **Feature Settings**, you need the `Inference Endpoints: all` and `Advanced Settings: read` {{kib}} privileges.

To modify the settings, you also need the `Advanced Settings: all` {{kib}} privilege.

## GenAI settings

Go to the **GenAI Settings** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::::{applies-switch}

::::{applies-item} serverless: ga
:::{image} /explore-analyze/images/genai-settings.png
:alt: GenAI Settings for Serverless
:screenshot:
:::

The **GenAI Settings** page has the following settings:

- **Chat experience**: Select whether to use AI Assistant or AI Agent. To learn about the differences, go to [Compare AI Agent and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
- **Token usage tracking**: Turn on tracking of token usage by AI features.
- **Documentation**: Install Elastic documentation or content from Security labs to improve Agent Builder responses.
::::
::::{applies-item} stack: ga 9.4+

:::{image} /explore-analyze/images/genai-settings-stack.png
:alt: GenAI Settings for Stack in 9.4
:screenshot:
:::

The **GenAI Settings** page has the following settings:

- **AI feature visibility**: This button opens the current Space's settings page, where you can specify which features are enabled in your environment, including AI-powered features.
- **Chat experience**: Select whether to use AI Assistant or AI Agent. To learn about the differences, go to [Compare AI Agent and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
- **Documentation**: Install Elastic documentation or content from Security labs to improve Agent Builder responses.
::::
::::{applies-item} stack: ga 9.2-9.3

:::{image} /explore-analyze/images/ai-assistant-settings-page.png
:alt: GenAI Settings page for Stack in 9.2 and 9.3
:::

The **GenAI Settings** page has the following settings:

- **Default AI Connector**: Use this setting to specify which connector is selected by default when you access AI-powered features. For available connectors and tested models, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md). Default setting: **No default connector**.
  - If **No default connector** is selected, AI-powered features will default to the connector that was most recently used in your environment.
  - If an **Elastic Managed LLM** or a custom LLM connector is selected, AI-powered features will default to that connector regardless of which connector was used most recently in your environment.
- **Disallow all other connectors**: When this setting is disabled, whenever you use an AI-powered feature you can select which connector should power it. Enable it to prevent connectors other than the default connector from being used in your space. Default setting: disabled.
- **AI feature visibility**: This button opens the current Space's settings page, where you can specify which features are enabled in your environment, including AI-powered features.
- **Chat experience**: {applies_to}`stack: preview 9.3+` Select whether to use AI Assistant or AI Agent. For information about choosing one, refer to [Compare AI Agent and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
- **AI Assistant visibility**: This setting allows you to choose which AI Assistants are available to use and where. There are several options:
  - **Only in their solutions** (default): The Security AI Assistant appears in {{elastic-sec}}, and the {{obs-ai-assistant}} appears in {{es}} and {{observability}}.
  - **{{obs-ai-assistant}} in other apps**: The {{obs-ai-assistant}} appears throughout {{kib}} regardless of solution. The Security AI Assistant does not appear anywhere.
  - **Security AI Assistant in other apps**: The Security AI Assistant appears throughout {{kib}} regardless of solution. The {{obs-ai-assistant}} does not appear anywhere.
  - **Hide all assistants**: Turns off AI Assistant throughout {{kib}}.

::::
:::::

## Feature settings
```{applies_to}
stack: ga 9.4+
serverless: ga
```

Elastic's AI-powered features can use [EIS](/explore-analyze/elastic-inference/eis.md) and [External Inference](/explore-analyze/elastic-inference/external.md) models, as well as your custom [Generative AI connectors](kibana://reference/connectors-kibana/gen-ai-connectors.md).

To control the models used by each feature, go to **Feature Settings** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/feature-settings.png
:alt: Feature Settings app
:screenshot:
:::

Available actions include:

- Choose a default model.
- Add a model to a feature's list of assigned models.
- Copy the list of assigned models across multiple features.
- Reset all settings to their defaults.
- Turn off feature-specific assigned models, which means all features can use only the default model.

To change the order of precedence of models for each feature, select and drag items in the list.
