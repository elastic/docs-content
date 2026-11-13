---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Use Elastic Inference Service (EIS) to run inference for search, embeddings, and chat without deploying models in your environment.
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your environment.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

{applies_to}`stack: ga 9.3` You can use EIS with your [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md), [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), or [self-managed](/deploy-manage/deploy/self-managed.md) cluster through Cloud Connect. For details, refer to [](connect-self-managed-cluster-to-eis.md).

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with [Elastic Managed LLMs](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm) by default. These can be used in Agent Builder, the AI Assistant, Attack Discovery, and Automatic Import. For the list of available models, refer to [Supported models](/explore-analyze/elastic-inference/eis-supported-models.md).

* Search Playground also uses Elastic Managed LLMs. {applies_to}`stack: preview =9.0, beta 9.1-9.3, deprecated 9.4-9.5, removed 9.6+` {applies_to}`serverless: unavailable`

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview =9.1, ga 9.2+` {applies_to}`serverless: ga`

* You can use the [`jina-embeddings-v3`](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-text-embeddings) multilingual dense vector embedding model to perform semantic search through the Elastic {{infer-cap}} Service. {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`

## Manage your models [manage-models]

{{kib}} provides interfaces for managing EIS models and endpoints.

:::::{applies-switch}
::::{applies-item} { stack: ga 9.4+, serverless: ga }
Go to the **Elastic inference** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/eis-ui.png
:alt: Elastic Inference UI
:screenshot:
:::

:::{tip}
To access **Elastic {{infer}}**, you need the `Inference Endpoints: all` and `Advanced Settings: read` {{kib}} privileges.
:::
::::
::::{applies-item} stack: ga 9.0-9.3
Go to the **{{infer-cap}} endpoints** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:screenshot:
:::
::::
:::::

Available actions include:

