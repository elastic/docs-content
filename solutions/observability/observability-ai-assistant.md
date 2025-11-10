---
navigation_title: AI Assistant
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/obs-ai-assistant.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# {{obs-ai-assistant}} [obs-ai-assistant]

The AI Assistant is an integration with a large language model (LLM) that helps you understand, analyze, and interact with your Elastic data.

You can [interact with the AI Assistant](#obs-ai-interact) in two ways:

* **Contextual insights**: Embedded assistance throughout Elastic UIs that explains errors and messages with suggested remediation steps.
* **Chat interface**: A conversational experience where you can ask questions and receive answers about your data. The assistant uses function calling to request, analyze, and visualize information based on your needs.

The AI Assistant integrates with your large language model (LLM) provider through our [supported {{stack}} connectors](kibana://reference/connectors-kibana/gen-ai-connectors.md). Refer to the [{{obs-ai-assistant}} LLM performance matrix](./llm-performance-matrix.md) for supported third-party LLM providers and their performance ratings.

## Use cases

The {{obs-ai-assistant}} helps you:

* **Decode error messages**: Interpret stack traces and error logs to pinpoint root causes.
* **Identify performance bottlenecks**: Find resource-intensive operations and slow queries in {{es}}.
* **Generate reports**: Create alert summaries and incident timelines with key metrics.
* **Build and execute queries**: Build {{es}} queries from natural language, convert Query DSL to {{esql}} syntax, and execute queries directly from the chat interface.
* **Visualize data**: Create time-series charts and distribution graphs from your {{es}} data.

## Requirements [obs-ai-requirements]

The AI assistant requires the following:

- An **Elastic deployment**:

  - For **{{observability}}**: {{stack}} version **8.9** or later, or an **{{observability}} serverless project**.

  - For **Search**: {{stack}}  version **8.16.0** or later, or **{{serverless-short}} {{es}} project**.

    - To run {{obs-ai-assistant}} on a self-hosted Elastic stack, you need an [appropriate license](https://www.elastic.co/subscriptions).

- An account with a third-party generative AI provider that preferably supports function calling. If your AI provider does not support function calling, you can configure [AI Assistant settings](../../solutions/observability/observability-ai-assistant.md#obs-ai-settings) to simulate function calling, but this might affect performance.

  - The free tier offered by third-party generative AI provider may not be sufficient for the proper functioning of the AI assistant. In most cases, a paid subscription to one of the supported providers is required.

    Refer to the [documentation](kibana://reference/connectors-kibana/gen-ai-connectors.md) for your provider to learn about supported and default models.

* The knowledge base requires a 4 GB {{ml}} node.
  - In {{ecloud}} or {{ece}}, if you have Machine Learning autoscaling enabled, Machine Learning nodes will be started when using the knowledge base and AI Assistant. Therefore using these features will incur additional costs.

* A self-deployed connector service if you're using [content connectors](elasticsearch://reference/search-connectors/index.md) to populate external data into the knowledge base.

## Manage access to AI Assistant

```{applies_to}
stack: ga 9.2
serverless: ga
```

The [**GenAI settings**](/explore-analyze/manage-access-to-ai-assistant.md) page allows you to:

- Manage which AI connectors are available in your environment.
- Enable or disable AI Assistant and other AI-powered features in your environment.
- {applies_to}`stack: ga 9.2` {applies_to}`serverless: unavailable` Specify in which Elastic solutions the `AI Assistant for {{observability}} and Search` and the `AI Assistant for Security` appear.

## Your data and the AI Assistant [data-information]

It's important to understand how your data is handled when using the AI Assistant. Here are some key points:

**Data usage by Elastic**
:   Elastic does not use customer data for model training, but all data is processed by third-party AI providers.

**Anonymization**
:   Data sent to the AI Assistant is *not* anonymized, including alert data, configurations, queries, logs, and chat interactions. If you need to anonymize data, use the [anonymization pipeline](#obs-ai-anonymization).

**Permission context**
:   When the AI Assistant performs searches, it uses the same permissions as the current user.

**Third-party processing**
:   Any data submitted may be used by the provider for AI training or other purposes with no guarantee of security or confidentiality.

**Telemetry collection**: Your AI provider may collect telemetry during usage. Contact them for details on what data is collected.

## Set up the AI Assistant [obs-ai-set-up]

The AI Assistant connects to one of these supported LLM providers:

| Provider | Configuration | Authentication |
|----------|---------------------|---------------------|
| Preconfigured LLM (default) | No configuration needed | N/A |
| OpenAI | [Configure connector](kibana://reference/connectors-kibana/openai-action-type.md) | [Get API key](https://platform.openai.com/docs/api-reference) |
| Azure OpenAI | [Configure connector](kibana://reference/connectors-kibana/openai-action-type.md) | [Get API key](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference) |
| Amazon Bedrock | [Configure connector](kibana://reference/connectors-kibana/bedrock-action-type.md) | [Get auth keys](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html) |
| Google Gemini | [Configure connector](kibana://reference/connectors-kibana/gemini-action-type.md) | [Get service account key](https://cloud.google.com/iam/docs/keys-list-get) |

**Setup steps**:

1. **Create authentication credentials** with your chosen provider using the links in the previous table.
2. **Create an LLM connector** for your chosen provider by going to the **Connectors** management page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. **Authenticate the connection** by entering:
   - The provider's API endpoint URL.
   - Your authentication key or secret.

::::{admonition} Recommended models
While the {{obs-ai-assistant}} is compatible with many different models, refer to the [Large language model performance matrix](/solutions/observability/llm-performance-matrix.md) to select models that perform well with your desired use cases.

::::

### Elastic Managed LLM [elastic-managed-llm-obs-ai-assistant]

:::{include} ../_snippets/elastic-managed-llm.md
:::

### Connect to a custom local LLM
```{applies_to}
serverless: ga
stack: ga 9.2
```

[Connect to LM Studio](/solutions/observability/connect-to-own-local-llm.md) to use a custom LLM deployed and managed by you.

## Add data to the AI Assistant knowledge base [obs-ai-add-data]

The AI Assistant uses one of the following text embedding models to run  semantic search against the internal knowledge base index. The top results are passed to the LLM as context (retrieval‑augmented generation), producing more accurate and grounded responses:

* [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md): Recommended for English-only use cases.
* [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md): {applies_to}`stack: ga 9.1` Recommended for non-English use cases.

Adding data such as Runbooks, GitHub issues, internal documentation, and Slack messages to the knowledge base gives the AI Assistant context to provide more specific assistance.

Add data to the knowledge base with one or more of the following methods:

* [Use the knowledge base UI](#obs-ai-kb-ui) available at [AI Assistant Settings](#obs-ai-settings) page.
* [Use content connectors](#obs-ai-search-connectors)

You can also add information to the knowledge base by asking the AI Assistant to remember something while chatting (for example, "remember this for next time"). The assistant will create a summary of the information and add it to the knowledge base.


### Use the knowledge base UI [obs-ai-kb-ui]

To add external data to the knowledge base in {{kib}}:

1. To open AI Assistant settings, find `AI Assistants` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **{{obs-ai-assistant}}**, click **Manage settings**.
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

### Use content connectors [obs-ai-search-connectors]

[Content connectors](elasticsearch://reference/search-connectors/index.md) index content from external sources like GitHub, Confluence, Google Drive, Jira, S3, Teams, and Slack to improve the AI Assistant's responses.

#### Requirements and limitations

- For {{stack}} 9.0.0+ or {{serverless-short}}, connectors must be [self-managed](elasticsearch://reference/search-connectors/self-managed-connectors.md).
- Manage connectors through the Search Solution in {{kib}} (pre-9.0.0) or with the [Connector APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-connector).

#### Knowledge base data sources
By default, the AI Assistant queries all search connector indices. To customize which indices are used in the knowledge base, set the **Search connector index pattern** setting on the [AI Assistant Settings](#obs-ai-settings) page.

:::{note}
You're not limited to search connector indices in the **Search connector index pattern setting**. You can specify any index pattern.
:::

##### Space awareness
The **Search connector index pattern** setting is [space](../../deploy-manage/manage-spaces.md) aware. This means you can assign different values for different spaces. For example, a "Developers" space may include an index pattern like `github-*,jira*`, while an "HR" space may include an index pattern like `employees-*`.

##### Custom index field name requirements
Field names in custom indices have no specific requirements. Any `semantic_text` field is automatically queried. Documents matching the index pattern are sent to the LLM in full, including all fields. It's not currently possible to include or exclude specific fields.

#### Setup process:

1. **Create a connector**

   **Use the UI**:

   - Navigate to `Content / Connectors` in the global search field
   - Create a connector for your data source (example: [GitHub connector](elasticsearch://reference/search-connectors/es-connectors-github.md))
   - If your Space lacks the Search solution, either create the connector from a different space or change your space **Solution view** to `Classic`

   **Use the API**:
    - Create a connector using the [Connector APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-connector)

2. **Create embeddings** (choose one method):
   - [`semantic_text` field](#obs-ai-search-connectors-semantic-text): Recommended workflow which handles model setup automatically. Allows the use of any available ML model (Elser, e5, or custom models).
   - [ML pipeline](#obs-ai-search-connectors-ml-embeddings): Requires manual setup of the ELSER model and inference pipeline.

#### Option 1: Use a `semantic_text` field type to create embeddings (recommended) [obs-ai-search-connectors-semantic-text]

To create the embeddings needed by the AI Assistant using a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type:

1. Open the previously created connector, and select the **Mappings** tab.
2. Select **Add field**.
3. Under **Field type**, select **Semantic text**.
4. Under **Reference field**, select the field you want to use for model inference.
5. Under **Select an inference endpoint**, select the model you want to use to add the embeddings to the data.
6. Add the field to your mapping by selecting **Add field**.
7. Sync the data by selecting **Full Content** from the **Sync** menu.

The AI Assistant will now query the connector you’ve set up using the model you’ve selected. Check that the AI Assistant is using the index by asking it something related to the indexed data.

#### Option 2: Use machine learning pipelines to create embeddings [obs-ai-search-connectors-ml-embeddings]

This is a more complex method that requires you to set up the ELSER model and inference pipeline manually.

To create the embeddings needed by the AI Assistant (weights and tokens into a sparse vector field) using an **ML Inference Pipeline**:

1. Open the previously created content connector in **Content / Connectors**, and select the **Pipelines** tab.
2. Select **Copy and customize** under `Unlock your custom pipelines`.
3. Select **Add Inference Pipeline** under `Machine Learning Inference Pipelines`.
4. Select the **ELSER (Elastic Learned Sparse EncodeR)** ML model to add the necessary embeddings to the data.
5. Select the fields that need to be evaluated as part of the inference pipeline.
6. Test and save the inference pipeline and the overall pipeline.

After creating the pipeline, complete the following steps:

1. Sync the data.

    Once the pipeline is set up, perform a **Full Content Sync** of the connector. The inference pipeline will process the data as follows:

    * As data comes in, ELSER is applied to the data, and embeddings (weights and tokens into a [sparse vector field](elasticsearch://reference/query-languages/query-dsl/query-dsl-sparse-vector-query.md)) are added to capture semantic meaning and context of the data.
    * When you look at the ingested documents, you can see the embeddings are added to the `predicted_value` field in the documents.

2. Check if AI Assistant can use the index (optional).

    Ask something to the AI Assistant related with the indexed data.

### Add user-specific system prompts [obs-ai-assistant-user-prompt]

User-specific prompts customize how the AI assistant responds by appending personalized instructions to built-in system prompts. For example, you could specify "Always respond in French," and all subsequent responses will be in French.

A user-specific prompt only applies to the user that sets it.

To edit the **User-specific System Prompt**:

1. Go to the **{{obs-ai-assistant}}** management page. You can find it in the **Management** menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Switch to the **Knowledge base** tab.
4. Select **Edit User-specific Prompt**.

#### User-specific prompt example
User-specific prompts are useful when configuring specific workflows. For example, if you want the assistant to respond in a consistent, readable format when asked about Kubernetes metadata, you might add the following **user-specific system prompt**:

```
<kubernetes_info>
If asked about a Kubernetes pod, namespace, cluster, location, or owner, return the info in this format.  Use the field names to find the relevant information requested.  Don't mention the field names, just the results.
- Pod: agent.name
- Namespace: data_stream.namespace
- Cluster Name: orchestrator.cluster.name
- Owner: cloud.account.id
</kubernetes_info>
```

### Choose the Knowledge Base language model
```{applies_to}
stack: ga 9.1
```
Choose the default language model for the AI Assistant in the AI Assistant settings under **Set text embeddings model**.

* [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md): recommended for English-only use cases.
* [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md): supports multilingual use cases.

Select the language model and click **Update**.

When switching models, all existing Knowledge Base entries must be reindexed. Entries will be unavailable until reindexing is complete.

To have the AI Assistant respond in a language other than English, set a [user specific prompt](#obs-ai-assistant-user-prompt).

## Interact with the AI Assistant [obs-ai-interact]

::::{important}
The AI Assistant uses large language models (LLMs) which are probabilistic and liable to provide incomplete or incorrect information. Elastic supports LLM configuration and connectivity but is not responsible for response accuracy. Always verify important information before implementing suggested changes.
::::

Chat with the AI Assistant or interact with contextual insights located throughout the UI. Check the following sections for more on interacting with the AI Assistant.

::::{tip}
After every answer the LLM provides, let us know if the answer was helpful. Your feedback helps us improve the AI Assistant!
::::

### Chat with the assistant [obs-ai-chat]

Select the **AI Assistant** icon (![AI Assistant icon](/solutions/images/observability-ai-assistant-icon.png "")) at the upper-right corner of the Serverless or {{kib}} UI to start the chat.

This opens the AI Assistant flyout, where you can ask the assistant questions about your instance:

:::{image} /solutions/images/observability-obs-ai-chat.png
:alt: Observability AI assistant chat
:screenshot:
:::

::::{important}
Asking questions about your data requires `function calling`, which enables LLMs to reliably interact with third-party generative AI providers to perform searches or run advanced functions using customer data.

When the {{obs-ai-assistant}} performs searches in the cluster, the queries are run with the same level of permissions as the user.
::::

#### Suggest functions [obs-ai-functions]

```{applies_to}
stack: preview
serverless: preview
```

The AI Assistant uses functions to include relevant context in the chat conversation through text, data, and visual components. Both you and the AI Assistant can suggest functions. You can also edit the AI Assistant’s function suggestions and inspect function responses.

Main functions:

`alerts`
:   Get alerts for {{observability}}.

`changes`
:   Get change points like spikes and dips for logs and metrics data.

`elasticsearch`
:   Call {{es}} APIs on your behalf.

`execute_connector`
:   Call a {{kib}} connector on your behalf.

`get_alerts_dataset_info`
:   Get information about alerts data within a specified time range.

`get_data_on_screen`
:   Get the structured data of content currently visible on the user's screen. Use this function to provide more accurate and context-aware responses to your questions.

`get_dataset_info`
:    Get information about available indices and datasets and their fields.

`kibana`
:   Call {{kib}} APIs on your behalf.

`query`
:   Generate, execute, and visualize queries based on your request.

`retrieve_elastic_doc`
:   Get relevant Elastic documentation. This function is only available if the product documentation is installed.

`summarize`
:   Store information and facts in the knowledge base for future use. This function is only available if the [knowledge base](#obs-ai-add-data) has already been installed.

Additional functions are available when your cluster has APM data:

`get_apm_dataset_info`
:   Get information about APM data.

`get_apm_downstream_dependencies`
:   Get the downstream dependencies (services or uninstrumented backends) for a service. Map the downstream dependency name to a service by returning both `span.destination.service.resource` and `service.name`. Use this to drill down further if needed.

`get_apm_services_list`
:   Get the list of monitored services, their health statuses, and alerts.

### Use contextual prompts [obs-ai-prompts]

AI Assistant contextual prompts throughout {{observability}} provide the following information:

* **Universal Profiling**: explains the most expensive libraries and functions in your fleet and provides optimization suggestions.
* **Application performance monitoring (APM)**: explains APM errors and provides remediation suggestions.
* **Infrastructure Observability**: explains the processes running on a host.
* **Logs**: explains log messages and generates search patterns to find similar issues.
* **Alerting**: provides possible causes and remediation suggestions for log rate changes.

For example, in the log details, you’ll see prompts for **What’s this message?** and **How do I find similar log messages?**:

:::{image} /solutions/images/observability-obs-ai-logs-prompts.png
:alt: Observability AI assistant logs prompts
:screenshot:
:::

Clicking a prompt generates a message specific to that log entry:

:::{image} /solutions/images/observability-obs-ai-logs.gif
:alt: Observability AI assistant example
:screenshot:
:::

Continue a conversation from a contextual prompt by clicking **Start chat** to open the AI Assistant chat.

### Add the AI Assistant connector to alerting workflows [obs-ai-connector]

Use the [Observability AI Assistant connector](kibana://reference/connectors-kibana/obs-ai-assistant-action-type.md) to add AI-generated insights and custom actions to your alerting workflows as follows:

1. Navigate to **Observability / Alerts** to [create (or edit) an alerting rule](incident-management/create-manage-rules.md) that uses the AI Assistant connector. Specify the conditions that must be met for the alert to fire.
2. Under **Actions**, select the **Observability AI Assistant** connector type.
3. In the **Connector** list, select the AI connector you created when you set up the assistant.
4. In the **Message** field, specify the message to send to the assistant:

    :::{image} /solutions/images/observability-obs-ai-assistant-action-high-cpu.png
    :alt: Add an Observability AI assistant action while creating a rule in the Observability UI
    :screenshot:
    :::

You can ask the assistant to generate a report of the alert that fired, recall any information or potential resolutions of past occurrences stored in the knowledge base, provide troubleshooting guidance and resolution steps, and also include other active alerts that may be related. As a last step, you can ask the assistant to trigger an action, such as sending the report (or any other message) to a Slack webhook.

::::{note}
Currently only Slack, email, Jira, PagerDuty, or webhook actions are supported. Additional actions will be added in the future.
::::

When the alert fires, contextual details about the event—such as when the alert fired, the service or host impacted, and the threshold breached—are sent to the AI Assistant, along with the message provided during configuration. The AI Assistant runs the tasks requested in the message and creates a conversation you can use to chat with the assistant:

:::{image} /solutions/images/observability-obs-ai-assistant-output.png
:alt: AI Assistant conversation created in response to an alert
:screenshot:
:::

::::{important}
Conversations created by the AI Assistant are public and accessible to every user with permissions to use the assistant.
::::

It might take a minute or two for the AI Assistant to process the message and create the conversation.

Note that overly broad prompts may result in the request exceeding token limits. For more information, refer to [Token limits](#obs-ai-token-limits). Also, attempting to analyze several alerts in a single connector execution may cause you to exceed the function call limit. If this happens, modify the message specified in the connector configuration to avoid exceeding limits.

When asked to send a message to another connector, such as Slack, the AI Assistant attempts to include a link to the generated conversation.

::::{tip}
The `server.publicBaseUrl` setting must be correctly specified under {{kib}} settings, or the AI Assistant is unable to generate this link.
::::

:::{image} /solutions/images/observability-obs-ai-assistant-slack-message.png
:alt: Message sent by Slack by the AI Assistant includes a link to the conversation
:screenshot:
:::

{{obs-ai-assistant}} connector is called when the alert fires and when it recovers.

To learn more about alerting, actions, and connectors, refer to [Alerting](incident-management/alerting.md).

## AI Assistant Settings [obs-ai-settings]

To access the AI Assistant Settings page, you can:

* Find `AI Assistants` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Use the **More actions** menu inside the AI Assistant window.

The AI Assistant Settings page contains the following tabs:

* **Settings**: Configures the main AI Assistant settings, which are explained directly within the interface.
* **Knowledge base**: Manages [knowledge base entries](#obs-ai-kb-ui).
* **Content connectors**: Provides a link to {{kib}} **Search** → **Content** → **Connectors** UI for connectors configuration.

### Add Elastic documentation [obs-ai-product-documentation]

You can make the official Elastic documentation available to the AI Assistant, which significantly improves its ability to accurately answer questions about the Elastic Stack and Elastic products.

Enable this feature from the **Settings** tab in AI Assistant Settings by using the "Install Elastic Documentation" action.

::::{important}
For air-gapped environments, installing product documentation requires special configuration. See the [{{kib}} AI Assistants settings documentation](kibana://reference/configuration-reference/ai-assistant-settings.md) for detailed instructions.
::::

## Anonymization [obs-ai-anonymization]
```{applies_to}
serverless: preview
stack: preview 9.1
```

Anonymization masks personally identifiable or otherwise sensitive information before chat messages leave Kibana for a third-party LLM.
Enabled rules substitute deterministic tokens (for example `EMAIL_ee4587…`) so the model can keep context without ever seeing the real value.
When all rules are disabled (the default), data is forwarded unchanged.

### How it works [obs-ai-anonymization-how]

When an anonymization rule is enabled in the [AI Assistant settings](#obs-ai-settings), every message in the request (system prompt, message content, function call arguments/responses) is run through an *anonymization pipeline* before it leaves Kibana:

1. Each enabled **rule** scans the text and replaces any match with a deterministic token such as
   `EMAIL_ee4587b4ba681e38996a1b716facbf375786bff7`.
   The prefix (`EMAIL`, `PER`, `LOC`, …) is the *entity class*; the suffix is a deterministic hash of the original value.
2. The fully masked conversation is sent to the LLM.
3. After the LLM responds, the original values are restored so the user sees deanonymized text and any persisted conversation history stores the original content. Deanonymization information is stored with the conversation messages to enable the UI to highlight anonymized content.

### Rule types [obs-ai-anonymization-rules]


**RegExp**: Runs a JavaScript‑style regular expression. Use for fixed patterns such as email addresses, host names, etc.

```jsonc
{
  "type": "RegExp",
  "pattern": "([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})",
  "entityClass": "EMAIL",
  "enabled": true
}
```

**NER**: Runs a named entity recognition (NER) model on free text.

```jsonc
{
  "type": "NER",
  "modelId": "elastic__distilbert-base-uncased-finetuned-conll03-english",
  "allowedEntityClasses": ["PER", "ORG", "LOC"],
  "enabled": true
}
```

Rules are evaluated top-to-bottom with `RegExp` rules processed first, then `NER` rules; the first rule that captures a given entity wins. Rules can be configured in the [AI Assistant Settings](#obs-ai-settings) page.

### Example

The following example shows the anonymized content highlighted in the chat window using a `RegExp` rule to mask GKE hostnames:

```jsonc
{
  "entityClass": "GKE_HOST",
  "type": "RegExp",
  "pattern": "(gke-[a-zA-Z0-9-]+-[a-f0-9]{8}-[a-zA-Z0-9]+)",
  "enabled": true
}
```

:::{image} /solutions/images/observability-obs-ai-assistant-anonymization.png
:alt: AI Assistant chat showing hostname anonymization in action
:screenshot:
:::

### Requirements [obs-ai-anonymization-requirements]
Anonymization requires the following:

* **Advanced Settings privilege**: Necessary to edit the configuration and enable rules.
  Once saved, *all* users in the same **Space** benefit from the anonymization (the setting is [space-aware](../../deploy-manage/manage-spaces.md)).
* **ML privilege and resources**: If you enable a rule of type NER, you must first [deploy and start a named-entity-recognition model](/explore-analyze/machine-learning/nlp/ml-nlp-ner-example.md#ex-ner-deploy) and have sufficient ML capacity.

::::{important}
The anonymization pipeline has only been validated with Elastic’s English model
[elastic/distilbert-base-uncased-finetuned-conll03-english](https://huggingface.co/elastic/distilbert-base-uncased-finetuned-conll03-english).
Results for other languages or models may vary.
::::

### Limitations [obs-ai-anonymization-limitations]
Anonymization has the following limitations:

* **Non-string fields**:  {applies_to}`stack: ga 9.1.3` Anonymization only applies to string values. Booleans, numbers, image types, and other non-string values are ignored.
* **Performance (NER)**: Running an NER model can add latency depending on the request. To improve performance of the model, consider scaling up your ML nodes by adjusting deployment parameters: increase `number_of_allocations` for better throughput and `threads_per_allocation` for faster individual requests. For details, refer to [start trained model deployment API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment).
* **Structured JSON**: The NER model we validated (`elastic/distilbert-base-uncased-finetuned-conll03-english`) is trained on natural English text and often misses entities inside JSON or other structured data. If thorough masking is required, prefer regex rules and craft them to account for JSON syntax.
* **False negatives / positives**: No model or pattern is perfect. Model accuracy may vary depending on model and input.
* **JSON malformation risk** {applies_to}`{stack: "removed 9.1.3", serverless: "removed"}`: Both NER inference and regex rules can potentially create malformed JSON when anonymizing JSON data such as function responses. This can occur by replacing text across character boundaries, which may break JSON structure causing the whole request to fail. If this occurs, you may need to adjust your regex pattern or disable the NER rule.


## Known issues [obs-ai-known-issues]

### Token limits [obs-ai-token-limits]

Most LLMs have a set number of tokens they can manage in single a conversation. When you reach the token limit, the LLM will throw an error, and Elastic will display a "Token limit reached" error in Kibana. The exact number of tokens that the LLM can support depends on the LLM provider and model you’re using. If you use an OpenAI connector, monitor token utilization in **OpenAI Token Usage** dashboard. For more information, refer to the [OpenAI Connector documentation](kibana://reference/connectors-kibana/openai-action-type.md#openai-connector-token-dashboard).


## AI Assistant for Security

The capabilities and ways to interact with AI Assistant can differ for each solution. For more information about how AI Assistant works in {{elastic-sec}}, refer to [AI Assistant for Security](/solutions/security/ai/ai-assistant.md).