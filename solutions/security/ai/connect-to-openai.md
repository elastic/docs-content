---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/assistant-connect-to-openai.html
  - https://www.elastic.co/guide/en/serverless/current/security-connect-to-openai.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to OpenAI

This page provides step-by-step instructions for setting up an OpenAI connector for the first time. This connector type enables you to leverage OpenAI’s large language models (LLMs) within {{kib}}. You’ll first need to create an OpenAI API key, then configure the connector in {{kib}}.


## Configure OpenAI [_configure_openai]


### Select a model [_select_a_model]

Before creating an API key, you must choose a model. Refer to the [OpenAI docs](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4) to select a model. Take note of the specific model name (for example `gpt-4-turbo`); you’ll need it when configuring {{kib}}.

::::{note}
`GPT-4o` offers increased performance over previous versions. For more information on how different models perform for different tasks, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
::::



### Create an API key [_create_an_api_key]

To generate an API key:

1. Log in to the OpenAI platform and navigate to **API keys**.
2. Select **Create new secret key**.
3. Name your key, select an OpenAI project, and set the desired permissions.
4. Click **Create secret key** and then copy and securely store the key. It will not be accessible after you leave this screen.

The following video demonstrates these steps (click to watch).

[![openai-apikey-video](https://play.vidyard.com/vbD7fGBGgyxK4TRbipeacL.jpg)](https://videos.elastic.co/watch/vbD7fGBGgyxK4TRbipeacL?)


## Configure the OpenAI connector [_configure_the_openai_connector]

To integrate with {{kib}}:

1. Log in to {{kib}}.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **OpenAI**.
3. Provide a name for your connector, such as `OpenAI (GPT-4 Turbo Preview)`, to help keep track of the model and version you are using.
4. Under **Select an OpenAI provider**, choose **OpenAI**.
5. The **URL** field can be left as default.
6. Under **Default model**, specify which [model](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4) you want to use.
7. Paste the API key that you created into the corresponding field.
8. Click **Save**.

The following video demonstrates these steps (click to watch).

[![openai-configure-connector-video](https://play.vidyard.com/BGaQ73KBJCzeqWoxXkQvy9.jpg)](https://videos.elastic.co/watch/BGaQ73KBJCzeqWoxXkQvy9?)