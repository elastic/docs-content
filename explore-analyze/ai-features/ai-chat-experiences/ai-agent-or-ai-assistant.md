---
applies_to:
  stack: preview 9.3
  serverless: preview
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Compare Agent Builder and AI Assistant

::::{admonition} Requirements
{{agent-builder}} requires an **Enterprise [license](/deploy-manage/license.md)**.
::::

Elastic's [Agent Builder](/solutions/search/elastic-agent-builder.md) is a powerful and flexible platform for building AI agents, tools and workflows. Agent Builder was introduced in the {{es}} solution and project type in 9.2.

The primary interface to Agent Builder is its chat experience. Agent Builder comes with built-in agents and tools for common use cases, and lets you create custom agents and tools for your specific needs. Eventually, it will power the default chat experience for all solutions and replace AI Assistant.

Currently, Agent Builder is available as an opt-in feature for Security and {{observability}} users. When you opt in, it replaces the AI Assistant chat experience. While Agent Builder offers expanded functionalities, a number of AI Assistant convenience features are not yet available. Users who rely on those AI Assistant features may not want to migrate immediately. For this reason, we've made it easy to try out Agent Builder and switch back to AI Assistant at any time.

Use this page to learn about:

- [How to switch](#switch-between-chat-experiences)
- [Feature differences](#feature-differences-between-agent-builder-and-ai-assistant)
- [The two Agent Builder GUI modes](#agent-builder-gui-interfaces)

## Switch between chat experiences

:::{important}
Agent Builder will not have access to your chats, prompts, or knowledge base entries from AI Assistant. However, this data remains accessible if you switch back to the AI Assistant chat experience.
:::

You will be prompted to switch to the Agent Builder chat experience on supporting Elastic deployments. You can opt-in from this prompt immediately.

You can also switch chat experiences at any time:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 
2. Toggle between the two experiences under **Chat Experience**.

## Feature differences between Agent Builder and AI Assistant

Agent Builder doesn't yet support all AI Assistant features. The specific differences vary by solution:

::::{tab-set}
:group: example-group

:::{tab-item} {{elastic-sec}}
:sync: tab1

| Feature | Agent Builder | AI Assistant |
| :--- | :---: | :---: |
| **Knowledge Base** | ❌ | ✅ |
| **Data anonymization** | ❌ | ✅ |
| **Time awareness** | ❌ | ✅ |
| **Chat sharing** | ❌ | ✅ |
| **Citations** | ❌ | ✅ |
| **Audit logging** | ❌ | ✅ |
| **Quick prompts** | ❌ | ✅ |
| **Use-case specific agents** | ✅ | ❌ |
| **Custom agent creation** | ✅ | ❌ |
| **Custom tool selection** | ✅ | ❌ |

Also, AI Agent chats do not show previews of data you attach to a message, such as Alerts and Attacks.
:::

:::{tab-item} Elastic {{observability}} and Search
:sync: tab2

| Feature | Agent Builder | AI Assistant |
| :--- | :---: | :---: |
| **Knowledge Base** | ❌ | ✅ |
| **Data anonymization** | ❌ | ✅ |
| **Chat sharing** | ❌ | ✅ |
| **Chat duplication** | ❌ | ✅ |
| **Chat archiving** | ❌ | ✅ |
| **Alerting rule connector action** | ❌ | ✅ |
| **AI insights** | ✅ | ✅ |
| **Use-case specific agents** | ✅ | ❌ |
| **Custom agent creation** | ✅ | ❌ |
| **Custom tool selection** | ✅ | ❌ |

:::

::::

## Agent Builder GUI interfaces

% TODO: Maybe this doesn't even belong here, food for thought, will need to be duplicated in main AB docs in any case

Agent Builder UI functionality is available in two modes:

- Standalone experience {applies_to}`stack: preview 9.2, ga 9.3`
- A flyout experience (referred to as **AI Agent** in the UI) that replaces the AI Assistant chat experience {applies_to}`stack: preview 9.3` {applies_to}`serverless: preview 9.3`

% TODO: Link to /solutions/search/agent-builder/chat once that page is updated with two modes

This behavior varies by solution:

- **{{observability}} and {{elastic-sec}}:** Each solution's classic AI Assistant remains the default chat experience. You must [opt in to Agent Builder](#switch-between-chat-experiences) to enable both the standalone and flyout experiences.
- **{{es}}:** Agent Builder is the default chat experience. You must opt out of Agent Builder to use the AI Assistant flyout experience.
