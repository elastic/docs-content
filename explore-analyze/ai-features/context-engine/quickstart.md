---
navigation_title: "Get started with Context Engine"
description: Create an AI index, generate knowledge from your source data, and make that context available to an agent.
applies_to:
  stack: preview 9.6
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Get started with Context Engine

:::{important}
This page is currently hidden from the documentation navigation. The current quickstart is intended for testing Context Engine enablement and the end-to-end workflow while the feature is under development.
:::

Context Engine turns raw source data into distilled context agents can use to solve problems faster. In this tutorial, you will create an AI index for data already stored in Elasticsearch, add a source, generate a Knowledge Indicator, and test it with an Agent Builder agent. You can use your own data or the Kibana sample ecommerce data.

## What you will build

You will create an AI index containing one Knowledge Indicator about a dataset you select.

A Knowledge Indicator (KI) is a document generated from source data, stored in an AI index, and retrieved as context by agents to help answer questions. A KI can contain distilled findings, explanations of how to interpret the data, limitations, and verified ESQL queries for retrieving current information from the source.

An automation generates and refreshes the KI. In Context Engine, an automation is implemented as a Kibana Workflow.

## Before you begin

You need:

- Kibana 9.6 or a compatible Serverless project.
- Permission to change Advanced Settings in the current Kibana space.
- Permission to create and run Workflows and manage Context Engine AI indices.
- Elasticsearch data that you can read. If you do not have suitable data, install the [**Sample eCommerce orders** data](https://www.elastic.co/docs/manage-data/ingest/sample-data#add-sample-data-sets), which creates the `kibana_sample_data_ecommerce` index.

Starting with existing data matters. An AI index does not ingest source data by itself. Its sources identify the data that an automation can use to generate KIs.

## 1. Enable Context Engine

Turn on Context Engine for the current Kibana space:

1. In Kibana, open **Stack Management → Advanced Settings**.
2. Search for **Context Engine**.
3. Turn on **Context Engine** (`contextEngine:enabled`).
4. Open **Context** from the Kibana navigation.

This setting applies to the current Kibana space.

**Checkpoint:** The Context page displays **Create AI Index**.

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

**Checkpoint:** The AI index overview opens and its **Automations** section is locked until a source is added.

## 3. Add the source data

An ESQL source is the complete result returned by its query. It is not merely the Elasticsearch index named in `FROM`.

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

This example source contains the 100 newest orders. If you use your own data, change the index, sort field, filters, and limit to produce a representative result set. Any findings generated from a source describe the query result, not necessarily the complete contents of the Elasticsearch indices named in `FROM`.

An AI index can have multiple ESQL and connector sources. Keep this first example narrow so that you can inspect the generated KI before expanding its coverage.

**Checkpoint:** The source appears on the AI index overview and the automation actions become available.

## 4. Ask Agent Builder to suggest an automation

Use the guided route for this tutorial:

1. In **Automations**, select **Suggest automation**.
2. Agent Builder opens a conversation using the AI index and its configured source as context.
3. Ask it to create one `index_metadata` KI that:

   - explains the dataset's purpose and limitations;
   - records useful interpretations of its important entities, measures, and dimensions;
   - includes verified ESQL for common questions about the data;
   - uses a stable ID so later runs update the KI instead of creating duplicates; and
   - validates its ESQL before writing the KI.

4. Review the proposed plan before confirming it.

The proposal should identify the source result it will analyze, the KI it will produce, the access patterns it will generate, and any limits introduced by the source query.

:::{note}
**Create automation** is the manual route. It opens a new, disabled Workflow in the general Workflows editor with a manual trigger and generic starter YAML. Use it when you intend to author the KI-generation Workflow yourself.
:::

**Checkpoint:** Agent Builder proposes a specific KI-generation plan and asks for confirmation before creating or replacing an automation.

## 5. Create and review the automation

Create the suggested automation and review its Workflow before running it:

1. Confirm the proposed plan.
2. Let Agent Builder create the automation.
3. Open the resulting Workflow.
4. Before running it, confirm that the Workflow:

   - uses the configured source;
   - creates one `index_metadata` KI;
   - records the source's sampling limitation;
   - validates any generated ESQL before writing it; and
   - updates a stable KI document on later runs.

An automation is the process that generates and refreshes KIs. The Workflow can execute ESQL while analyzing the source or validating access patterns. The resulting KI can also store verified ESQL that an agent can later use to query the source data.

**Checkpoint:** The automation appears on the AI index overview and its Workflow contains KI-generation logic rather than the generic starter steps.

## 6. Run the automation and inspect the KI

Run the automation and inspect the KI it creates:

1. Run the Workflow manually.
2. Check its execution and confirm that it completes successfully.
3. Return to the AI index in **Context**.
4. Open **Knowledge Indicators**.
5. Inspect the generated KI.

Check that the KI:

- accurately describes the data represented by the source result;
- distinguishes source limitations from general dataset information;
- contains useful interpretation rather than merely repeating field mappings;
- includes ESQL that targets the original source data; and
- uses a stable document ID.

A mapping query can already return field names and types. The KI is more useful when it captures business meaning, limitations, derived findings, or tested ways to use fields correctly.

**Checkpoint:** The AI index contains one useful `index_metadata` KI.

## 7. Make the AI index available to an agent

Add the populated AI index to an Agent Builder agent:

1. Open **Agent Builder**.
2. Create an agent or edit an existing one.
3. Add the AI index you created to the agent's AI index configuration.
4. Save the agent.

The assignment makes the AI index available to the agent. Its name and description help the agent decide when to retrieve its KIs.

**Checkpoint:** The AI index appears in the agent's configuration.

## 8. Test how the agent uses the KI

Ask the agent questions that exercise both kinds of context:

1. Ask a question the KI can answer from its distilled content, such as what the dataset represents and what its important limitations are.
2. Ask for current or detailed information that requires one of the KI's verified ESQL queries.

Confirm that the agent:

- selects the relevant AI index;
- retrieves the KI as context;
- answers directly when the KI contains the required knowledge; and
- uses targeted ESQL against the source when current detail is required.

KIs do not eliminate source retrieval. They replace repeated exploration of raw data with distilled knowledge and tested access guidance.

**Final checkpoint:** The agent uses the KI directly when it can and queries the source deliberately when it needs current details.

## 9. Test refresh behavior

Run the automation again to confirm that it refreshes the existing KI:

1. Run the automation again.
2. Return to **Knowledge Indicators**.
3. Confirm that the existing KI was updated and that a duplicate was not created.
4. When the output is satisfactory, add an appropriate schedule to the Workflow.

Choose a production schedule based on how quickly the source changes and how current the generated context must be.

## Next steps

After completing this tutorial, you can:

- Expand or revise the source query after validating the initial KI.
- Add connector sources for data that is not already in Elasticsearch.
- Create separate automations for more focused knowledge, such as cumulative product or customer profiles.
- Query an existing AI index from Claude Code through the read-only Context Engine MCP tools.
- Review Context Engine API, permissions, space isolation, retention, and cleanup guidance before production use.
