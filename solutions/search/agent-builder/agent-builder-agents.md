---
navigation_title: "Agents"
applies_to:
  stack: preview 9.2
  deployment: 
    self: unavailable
  serverless:
    elasticsearch: preview
---

# Agents

Agents are AI assistants that engage in natural language conversations with users and interact with your {{es}} data through tools. Each agent manages the conversation flow, interprets user requests, and provides responses based on its configured tools, instructions, and behavior settings.

## How agents work

When you ask a question to an agent, it analyzes your request, selects the most appropriate tool, and determines the right arguments to use. After receiving results, the agent evaluates the information and decides whether to use additional tools or formulate a response. This iterative process of tool selection, execution, and analysis continues until the agent can provide a complete answer.

{{agent-builder}} includes a default agent with access to all system tools. You can create specialized agents with custom instructions and selected tools to address specific use cases or workflows.

## Create a new agent

To create a new agent:

1. Navigate to the Agents subpage under **Chat**
2. Click the **New agent** button in the top right corner
3. Configure the agent settings:
   - Enter an **Agent ID** - unique identifier for reference in code
   - Add **Custom instructions** (optional) to guide the agent's behavior
   - Add **Labels** (optional) to organize your agents
   - Set the **Display name** that users will see
   - Add a **Display description** to explain the agent's purpose
   - Choose an **Avatar color** and **Avatar symbol** (both optional)
4. Switch to the **Tools** tab to assign [tools](tools.md) to the agent
5. Click the **Save** button to create your agent