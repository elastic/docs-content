# Observability AI Assistant [obs-ai-assistant]

::::{important}
To run the Observability AI Assistant on self-hosted Elastic stack, you need an [appropriate license](https://www.elastic.co/subscriptions).
::::


The AI Assistant uses generative AI to provide:

* **Contextual insights** — open prompts throughout {{observability}} that explain errors and messages and suggest remediation.
* **Chat** —  have conversations with the AI Assistant. Chat uses function calling to request, analyze, and visualize your data.

:::{image} ../../../images/observability-obs-assistant2.gif
:alt: Observability AI assistant preview
:class: screenshot
:::

The AI Assistant integrates with your large language model (LLM) provider through our supported {{stack}} connectors:

* [OpenAI connector](https://www.elastic.co/guide/en/kibana/current/openai-action-type.html) for OpenAI or Azure OpenAI Service.
* [Amazon Bedrock connector](https://www.elastic.co/guide/en/kibana/current/bedrock-action-type.html) for Amazon Bedrock, specifically for the Claude models.
* [Google Gemini connector](https://www.elastic.co/guide/en/kibana/current/gemini-action-type.html) for Google Gemini.

::::{important}
The AI Assistant is powered by an integration with your large language model (LLM) provider. LLMs are known to sometimes present incorrect information as if it’s correct. Elastic supports configuration and connection to the LLM provider and your knowledge base, but is not responsible for the LLM’s responses.

::::


::::{important}
Also, the data you provide to the Observability AI assistant is *not* anonymized, and is stored and processed by the third-party AI provider. This includes any data used in conversations for analysis or context, such as alert or event data, detection rule configurations, and queries. Therefore, be careful about sharing any confidential or sensitive details while using this feature.

::::



## Requirements [obs-ai-requirements]

The AI assistant requires the following:

* {{stack}} version 8.9 and later.
* A [self-managed](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-build-connector.html) connector service must be deployed if search connectors are used to populate external data into the knowledge base.
* An account with a third-party generative AI provider that preferably supports function calling. If your AI provider does not support function calling, you can configure AI Assistant settings under **Stack Management** to simulate function calling, but this might affect performance.

    Refer to the [connector documentation](../../../deploy-manage/manage-connectors.md) for your provider to learn about supported and default models.

* The knowledge base requires a 4 GB {{ml}} node.

::::{important}
The free tier offered by third-party generative AI provider may not be sufficient for the proper functioning of the AI assistant. In most cases, a paid subscription to one of the supported providers is required.

The Observability AI assistant doesn’t support connecting to a private LLM. Elastic doesn’t recommend using private LLMs with the Observability AI assistant.

::::


::::{important}
In {{ecloud}} or {{ece}}, if you have Machine Learning autoscaling enabled, Machine Learning nodes will be started when using the knowledge base and AI Assistant. Therefore using these features will incur additional costs.

::::



## Your data and the AI Assistant [data-information]

Elastic does not use customer data for model training. This includes anything you send the model, such as alert or event data, detection rule configurations, queries, and prompts. However, any data you provide to the AI Assistant will be processed by the third-party provider you chose when setting up the OpenAI connector as part of the assistant setup.

Elastic does not control third-party tools, and assumes no responsibility or liability for their content, operation, or use, nor for any loss or damage that may arise from your using such tools. Please exercise caution when using AI tools with personal, sensitive, or confidential information. Any data you submit may be used by the provider for AI training or other purposes. There is no guarantee that the provider will keep any information you provide secure or confidential. You should familiarize yourself with the privacy practices and terms of use of any generative AI tools prior to use.


## Set up the AI Assistant [obs-ai-set-up]

To set up the AI Assistant:

1. Create an authentication key with your AI provider to authenticate requests from the AI Assistant. You’ll use this in the next step. Refer to your provider’s documentation for information about creating authentication keys:

    * [OpenAI API keys](https://platform.openai.com/docs/api-reference)
    * [Azure OpenAI Service API keys](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference)
    * [Amazon Bedrock authentication keys and secrets](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.md)
    * [Google Gemini service account keys](https://cloud.google.com/iam/docs/keys-list-get)

2. Create a connector for your AI provider. Refer to the connector documentation to learn how:

    * [OpenAI](https://www.elastic.co/guide/en/kibana/current/openai-action-type.html)
    * [Amazon Bedrock](https://www.elastic.co/guide/en/kibana/current/bedrock-action-type.html)
    * [Google Gemini](https://www.elastic.co/guide/en/kibana/current/gemini-action-type.html)

3. Authenticate communication between {{observability}} and the AI provider by providing the following information:

    1. In the **URL** field, enter the AI provider’s API endpoint URL.
    2. Under **Authentication**, enter the key or secret you created in the previous step.



## Add data to the AI Assistant knowledge base [obs-ai-add-data]

::::{important}
**If you started using the AI Assistant in technical preview**, any knowledge base articles you created before 8.12 will have to be reindexed or upgraded before they can be used. Knowledge base articles created before 8.12 use ELSER v1. In 8.12, knowledge base articles must use ELSER v2. Options include:

* Clear all old knowledge base articles manually and reindex them.
* Upgrade all knowledge base articles indexed with ELSER v1 to ELSER v2 using a [Python script](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/model-upgrades/upgrading-index-to-use-elser.ipynb).

::::


The AI Assistant uses [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md), Elastic’s semantic search engine, to recall data from its internal knowledge base index to create retrieval augmented generation (RAG) responses. Adding data such as Runbooks, GitHub issues, internal documentation, and Slack messages to the knowledge base gives the AI Assistant context to provide more specific assistance.

::::{note}
Your AI provider may collect telemetry when using the AI Assistant. Contact your AI provider for information on how data is collected.
::::


Add data to the knowledge base with one or more of the following methods:

* [Use the knowledge base UI](../../../solutions/observability/observability-ai-assistant.md#obs-ai-kb-ui) available at [AI Assistant Settings](../../../solutions/observability/observability-ai-assistant.md#obs-ai-settings) page.
* [Use search connectors](../../../solutions/observability/observability-ai-assistant.md#obs-ai-search-connectors)

You can also add information to the knowledge base by asking the AI Assistant to remember something while chatting (for example, "remember this for next time"). The assistant will create a summary of the information and add it to the knowledge base.


### Use the knowledge base UI [obs-ai-kb-ui]

To add external data to the knowledge base in {{kib}}:

1. To open AI Assistant settings, find `AI Assistants` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Elastic AI Assistant for Observability**, click **Manage settings**.
3. Switch to the **Knowledge base** tab.
4. Click the **New entry** button, and choose either:

    * **Single entry**: Write content for a single entry in the UI.
    * **Bulk import**: Upload a newline delimited JSON (`ndjson`) file containing a list of entries to add to the knowledge base. Each object should conform to the following format:

        ```json
        {
          "id": "a_unique_human_readable_id",
          "text": "Contents of item"
        }
        ```



### Use search connectors [obs-ai-search-connectors]

::::{tip}
The [search connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html) described in this section differ from the [Stack management → Connectors](../../../deploy-manage/manage-connectors.md) configured during the [AI Assistant setup](../../../solutions/observability/observability-ai-assistant.md#obs-ai-set-up). Search connectors are only needed when importing external data into the Knowledge base of the AI Assistant, while the stack connector to the LLM is required for the AI Assistant to work.

::::


[Connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html) allow you to index content from external sources thereby making it available for the AI Assistant. This can greatly improve the relevance of the AI Assistant’s responses. Data can be integrated from sources such as GitHub, Confluence, Google Drive, Jira, AWS S3, Microsoft Teams, Slack, and more.

UI affordances for creating and managing search connectors are available in the Search Solution in {{kib}}. You can also use the {{es}} [Connector APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-connector) to create and manage search connectors.

A [self-managed](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-build-connector.html) connector service must be deployed to run connectors.

By default, the AI Assistant queries all search connector indices. To override this behavior and customize which indices are queried, adjust the **Search connector index pattern** setting on the [AI Assistant Settings](../../../solutions/observability/observability-ai-assistant.md#obs-ai-settings) page. This allows precise control over which data sources are included in AI Assistant knowledge base.

To create a connector in the {{kib}} UI and make its content available to the AI Assistant knowledge base, follow these steps:

1. Open **Connectors** by finding `Content / Connectors` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    ::::{note}
    If your {{kib}} Space doesn’t include the Search solution you will have to create the connector from a different space or change your space **Solution view** setting to `Classic`.

    ::::

2. Follow the instructions to create a new connector.

    For example, if you create a [GitHub connector](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors-github.html) you have to set a `name`, attach it to a new or existing `index`, add your `personal access token` and include the `list of repositories` to synchronize.

    Learn more about configuring and [using connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors-usage.html) in the Elasticsearch documentation.


After creating your connector, create the embeddings needed by the AI Assistant. You can do this using either:

* [a machine learning (ML) pipeline](../../../solutions/observability/observability-ai-assistant.md#obs-ai-search-connectors-ml-embeddings): requires the ELSER ML model.
* [a `semantic_text` field type](../../../solutions/observability/observability-ai-assistant.md#obs-ai-search-connectors-semantic-text): can use any available ML model (ELSER, E5, or a custom model).


#### Use machine learning pipelines to create AI Assistant embeddings [obs-ai-search-connectors-ml-embeddings]

To create the embeddings needed by the AI Assistant (weights and tokens into a sparse vector field) using an **ML Inference Pipeline**:

1. Open the previously created connector, and select the **Pipelines** tab.
2. Select **Copy and customize** under `Unlock your custom pipelines`.
3. Select **Add Inference Pipeline** under `Machine Learning Inference Pipelines`.
4. Select the **ELSER (Elastic Learned Sparse EncodeR)** ML model to add the necessary embeddings to the data.
5. Select the fields that need to be evaluated as part of the inference pipeline.
6. Test and save the inference pipeline and the overall pipeline.

After creating the pipeline, complete the following steps:

1. Sync the data.

    Once the pipeline is set up, perform a **Full Content Sync** of the connector. The inference pipeline will process the data as follows:

    * As data comes in, ELSER is applied to the data, and embeddings (weights and tokens into a [sparse vector field](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-sparse-vector-query.html)) are added to capture semantic meaning and context of the data.
    * When you look at the ingested documents, you can see the embeddings are added to the `predicted_value` field in the documents.

2. Check if AI Assistant can use the index (optional).

    Ask something to the AI Assistant related with the indexed data.



#### Use a `semantic_text` field type to create AI Assistant embeddings [obs-ai-search-connectors-semantic-text]

To create the embeddings needed by the AI Assistant using a [`semantic_text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html) field type:

1. Open the previously created connector, and select the **Mappings** tab.
2. Select **Add field**.
3. Under **Field type**, select **Semantic text**.
4. Under **Reference field**, select the field you want to use for model inference.
5. Under **Select an inference endpoint**, select the model you want to use to add the embeddings to the data.
6. Add the field to your mapping by selecting **Add field**.
7. Sync the data by selecting **Full Content** from the **Sync** menu.

The AI Assistant will now query the connector you’ve set up using the model you’ve selected. Check that the AI Assistant is using the index by asking it something related to the indexed data.


## Interact with the AI Assistant [obs-ai-interact]

Chat with the AI Assistant or interact with contextual insights located throughout {{observability}}. Check the following sections for more on interacting with the AI Assistant.

::::{tip}
After every answer the LLM provides, let us know if the answer was helpful. Your feedback helps us improve the AI Assistant!
::::



### Chat with the assistant [obs-ai-chat]

Select the **AI Assistant** icon (![AI Assistant icon](../../../images/observability-ai-assistant-icon.png "")) at the upper-right corner of any {{observability}} application to start the chat.

This opens the AI Assistant flyout, where you can ask the assistant questions about your instance:

:::{image} ../../../images/observability-obs-ai-chat.png
:alt: Observability AI assistant chat
:class: screenshot
:::

::::{important}
Asking questions about your data requires `function calling`, which enables LLMs to reliably interact with third-party generative AI providers to perform searches or run advanced functions using customer data.

When the {{observability}} AI Assistant performs searches in the cluster, the queries are run with the same level of permissions as the user.

::::



### Suggest functions [obs-ai-functions]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


The AI Assistant uses functions to include relevant context in the chat conversation through text, data, and visual components. Both you and the AI Assistant can suggest functions. You can also edit the AI Assistant’s function suggestions and inspect function responses.

Main functions:

`alerts`
:   Get alerts for {{observability}}.

`elasticsearch`
:   Call {{es}} APIs on your behalf.

`kibana`
:   Call {{kib}} APIs on your behalf.

`summarize`
:   Summarize parts of the conversation.

`visualize_query`
:   Visualize charts for ES|QL queries.

Additional functions are available when your cluster has APM data:

`get_apm_correlations`
:   Get field values that are more prominent in the foreground set than the background set. This can be useful in determining which attributes (such as `error.message`, `service.node.name`, or `transaction.name`) are contributing to, for instance, a higher latency. Another option is a time-based comparison, where you compare before and after a change point.

`get_apm_downstream_dependencies`
:   Get the downstream dependencies (services or uninstrumented backends) for a service. Map the downstream dependency name to a service by returning both `span.destination.service.resource` and `service.name`. Use this to drill down further if needed.

`get_apm_error_document`
:   Get a sample error document based on the grouping name. This also includes the stacktrace of the error, which might hint to the cause.

`get_apm_service_summary`
:   Get a summary of a single service, including the language, service version, deployments, the environments, and the infrastructure that it is running in. For example, the number of pods and a list of their downstream dependencies. It also returns active alerts and anomalies.

`get_apm_services_list`
:   Get the list of monitored services, their health statuses, and alerts.

`get_apm_timeseries`
:   Display different APM metrics (such as throughput, failure rate, or latency) for any service or all services and any or all of their dependencies. Displayed both as a time series and as a single statistic. Additionally, the function  returns any changes, such as spikes, step and trend changes, or dips. You can also use it to compare data by requesting two different time ranges, or, for example, two different service versions.


### Use contextual prompts [obs-ai-prompts]

AI Assistant contextual prompts throughout {{observability}} provide the following information:

* **Universal Profiling** — explains the most expensive libraries and functions in your fleet and provides optimization suggestions.
* **Application performance monitoring (APM)** — explains APM errors and provides remediation suggestions.
* **Infrastructure Observability** — explains the processes running on a host.
* **Logs** — explains log messages and generates search patterns to find similar issues.
* **Alerting** — provides possible causes and remediation suggestions for log rate changes.

For example, in the log details, you’ll see prompts for **What’s this message?** and **How do I find similar log messages?**:

:::{image} ../../../images/observability-obs-ai-logs-prompts.png
:alt: Observability AI assistant logs prompts
:class: screenshot
:::

Clicking a prompt generates a message specific to that log entry:

:::{image} ../../../images/observability-obs-ai-logs.gif
:alt: Observability AI assistant example
:class: screenshot
:::

Continue a conversation from a contextual prompt by clicking **Start chat** to open the AI Assistant chat.


### Add the AI Assistant connector to alerting workflows [obs-ai-connector]

Use the [Observability AI Assistant connector](https://www.elastic.co/guide/en/kibana/current/obs-ai-assistant-action-type.html) to add AI-generated insights and custom actions to your alerting workflows as follows:

1. [Create (or edit) an alerting rule](../../../solutions/observability/incident-management/create-manage-rules.md) and specify the conditions that must be met for the alert to fire.
2. Under **Actions**, select the **Observability AI Assistant** connector type.
3. In the **Connector** list, select the AI connector you created when you set up the assistant.
4. In the **Message** field, specify the message to send to the assistant:

    :::{image} ../../../images/observability-obs-ai-assistant-action-high-cpu.png
    :alt: Add an Observability AI assistant action while creating a rule in the Observability UI
    :class: screenshot
    :::


You can ask the assistant to generate a report of the alert that fired, recall any information or potential resolutions of past occurrences stored in the knowledge base, provide troubleshooting guidance and resolution steps, and also include other active alerts that may be related. As a last step, you can ask the assistant to trigger an action, such as sending the report (or any other message) to a Slack webhook.

::::{note}
Currently only Slack, email, Jira, PagerDuty, or webhook actions are supported. Additional actions will be added in the future.
::::


When the alert fires, contextual details about the event—such as when the alert fired, the service or host impacted, and the threshold breached—are sent to the AI Assistant, along with the message provided during configuration. The AI Assistant runs the tasks requested in the message and creates a conversation you can use to chat with the assistant:

:::{image} ../../../images/observability-obs-ai-assistant-output.png
:alt: AI Assistant conversation created in response to an alert
:class: screenshot
:::

::::{important}
Conversations created by the AI Assistant are public and accessible to every user with permissions to use the assistant.
::::


It might take a minute or two for the AI Assistant to process the message and create the conversation.

Note that overly broad prompts may result in the request exceeding token limits. For more information, refer to [Token limits](../../../solutions/observability/observability-ai-assistant.md#obs-ai-token-limits). Also, attempting to analyze several alerts in a single connector execution may cause you to exceed the function call limit. If this happens, modify the message specified in the connector configuration to avoid exceeding limits.

When asked to send a message to another connector, such as Slack, the AI Assistant attempts to include a link to the generated conversation.

::::{tip}
The `server.publicBaseUrl` setting must be correctly specified under {{kib}} settings, or the AI Assistant is unable to generate this link.
::::


:::{image} ../../../images/observability-obs-ai-assistant-slack-message.png
:alt: Message sent by Slack by the AI Assistant includes a link to the conversation
:class: screenshot
:::

The Observability AI Assistant connector is called when the alert fires and when it recovers.

To learn more about alerting, actions, and connectors, refer to [Alerting](../../../solutions/observability/incident-management/alerting.md).


## AI Assistant Settings [obs-ai-settings]

To access the AI Assistant Settings page, you can:

* Find `AI Assistants` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Use the **More actions** menu inside the AI Assistant window.

The AI Assistant Settings page contains the following tabs:

* **Settings**: Configures the main AI Assistant settings, which are explained directly within the interface.
* **Knowledge base**: Manages [knowledge base entries](../../../solutions/observability/observability-ai-assistant.md#obs-ai-kb-ui).
* **Search Connectors**: Provides a link to {{kib}} **Search** → **Content** → **Connectors** UI for connectors configuration.


## Elastic documentation for the AI Assistant [obs-ai-product-documentation]

It is possible to make the Elastic official documentation available to the AI Assistant, which significantly increases its efficiency and accuracy in answering questions related to the Elastic stack and Elastic products.

Enabling that feature can be done from the **Settings** tab of the AI Assistant Settings page, using the "Install Elastic Documentation" action.

::::{important}
Installing the product documentation in air gapped environments requires specific installation and configuration instructions, which are available in the [{{kib}} Kibana AI Assistants settings documentation](https://www.elastic.co/guide/en/kibana/current/ai-assistant-settings-kb.html).
::::



## Known issues [obs-ai-known-issues]


### Token limits [obs-ai-token-limits]

Most LLMs have a set number of tokens they can manage in single a conversation. When you reach the token limit, the LLM will throw an error, and Elastic will display a "Token limit reached" error in Kibana. The exact number of tokens that the LLM can support depends on the LLM provider and model you’re using. If you use an OpenAI connector, monitor token utilization in **OpenAI Token Usage** dashboard. For more information, refer to the [OpenAI Connector documentation](https://www.elastic.co/guide/en/kibana/current/openai-action-type.html#openai-connector-token-dashboard).
