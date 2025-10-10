---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-pipeline-search-inference.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# {{infer-cap}} processing [ingest-pipeline-search-inference]

When you create an index through the **Content** UI, a set of default ingest pipelines are also created, including a {{ml}} {{infer}} pipeline. The [ML {{infer}} pipeline](/solutions/search/search-pipelines.md#ingest-pipeline-search-details-specific-ml-reference) uses {{infer}} processors to analyze fields and enrich documents with the output. Inference processors use ML trained models, so you need to use a built-in model or [deploy a trained model in your cluster](../nlp/ml-nlp-deploy-models.md) to use this feature.

This guide focuses on the ML {{infer}} pipeline, its use, and how to manage it.

::::{important}
This feature is not available at all Elastic subscription levels. Refer to the Elastic subscriptions pages for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [self-managed](https://www.elastic.co/subscriptions) deployments.

::::

## NLP use cases [ingest-pipeline-search-inference-nlp-use-cases]

[Natural Language Processing (NLP)](../nlp/ml-nlp-overview.md) enables developers to create rich search experiences that go beyond the standards of lexical search. A few examples of ways to improve search experiences through the use of NLP models:

### ELSER text expansion [ingest-pipeline-search-inference-elser]

Using Elastic’s [ELSER machine learning model](../nlp/ml-nlp-elser.md) you can easily incorporate text expansion for your queries. This works by using ELSER to provide semantic enrichments to your documents upon ingestion, combined with the power of [Elastic Search Application templates](../../../solutions/search/search-applications.md) to provide automated text expansion at query time.

### Named entity recognition (NER) [ingest-pipeline-search-inference-ner]

Most commonly used to detect entities such as People, Places, and Organization information from text, [NER](../nlp/ml-nlp-extract-info.md#ml-nlp-ner) can be used to extract key information from text and group results based on that information. A sports news media site could use NER to automatically extract names of professional athletes, stadiums, and sports teams in their articles and link to season stats or schedules.

### Text classification [ingest-pipeline-search-inference-text-classification]

[Text classification](../nlp/ml-nlp-classify-text.md#ml-nlp-text-classification) is commonly used for sentiment analysis and can be used for similar tasks, such as labeling content as containing hate speech in public forums, or triaging and labeling support tickets so they reach the correct level of escalation automatically.

### Text embedding [ingest-pipeline-search-inference-text-embedding]

Analyzing a text field using a [Text embedding](../nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding) model will generate a [dense vector](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) representation of the text. This array of numeric values encodes the semantic *meaning* of the text. Using the same model with a user’s search query will produce a vector that can then be used to search, ranking results based on vector similarity - semantic similarity - as opposed to traditional word or text similarity.

A common use case is a user searching FAQs, or a support agent searching a knowledge base, where semantically similar content may be indexed with little similarity in phrasing.

## NLP in the Content UI [ingest-pipeline-search-inference-nlp-in-enterprise-search]

### Overview of the ML {{infer}} pipeline [ingest-pipeline-search-inference-overview]

The diagram below shows how documents are processed during ingestion.

:::{image} /explore-analyze/images/elasticsearch-reference-document-enrichment-diagram.png
:alt: ML inference pipeline diagram
:::

* Documents are processed by the `my-index-0001` pipeline, which happens automatically when indexing through a an Elastic connector or crawler.
* The `_run_ml_inference` field is set to `true` to ensure the ML {{infer}} pipeline (`my-index-0001@ml-inference`) is executed. This field is removed during the ingestion process.
* The {{infer}} processor analyzes the `message` field on the document using the `my-positivity-model-id` trained model. The {{infer}} output is stored in the `ml.inference.positivity_prediction` field.
* The resulting enriched document is then indexed into the `my-index-0001` index.
* The `ml.inference.positivity_prediction` field can now be used at query time to search for documents above or below a certain threshold.

## Find, deploy, and manage trained models [ingest-pipeline-search-inference-find-deploy-manage-trained-models]

This feature is intended to make it easier to use your ML trained models. First, you need to figure out which model works best for your data. Make sure to use a [compatible third party NLP model](../nlp/ml-nlp-model-ref.md). Since these are publicly available, it is not possible to fine-tune models before [deploying them](../nlp/ml-nlp-deploy-models.md).

Trained models must be available in the current [Kibana Space](../../../deploy-manage/manage-spaces.md) and running in order to use them. By default, models should be available in all Kibana Spaces that have the **Analytics** > **Machine Learning** feature enabled. To manage your trained models, use the Kibana UI and navigate to **Stack Management → Machine Learning → Trained Models**. Spaces can be controlled in the **spaces** column. To stop or start a model, go to the **Machine Learning** tab in the **Analytics** menu of Kibana and click **Trained Models** in the **Model Management** section.

::::{note}
The `monitor_ml` [Elasticsearch cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md) is required to manage ML models and ML {{infer}} pipelines which use those models.

::::

### Add {{infer}} processors to your ML {{infer}} pipeline [ingest-pipeline-search-inference-add-inference-processors]

To create the index-specific ML {{infer}} pipeline, go to **Search → Content → Indices → <your index> → Pipelines** in the Kibana UI.

If you only see the `search-default-ingestion` pipeline, you will need to click **Copy and customize** to create index-specific pipelines. This will create the `{{index_name}}@ml-inference` pipeline.

Once your index-specific ML {{infer}} pipeline is ready, you can add {{infer}} processors that use your ML trained models. To add an {{infer}} processor to the ML {{infer}} pipeline, click the **Add Inference Pipeline** button in the **Machine Learning Inference Pipelines** card.

:::{image} /explore-analyze/images/elasticsearch-reference-document-enrichment-add-inference-pipeline.png
:alt: Add Inference Pipeline
:screenshot:
:::

Here, you’ll be able to:

1. Choose a name for your pipeline.

    * This name will need to be unique across the whole deployment. If you want this pipeline to be index-specific, we recommend including the name of your index in the pipeline name.
    * If you do not set the pipeline name, a default unique name will be provided upon selecting a trained model.

2. Select the ML trained model you want to use.

    * The model must be deployed before you can select it. To begin deployment of a model, click the **Deploy** button.

3. Select one or more source fields as input for the {{infer}} processor.

    * If there are no source fields available, your index will need a [field mapping](../../../manage-data/data-store/mapping.md).

4. (Optional) Choose a name for your target field(s). This is where the output of the {{infer}} model will be stored. Changing the default name is only possible if you have a single source field selected.
5. Add the source-target field mapping to the configuration by clicking the **Add** button.
6. Repeat steps 3-5 for each field mapping you want to add.
7. (Optional) Test the pipeline with a sample document.
8. (Optional) Review the pipeline definition before creating it with the **Create pipeline** button.

### Manage and delete {{infer}} processors from your ML {{infer}} pipeline [ingest-pipeline-search-inference-manage-inference-processors]

Inference processors added to your index-specific ML {{infer}} pipelines are normal Elasticsearch pipelines. Once created, each processor will have options to **View in Stack Management** and **Delete Pipeline**. Deleting an {{infer}} processor from within the **Content** UI deletes the pipeline and also removes its reference from your index-specific ML {{infer}} pipeline.

These pipelines can also be viewed, edited, and deleted in Kibana from the **Ingest Pipelines** management page, just like all other Elasticsearch ingest pipelines. You may also use the [Ingest pipeline APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ingest). If you delete any of these pipelines outside of the **Content** UI in Kibana, make sure to edit the ML {{infer}} pipelines that reference them.

## Test your ML {{infer}} pipeline [ingest-pipeline-search-inference-test-inference-pipeline]

You can verify the expected structure of the {{infer}} output before indexing any documents while creating the {{ml}} {{infer}} pipeline under the **Test** tab. Provide a sample document, click **Simulate**, and look for the `ml.inference` object in the results.

To ensure the ML {{infer}} pipeline will be run when ingesting documents, you must make sure the documents you are ingesting have a field named `_run_ml_inference` that is set to `true` and you must set the pipeline to `{{index_name}}`. For connector and crawler indices, this will happen automatically if you’ve configured the settings appropriately for the pipeline name `{{index_name}}`. To manage these settings:

1. Go to **Search > Content > Indices > <your index> > Pipelines**.
2. Click on the **Settings** link in the **Ingest Pipelines** card for the `{{index_name}}` pipeline.
3. Ensure **ML {{infer}} pipelines** is selected. If it is not, select it and save the changes.

## Learn More [ingest-pipeline-search-inference-learn-more]

* See [Overview](/solutions/search/search-pipelines.md#ingest-pipeline-search-in-enterprise-search) for information on the various pipelines that are created.
* Learn about [ELSER](../nlp/ml-nlp-elser.md), Elastic’s proprietary retrieval model for semantic search with sparse vectors.
* [NER HuggingFace Models](https://huggingface.co/models?library=pytorch&pipeline_tag=token-classification&sort=downloads)
* [Text Classification HuggingFace Models](https://huggingface.co/models?library=pytorch&pipeline_tag=text-classification&sort=downloads)
* [Text Embedding HuggingFace Models](https://huggingface.co/models?library=pytorch&pipeline_tag=sentence-similarity&sort=downloads)
