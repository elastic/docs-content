---
description: Learn about the differences between the AI Assistant and Agent Builder chat experiences and how to switch between the two.
applies_to:
  stack: preview 9.3+
  serverless: preview
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Compare Agent Builder and AI Assistant

::::{admonition} Requirements
- {{stack}} users: an **Enterprise [subscription](/deploy-manage/license.md)**.
- {{sec-serverless}} users: the **Security Analytics Complete** or **Elastic AI Soc Engine (EASE)** feature tier.
- {{obs-serverless}} and {{es-serverless}} users: the **Complete** feature tier. 
::::

[{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) is a powerful and flexible platform for building AI agents, tools, and workflows. Agent Builder comes with built-in agents and [tools](/explore-analyze/ai-features/agent-builder/tools.md) for common use cases, and lets you create custom agents and tools for your specific needs. Eventually, it will power the default chat experience for all solutions and replace AI Assistant.

Agent Builder powers the AI Agent chat experience. Currently, AI Agent is available by default for {{es}} solution users, and as an opt-in feature for Security solution and {{observability}} solution users. When you opt in, it replaces the AI Assistant chat experience. You can opt in to Agent Builder and switch back to AI Assistant at any time.

While Agent Builder offers expanded functionality compared to AI Assistant, it does not yet support a number of AI Assistant features. If you rely on AI Assistant capabilities today, consider the differences between each experience before opting in.

Use this page to learn about:

- [How to switch between the AI Assistant and Agent Builder chat experiences](#switch-between-chat-experiences)
- [Feature differences between AI Assistant and Agent Builder](#feature-differences-between-agent-builder-and-ai-assistant)

## Switch between chat experiences

:::{important}
Agent Builder cannot access your chats, prompts, or knowledge base entries from AI Assistant. However, this data remains accessible if you switch back to the AI Assistant chat experience.
:::

{{kib}} will prompt you to switch to the Agent Builder chat experience if your deployment supports it and you have sufficient privileges. You can opt-in from this prompt immediately.

You can also switch chat experiences at any time:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 
2. Toggle between the two experiences under **Chat Experience**.

% TODO: Link to /solutions/search/agent-builder/standalone-and-flyout-modes.md once that page exists

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
| **In-chat previews of attached data** | ❌ | ✅ |
| **AI insights** | ✅ | ✅ |
| **Use-case specific agents** | ✅ | ❌ |
| **Custom agent creation** | ✅ | ❌ |
| **Custom tool selection** | ✅ | ❌ |
| **Integration with Elastic workflows** | ✅ | ❌ |

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

## API differences between Agent Builder and AI Assistant

Each AI chat experience has different APIs. To learn which actions each option supports, refer to:

- [Agent Builder](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder)
- [AI Assistant for Security](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-ai-assistant-api)
- [AI Assistant for Observability](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-observability_ai_assistant)