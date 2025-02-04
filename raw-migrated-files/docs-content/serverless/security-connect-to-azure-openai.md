# Connect to Azure OpenAI [security-connect-to-azure-openai]

This page provides step-by-step instructions for setting up an Azure OpenAI connector for the first time. This connector type enables you to leverage large language models (LLMs) within {{kib}}. You’ll first need to configure Azure, then configure the connector in {{kib}}.


## Configure Azure [security-connect-to-azure-openai-configure-azure]


### Configure a deployment [security-connect-to-azure-openai-configure-a-deployment]

First, set up an Azure OpenAI deployment:

1. Log in to the Azure console and search for Azure OpenAI.
2. In **Azure AI services**, select **Create**.
3. For the **Project Details**, select your subscription and resource group. If you don’t have a resource group, select **Create new** to make one.
4. For **Instance Details**, select the desired region and specify a name, such as `example-deployment-openai`.
5. Select the **Standard** pricing tier, then click **Next**.
6. Configure your network settings, click **Next**, optionally add tags, then click **Next**.
7. Review your deployment settings, then click **Create**. When complete, select **Go to resource**.

The following video demonstrates these steps.

 <iframe
  src="https://drive.google.com/file/d/16qq8Rfd1O-LRJkXTwRJemjOJjxSgl44L/preview?usp=sharing"
  width="100%"
  height="100%"
  style="border:none"
></iframe>

### Configure keys [security-connect-to-azure-openai-configure-keys]

Next, create access keys for the deployment:

1. From within your Azure OpenAI deployment, select **Click here to manage keys**.
2. Store your keys in a secure location.

The following video demonstrates these steps.

 <iframe
  src="https://drive.google.com/file/d/1u5nf9bVCc9Jbe9A4jVk6V0c8LX6hJmM0/preview?usp=sharing"
  width="100%"
  height="100%"
  style="border:none"
></iframe>

### Configure a model [security-connect-to-azure-openai-configure-a-model]

Now, set up the Azure OpenAI model:

1. From within your Azure OpenAI deployment, select **Model deployments**, then click **Manage deployments**.
2. On the **Deployments** page, select **Create new deployment**.
3. Under **Select a model**, choose `gpt-4o` or `gpt-4 turbo`.
4. Set the model version to "Auto-update to default".
5. Under **Deployment type**, select **Standard**.
6. Name your deployment.
7. Slide the **Tokens per Minute Rate Limit** to the maximum. The following example supports 80,000 TPM, but other regions might support higher limits.
8. Click **Create**.

::::{important}
The models available to you will depend on [region availability](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability). For best results, use `GPT-4o 2024-05-13` with the maximum Tokens-Per-Minute (TPM) capacity. For more information on how different models perform for different tasks, refer to the [LLM performance matrix](../../../solutions/security/ai/large-language-model-performance-matrix.md).

::::


The following video demonstrates these steps.

 <iframe
  src="https://drive.google.com/file/d/1cjBettKhrs2I9kVceExdZNlkHyIDXp7P/preview?usp=sharing"
  width="100%"
  height="100%"
  style="border:none"
></iframe>

## Configure Elastic AI Assistant [security-connect-to-azure-openai-configure-elastic-ai-assistant]

Finally, configure the connector in {{kib}}:

1. Log in to {{kib}}.
2. Find **Connectors** in the navigation menu or use the global search field. Then click **Create Connector**, and select **OpenAI**.
3. Give your connector a name to help you keep track of different models, such as `Azure OpenAI (GPT-4 Turbo v. 0125)`.
4. For **Select an OpenAI provider**, choose **Azure OpenAI**.
5. Update the **URL** field. We recommend doing the following:

    * Navigate to your deployment in Azure AI Studio and select **Open in Playground**. The **Chat playground** screen displays.
    * Select **View code**, then from the drop-down, change the **Sample code** to `Curl`.
    * Highlight and copy the URL without the quotes, then paste it into the **URL** field in {{kib}}.
    * (Optional) Alternatively, refer to the [API documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) to learn how to create the URL manually.

6. Under **API key**, enter one of your API keys.
7. Click **Save & test**, then click **Run**.

The following video demonstrates these steps.

 <iframe
  src="https://drive.google.com/file/d/1T5gzfUyaV2Wu2vYhSHxU4I6yCekim51K/preview?usp=sharing"
  width="100%"
  height="100%"
  style="border:none"
></iframe>
