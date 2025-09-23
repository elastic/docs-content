---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/assistant-connect-to-azure-openai.html
  - https://www.elastic.co/guide/en/serverless/current/security-connect-to-azure-openai.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to Azure OpenAI

This page provides step-by-step instructions for setting up an Azure OpenAI connector for the first time. This connector type enables you to leverage large language models (LLMs) within {{kib}}. You’ll first need to configure Azure, then configure the connector in {{kib}}.


## Configure Azure [_configure_azure]


### Configure a deployment [_configure_a_deployment]

First, set up an Azure OpenAI deployment:

1. Log in to the Azure console and search for Azure OpenAI.
2. In **Azure AI services**, select **Create**.
3. For the **Project Details**, select your subscription and resource group. If you don’t have a resource group, select **Create new** to make one.
4. For **Instance Details**, select the desired region and specify a name, such as `example-deployment-openai`.
5. Select the **Standard** pricing tier, then click **Next**.
6. Configure your network settings, click **Next**, optionally add tags, then click **Next**.
7. Review your deployment settings, then click **Create**. When complete, select **Go to resource**.

The following video demonstrates these steps (click to watch).

[![azure-openai-configure-deployment-video](https://play.vidyard.com/7NEa5VkVJ67RHWBuK8qMXA.jpg)](https://videos.elastic.co/watch/7NEa5VkVJ67RHWBuK8qMXA?)

### Configure keys [_configure_keys]

Next, create access keys for the deployment:

1. From within your Azure OpenAI deployment, select **Click here to manage keys**.
2. Store your keys in a secure location.

The following video demonstrates these steps (click to watch).

[![azure-openai-configure-keys-video](https://play.vidyard.com/cQXw96XjaeF4RiB3V4EyTT.jpg)](https://videos.elastic.co/watch/cQXw96XjaeF4RiB3V4EyTT?)


### Configure a model [_configure_a_model]

Now, set up the Azure OpenAI model:

1. From within your Azure OpenAI deployment, select **Model deployments**, then click **Manage deployments**.
2. On the **Deployments** page, select **Create new deployment**.
3. Under **Select a model**, choose `gpt-4o` or `gpt-4 turbo`.
4. Set the model version to "Auto-update to default".

   :::{important}
   The models available to you depend on [region availability](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability). For best results, use `GPT-4o 2024-05-13` with the maximum Tokens-Per-Minute (TPM) capacity. For more information on how different models perform for different tasks, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
   :::

5. Under **Deployment type**, select **Standard**.
6. Name your deployment.
7. Slide the **Tokens per Minute Rate Limit** to the maximum. The following example supports 80,000 TPM, but other regions might support higher limits.
8. Click **Create**.

The following video demonstrates these steps (click to watch).

[![azure-openai-configure-model-video](https://play.vidyard.com/PdadFyV1p1DbWRyCr95whT.jpg)](https://videos.elastic.co/watch/PdadFyV1p1DbWRyCr95whT?)



## Configure Elastic AI Assistant [_configure_elastic_ai_assistant]

Finally, configure the connector in {{kib}}:

1. Log in to {{kib}}.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **OpenAI**.
3. Give your connector a name to help you keep track of different models, such as `Azure OpenAI (GPT-4 Turbo v. 0125)`.
4. For **Select an OpenAI provider**, choose **Azure OpenAI**.
5. Update the **URL** field. We recommend doing the following:

    1. Navigate to your deployment in Azure AI Studio and select **Open in Playground**. The **Chat playground** screen displays.
    2. Select **View code**, then from the drop-down, change the **Sample code** to `Curl`.
    3. Highlight and copy the URL without the quotes, then paste it into the **URL** field in {{kib}}.
    4. (Optional) Alternatively, refer to the [API documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) to learn how to create the URL manually.

6. Under **API key**, enter one of your API keys.
7. Click **Save & test**, then click **Run**.

Your LLM connector is now configured. The following video demonstrates these steps (click to watch).

[![azure-openai-configure-model-video](https://play.vidyard.com/RQZVcnXHokC3RcV6ZB2pmF.jpg)](https://videos.elastic.co/watch/RQZVcnXHokC3RcV6ZB2pmF?)