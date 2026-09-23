---
navigation_title: "Get started with Context Engine"
description: Complete an end-to-end Context Engine workflow with existing {{es}} data and {{agent-builder}}.
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

# Get started with Context Engine

:::{include} _snippets/hidden-docs-notice.md
:::

In this tutorial, you use Context Engine to create reusable context from data already stored in {{es}}. You create an AI index, add a source, generate a Knowledge Indicator, and test it with an {{agent-builder}} agent. You can use your own data or the {{kib}} sample ecommerce data.

## Tutorial outcome

The result is an AI index containing one Knowledge Indicator about a dataset you select.

A Knowledge Indicator (KI) is a document generated from source data, stored in an AI index, and retrieved as context by agents to help answer questions. A KI can contain distilled findings, explanations of how to interpret the data, limitations, and verified ESQL queries for retrieving current information from the source.

An automation generates and refreshes the KI. In Context Engine, an automation is implemented as an [Elastic Workflow](/explore-analyze/workflows.md).

## Before you begin

You need:

- Kibana 9.6 or a compatible Serverless project.
- Permission to change Advanced Settings in the current Kibana space.
- Permission to [create and run Workflows](/explore-analyze/workflows/get-started/setup.md) and manage Context Engine AI indices.
- Elasticsearch data that you can read. If you do not have suitable data, install the [**Sample eCommerce orders** data](https://www.elastic.co/docs/manage-data/ingest/sample-data#add-sample-data-sets), which creates the `kibana_sample_data_ecommerce` index.

Starting with existing data matters. An AI index does not ingest source data by itself. Its sources identify the data that an automation can use to generate KIs.

## 1. Enable Context Engine

Turn on Context Engine for the current Kibana space:

1. In Kibana, open **Stack Management → Advanced Settings**.
2. Search for **Context Engine**.
3. Turn on **Context Engine** (`contextEngine:enabled`).
4. Open **Context** from the Kibana navigation.

This setting applies to the current Kibana space.

## 2. Create an AI index

An AI index stores KIs for a particular purpose. Its name and description also help agents decide whether it is relevant to a question.

Create the AI index:

1. Select **Create AI Index**.
2. Enter a name that identifies the knowledge the AI index will contain. For example, enter `ecommerce-orders` if you are using the sample data.
3. Add a description that identifies the data and the questions it should support. For example:

   > Context about [your data], including [the important subjects and questions] and tested ESQL for retrieving current details.

4. Select **Index** as the storage type.
5. Select **Create AI Index**.

The AI index initially has no sources, automations, or KIs. You must add a source before you can create an automation.

## 3. Add the source data

An ESQL source gives Context Engine data to inspect when it suggests an automation. Start with a small, current sample so that you can review the resulting KI before expanding its coverage.

Add an ESQL source to the AI index:

1. In **Sources**, select **Edit**.
2. On the **ESQL** tab, enter a query that returns a small, representative set of records from your data. If you are using the ecommerce sample data, enter:

   ```esql
   FROM kibana_sample_data_ecommerce
   | SORT order_date DESC
   | LIMIT 100
   ```

3. Select **Add ESQL source**.
4. Confirm that the query appears under **Selected sources**.
5. Select **Save**.

This source gives Context Engine the 100 newest orders as a grounding sample. If you use your own data, change the index, sort field, filters, and limit to select representative records.

The generated Workflow can also inspect the mapping and run aggregations over the underlying index. Review those queries before you run the automation, and distinguish sampled observations from full-dataset findings.

An AI index can have multiple ESQL and connector sources. Keep this first example narrow so that you can inspect the generated KI before expanding its coverage.

## 4. Ask Agent Builder to suggest an automation

Use the guided route for this tutorial:

1. In **Automations**, select **Suggest automation**.
2. Agent Builder opens a conversation using the AI index and its configured source as context.
3. Ask it to create one `index_metadata` KI that:

   - explains the dataset's purpose and limitations
   - records useful interpretations of its important entities, measures, and dimensions
   - includes verified ESQL for common questions about the data
   - uses a stable ID so later runs update the KI instead of creating duplicates
   - validates its ESQL before writing the KI

4. Review the proposed plan before confirming it.

The proposal should identify the source result it will analyze, the KI it will produce, the access patterns it will generate, and any limits introduced by the source query. It should also identify any additional mapping, sampling, or aggregation queries it plans to run against the underlying data.

For a new AI index, {{agent-builder}} might recommend an Index/Table Metadata automation first. This automation creates an `index_metadata` KI that describes what the data contains, when to use it, and how to query it.

:::{note}
**Create automation** is the manual route. It opens a new, disabled Workflow in the [Workflows YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) with a manual trigger and generic starter YAML. Use it when you intend to author the KI-generation Workflow yourself.
:::

## 5. Create and review the automation

Create the suggested automation and review its Workflow:

1. Confirm the proposed plan.
2. Let {{agent-builder}} build and pilot the Workflow.
3. Review the pilot summary and proposed Workflow.
4. Before saving it, confirm that the Workflow:

   - uses the configured source as grounding input and identifies any additional queries against the underlying data
   - creates one `index_metadata` KI
   - records which claims come from a sample and which come from full-dataset aggregations
   - validates any generated ESQL before writing it
   - updates a stable KI document on later runs

5. Authorize {{agent-builder}} to save the automation.
6. Open the saved Workflow. Refer to [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md) for details about its YAML structure and execution lifecycle.

An automation is the process that generates and refreshes KIs. A suggested Workflow might include operations that:

- Retrieve the source mapping.
- Sample source documents and calculate grounding aggregations.
- Generate structured KI content with an AI prompt.
- Assemble the KI document.
- Check the syntax and runtime behavior of generated ESQL.
- Write the KI only when verification passes.

Review the scope of every query. For example, a Workflow might use the configured 100-document source as a sample but calculate totals and date ranges over the complete underlying index. The KI must make that distinction clear.

The pilot can create a temporary KI to validate the Workflow and then remove it before saving the final automation. After saving, {{agent-builder}} might start the automation immediately.

## 6. Run the automation and inspect the KI

Inspect the automation run and the KI it creates:

1. If {{agent-builder}} did not start the Workflow after saving it, run it manually.
2. [Check its execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md) and confirm that it completes successfully.
3. Return to the AI index in **Context**.
4. Open **Knowledge Indicators**.
5. Inspect the generated KI.

For a detailed explanation of the KI fields and a reusable review process, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

Start by inspecting the KI's identity and provenance:

- `id` remains stable across runs.
- `type` is `index_metadata`.
- `title` and `description` identify the data and its intended use.
- `governance.provenance` identifies the Workflow and run that created or updated the KI.

Then check that its content:

- accurately describes the data represented by the source result
- distinguishes sampled observations from full-dataset findings
- contains useful interpretation rather than merely repeating field mappings
- includes ESQL that targets the original source data
- explains when to use the data and which questions it cannot answer

A mapping query can already return field names and types. The KI is more useful when it captures business meaning, limitations, derived findings, or tested ways to use fields correctly. Syntax and runtime verification show that a query parses and runs, but you must still confirm that its grouping and calculations answer the intended question.

## 7. Make the AI index available to an agent

Add the populated AI index to an Agent Builder agent:

1. Open **Agent Builder**.
2. Create an agent or edit an existing one.
3. In **AI Indices**, add the AI index under **Additional indices**.
4. Save the agent.

The assignment makes the AI index and the dedicated Context Engine retrieval tools available to the agent. Its name and description help the agent decide when to retrieve its KIs. For details about the tools, source-data access, and custom instructions, refer to [Use Context Engine with {{agent-builder}}](use-context-engine-with-agent-builder.md).

## 8. Test how the agent uses the KI

Ask the agent questions that exercise both kinds of context:

1. Ask a question the KI can answer from its distilled content, such as what the dataset represents and what its important limitations are.
2. Ask for current or detailed information that requires one of the KI's verified ESQL queries.

For the ecommerce sample data, ask which questions the index cannot answer, then ask for a current revenue breakdown by manufacturer. The first answer should come from the KI. The second should cause the agent to query the source data.

Confirm that the agent:

- selects the relevant AI index
- retrieves the KI as context
- answers directly when the KI contains the required knowledge
- uses targeted ESQL against the source when current detail is required

KIs can reduce the time and model tokens agents spend exploring source data. They provide reusable knowledge and tested query guidance while preserving access to current source data.

## 9. Test refresh behavior

Run the automation again to confirm that it refreshes the existing KI:

1. Run the automation again.
2. Return to **Knowledge Indicators**.
3. Confirm that the existing KI was updated and that a duplicate was not created.
4. Compare the KI's `updated_at` value and provenance run ID with the previous run.
5. When the output is satisfactory, add an appropriate [scheduled trigger](/explore-analyze/workflows/triggers/scheduled-triggers.md) to the Workflow.

Choose a production schedule based on how quickly the source changes and how current the generated context must be.

## Next steps

After completing this tutorial, you can:

- Expand or revise the source query after validating the initial KI.
- Add connector sources for data that is not already in Elasticsearch.
- Select another [KI generation strategy](concepts.md#knowledge-indicators) for specific subjects, such as cumulative product or customer profiles.
- [Evaluate and improve the generated KIs](evaluate-and-improve-knowledge-indicators.md) as their sources and intended uses change.
- [Use the AI index with another agent](use-context-engine-with-agents.md).
