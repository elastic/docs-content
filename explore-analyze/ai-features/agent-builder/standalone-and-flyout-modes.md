---
description: Learn about the standalone and flyout modes for the Elastic Agent Builder chat UI
navigation_title: "Chat UI modes"
applies_to:
  stack: 
  serverless:
    elasticsearch:
    observability:
    security:
---

# Standalone and flyout chat UI modes in {{agent-builder}}

The {{agent-builder}} [chat UI](chat.md#agent-chat-gui) is available in two modes: 

1. [Standalone experience](#standalone-experience)
2. [Flyout experience](#flyout-experience)

:::{note}
The standalone and flyout mode have the same functionalities and can be used interchangeably. Conversation history is preserved across both modes.
:::

## Standalone experience

{applies_to}`stack: preview =9.2, ga 9.3` {applies_to}`observability: ga 9.3+` {applies_to}`security: ga 9.3+`

Access Agent Builder using the **Agents** tab in the main navigation. For {{observability}} and {{elastic-sec}}, the standalone experience is available when you [switch from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-agent-or-ai-assistant.md).

:::{image} images/agents-nav.png
:alt: Agents tab in main navigation
:width: 150px
:screenshot:
:::

## Flyout experience

{applies_to}`stack: preview 9.3` {applies_to}`serverless: preview 9.3`

Once enabled by [switching from AI Assistant to Agent Builder](/explore-analyze/ai-features/ai-agent-or-ai-assistant.md), you can access the flyout in two ways:

1. Select the **AI Agent** button from any page:

:::{image} images/ai-agent-flyout-button.png
:alt: AI Agent button
:width: 150px
:screenshot:
:::

2. Use the keyboard shortcut {kbd}`cmd+;`

You can resize the flyout by dragging its side edge. The flyout persists when you change pages in the main navigation.

## Default chat experiences

The default chat experience varies by solution:

- **{{observability}} and {{elastic-sec}}:** Each solution's classic AI Assistant is the default chat experience. You must [switch between chat experiences](/explore-analyze/ai-features/ai-agent-or-ai-assistant.md) to enable Agent Builder.
  - Once enabled:
    - The flyout experience replaces the AI Assistant chat experience
    - The standalone experience is available through the **Agents** tab in the main navigation.
- **{{es}}:** Agent Builder is the default chat experience and appears in the navigation automatically.

<!--  TODO 
 Replace
/explore-analyze/ai-features/ai-agent-or-ai-assistant.md

with 
/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences

when that page is live 
-->

## Related pages

- [Agent Builder chat UI](chat.md#agent-chat-gui)
