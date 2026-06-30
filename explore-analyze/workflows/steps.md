---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn about workflow steps, the building blocks that define how workflows operate and produce outcomes.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Steps

Workflow steps are the fundamental building blocks of automation. Each step represents a single unit of logic, action, transformation, or reasoning. Together, they define how a workflow operates and what outcomes it can produce. Steps are chained together to move data, coordinate logic, and drive results.

Workflow steps are grouped into the following categories based on their function within the automation.

## Action steps

Action steps carry out operations in internal or external systems. They produce real-world outcomes by performing tasks such as:

* Interact with Elastic features across solutions, including common operations like:
  * Querying data from {{es}} or data streams
  * Indexing new documents or updating existing fields
  * Creating or updating cases
  * Changing detection alert status or tags
  * Modifying dashboards or saved objects
* Trigger actions in external systems using APIs, integrations, or service connectors
* Send messages, alerts, or notifications to systems such as Slack or email
* Invoke other workflows

These actions are available as pre-built operations, so you don't need to configure API endpoints or manage authentication details. You select the action you want to perform and provide the required parameters.

Refer to [](/explore-analyze/workflows/steps/action-steps.md) for the complete action-step catalog.

## Flow control steps

Flow control steps define how a workflow runs. They control the order, structure, and branching logic of execution. This includes:

* **Conditional logic** (`if`, `switch`): Run different steps based on values and predicates.
* **Loops and iteration** (`foreach`, `while`): Process collections or repeat until a condition changes.
* **Loop control** (`loop.break`, `loop.continue`): Exit early or skip to the next iteration.
* **Pauses and waits** (`wait`, `waitForInput`): Introduce timed pauses or pause for human input.

These steps make workflows dynamic and responsive, allowing them to adapt in real time to data and conditions.

Refer to [](/explore-analyze/workflows/steps/flow-control-steps.md) for more information.

## AI steps

AI steps introduce reasoning and language understanding into workflows. Use them to process natural language, classify inputs, summarize content, or operate through agents:

* Send prompts to a generative AI connector with [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt), optionally returning structured output.
* Classify inputs into a fixed category set with [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify).
* Summarize content with [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize).
* Invoke an {{agent-builder}} agent as a step with [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent).

Refer to [](/explore-analyze/workflows/steps/ai-steps.md) for the complete AI-step catalog.

### {{agent-builder}} integration

In addition to calling agents from workflows, agents built with {{agent-builder}} can also trigger workflows. To enable this, create a custom workflow tool type and assign it to an agent. The agent can then trigger the workflow from a conversation.

Refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md) and [](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md) for more information.

## Data action steps

Data action steps transform data between other workflow steps. Use them for filtering, mapping, grouping, JSON parsing, regex extraction, and deduplication: anything that would be brittle or hard to read as inline Liquid.

Refer to [](/explore-analyze/workflows/steps/data.md) for the complete data-step catalog.

## Composition steps

Composition steps let one workflow call another. A parent workflow can invoke a child synchronously (and use its output) or asynchronously (fire and forget). Use composition for reusable building blocks and fan-out patterns.

```{applies_to}
stack: preview 9.4+
serverless: preview
```

Refer to [](/explore-analyze/workflows/steps/composition.md) for the complete composition-step catalog.
