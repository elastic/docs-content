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
You can use either AI Assistant (default) or AI Agent chat experiences throughout {{kib}}. This page explains their differences and how to opt-in to AI Agent.

::::{admonition} Requirements
- To use Elastic's AI-powered features, you need an appropriate subscription level or serverless feature tier. These vary by solution and feature. Refer to each feature's documentation to learn more.
::::

## Switch between chat options

AI Agent uses Elastic's [Agent Builder](/solutions/search/elastic-agent-builder.md) platform to provide a cohesive AI chat experience across all Elastic's products. It lets you design your own purpose-built agents for use in different workflows, and give them precise access to the tools and data they need.

While Agent Builder is in technical preview, you may need to manually enable it. This behavior varies by solution:

- **{{observability}} and {{elastic-sec}}:** Each solution's classic AI Assistant remains the default chat experience. 
- **{{es}}:** Agent Builder is the default chat experience.

To enable or disable Agent Builder, use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 

## Feature differences between Agent Builder and AI Assistant

Some functionality supported by Elastic's AI Assistants is not supported by Agent Builder. The differences vary by solution.

Agent Builder provides a similar experience to AI Assistant at a high level, but with a number of differences. 

The following AI Assistant chat features are not supported by Agent Builder:

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
- **Knowledge Base**
- **Data anonymization**
- **Chat sharing**
- **Chat duplication**
- **Chat archiving**
- **Screen context (unavailable for some use cases)**
- **AI insights (unavailable for some use cases)**
- **Alerting Rule connector action**
:::

::::
