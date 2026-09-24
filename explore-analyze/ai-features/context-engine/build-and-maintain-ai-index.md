---
navigation_title: "Build and maintain an AI index"
description: Plan the sources, Knowledge Indicators, automations, and refresh behavior for an AI index.
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

# Build and maintain an AI index

:::{include} _snippets/hidden-docs-notice.md
:::

Building a useful AI index starts with decisions about its purpose, source data, Knowledge Indicator (KI) granularity, and refresh schedule. Use this page to plan those decisions before creating or revising an automation.

This page covers AI indices that you create and maintain. Elastic integrations can also supply [managed AI indices](concepts.md#managed-ai-indices) whose configuration is read-only.

For a UI-led example that creates and tests an AI index, follow [Get started with Context Engine](quickstart.md).

## Define the AI index's purpose

Start with the recurring questions that the AI index should help answer. Use them to define its subject, boundaries, and intended users or agents. A narrow purpose makes it easier to select relevant source data and evaluate whether the generated KIs are useful.

Give the AI index a name and description that distinguish it from other available context. Agents use this metadata to decide whether the AI index is relevant before they retrieve its KIs.

## Select source data

Source selection controls what an automation can analyze. An {{esql}} source represents the complete query result, which can combine or filter data from multiple {{es}} indices. Connector sources make data outside {{es}} available to an automation.

Start with a source whose result represents the data you want the automation to analyze. Confirm that it contains the information needed for the KIs you want to generate, and record any filters, sampling, or freshness limits that affect interpretation.

Avoid adding data only because it is available. Unrelated records increase the work required to generate and retrieve context and make the boundaries of resulting claims harder to understand.

## Select a generation strategy

Select a strategy based on what each KI needs to represent. For example, one KI can describe an entire dataset, several KIs can capture atomic facts from the same document, or a long-lived KI can accumulate a profile for one entity.

| Strategy | What each KI represents | Useful for |
|---|---|---|
| Index or table metadata | One data source | Explaining what a dataset contains, when to use it, and how to query it |
| Bottom-up | One source document | Bounded collections of articles, cases, product documentation, or other substantial records |
| Selective or outlier | One significant record | Event or log data where unusual records matter more than routine records |
| Atomic facts | One specific fact, with several KIs extracted from one document | Information-dense material where a document-level summary would lose important details |
| Cumulative entity profile | One profile that is enriched as an entity recurs | Services, hosts, accounts, projects, or other entities represented across many records |
| Detection or feature | One named condition or entity feature | Runnable detection logic or a structured inventory of observed capabilities and characteristics |

The questions the AI index must answer determine the useful granularity. A dataset-level KI can orient an agent to a source, entity profiles can preserve knowledge that develops across records, and selective KIs can surface only the events that warrant attention. Prefer fewer, substantial KIs over many thin KIs that repeat the source documents.

## Design useful Knowledge Indicators

A useful KI adds context that an agent cannot get from field mappings alone. Depending on the use case, capture:

- Business meaning and relationships in the data.
- Derived findings that help answer recurring questions.
- Known limitations or boundaries of the source.
- Verified query patterns for retrieving current details from source data.

KIs can reduce the time and model tokens agents spend exploring source data. When an answer depends on current or detailed information, the KI can direct the agent to a targeted source query.

## Review an automation before running it

When {{agent-builder}} suggests an automation, review the proposal before you confirm it. Check:

- Which sources and additional queries the Workflow reads.
- Which KI generation strategy and type it uses.
- How much source data each KI represents.
- Which claims, query patterns, and references the KI contains.
- How the Workflow verifies its output before writing the KI.

Reviewing these decisions before the first run limits unnecessary model calls and makes the resulting context easier to evaluate.

## Plan inspection and maintenance

After an automation runs, inspect its KIs for accuracy, useful interpretation, source limitations, and stable identifiers. Test the context with recurring questions, questions that require current source data, and questions outside the AI index's scope.

Where [agent traces](concepts.md#agent-traces) are available, look for empty retrievals, query errors, broad source exploration, and repeated sequences of tool calls. These behaviors can reveal missing context, weak retrieval metadata, or query guidance that the automation should generate in advance.

Use those observations to revise the AI index description, source coverage, generation strategy, automation instructions, or refresh schedule. Run the automation again and compare the resulting KIs and agent behavior. Improving the automation makes the change repeatable for later runs and for every agent that uses the AI index. For a structured review process, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

For definitions of the objects involved, refer to [Context Engine concepts](concepts.md). To make the resulting context available to an agent, refer to [Use Context Engine with agents](use-context-engine-with-agents.md).