- Add endpoints
- View endpoint details
- Copy the inference endpoint ID
- Delete endpoints
- {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` [Region preferences](eis-region-and-hosting.md#inference-region-preferences) for where EIS processes {{infer}} requests
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` [Show or hide models](#eis-display-options) that are in preview, past end of life, or outside your region preferences
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Find models available in specific geographies or regions with the **Region** filter on the toolbar. The filter doesn't change where EIS processes {{infer}} requests, which [region preferences](eis-region-and-hosting.md#inference-region-preferences) control. Models that are [hidden by default](#eis-display-options) stay hidden unless you show them.

:::{tip}
:applies_to: { serverless: ga, stack: ga 9.6+ }
To find a model faster, filter the list by region, sort the model cards by name or release date, or [show models that are hidden by default](#eis-display-options).
:::

### Show models that are hidden by default [eis-display-options]

```{applies_to}
serverless: ga
stack: ga 9.6+
```

If a model you expect is missing from the list, it might be hidden. By default, {{kib}} leaves out three groups of models:

- **Models outside your region preferences**: Models that you can't use until you update your [region preferences](eis-region-and-hosting.md#inference-region-preferences). If you can edit region preferences, open the model's details, expand the banner with **View details**, and select **Edit Region preferences**.
- **End-of-life models**: Models that have already reached their end-of-life date, which you can't use. Models that are close to that date stay in the list.
- **Preview models**: Models in preview, which aren't recommended for production use.

To show or hide any of these groups:

1. On the toolbar, select {icon}`controls` **Display options**.
1. In **Model display options**, set each group to **Show** or **Hide**.
1. Select **Apply**.

The list now includes the groups you set to **Show**. In card view, {{kib}} shows how many models match, for example **Showing 12 of 20**. The second number also counts hidden models, so a lower first number doesn't always mean that your search or filters removed a model.

{{kib}} doesn't save your selection. After you reload {{kib}}, all three groups are hidden again.

## Add endpoints [add-endpoint]

Your deployment includes default {{infer}} endpoints which are preconfigured and ready to use.
In most cases, you should use these default endpoints.
However, you can choose to create custom EIS endpoints if you need to instantiate a specific model version or configuration that is not covered by the defaults.

:::::{applies-switch}
::::{applies-item} { stack: ga 9.4+, serverless: ga }

1. Go to the **Elastic inference** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the model you want the new endpoint to use.
1. Click **Add endpoint**.
1. Enter a unique **Model ID**. For a complete list of valid Model IDs and their corresponding task types, refer to the [Supported models](/explore-analyze/elastic-inference/eis-supported-models.md).
1. Select **Save**.
::::
::::{applies-item} stack: ga 9.0-9.3
1. Go to the **{{infer-cap}} endpoints** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Service** dropdown, select **Elastic Inference Service**.
1. In the **Settings** section, enter the specific **Model ID**. For a complete list of valid Model IDs and their corresponding task types, refer to the [Elastic {{infer-cap}} Service supported models](/explore-analyze/elastic-inference/eis-supported-models.md).
1. (Optional) Under **More options**, set the **Maximum Input Tokens**. This limits the number of tokens processed per request. If left blank, the model's default limit is used.
1. Expand **Additional settings** and select the **Task type** that corresponds to your model.
1. Select **Save**.
::::
:::::

Alternatively, you can use [{{infer}} APIs]({{es-apis}}group/endpoint-inference), as described in the following section.

## Get started with models on EIS

The following sections describe how to get started with specific models available through Elastic {{infer-cap}} Service, including creating {{infer}} endpoints and using them for search and ingest.

### Jina v5 omni embedding models [jina-embeddings-v5-omni]

```{applies_to}
stack: ga 9.3+
serverless: ga
```

::::{important}
The Jina v5 omni models availability and the support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type depend on your {{stack}} version:

- {applies_to}`stack: ga 9.3+` In {{stack}} 9.3 and later, you can create endpoints and run multimodal `embedding` {{infer}} requests. You cannot use these models with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type.
- {applies_to}`stack: ga 9.4+` In {{stack}} 9.4 and later, you can use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) mappings for text-only embeddings at ingest and search time.
- {applies_to}`stack: ga 9.5+` In {{stack}} 9.5 and later, the `semantic` field type supports all modalities, such as text, images, video, audio, and documents.
::::

There are two Jina v5 omni embedding models available through Elastic {{infer-cap}} Service, [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small-on-eis) and [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano-on-eis). Both models support multimodal embeddings for text, images, video, audio, and documents such as PDF in one shared vector space.

- Use [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small-on-eis) for larger context windows and higher-capacity retrieval workloads. 
- Use [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano-on-eis) for lower cost and lower resource usage.

#### `jina-embeddings-v5-omni-small` on EIS [jina-embeddings-v5-omni-small-on-eis]

Create an {{infer}} endpoint that references the `jina-embeddings-v5-omni-small` model in the `model_id` field. Use the `embedding` task type so the endpoint can accept multimodal input.

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-small"
  }
}
```

You can reference the `inference_id` in `embedding` {{infer}} tasks and search queries on any supported version. 

For examples of ingesting different media types and generating embeddings for text, images, audio, and video, refer to [Getting started with Jina v5 omni embedding models through Elastic {{infer-cap}} Service](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started). Select the jina-embeddings-v5-omni-small tab in each example.

#### `jina-embeddings-v5-omni-nano` on EIS [jina-embeddings-v5-omni-nano-on-eis]

Create an {{infer}} endpoint that references the `jina-embeddings-v5-omni-nano` model in the `model_id` field. Use the `embedding` task type so the endpoint can accept multimodal input.

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-nano"
  }
}
```

You can reference the `inference_id` in `embedding` {{infer}} tasks and search queries on any supported version. 

For examples of ingesting different media types and generating embeddings for text, images, audio, and video, refer to [Getting started with Jina v5 omni embedding models through Elastic {{infer-cap}} Service](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started). Select the jina-embeddings-v5-omni-nano tab in each example.

### `jina-embeddings-v5-text-small` on EIS [jina-embeddings-v5-on-eis]

```{applies_to}
stack: preview 9.4
serverless: preview
```

You can use the `jina-embeddings-v5-text-small` model through Elastic {{infer-cap}} Service. Running the model on EIS means that you use the model on GPUs, without the need of managing infrastructure and model resources.

#### Get started with `jina-embeddings-v5-text-small` on EIS

Create an {{infer}} endpoint that references the `jina-embeddings-v5-text-small` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-embeddings-v5-text-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-text-small"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on the Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, `text_embedding` {{infer}} tasks, or search queries.

### `jina-embeddings-v3` on EIS [jina-embeddings-on-eis]

```{applies_to}
stack: preview 9.3
serverless: preview
```

You can use the `jina-embeddings-v3` model through Elastic {{infer-cap}} Service. Running the model on EIS means that you use the model on GPUs, without the need of managing infrastructure and model resources.

#### Get started with `jina-embeddings-v3` on EIS

Create an {{infer}} endpoint that references the `jina-embeddings-v3` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-embeddings-v3
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v3"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on the Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, text_embedding {{infer}} tasks, or search queries.

### Document extraction with Jina Reader on EIS [document-extraction-on-eis]

```{applies_to}
stack: preview 9.6
serverless: preview
```

