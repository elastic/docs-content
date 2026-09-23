---
navigation_title: "Context Engine"
description: Learn how AI indices, sources, automations, and Knowledge Indicators make context available to agents.
type: overview
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Context Engine

:::{include} context-engine/_snippets/hidden-docs-notice.md
:::

Context Engine helps you turn enterprise data into reusable context for agents and applications. By investing in useful context up front, you reduce the time and tokens agents spend repeatedly finding and interpreting the same information and help them answer recurring questions more consistently. Because that context is stored as inspectable Knowledge Indicators (KIs), you can review what agents rely on and improve it over time.

You organize context around a specific subject or set of questions, generate KIs from relevant data, and make that knowledge available to an agent.

## How Context Engine works

To build and use context with Context Engine:

:::::{stepper}

::::{step} Create an AI index
Create an [AI index](context-engine/concepts.md#ai-indices) for a defined area of context.
::::

::::{step} Add source data
Add one or more [sources](context-engine/concepts.md#sources) that contain the relevant data.
::::

::::{step} Generate Knowledge Indicators
Configure [automations](context-engine/concepts.md#automations-and-workflows), implemented as [Elastic Workflows](/explore-analyze/workflows.md), to generate and refresh [KIs](context-engine/concepts.md#knowledge-indicators) from those sources.
::::

::::{step} Make the context available
Make the AI index available to an [agent or application](context-engine/concepts.md#agents-and-applications).
::::

::::{step} Configure context retrieval
Configure the agent or application with the appropriate [tools and instructions](context-engine/concepts.md#tools-system-instructions-and-skills) to retrieve KIs as context and query source data when current detail is required.
::::

:::::

## Get started with Context Engine

Follow [Get started with Context Engine](context-engine/quickstart.md) to create an AI index from existing {{es}} data, generate your first KI, and test how an {{agent-builder}} agent uses it.

## Context Engine concepts

Learn how AI indices, sources, automations, KIs, and agent access fit together in [Context Engine concepts](context-engine/concepts.md).

## Build and maintain an AI index

Learn how to choose source data, select a KI generation strategy, review automations, and maintain useful context in [Build and maintain an AI index](context-engine/build-and-maintain-ai-index.md).

## Use Context Engine with agents

Learn how to [use Context Engine with agents](context-engine/use-context-engine-with-agents.md), including {{agent-builder}} agents and agents built with LangChain.
