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

# Compare AI Agent and AI Assistant

AI Agent is a technical preview chat experience designed to replace Elastic Assistant for {{observability}} & Search and Elastic Assistant for Security. 

AI Agent uses Elastic's [Agent Builder](/solutions/search/elastic-agent-builder.md) platform. It lets you design your own purpose-built agents and enables a more cohesive AI chat experience across all Elastic's products. You can create specific agents for use in different workflows, and give them precise access to the tools and data they need. 

## Enable AI Agent

While AI Agent is in technical preview, you may have to opt in to enable it. This behavior varies by solution:

- **{{observability}} and {{elastic-sec}}:** Each solution's classic AI Assistant remains the default chat experience. 
- **{{es}}:** AI Agent is the default chat experience.

To enable AI Agent, use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 

## Feature differences between AI Agent and AI Assistant

Some functionality supported by Elastic's AI Assistants is not supported by AI Agents. The differences vary by solution.

### AI Agent features in {{elastic-sec}}

AI Agent for {{elastic-sec}} provides a similar experience to AI Assistant for Security at a high level, but with a number of differences.

The following AI Assistant for Security features are not supported in AI Agent:

- **Knowledge Base** 
- **Data anonymization**
- **Time awareness**
- **Chat sharing**
- **Citations**
- **Audit logging**
- **Quick prompts**

Also, AI Agent chats do not show previews of data you attach to a message, such as Alerts and Attacks.

### AI Agent features in Elastic {{observability}}

### AI Agent features in {{es}}