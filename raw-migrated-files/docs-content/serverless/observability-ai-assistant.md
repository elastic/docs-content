# {{observability}} AI Assistant [observability-ai-assistant]

The AI Assistant uses generative AI to provide:

* **Chat**: Have conversations with the AI Assistant. Chat uses function calling to request, analyze, and visualize your data.
* **Contextual insights**: Open prompts throughout {{obs-serverless}} that explain errors and messages and suggest remediation.

:::{image} ../../../images/serverless-ai-assistant-overview.gif
:alt: Observability AI assistant preview
:class: screenshot
:::

The AI Assistant integrates with your large language model (LLM) provider through our supported Elastic connectors:

* [OpenAI connector](kibana://reference/connectors-kibana/openai-action-type.md) for OpenAI or Azure OpenAI Service.
* [Amazon Bedrock connector](kibana://reference/connectors-kibana/bedrock-action-type.md) for Amazon Bedrock, specifically for the Claude models.
* [Google Gemini connector](kibana://reference/connectors-kibana/gemini-action-type.md) for Google Gemini.

::::{important}
The AI Assistant is powered by an integration with your large language model (LLM) provider. LLMs are known to sometimes present incorrect information as if it’s correct. Elastic supports configuration and connection to the LLM provider and your knowledge base, but is not responsible for the LLM’s responses.

::::


::::{important}
Also, the data you provide to the Observability AI assistant is *not* anonymized, and is stored and processed by the third-party AI provider. This includes any data used in conversations for analysis or context, such as alert or event data, detection rule configurations, and queries. Therefore, be careful about sharing any confidential or sensitive details while using this feature.

::::



## Requirements [observability-ai-assistant-requirements]

The AI assistant requires the following:

* An account with a third-party generative AI provider that preferably supports function calling. If your AI provider does not support function calling, you can configure AI Assistant settings under **Project settings** → **Management** → **AI Assistant for Observability Settings** to simulate function calling, but this might affect performance.

    Refer to the [connector documentation](../../../deploy-manage/manage-connectors.md) for your provider to learn about supported and default models.

* The knowledge base requires a 4 GB {{ml}} node.

::::{important}
The free tier offered by third-party generative AI providers may not be sufficient for the proper functioning of the AI assistant. In most cases, a paid subscription to one of the supported providers is required. The Observability AI assistant doesn’t support connecting to a private LLM. Elastic doesn’t recommend using private LLMs with the Observability AI assistant.

::::



## Your data and the AI Assistant [observability-ai-assistant-your-data-and-the-ai-assistant]

Elastic does not use customer data for model training. This includes anything you send the model, such as alert or event data, detection rule configurations, queries, and prompts. However, any data you provide to the AI Assistant will be processed by the third-party provider you chose when setting up the OpenAI connector as part of the assistant setup.

Elastic does not control third-party tools, and assumes no responsibility or liability for their content, operation, or use, nor for any loss or damage that may arise from your using such tools. Please exercise caution when using AI tools with personal, sensitive, or confidential information. Any data you submit may be used by the provider for AI training or other purposes. There is no guarantee that the provider will keep any information you provide secure or confidential. You should familiarize yourself with the privacy practices and terms of use of any generative AI tools prior to use.


## Set up the AI Assistant [observability-ai-assistant-set-up-the-ai-assistant]

To set up the AI Assistant:

1. Create an authentication key with your AI provider to authenticate requests from the AI Assistant. You’ll use this in the next step. Refer to your provider’s documentation for information about creating authentication keys:

    * [OpenAI API keys](https://platform.openai.com/docs/api-reference)
    * [Azure OpenAI Service API keys](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference)
    * [Amazon Bedrock authentication keys and secrets](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.md)
    * [Google Gemini service account keys](https://cloud.google.com/iam/docs/keys-list-get)

2. From **Project settings** → **Management** → **Connectors**, create a connector for your AI provider:

    * [OpenAI](kibana://reference/connectors-kibana/openai-action-type.md)
    * [Amazon Bedrock](kibana://reference/connectors-kibana/bedrock-action-type.md)
    * [Google Gemini](kibana://reference/connectors-kibana/gemini-action-type.md)

3. Authenticate communication between {{obs-serverless}} and the AI provider by providing the following information:

    1. In the **URL** field, enter the AI provider’s API endpoint URL.
    2. Under **Authentication**, enter the key or secret you created in the previous step.



## Add data to the AI Assistant knowledge base [observability-ai-assistant-add-data-to-the-ai-assistant-knowledge-base]

::::{important}
**If you started using the AI Assistant in technical preview**, any knowledge base articles you created using ELSER v1 will need to be reindexed or upgraded before they can be used. Going forward, you must create knowledge base articles using ELSER v2. You can either:

* Clear all old knowledge base articles manually and reindex them.
* Upgrade all knowledge base articles indexed with ELSER v1 to ELSER v2 using a [Python script](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/model-upgrades/upgrading-index-to-use-elser.ipynb).

::::


The AI Assistant uses [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md), Elastic’s semantic search engine, to recall data from its internal knowledge base index to create retrieval augmented generation (RAG) responses. Adding data such as Runbooks, GitHub issues, internal documentation, and Slack messages to the knowledge base gives the AI Assistant context to provide more specific assistance.

::::{note}
Your AI provider may collect telemetry when using the AI Assistant. Contact your AI provider for information on how data is collected.

::::


You can add information to the knowledge base by asking the AI Assistant to remember something while chatting (for example, "remember this for next time"). The assistant will create a summary of the information and add it to the knowledge base.

You can also add external data to the knowledge base either in the Project Settings UI or using the {{es}} Index API.


### Use the UI [observability-ai-assistant-use-the-ui]

To add external data to the knowledge base in the Project Settings UI:

1. Go to **Project Settings**.
2. In the *Other* section, click **AI assistant for Observability settings**.
3. Then select the **Elastic AI Assistant for Observability**.
4. Switch to the **Knowledge base** tab.
5. Click the **New entry** button, and choose either:

    * **Single entry**: Write content for a single entry in the UI.
    * **Bulk import**: Upload a newline delimited JSON (`ndjson`) file containing a list of entries to add to the knowledge base. Each object should conform to the following format:

        ```json
        {
          "id": "a_unique_human_readable_id",
          "text": "Contents of item",
        }
        ```



### Use the {{es}} Index API [observability-ai-assistant-use-the-es-index-api]

1. Ingest external data (GitHub issues, Markdown files, Jira tickets, text files, etc.) into {{es}} using the {{es}} [Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create).
2. Reindex your data into the AI Assistant’s knowledge base index by completing the following query in **Developer Tools** → **Console**. Update the following fields before reindexing:

    * `InternalDocsIndex`: Name of the index where your internal documents are stored.
    * `text_field`: Name of the field containing your internal documents' text.
    * `timestamp`: Name of the timestamp field in your internal documents.
    * `public`: If `true`, the document is available to all users with access to your Observability project. If `false`, the document is restricted to the user indicated in the following `user.name` field.
    * `user.name` (optional): If defined, restricts the internal document’s availability to a specific user.
    * You can add a query filter to index specific documents.


```console
POST _reindex
{
    "source": {
        "index": "<InternalDocsIndex>",
        "_source": [
            "<text_field>",
            "<timestamp>",
            "namespace",
            "is_correction",
            "public",
            "confidence"
        ]
    },
    "dest": {
        "index": ".kibana-observability-ai-assistant-kb-000001",
        "pipeline": ".kibana-observability-ai-assistant-kb-ingest-pipeline"
    },
    "script": {
        "inline": "ctx._source.text = ctx._source.remove(\"<text_field>\");ctx._source.namespace=\"<space>\";ctx._source.is_correction=false;ctx._source.public=<public>;ctx._source.confidence=\"high\";ctx._source['@timestamp'] = ctx._source.remove(\"<timestamp>\");ctx._source['user.name'] = \"<user.name>\""
    }
}
```


## Interact with the AI Assistant [observability-ai-assistant-interact-with-the-ai-assistant]

You can chat with the AI Assistant or interact with contextual insights located throughout {{obs-serverless}}. See the following sections for more on interacting with the AI Assistant.

::::{tip}
After every answer the LLM provides, let us know if the answer was helpful. Your feedback helps us improve the AI Assistant!

::::



### Chat with the assistant [observability-ai-assistant-chat-with-the-assistant]

Click the AI Assistant button (![AI Assistant icon](../../../images/serverless-ai-assistant-button.png "")) in the upper-right corner where available to start the chat.

This opens the AI Assistant flyout, where you can ask the assistant questions about your instance:

:::{image} ../../../images/serverless-ai-assistant-chat.png
:alt: Observability AI assistant chat
:class: screenshot
:::

::::{important}
Asking questions about your data requires function calling, which enables LLMs to reliably interact with third-party generative AI providers to perform searches or run advanced functions using customer data.

When the Observability AI Assistant performs searches in the cluster, the queries are run with the same level of permissions as the user.

::::



### Suggest functions [observability-ai-assistant-suggest-functions]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


The AI Assistant uses several functions to include relevant context in the chat conversation through text, data, and visual components. Both you and the AI Assistant can suggest functions. You can also edit the AI Assistant’s function suggestions and inspect function responses. For example, you could use the `kibana` function to call a {{kib}} API on your behalf.

You can suggest the following functions:

| Function | Description |
| --- | --- |
| `alerts` | Get alerts for {{obs-serverless}}. |
| `elasticsearch` | Call {{es}} APIs on your behalf. |
| `kibana` | Call {{kib}} APIs on your behalf. |
| `summarize` | Summarize parts of the conversation. |
| `visualize_query` | Visualize charts for ES |

Additional functions are available when your cluster has APM data:

| Function | Description |
| --- | --- |
| `get_apm_correlations` | Get field values that are more prominent in the foreground set than the background set. This can be useful in determining which attributes (such as `error.message`, `service.node.name`, or `transaction.name`) are contributing to, for instance, a higher latency. Another option is a time-based comparison, where you compare before and after a change point. |
| `get_apm_downstream_dependencies` | Get the downstream dependencies (services or uninstrumented backends) for a service. Map the downstream dependency name to a service by returning both `span.destination.service.resource` and `service.name`. Use this to drill down further if needed. |
| `get_apm_error_document` | Get a sample error document based on the grouping name. This also includes the stacktrace of the error, which might hint to the cause. |
| `get_apm_service_summary` | Get a summary of a single service, including the language, service version, deployments, the environments, and the infrastructure that it is running in. For example, the number of pods and a list of their downstream dependencies. It also returns active alerts and anomalies. |
| `get_apm_services_list` | Get the list of monitored services, their health statuses, and alerts. |
| `get_apm_timeseries` | Display different APM metrics (such as throughput, failure rate, or latency) for any service or all services and any or all of their dependencies. Displayed both as a time series and as a single statistic. Additionally, the function  returns any changes, such as spikes, step and trend changes, or dips. You can also use it to compare data by requesting two different time ranges, or, for example, two different service versions. |


### Use contextual prompts [observability-ai-assistant-use-contextual-prompts]

AI Assistant contextual prompts throughout {{obs-serverless}} provide the following information:

* **Alerts**: Provides possible causes and remediation suggestions for log rate changes.
* **Application performance monitoring (APM)**: Explains APM errors and provides remediation suggestions.
* **Logs**: Explains log messages and generates search patterns to find similar issues.

For example, in the log details, you’ll see prompts for **What’s this message?** and **How do I find similar log messages?**:

:::{image} ../../../images/serverless-ai-assistant-logs-prompts.png
:alt: Observability AI assistant example prompts for logs
:class: screenshot
:::

Clicking a prompt generates a message specific to that log entry. You can continue a conversation from a contextual prompt by clicking **Start chat** to open the AI Assistant chat.

:::{image} ../../../images/serverless-ai-assistant-logs.png
:alt: Observability AI assistant example
:class: screenshot
:::


### Add the AI Assistant connector to alerting workflows [observability-ai-assistant-add-the-ai-assistant-connector-to-alerting-workflows]

You can use the [Observability AI Assistant connector](kibana://reference/connectors-kibana/obs-ai-assistant-action-type.md) to add AI-generated insights and custom actions to your alerting workflows. To do this:

1. [Create (or edit) an alerting rule](../../../solutions/observability/incident-management/create-manage-rules.md) and specify the conditions that must be met for the alert to fire.
2. Under **Actions**, select the **Observability AI Assistant** connector type.
3. In the **Connector** list, select the AI connector you created when you set up the assistant.
4. In the **Message** field, specify the message to send to the assistant:

:::{image} ../../../images/serverless-obs-ai-assistant-action-high-cpu.png
:alt: Add an Observability AI assistant action while creating a rule in the Observability UI
:class: screenshot
:::

You can ask the assistant to generate a report of the alert that fired, recall any information or potential resolutions of past occurrences stored in the knowledge base, provide troubleshooting guidance and resolution steps, and also include other active alerts that may be related. As a last step, you can ask the assistant to trigger an action, such as sending the report (or any other message) to a Slack webhook.

::::{admonition} NOTE
:class: note

Currently you can only send messages to Slack, email, Jira, PagerDuty, or a webhook. Additional actions will be added in the future.

::::


When the alert fires, contextual details about the event—such as when the alert fired, the service or host impacted, and the threshold breached—are sent to the AI Assistant, along with the message provided during configuration. The AI Assistant runs the tasks requested in the message and creates a conversation you can use to chat with the assistant:

:::{image} ../../../images/serverless-obs-ai-assistant-output.png
:alt: AI Assistant conversation created in response to an alert
:class: screenshot
:::

::::{important}
Conversations created by the AI Assistant are public and accessible to every user with permissions to use the assistant.

::::


It might take a minute or two for the AI Assistant to process the message and create the conversation.

Note that overly broad prompts may result in the request exceeding token limits. For more information, refer to [Token limits](../../../explore-analyze/ai-assistant.md#token-limits). Also, attempting to analyze several alerts in a single connector execution may cause you to exceed the function call limit. If this happens, modify the message specified in the connector configuration to avoid exceeding limits.

When asked to send a message to another connector, such as Slack, the AI Assistant attempts to include a link to the generated conversation.

:::{image} ../../../images/serverless-obs-ai-assistant-slack-message.png
:alt: Message sent by Slack by the AI Assistant includes a link to the conversation
:class: screenshot
:::

The Observability AI Assistant connector is called when the alert fires and when it recovers.

To learn more about alerting, actions, and connectors, refer to [Alerting](../../../solutions/observability/incident-management/alerting.md).


## Elastic documentation for the AI Assistant [obs-ai-product-documentation]

It is possible to make the Elastic official documentation available to the AI Assistant, which significantly increases its efficiency and accuracy in answering questions related to the Elastic stack and Elastic products.

Enabling that feature can be done from the **Settings** tab of the AI Assistant Settings page, using the "Install Elastic Documentation" action.


## Known issues [observability-ai-assistant-known-issues]


### Token limits [token-limits]

Most LLMs have a set number of tokens they can manage in single a conversation. When you reach the token limit, the LLM will throw an error, and Elastic will display a "Token limit reached" error. The exact number of tokens that the LLM can support depends on the LLM provider and model you’re using. If you are using an OpenAI connector, you can monitor token usage in **OpenAI Token Usage** dashboard. For more information, refer to the [OpenAI Connector documentation](kibana://reference/connectors-kibana/openai-action-type.md#openai-connector-token-dashboard).