The `document_extraction` task type converts PDFs, images, and web pages into Markdown. On EIS, the `jina-reader` model runs document extraction with [Jina Reader](https://jina.ai/reader/). Use it to prepare documents for indexing and retrieval-augmented generation (RAG).

Document extraction returns Markdown but doesn't index it. To make the extracted content searchable, index it yourself. Refer to [](#document-extraction-index).

#### Extract content from documents [document-extraction-run]

Use the preconfigured `.jina-reader` endpoint to extract content without creating an endpoint first. It handles every supported document type, so one endpoint covers PDFs, images, and web pages.

Send one or more documents in the `input` array. Each item has a `content` object with the following fields:

`type`
:   The document type. Supported values are `pdf`, `image`, and `html`.

`format`
:   How you provide the document. Use `url` to pass a link that Jina Reader fetches, or `base64` to pass the document as a base64-encoded data URL. The `html` type supports `url` only. Defaults to `base64` for `pdf` and `image`, and `url` for `html`.

`value`
:   The URL or the base64-encoded data URL.

The following example extracts a PDF from a URL:

```console
POST _inference/document_extraction/.jina-reader
{
  "input": [
    {
      "content": {
        "type": "pdf", <1>
        "format": "url", <2>
        "value": "https://example.com/annual-report.pdf" <3>
      }
    }
  ]
}
```

1. The document type: `pdf`, `image`, or `html`.
2. With `url`, Jina Reader downloads the document directly.
3. The document's URL. Jina Reader must be able to reach it.

The following example extracts a PDF from a base64-encoded data URL:

```console
POST _inference/document_extraction/.jina-reader
{
  "input": [
    {
      "content": {
        "type": "pdf",
        "format": "base64", <1>
        "value": "data:application/pdf;base64,JVBERi0xLjQK..." <2>
      }
    }
  ]
}
```

1. With `base64`, you send the document in the request body. Use this for files that aren't available at a URL.
2. A data URL: `data:`, the document's media type, `;base64,`, and then the base64-encoded file.

The response contains one result for each document, in the same order as the `input` array:

```console-result
{
  "document_extraction": [
    {
      "content": "# Annual Report 2025\n\nRevenue grew by 12% year over year...", <1>
      "format": "markdown" <2>
    }
  ]
}
```

1. The extracted content. Index this value to make the document searchable.
2. The format of `content`. It's always `markdown`.

A result can also include a `metadata` object. Its fields can change, so don't rely on them in your application.

There's no limit on the number of documents in a request. The request size is limited by the [`http.max_content_length`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) setting, which defaults to 100 MB. Base64 encoding adds overhead, so the largest base64-encoded PDF you can send is about 75 MB.

#### Default extraction behavior [document-extraction-defaults]

Each document type uses a different extraction method by default:

- PDFs: Converts the PDF's text layer to Markdown. Scanned PDFs have no text layer, so use OCR to extract their content. Refer to [](#document-extraction-parameters).
- Images: Extracts text with optical character recognition (OCR).
- Web pages: Converts the page content to Markdown.

#### Change how documents are extracted [document-extraction-parameters]

Use the `parameters` task setting to pass [Jina Reader options](https://r.jina.ai/docs) to Jina Reader. Options you set are combined with the defaults, and setting `preset` replaces the default extraction method. The `output_format` task setting supports `markdown` only.

Use the `preset` option to choose how Jina Reader extracts content. For example:

- `ocr`: Extracts text with the `jina-ocr-v1` OCR model. Use it for scanned PDFs.
- `pdf+`: Reads the PDF's text layer, adds support for images in the PDF, and uses `jina-ocr-v1` for tables, formulas, and pages without text. Use it for PDFs with tables or formulas, or with a mix of text and scanned pages.

OCR and layout presets extract pages 1 to 35 by default. A request extracts at most 35 pages, so use the `page` option to choose which pages to extract.

The following example extracts the first three pages of a PDF with the `pdf+` preset:

```console
POST _inference/document_extraction/.jina-reader
{
  "input": [
    {
      "content": {
        "type": "pdf",
        "format": "url",
        "value": "https://example.com/research-paper.pdf"
      }
    }
  ],
  "task_settings": {
    "parameters": { <1>
      "preset": "pdf+", <2>
      "page": "1-3" <3>
    }
  }
}
```

1. Jina Reader options for this request only. Each option here overrides the same option in the endpoint's `parameters`.
2. Reads the PDF's text layer and uses OCR for tables, formulas, and pages without text.
3. The pages to extract.

#### Create a document extraction endpoint [document-extraction-create-endpoint]

To apply the same `parameters` to every request, create your own {{infer}} endpoint and set them in `task_settings`:

```console
PUT _inference/document_extraction/my-jina-reader
{
  "service": "elastic", <1>
  "service_settings": {
    "model_id": "jina-reader" <2>
  },
  "task_settings": {
    "parameters": {
      "preset": "pdf+" <3>
    }
  }
}
```

1. The `elastic` service runs the endpoint on EIS.
2. The Jina Reader model.
3. Every request to this endpoint uses the `pdf+` preset, unless the request sets its own `preset`.

#### Index the extracted content [document-extraction-index]

Your application sends each document to the extraction endpoint and then indexes the `content` value from the response. To search the content semantically, index it into a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field:

1. Create an index with a `semantic_text` field for the extracted content:

    ```console
    PUT annual-reports
    {
      "mappings": {
        "properties": {
          "source_url": { "type": "keyword" }, <1>
          "content": { "type": "semantic_text" } <2>
        }
      }
    }
    ```

    1. The URL of the original document, so search results can link back to it.
    2. Splits the content into chunks and generates embeddings for them when you index a document.

2. Extract the content from the document, as shown in [](#document-extraction-run).
3. Index the `content` value from the response:

    ```console
    POST annual-reports/_doc
    {
      "source_url": "https://example.com/annual-report.pdf",
      "content": "# Annual Report 2025\n\nRevenue grew by 12% year over year..."
    }
    ```

### ELSER through Elastic {{infer-cap}} Service (ELSER on EIS) [elser-on-eis]

```{applies_to}
stack: preview =9.1, ga 9.2+
serverless: ga
```

ELSER on EIS enables you to use the ELSER model on GPUs, without having to manage your own ML nodes. We expect better performance for ingest throughput than ML nodes and equivalent performance for search latency. We will continue to benchmark, remove limitations and address concerns.

#### Using the ELSER on EIS endpoint

You can now use `semantic_text` with the new ELSER endpoint on EIS. To learn how to use the `.elser-2-elastic` inference endpoint, refer to [Using ELSER on EIS](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#using-elser-on-eis).

##### Get started with semantic search with ELSER on EIS

[Semantic Search with `semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) has a detailed tutorial on using the `semantic_text` field and using the ELSER endpoint on EIS instead of the default endpoint. This is a great way to get started and try the new endpoint.

:::{note}
If you ran a kNN search and it failed or returned no results, [check whether your vectors are searchable and compatible with kNN search](/solutions/search/vector/knn/troubleshoot-knn-search.md).
:::

## Pricing [pricing]

All models on EIS incur a charge per million tokens. Certain LLM providers charge different prices depending on the prompt size. The pricing details are available on our [Pricing page](https://cloud.elastic.co/cloud-pricing-table?productType=serverless).

This pricing model differs from the existing [Machine Learning Nodes](https://www.elastic.co/docs/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models), which is billed through VCUs consumed.

### Token-based billing

EIS is billed per million tokens used:

* For **chat** models, input and output tokens are billed. Longer conversations with extensive context or detailed responses will consume more tokens.
* For **embeddings** models, only input tokens are billed.

Tokens are the fundamental units that language models process for both input and output. Tokenizers convert text into numerical data by segmenting it into subword units. A token can be a complete word, part of a word, or a punctuation mark, depending on the model's trained tokenizer and the frequency patterns in its training data.

For example, the sentence `It was the best of times, it was the worst of times.` contains 52 characters but would tokenize into approximately 14 tokens with a typical word-based approach, though the exact count varies by tokenizer.

### Monitor your token usage [monitor-your-token-usage]

To track your token consumption:

1. Navigate to [**Billing > Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} Console.
2. Look for line items where the **Billing dimension** is set to "Inference".

## Service status [eis-service-status]

Elastic {{infer-cap}} Service (EIS) is a global service on {{ecloud}}. Like any service, it might undergo availability changes from time to time. When availability changes, Elastic posts updates on the [Cloud Status](https://status.elastic.co/) page.

EIS incidents and maintenance affect features that rely on EIS, such as semantic search, embeddings, reranking, and AI-powered assistants.

To check current and past EIS availability, go to the [Cloud Status](https://status.elastic.co/) page. EIS is listed under **Global services** as **Elastic {{infer-cap}} Service**.

:::{image} /explore-analyze/images/eis-status.png
:alt: Elastic Inference Service status on the Cloud Status page
:screenshot:
:::

Learn how to [subscribe to updates](/deploy-manage/cloud-organization/service-status.md#ec_subscribe_to_updates) on the Service status page.
