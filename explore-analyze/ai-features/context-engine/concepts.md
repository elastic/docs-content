---
navigation_title: "Concepts"
description: Understand AI indices, sources, automations, Knowledge Indicators, and agent access in Context Engine.
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

# Context Engine concepts

:::{include} _snippets/hidden-docs-notice.md
:::

Context Engine has four core building blocks:

- [AI indices](#ai-indices)
- [Sources](#sources)
- [Automations](#automations-and-workflows)
- [Knowledge Indicators (KIs)](#knowledge-indicators)

Optional [agent traces](#agent-traces) provide feedback about how well that context supports real questions.

[Agents and applications](#agents-and-applications) use [tools and instructions](#tools-system-instructions-and-skills) to retrieve and apply the resulting context.

For a hands-on introduction to these building blocks, follow [Get started with Context Engine](quickstart.md).

## AI indices

An AI index groups the metadata, [sources](#sources), [automations](#automations-and-workflows), optional [agent traces](#agent-traces), and {{es}} storage for a particular body of context. Its name and description help an [agent](#agents-and-applications) determine whether that context is relevant to a question. Its generated [Knowledge Indicators (KIs)](#knowledge-indicators) provide the context that agents and applications query.

Creating an AI index does not ingest source data or generate knowledge. Sources define the data that its automations can analyze, and KIs are stored as the generated context. To plan and maintain one, refer to [Build and maintain an AI index](build-and-maintain-ai-index.md). For the complete UI-led example, follow [Get started with Context Engine](quickstart.md).

### Managed AI indices

A managed AI index is a built-in AI index supplied by an Elastic integration. The owning Elastic feature defines its configuration and supplies its [KIs](#knowledge-indicators), giving [agents](#agents-and-applications) access to product-provided context without requiring you to configure its [sources](#sources) or [automations](#automations-and-workflows).

Managed AI indices have a **Managed** badge in **Context**. Agents can discover and query them in the same way as user-created AI indices, subject to the same access checks. You can open a managed AI index and inspect its KIs, but you cannot edit its description, sources, automations, or [agent traces](#agent-traces), or delete it. To build context for your own use case, create a user-created AI index instead.

## Sources

A source is the data from which an [automation](#automations-and-workflows) generates [Knowledge Indicators (KIs)](#knowledge-indicators). Context Engine supports two source types:

- An {{esql}} source uses a query to select data from one or more {{es}} indices or data streams.
- A connector source names a configured connector to an external system. Supported connectors include services such as Google Drive, GitHub, Jira, ServiceNow, and Slack, and cloud object stores. Refer to [Connectors in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/connectors.md) for more information about configuring connectors.

An {{esql}} source can provide a small sample that grounds an automation proposal. The source query is not necessarily the only query the resulting Workflow runs. A Workflow can inspect mappings, take other samples, or calculate full-dataset aggregations. To add an {{esql}} source and review the generated Workflow, follow [Get started with Context Engine](quickstart.md).

## Agent traces

Agent traces record how an [agent](#agents-and-applications) runs, including its model calls and tool calls. An [AI index](#ai-indices) can reference traces from an {{agent-builder}} agent or from a data stream that contains OpenTelemetry generative AI spans.

Context Engine can analyze these traces to identify query errors, empty retrievals, and cases where an agent queries raw data because its [KIs](#knowledge-indicators) do not cover the question. This feedback can expose gaps in the index's [sources](#sources), [automations](#automations-and-workflows), or generated context. Agent traces are feedback about context use. They are not sources from which automations generate KIs.

Agent traces do not update KIs by themselves. Use their evidence to refine sources or automations, then regenerate and retest the KIs. This process turns repeated agent work into improvements to shared context instead of one-off changes to individual agent instructions.

For information about trace collection, contents, privacy, and access, refer to [Collect {{agent-builder}} traces](/explore-analyze/ai-features/agent-builder/collect-traces.md).

## Automations and Workflows

An automation generates or refreshes [Knowledge Indicators (KIs)](#knowledge-indicators) from an [AI index's](#ai-indices) [sources](#sources). Context Engine implements each automation as an [Elastic Workflow](/explore-analyze/workflows.md), which defines the operations and [instructions](#tools-system-instructions-and-skills) used to analyze the source and write the result.

The Workflow can retrieve mappings, run {{esql}} samples and aggregations, generate structured content with an AI prompt, assemble the KI, verify generated queries, and write the KI when verification passes. You can inspect the Workflow to verify the scope of its queries and the evidence behind its output. Refer to [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md) to understand its triggers, constants, steps, and execution lifecycle.

Passing syntax and runtime checks means that a generated query parses and runs. It does not confirm that the query's fields, grouping, or calculations answer the intended question. To review and run a generated automation, follow [Get started with Context Engine](quickstart.md).

## Knowledge Indicators

A Knowledge Indicator (KI) is a document that records reusable context derived from [raw source data](#sources). [Automations](#automations-and-workflows) generate KIs and store them in an [AI index](#ai-indices), where [agents](#agents-and-applications) retrieve them to answer recurring questions without repeatedly finding and interpreting the same information. This can reduce response time and model token use. Depending on the use case, a KI can contain business meaning, derived findings, source limitations, or verified query patterns for retrieving current details.

Unlike a cached answer to one request, a KI can support different questions and multiple agents. When evaluation reveals a gap, improve the source or automation and regenerate the KI so the correction is available to future retrievals.

The [generation strategy](build-and-maintain-ai-index.md#select-a-generation-strategy) determines how an automation divides source data into KIs and how much information each KI contains. To examine a generated KI and evaluate its usefulness, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

## Agents and applications

Agents and applications retrieve [KIs](#knowledge-indicators) from an [AI index](#ai-indices) as context. In {{agent-builder}}, you make an AI index available by adding it to an agent's configuration. Other agent frameworks and applications can use supported Context Engine operations through Model Context Protocol (MCP) [tools](#tools-system-instructions-and-skills) or APIs.

At retrieval time, an agent or application:

1. Lists the AI indices it can access and selects one that is relevant to the question.
2. Describes that AI index to discover its fields, KI types, tags, and example queries.
3. Queries the AI index for relevant KIs.

To configure retrieval for an agent, refer to [Use Context Engine with agents](use-context-engine-with-agents.md). For the built-in integration, follow [Use Context Engine with {{agent-builder}}](use-context-engine-with-agent-builder.md).

## Tools, system instructions, and skills

A tool is an operation an [agent](#agents-and-applications) can perform. MCP exposes tools to compatible clients, while APIs let applications call supported operations directly or wrap them as tools.

System instructions and skills guide an agent in deciding when and how to use those operations. A skill packages reusable instructions and can associate them with tools and reference content, but it is not itself a tool, connection mechanism, or agent framework. Refer to the [Context Engine entries in the built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-context-engine-skills) for the skills that support context generation, evaluation, and retrieval.
