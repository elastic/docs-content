---
navigation_title: Playground
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-playground.html
  - https://www.elastic.co/guide/en/kibana/current/playground.html
applies_to:
  stack: preview 9.0, beta 9.1
  serverless: beta
products:
  - id: cloud-serverless
  - id: kibana
---

# Playground for RAG [playground]

Use Playground to combine your Elasticsearch data with the power of large language models (LLMs) for retrieval augmented generation (RAG). The chat interface translates your natural language questions into {{es}} queries, retrieves the most relevant results from your {{es}} documents, and passes those documents to the LLM to generate tailored responses.

Once you start chatting, use the UI to view and modify the Elasticsearch queries that search your data. You can also view the underlying Python code that powers the chat interface, and download this code to integrate into your own application.

Learn how to get started on this page. Refer to the following for more advanced topics:

* [Optimize model context](playground-context.md)
* [View and modify queries](playground-query.md)
* [Troubleshooting](playground-troubleshooting.md)

::::{admonition} 🍿 Getting started videos
Watch these video tutorials to help you get started:

* [Getting Started](https://www.youtube.com/watch?v=zTHgJ3rhe10)
* [Using Playground with local LLMs](https://www.youtube.com/watch?v=ZtxoASFvkno)

::::

## How Playground works [playground-how-it-works]

Here’s a simpified overview of how Playground works:

* User **creates a connection** to LLM provider
* User **selects a model** to use for generating responses
* User **defines the model’s behavior and tone** with initial instructions

    * **Example**: "*You are a friendly assistant for question-answering tasks. Keep responses as clear and concise as possible.*"

* User **selects {{es}} indices** to search
* User **enters a question** in the chat interface
* Playground **autogenerates an {{es}} query** to retrieve relevant documents

    * User can **view and modify underlying {{es}} query** in the UI

* Playground **auto-selects relevant fields** from retrieved documents to pass to the LLM

    * User can **edit fields targeted**

* Playground passes **filtered documents** to the LLM

    * The LLM generates a response based on the original query, initial instructions, chat history, and {{es}} context

* User can **view the Python code** that powers the chat interface

    * User can also **Download the code** to integrate into application

## Availability and prerequisites [playground-availability-prerequisites]

For Elastic Cloud and self-managed deployments, select **Playground** from the left navigation menu.

For Elastic Serverless, Playground is available in your {{es}} project UI.

To use Playground, you’ll need the following:

1. An Elastic **v8.14.0+** deployment or {{es}} **Serverless** project. (Start a [free trial](https://cloud.elastic.co/registration)).
2. At least one **{{es}} index** with documents to search.

    * See [ingest data](playground.md#playground-getting-started-ingest) if you’d like to ingest sample data.

3. An account with a **supported LLM provider**. Playground supports the following:

    * **Elastic**
        * [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md)

    * **Amazon Bedrock**

        * Anthropic: Claude 3.5 Sonnet
        * Anthropic: Claude 3 Haiku

    * **OpenAI**

        * GPT-3 turbo
        * GPT-4 turbo
        * GPT-4 omni

    * **Azure OpenAI** (note: Buffers responses in large chunks)

        * GPT-3 turbo
        * GPT-4 turbo

    * **Google**

        * Google Gemini 2.5 Pro

::::{tip}
:name: playground-local-llms

You can also use locally hosted LLMs that are compatible with the OpenAI SDK. Once you’ve set up your LLM, you can connect to it using the OpenAI connector. Refer to the following for examples:

* [Using LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-observability.md)
* [LocalAI with `docker-compose`](https://www.elastic.co/search-labs/blog/localai-for-text-embeddings)

::::

## Getting started [playground-getting-started]

:::{image} /solutions/images/kibana-get-started.png
:alt: get started
:screenshot:
:::

### Connect to LLM provider [playground-getting-started-connect]

To get started with Playground, you need to create a [connector](../../../deploy-manage/manage-connectors.md) for your LLM provider. By default, an Elastic Managed LLM is connected. You can also connect to [locally hosted LLMs](playground.md#playground-local-llms) which are compatible with the OpenAI API, by using the OpenAI connector.

To connect to an LLM provider, use the following steps on the Playground landing page:

1. Select **New Playground**. Select the {icon}`wrench` button in the **Large Language Model (LLM)** tile to connect an LLM.
2. Select your **LLM provider**.
3. **Name** your connector.
4. Select a **URL endpoint** (or use the default).
5. Enter **access credentials** for your LLM provider. (If you’re running a locally hosted LLM using the OpenAI connector, you must input a value in the API key form, but the specific value doesn’t matter.)

::::{tip}
If you need to update a connector, or add a new one, click the 🔧 **Manage** button beside **Model settings**.

::::



### Ingest data (optional) [playground-getting-started-ingest]

*You can skip this step if you already have data in one or more {{es}} indices.*

There are many options for ingesting data into {{es}}, including:

* The [Elastic crawler](https://www.elastic.co/guide/en/enterprise-search/current/crawler.html) for web content (**NOTE**: Not yet available in *Serverless*)
* [Elastic connectors](elasticsearch://reference/search-connectors/index.md) for data synced from third-party sources
* The {{es}} [Bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) for JSON documents

    ::::{dropdown} Expand for example
    To add a few documents to an index called `books` run the following in Dev Tools Console:

    ```console
    POST /_bulk
    { "index" : { "_index" : "books" } }
    {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470}
    { "index" : { "_index" : "books" } }
    {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585}
    { "index" : { "_index" : "books" } }
    {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328}
    { "index" : { "_index" : "books" } }
    {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227}
    { "index" : { "_index" : "books" } }
    {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268}
    { "index" : { "_index" : "books" } }
    {"name": "The Handmaids Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311}
    ```

    ::::


We’ve also provided some Jupyter notebooks to easily ingest sample data into {{es}}. Find these in the [elasticsearch-labs](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/ingestion-and-chunking) repository. These notebooks use the official {{es}} Python client.


### Select {{es}} indices [playground-getting-started-index]

::::{note}
Playground does not support [data stream](/manage-data/data-store/data-streams.md) indices.
::::

Once you’ve connected to your LLM provider, it’s time to choose the data you want to search.

1. Select **Add data sources**.
2. Select one or more {{es}} indices.
3. Click **Save and continue** to launch the chat interface.

:::::{tip}
You can always add or remove indices later by selecting the **Data** button from the main Playground UI.

:::{image} /solutions/images/kibana-data-button.png
:alt: data button
:screenshot:
:width: 150px
:::

:::::



### Chat and query modes [playground-getting-started-chat-query-modes]

Since 8.15.0 (and earlier for {{es}} Serverless), the main Playground UI has two modes:

* **Chat mode**: The default mode, where you can chat with your data via the LLM.
* **Query mode**: View and modify the {{es}} query generated by the chat interface.

The **chat mode** is selected when you first set up your Playground instance.

:::{image} /solutions/images/kibana-chat-interface.png
:alt: chat interface
:screenshot:
:::

To switch to **query mode**, select **Query** from the main UI.

:::{image} /solutions/images/kibana-query-interface.png
:alt: query interface
:screenshot:
:::

::::{tip}
Learn more about the underlying {{es}} queries used to search your data in [View and modify queries](playground-query.md)

::::



### Set up the chat interface [playground-getting-started-setup-chat]

You can start chatting with your data immediately, but you might want to tweak some defaults first.

You can adjust the following under **LLM settings**:

* **AI Connector**. The model used for generating responses.
* **Instructions**. Also known as the *system prompt*, these initial instructions and guidelines define the behavior of the model throughout the conversation. Be **clear and specific** for best results.
* **Include citations**. A toggle to include citations from the relevant {{es}} documents in responses.

Playground also uses another LLM under the hood, to encode all previous questions and responses, and make them available to the main model. This ensures the model has "conversational memory".

Under **Indices**, you can edit which {{es}} indices will be searched. This will affect the underlying {{es}} query.

::::{tip}
Click **✨ Regenerate** to resend the last query to the model for a fresh response.

Click **⟳ Clear chat** to clear chat history and start a new conversation.

::::

### View and download Python code [playground-getting-started-view-code]

Select {icon}`export` to see the Python code that powers the chat interface. You can integrate it into your own application, modifying as needed. We currently support two implementation options:

* {{es}} Python Client + LLM provider
* LangChain + LLM provider

### Next steps [playground-next-steps]

Once you’ve got Playground up and running, and you’ve tested out the chat interface, you might want to explore some more advanced topics:

* [Optimize model context](playground-context.md)
* [View and modify queries](playground-query.md)
* [Troubleshooting](playground-troubleshooting.md)




