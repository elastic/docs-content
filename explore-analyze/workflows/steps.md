---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about workflow steps, the building blocks that define how workflows operate and produce outcomes.
---

# Steps

Workflow steps are the fundamental building blocks of automation. Each step represents a single unit of logic, action, transformation, or reasoning. Together, they define how a workflow operates and what outcomes it can produce. Steps are chained together to move data, coordinate logic, and drive results.

Workflow steps are grouped into the following categories based on their function within the automation.

## Action steps

Action steps carry out operations in internal or external systems. They produce real-world outcomes by performing tasks such as:

* Interact with Elastic features across solutions, including common operations like:
  * Querying data from {{es}} or data streams
  * Indexing new documents or updating existing fields
  * Closing or updating cases
  * Enriching alerts with additional context
  * Modifying dashboards or saved objects
* Trigger actions in external systems using APIs, integrations, or service connectors
* Send messages, alerts, or notifications to systems such as Slack or email
* Invoke other workflows

These actions are available as pre-built operations, so you don't need to configure API endpoints or manage authentication details. You select the action you want to perform and provide the required parameters.

Refer to [](/explore-analyze/workflows/steps/action-steps.md) for more information.


## Flow control steps

Flow control steps shape how a workflow moves. They control the order, structure, and branching logic of execution. This includes:

* **Conditional logic**: Execute certain steps only when conditions are met
* **Pauses and waits**: Introduce delays or time-based holds
* **Early exits**: Skip or halt execution when needed
* **Custom scripting**: Define custom logic that governs how the workflow progresses based on complex or non-standard conditions

These steps make workflows dynamic and responsive, allowing them to adapt in real time to data and conditions.

Refer to [](/explore-analyze/workflows/steps/flow-control-steps.md) for more information.

## AI steps

AI steps introduce reasoning and language understanding into workflows. Use AI steps to process natural language, make context-aware decisions, or operate through agents:

* Summarize or interpret information using a language model
* Extract key insights from unstructured data
* Implement an agentic step where an AI agent is configured with a goal, access to tools, and autonomy to act

You can define the instructions or prompts that guide the agent, the tools it has access to, and the expected outcome. You can also specify which large language model powers the step.

Refer to [](/explore-analyze/workflows/steps/ai.md) for more information.