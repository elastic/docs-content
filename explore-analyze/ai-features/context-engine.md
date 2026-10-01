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

# {{context-engine}}

:::{include} context-engine/_snippets/hidden-docs-notice.md
:::

{{context-engine}} enables you to distill raw source data into context optimized for retrieval by agents and applications. This upfront investment reduces repeated source data scanning and interpretation, helping agents respond faster and use fewer model tokens.

## {{context-engine}} use cases

{{context-engine}} is useful when agents repeatedly need to interpret large, complex, or changing bodies of data. For example, you can:

- Turn technical documentation, policies, cases, or runbooks into reusable explanations, procedures, and limitations.
- Give agents business definitions and verified query patterns for working with structured data.
- Build context that develops across records, such as profiles of services, systems, accounts, or projects.
- Surface significant findings or conditions without making every agent analyze all source records.

These use cases share the same advantage: move recurring interpretation into an automation, reuse the resulting context across questions and agents, and improve it as agent traces reveal gaps.

## How {{context-engine}} works

To build and use context with {{context-engine}}:

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

::::{step} Evaluate and improve the context
Review KIs and [agent traces](context-engine/concepts.md#agent-traces) to identify missing, misleading, or underused context. Refine the sources or automations, regenerate the KIs, and repeat as questions and source data change.
::::

:::::

## Get started with {{context-engine}}

Follow [Get started with {{context-engine}}](context-engine/quickstart.md) to create an AI index from existing {{es}} data, generate your first KI, and test how an {{agent-builder}} agent uses it.

## {{context-engine}} concepts

Learn how AI indices, sources, automations, KIs, and agent access fit together in [{{context-engine}} concepts](context-engine/concepts.md).

## Build and maintain an AI index

Learn how to choose source data, select a KI generation strategy, review automations, and maintain useful context in [Build and maintain an AI index](context-engine/build-and-maintain-ai-index.md).

## Use {{context-engine}} with agents and applications

Learn how to [use {{context-engine}} with agents and applications](context-engine/use-context-engine-with-agents.md), including {{agent-builder}} agents and agents built with LangChain.
