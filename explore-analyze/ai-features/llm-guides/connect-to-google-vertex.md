---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/connect-to-vertex.html
  - https://www.elastic.co/guide/en/serverless/current/security-connect-to-google-vertex.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to Google Vertex

This page provides step-by-step instructions for setting up a Google Vertex AI connector for the first time. This connector type enables you to leverage Vertex AI’s large language models (LLMs) within {{elastic-sec}}. You’ll first need to enable Vertex AI, then generate a key, and finally configure the connector in your {{elastic-sec}} project.

::::{important}
Before continuing, you should have an active project in one of Google Vertex AI’s [supported regions](https://cloud.google.com/vertex-ai/docs/general/locations#feature-availability).
::::



## Enable the Vertex AI API [_enable_the_vertex_ai_api]

1. Log in to the GCP console and navigate to **Vertex AI → Vertex AI Studio → Overview**.
2. If you’re new to Vertex AI, the **Get started with Vertex AI Studio** popup appears. Click **Vertex AI API**, then click **ENABLE**.

The following video demonstrates these steps.

[![connect-vertex-api-video](https://play.vidyard.com/vFhtbiCZiKhvdZGy2FjyeT.jpg)](https://videos.elastic.co/watch/vFhtbiCZiKhvdZGy2FjyeT?)


::::{note}
For more information about enabling the Vertex AI API, refer to [Google’s documentation](https://cloud.google.com/vertex-ai/docs/start/cloud-environment).
::::



## Create a Vertex AI service account [_create_a_vertex_ai_service_account]

1. In the GCP console, navigate to **APIs & Services → Library**.
2. Search for **Vertex AI API**, select it, and click **MANAGE**.
3. In the left menu, navigate to **Credentials** then click **+ CREATE CREDENTIALS** and select **Service account**.
4. Name the new service account, then click **CREATE AND CONTINUE**.
5. Under **Select a role**, select **Vertex AI User**, then click **CONTINUE**.
6. Click **Done**.

The following video demonstrates these steps.

[![create-vertex-account-video](https://play.vidyard.com/tmresYYiags2w2nTv3Gac8.jpg)](https://videos.elastic.co/watch/tmresYYiags2w2nTv3Gac8?)


## Generate a key [_generate_an_api_key]

1. Return to Vertex AI’s **Credentials** menu and click **Manage service accounts**.
2. Search for the service account you just created, select it, then click the link that appears under **Email**.
3. Go to the **KEYS** tab, click **ADD KEY**, then select **Create new key**.
4. Select **JSON**, then click **CREATE** to download the key. Keep it somewhere secure.

The following video demonstrates these steps.

[![create-vertex-key-video](https://play.vidyard.com/hrcy3F9AodwhJcV1i2yqbG.jpg)](https://videos.elastic.co/watch/hrcy3F9AodwhJcV1i2yqbG?)



## Configure the Google Gemini connector [_configure_the_google_gemini_connector]

Finally, configure the connector in your Elastic deployment:

1. Log in to your Elastic deployment.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, select **Google Gemini**.
3. Name your connector to help keep track of the model version you are using.
4. Under **URL**, enter the URL for your region.
5. Enter your **GCP Region** and **GCP Project ID**.
6. Under **Default model**, specify either `gemini-1.5.pro` or `gemini-1.5-flash`. [Learn more about the models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models).
7. Under **Authentication**, enter your credentials JSON.
8. Click **Save**.

The following video demonstrates these steps.


[![configure-gemini-connector-video](https://play.vidyard.com/8L2WPm2HKN1cH872Gs5uvL.jpg)](https://videos.elastic.co/watch/8L2WPm2HKN1cH872Gs5uvL?)
