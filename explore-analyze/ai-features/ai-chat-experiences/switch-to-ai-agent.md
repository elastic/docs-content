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

# Switch to AI Agent

AI Agent is a technical preview chat experience designed to replace Elastic Assistant for {{observability}} & Search and Elastic Assistant for Security. 

AI Agent is built on Elastic's [Agent Builder](/solutions/search/elastic-agent-builder.md) platform. It enables a more cohesive AI chat experience across all Elastic's products, and lets you design your own purpose-built agents. You can create agents for use in different workflows, and give them precise access to the tools and data they need. 

## Enable AI Agent

While AI Agent is in technical preview, depending which solution you're using you may have to opt in to enable it:

- **{{observability}} and {{elastic-sec}}:** The existing AI Assistants remain the default chat experiences for Elastic. 
- **{{es}}:** AI Agent is the default chat experience.

To enable AI Agent, use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 

## Feature differences between AI Agent and AI Assistant

Some of the functionality supported by Elastic's AI Assistants is not supported by AI Agents. The differences vary by solution.

### Feature differences in {{elastic-sec}}

AI Agent for {{elastic-sec}} provides a similar experience to AI Assistant for Security at a high level, but with a number of differences.

The following AI Assistant for Security features are not supported in AI Agent:

- **Knowledge Base** 
- **Data anonymization**
- **Time awareness**
- **Chat sharing**
- **Citations**
- **Audit logging**
- **Quick prompts**

In addition, AI Agent chats won't show a preview of data you attach to a message, such as Alerts and Attacks.

### Feature differences in Elastic {{observability}}