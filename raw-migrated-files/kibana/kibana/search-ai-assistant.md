# AI Assistant [search-ai-assistant]

::::{tip}
Don’t confuse AI Assistant with [Playground](../../../solutions/search/rag/playground.md)! Use Playground to chat with your data, test and tweak different {{es}} queries in the Playground UI, and download the code to integrate into your own RAG application.

Use AI Assistant to get help with Elasticsearch and Kibana tasks directly in the UI.

::::


::::{admonition} Observability use cases
Refer to the [Observability documentation](../../../solutions/observability/observability-ai-assistant.md) for more information on how to use AI Assistant in Observability contexts.

::::


**AI Assistant for Observability and Search** uses generative AI to help you with a variety of tasks related to Elasticsearch and Kibana, including:

1. **Constructing Queries**: Assists you in building queries to search and analyze your data.
2. **Indexing Data**: Guides you on how to index data into Elasticsearch.
3. **Searching Data**: Helps you search for specific data within your Elasticsearch indices.
4. **Using Elasticsearch APIs**: Calls Elasticsearch APIs on your behalf if you need specific operations performed.
5. **Generating Sample Data**: Helps you create sample data for testing and development purposes.
6. **Visualizing and Analyzing Data**: Assists you in creating visualizations and analyzing your data using Kibana.
7. **Explaining ES|QL**: Explains how ES|QL works and help you convert queries from other languages to [ES|QL.](../../../explore-analyze/query-filter/languages/esql.md)


## Requirements [ai-assistant-requirements]

To use AI Assistant in **Search** contexts, you must have the following:

* Elastic Stack version 8.16.0, or an Elasticsearch Serverless project.
* A [generative AI connector](../../../deploy-manage/manage-connectors.md) to connect to a LLM provider, or a local model.

    * You need an account with a third-party generative AI provider, which AI Assistant uses to generate responses, or else you need to host your own local model.
    * To set up AI Assistant, you need the `Actions and Connectors : All` [privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

* To use AI Assistant, you need at least the `Elastic AI Assistant : All` and `Actions and Connectors : Read` [privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
* AI Assistant requires [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md), Elastic’s proprietary semantic search model.


## Your data and AI Assistant [ai-assistant-data-information]

Elastic does not use customer data for model training. This includes anything you send the model, such as alert or event data, detection rule configurations, queries, and prompts. However, any data you provide to AI Assistant will be processed by the third-party provider you chose when setting up the generative AI connector as part of the assistant setup.

Elastic does not control third-party tools, and assumes no responsibility or liability for their content, operation, or use, nor for any loss or damage that may arise from your using such tools. Please exercise caution when using AI tools with personal, sensitive, or confidential information. Any data you submit may be used by the provider for AI training or other purposes. There is no guarantee that the provider will keep any information you provide secure or confidential. You should familiarize yourself with the privacy practices and terms of use of any generative AI tools prior to use.


## Using AI Assistant [ai-assistant-using]

To open AI Assistant, select the **AI Assistant** button in the top toolbar in the UI. You can also use the global search field in the UI to find AI Assistant.

:::{image} ../../../images/kibana-ai-assistant-button.png
:alt: AI Assistant button
:class: screenshot
:::

This opens the AI Assistant chat interface flyout.

:::{image} ../../../images/kibana-ai-assistant-welcome-chat.png
:alt: AI Assistant Welcome chat
:class: screenshot
:::

You can get started by selecting **✨ Suggest** to get some example prompts, or by typing into the chat field.


## Add data to the AI Assistant knowledge base [ai-assistant-add-custom-data]

::::{note}
This functionality is not available on Elastic Cloud Serverless projects.

::::


You can improve the relevance of AI Assistant’s responses by indexing your own data into AI Assistant’s knowledge base. AI Assistant uses [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md), Elastic’s proprietary semantic search model, to power its search capabilities.


### Use the UI [search-ai-assistant-use-the-ui]

To add external data to the knowledge base in UI:

1. In the AI Assistant UI, select the **Settings** icon: `⋮`.
2. Under **Actions**, click **Manage knowledge base**.
3. Click the **New entry** button, and choose either:

    * **Single entry**: Write content for a single entry in the UI.
    * **Bulk import**: Upload a newline delimited JSON (`ndjson`) file containing a list of entries to add to the knowledge base. Each object should conform to the following format:

        ```json
        {
          "id": "a_unique_human_readable_id",
          "text": "Contents of item",
        }
        ```



### Use Search connectors [observability-ai-assistant-add-data-to-kb]

::::{note}
This functionality is not available on Elastic Cloud Serverless projects.

::::


You can ingest external data (GitHub issues, Markdown files, Jira tickets, text files, etc.) into {{es}} using [Search Connectors](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/index.md). Connectors sync third party data sources to {{es}}.

Supported service types include [GitHub](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/es-connectors-github.md), [Slack](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/es-connectors-slack.md), [Jira](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/es-connectors-jira.md), and more. These can be Elastic managed or self-managed on your own infrastructure.

To create a connector and make its content available to the AI Assistant knowledge base, follow these steps:

1. **In {{kib}} UI, go to *Search → Content → Connectors* and follow the instructions to create a new connector.**

    For example, if you create a [GitHub connector](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/es-connectors-github.md) you must set a `name`, attach it to a new or existing `index`, add your `personal access token` and include the `list of repositories` to synchronize.

    ::::{tip}
    Learn more about configuring and [using connectors](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/connectors-ui-in-kibana.md) in the Elasticsearch documentation.
    ::::

2. **Create a pipeline and process the data with ELSER.**

    To process connector data using [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md), you must create an **ML Inference Pipeline**:

    1. Open the previously created connector and select the **Pipelines** tab.
    2. Select **Copy and customize** button at the `Unlock your custom pipelines` box.
    3. Select **Add Inference Pipeline** button at the `Machine Learning Inference Pipelines` box.
    4. Select **ELSER (Elastic Learned Sparse EncodeR)** ML model to add the necessary embeddings to the data.
    5. Select the fields that need to be evaluated as part of the inference pipeline.
    6. Test and save the inference pipeline and the overall pipeline.

3. **Sync data.**

    Once the pipeline is set up, perform a **Full Content Sync** of the connector. The inference pipeline will process the data as follows:

    * As data comes in, the ELSER model processes the data, creating sparse embeddings for each document.
    * If you inspect the ingested documents, you can see how the weights and tokens are added to the `predicted_value` field.

4. **Confirm AI Assistant can access the index.**

    Ask the AI Assistant a specific question to confirm that the data is available for the AI Assistant knowledge base.
