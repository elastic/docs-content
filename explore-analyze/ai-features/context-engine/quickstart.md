---
navigation_title: "Get started"
description: Step-by-step tutorial for creating reusable context from existing Elasticsearch data and testing it with an Agent Builder agent.
type: tutorial
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Get started with {{context-engine}}

:::{include} _snippets/hidden-docs-notice.md
:::

In this tutorial, you follow the complete {{kib}} and {{agent-builder}} path from data already stored in {{es}} to a Knowledge Indicator (KI) that an agent can retrieve. You can use your own data or the {{kib}} sample ecommerce data.

Suppose an agent regularly answers questions about an {{es}} index. Without reusable context, it might first inspect the mapping, interpret the fields, and construct suitable queries. This tutorial generates an index metadata KI that gives the agent that orientation and query guidance up front.

## Tutorial outcome

By the end of this tutorial, an {{agent-builder}} agent can retrieve an `index_metadata` KI. The KI explains what your selected {{es}} data contains, its limitations, and how to query it with verified {{esql}}.

An automation, implemented as a workflow in [Elastic Workflows](/explore-analyze/workflows.md), generates the KI and can refresh it when the source changes.

## Before you begin

You need:

- An {{stack}} 9.6 deployment with an Enterprise license, or an {{serverless-full}} project.
- Permission to change Advanced Settings in the current Kibana space.
- Permission to [create and run workflows](/explore-analyze/workflows/get-started/setup.md) and manage {{context-engine}} AI indices.
- Elasticsearch data that you can read. If you do not have suitable data, install the [**Sample eCommerce orders** data](https://www.elastic.co/docs/manage-data/ingest/sample-data#add-sample-data-sets), which creates the `kibana_sample_data_ecommerce` index.

Starting with existing data matters. An AI index does not ingest source data by itself. Its sources identify the data that an automation can use to generate KIs.

## 1. Enable {{context-engine}}

Turn on {{context-engine}} for the current Kibana space:

1. In Kibana, open **Stack Management → Advanced Settings**.
2. Search for **{{context-engine}}**.
3. Turn on **{{context-engine}}** (`contextEngine:enabled`).
4. Open **Context** from the Kibana navigation.

This setting applies to the current Kibana space.

## 2. Create an AI index [context-engine-create-ai-index]

An AI index stores KIs for a particular purpose. Its name and description also help agents decide whether it is relevant to a question.

Create the AI index:

1. Select **Create AI Index**.
2. Enter a name that identifies the knowledge the AI index will contain. For example, enter `ecommerce-orders` if you are using the sample data.
3. Add a description that identifies the data and the questions it should support. For example:

   > Context about ecommerce orders, including customers, products, order value, and sales trends. It should help answer questions about revenue, top products, and customer activity. It does not contain inventory, fulfillment, returns, or payment data.

4. Select **Create AI index**.

The AI index initially has no sources, automations, or KIs. You must add a source before you can create an automation.

## 3. Add the source data

A source identifies the data that the automation can analyze. For this tutorial, select one {{es}} index, data stream, or alias.

Add a source to the AI index:

1. In **Sources**, select **Edit**.
2. On the **Elasticsearch data** tab, start typing the name of an index, data stream, or alias. If you are using the ecommerce sample data, enter `kibana_sample_data_ecommerce`.
3. Select the matching result.
4. Confirm that the source appears under **Selected sources**, then select **Save**.

Selecting an index, data stream, or alias creates an {{esql}} source in the form `FROM <name>`. You can use **Advanced: ES|QL** to define a narrower source, but that is not necessary for this tutorial.

## 4. Create the automation

Use the guided route for this tutorial:

For an AI index without an automation, {{agent-builder}} starts with an Index/Table Metadata automation. It creates one `index_metadata` KI that describes what the data contains, when to use it, and how to query it.

1. In **Automations**, select **Suggest automation**.
2. {{agent-builder}} opens a conversation and sends **Suggest an automation for this AI index**.
3. Review the proposal. Confirm that it identifies the intended source index and a suitable keyword field for grouping the data. For the ecommerce sample data, `category.keyword` is an appropriate grouping field.
4. Approve the proposal when {{agent-builder}} asks whether to create the automation.

{{agent-builder}} installs the Index/Table Metadata template and attaches the resulting workflow to the AI index. The workflow inspects the index mapping, samples documents, runs grounding aggregations, generates the KI, and verifies any {{esql}} that the KI contains. Installing the automation does not run it.

:::{note}
**Create automation** is the manual route. It opens a new, disabled workflow in the [Workflows YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) with a manual trigger and generic starter YAML. Use it when you intend to author the KI-generation workflow yourself.
:::

## 5. Run the automation and inspect the KI

Run the automation and inspect its output:

1. Ask {{agent-builder}} to run the automation.
2. Confirm the run when prompted.
3. Follow the execution link and confirm that the workflow completes successfully.
4. Return to the AI index in **Context**, then open **Knowledge Indicators**.
5. Open the `index_metadata` KI and confirm that it describes the intended data, its limitations, and useful {{esql}} access patterns.

For a detailed review process, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

## 6. Make the AI index available to an agent

Add the populated AI index to an Agent Builder agent:

1. Open **Agent Builder**.
2. Create an agent or edit an existing one.
3. In **AI Indices**, add the AI index under **Additional indices**.
4. Save the agent.

The assignment makes the AI index and the dedicated {{context-engine}} retrieval tools available to the agent. Its name and description help the agent decide when to retrieve its KIs. For details about the tools, source-data access, and custom instructions, refer to [Use {{context-engine}} with {{agent-builder}}](use-context-engine-with-agent-builder.md).

## 7. Test how the agent uses the KI

Ask the agent questions that exercise both kinds of context:

1. Ask a question the KI can answer from its distilled content, such as what the dataset represents and what its important limitations are.
2. Ask for current or detailed information that requires one of the KI's verified ESQL queries.

For the ecommerce sample data, ask which questions the index cannot answer, then ask for a current revenue breakdown by manufacturer. The first answer should come from the KI. The second should cause the agent to query the source data.

Confirm that the agent:

- Selects the relevant AI index
- Retrieves the KI as context
- Answers directly when the KI contains the required knowledge
- Uses targeted {{esql}} against the source when current detail is required

KIs can reduce the time and model tokens agents spend exploring source data. They provide reusable knowledge and tested query guidance while preserving access to current source data.

## Next steps

After completing this tutorial, you can:

- [Add or refine sources](add-and-manage-sources.md) to control the data that automations analyze.
- [Create, run, and schedule automations](create-and-manage-automations.md) that generate other kinds of KIs.
- [Evaluate and improve the generated KIs](evaluate-and-improve-knowledge-indicators.md).
- [Use the AI index with another agent or application](use-context-engine-with-agents.md).
