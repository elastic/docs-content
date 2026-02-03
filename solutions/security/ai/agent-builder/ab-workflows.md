---
applies_to:
  stack: preview 9.3+
  serverless:
    security: preview 9.3+
products:
  - id: security
  - id: cloud-serverless
---

# Use Agent Builder with Elastic Workflows

You can use Agent Builder along with Elastic Workflows to automate your security operations. [Agent Builder](/explore-analyze/ai-features/agent-builder/get-started.md) is Elastic's AI chat platform that integrates into {{kib}} and allows you to create custom agents with specialized tool access. [Workflows](/explore-analyze/workflows.md) lets you automate end-to-end processes that include a wide range of tools, without needing an external automation platform.

## How Agent Builder and Workflows work together

There are two main ways to use these tools together:

- **Enable an agent to run workflows:** You can allow custom agents to independently start workflows. For more information, refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).
- **Add AI-powered steps to your workflows:** AI steps introduce reasoning and language understanding into workflows. Use AI steps to process natural language, make context-aware decisions, or operate through agents. For more information, refer to [](/explore-analyze/workflows/steps.md)

In combination, these tools can help:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools

## Examples

This section provides conceptual examples of what you can achieve with Agent Builder. For specific examples of workflows, including complete annotated code samples, refer to the [elastic/workflows/security](https://github.com/elastic/workflows/tree/main/workflows/security) GitHub repo.

### Example 1
You can create a workflow that:

 - Runs periodically, and initiates Attack Discovery when it runs
 - Sends any discovered attacks to Agent Builder to analyze and create a report 
 - Sends that report to a third-party incident management platform and sends alerts to your team

### Example 2
You can create a workflow that: 

 - Runs when Attack Discovery finds an attack, and creates a case for each attack
 - Uses Agent Builder to analyze the alerts that are part of the attack
 - Isolates the implicated host
 - Creates a report about the attack, and notifies your team

### Example 3
You can create a workflow that:

- Runs manually on an alert of your choosing
- Provides the alert data to Agent Builder with a pre-defined prompt such as `analyze this alert, check whether it's connected to existing attacks, and identify all implicated entities`
- Creates a report based on what it finds and sends it to a Slack channel
- Suggests next steps