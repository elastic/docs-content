---
navigation_title: "Chat UI modes"
description: "Learn how to use Agent Builder chat UI modes. Switch between the full-page standalone interface and the persistent sidebar for seamless multitasking in Kibana."
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

# Chat UI modes in {{agent-builder}}

The {{agent-builder}} [chat UI](chat.md#agent-chat-gui) is available in two modes: 

1. [Standalone mode](#standalone-mode)
2. [Sidebar mode](#sidebar-mode)

:::{note}
The standalone and sidebar modes have the same functionalities and can be used interchangeably. Conversation history is preserved across both modes.
:::

:::{tip}
When working with dashboards and visualizations, we recommend using **standalone mode**. This full-page chat experience gives you more room to comfortably analyze complex charts and read detailed agent replies. 
:::

## Standalone mode

```{applies_to}
stack: preview =9.2, ga 9.3+
serverless: ga
```

Access Agent Builder by selecting **Agents** in the main navigation.

{applies_to}`stack: preview =9.2, ga =9.3` In {{product.observability}} and {{product.security}} solution views, you must first [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to access the standalone experience.

:::{image} images/agents-nav.png
:alt: Agents logo in main navigation
:width: 100px
:screenshot:
:::

{applies_to}`stack: ga 9.4+` In standalone mode, the full-page experience includes the left sidebar with the [agent selector](chat.md#select-a-different-agent), [Customize accordion](chat.md#customize-your-agent), [Chats accordion](chat.md#find-conversation-history), and [Manage components](chat.md#manage-components) link.

:::{image} images/standalone-chat-mode.gif
:alt: Standalone agent builder chat mode in main navigation
:screenshot:
:::

## Sidebar mode

```{applies_to}
stack: preview =9.3, ga 9.4+
serverless: preview
```

Once you [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences), you can access the sidebar in two ways:

1. Select the **AI Agent** button from the header bar in any page:

:::{image} images/ai-agent-sidebar-button.png
:alt: AI Agent button
:width: 150px
:screenshot:
:::

2. Use the keyboard shortcut:
   - Mac: {kbd}`cmd+;`
   - Windows/Linux: {kbd}`ctrl+;`

You can resize the sidebar by dragging its side edge. The sidebar persists when you change pages in the main navigation.

:::{image} images/sidebar-chat-mode.gif
:alt: Sidebar chat mode demonstration
:screenshot:
:::

## Default chat experiences

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

{{agent-builder}} is the default chat experience for all solutions. It appears in the navigation automatically.

If you need to revert to the legacy AI Assistant, you can opt out by changing your space's **Chat Experience** to **Classic AI Assistant** in the **GenAI Settings**. Learn more about how to [switch between chat experiences](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).

:::

:::{applies-item} { stack: preview =9.2, ga =9.3 }

The default chat experience varies by solution:

- **{{product.observability}} and {{product.security}}:** Each solution's classic AI Assistant is the default chat experience. You must [switch between chat experiences](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences) to enable Agent Builder.
  - Once enabled:
    - The sidebar experience replaces the AI Assistant chat experience.
    - The standalone experience is available through the **Agents** button in the main navigation.
- **{{es}}:** Agent Builder appears in the navigation automatically.

:::

::::

## Related pages

- [Agent Builder chat UI](chat.md#agent-chat-gui)
- [Switch between AI assistant and Agent Builder chat](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences)
