---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-inference.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Add NLP inference to ingest pipelines [ml-nlp-inference]

After you [deploy a trained model in your cluster](ml-nlp-deploy-models.md), you can use it to perform {{nlp}} tasks in ingest pipelines.

1. Verify that all of the [ingest pipeline prerequisites](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md#ingest-prerequisites) are met.
2. [Add an {{infer}} processor to an ingest pipeline](#ml-nlp-inference-processor).
3. [Ingest documents](#ml-nlp-inference-ingest-docs).
4. [View the results](#ml-nlp-inference-discover).

## Add an {{infer}} processor to an ingest pipeline [ml-nlp-inference-processor]

In {{kib}}, you can create and edit pipelines from the **Ingest Pipelines** management page. You can find this page in the main menu or using the [global search field](../../find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/machine-learning-ml-nlp-pipeline-lang.png
:alt: Creating a pipeline
:screenshot:
:::

1. Click **Create pipeline** or edit an existing pipeline.
2. Add an [{{infer}} processor](elasticsearch://reference/enrich-processor/inference-processor.md) to your pipeline:

    1. Click **Add a processor** and select the **{{infer-cap}}** processor type.
    2. Set **Model ID** to the name of your trained model, for example `elastic__distilbert-base-cased-finetuned-conll03-english` or `lang_ident_model_1`.
    3. If you use the {{lang-ident}} model (`lang_ident_model_1`) that is provided in your cluster:

        1. The input field name is assumed to be `text`. If you want to identify languages in a field with a different name, you must map your field name to `text` in the **Field map** section. For example:

            ```js
            {
              "message": "text"
            }
            ```

        2. You can also optionally add [classification configuration options](elasticsearch://reference/enrich-processor/inference-processor.md#inference-processor-classification-opt) in the **{{infer-cap}} configuration** section. For example, to include the top five language predictions:

            ```js
            {
              "classification":{
                "num_top_classes":5
              }
            }
            ```

    4. Click **Add** to save the processor.

3. Optional: Add a [set processor](elasticsearch://reference/enrich-processor/set-processor.md) to index the ingest timestamp.

    1. Click **Add a processor** and select the **Set** processor type.
    2. Choose a name for the field (such as `event.ingested`) and set its value to `{{{_ingest.timestamp}}}`. For more details, refer to [Access ingest metadata in a processor](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md#access-ingest-metadata).
    3. Click **Add** to save the processor.

4. Optional: Add failure processors to handle exceptions. For example, in the **Failure processors** section:

    1. Add a set processor to capture the pipeline error message. Choose a name for the field (such as `ml.inference_failure`) and set its value to the `{{_ingest.on_failure_message}}` document metadata field.
    2. Add a set processor to reroute problematic documents to a different index for troubleshooting purposes. Use the `_index` metadata field and set its value to a new name (such as `failed-{{{ _index }}}`). For more details, refer to [Handling pipeline failures](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md#handling-pipeline-failures).

5. To test the pipeline, click **Add documents**.

    1. In the **Documents** tab, provide a sample document for testing.

        For example, to test a trained model that performs named entity recognition (NER):

        ```js
        [
          {
            "_source": {
            "text_field":"Hello, my name is Josh and I live in Berlin."
            }
          }
        ]
        ```

        To test a trained model that performs {{lang-ident}}:

        ```js
        [
         {
           "_source":{
             "message":"Sziasztok! Ez egy rövid magyar szöveg. Nézzük, vajon sikerül-e azonosítania a language identification funkciónak? Annak ellenére is sikerülni fog, hogy a szöveg két angol szót is tartalmaz."
             }
          }
        ]
        ```

    2. Click **Run the pipeline** and verify the pipeline worked as expected.

        In the {{lang-ident}} example, the predicted value is the ISO identifier of the language with the highest probability. In this case, it should be `hu` for Hungarian.

    3. If everything looks correct, close the panel, and click **Create pipeline**. The pipeline is now ready for use.

## Ingest documents [ml-nlp-inference-ingest-docs]

You can now use your ingest pipeline to perform NLP tasks on your data.

Before you add data, consider which mappings you want to use. For example, you can create explicit mappings with the create index API in the **{{dev-tools-app}}** > **Console**:

```console
PUT ner-test
{
  "mappings": {
    "properties": {
      "ml.inference.predicted_value": {"type": "annotated_text"},
      "ml.inference.model_id": {"type": "keyword"},
      "text_field": {"type": "text"},
      "event.ingested": {"type": "date"}
    }
  }
}
```

::::{tip}
To use the `annotated_text` data type in this example, you must install the [mapper annotated text plugin](elasticsearch://reference/elasticsearch-plugins/mapper-annotated-text.md). For more installation details, refer to [Add plugins provided with {{ech}}](elasticsearch://reference/elasticsearch-plugins/plugin-management.md).
::::

You can then use the new pipeline to index some documents. For example, use a bulk indexing request with the `pipeline` query parameter for your NER pipeline:

```console
POST /_bulk?pipeline=my-ner-pipeline
{"create":{"_index":"ner-test","_id":"1"}}
{"text_field":"Hello, my name is Josh and I live in Berlin."}
{"create":{"_index":"ner-test","_id":"2"}}
{"text_field":"I work for Elastic which was founded in Amsterdam."}
{"create":{"_index":"ner-test","_id":"3"}}
{"text_field":"Elastic has headquarters in Mountain View, California."}
{"create":{"_index":"ner-test","_id":"4"}}
{"text_field":"Elastic's founder, Shay Banon, created Elasticsearch to solve a simple need: finding recipes!"}
{"create":{"_index":"ner-test","_id":"5"}}
{"text_field":"Elasticsearch is built using Lucene, an open source search library."}
```

Or use an individual indexing request with the `pipeline` query parameter for your {{lang-ident}} pipeline:

```console
POST lang-test/_doc?pipeline=my-lang-pipeline
{
  "message": "Mon pays ce n'est pas un pays, c'est l'hiver"
}
```

You can also use NLP pipelines when you are reindexing documents to a new destination. For example, since the [sample web logs data set](../../index.md#gs-get-data-into-kibana) contain a `message` text field, you can reindex it with your {{lang-ident}} pipeline:

```console
POST _reindex
{
  "source": {
    "index": "kibana_sample_data_logs",
    "size": 50
  },
  "dest": {
    "index": "lang-test",
    "pipeline": "my-lang-pipeline"
  }
}
```

However, those web log messages are unlikely to contain enough words for the model to accurately identify the language.

::::{tip}
Set the reindex `size` option to a value smaller than the `queue_capacity` for the trained model deployment. Otherwise, requests might be rejected with a "too many requests" 429 error code.
::::

## View the results [ml-nlp-inference-discover]

Before you can verify the results of the pipelines, you must [create {{data-sources}}](../../find-and-organize/data-views.md). Then you can explore your data in **Discover**:

:::{image} /explore-analyze/images/machine-learning-ml-nlp-discover-ner.png
:alt: A document from the NER pipeline in the Discover app
:screenshot:
:::

The `ml.inference.predicted_value` field contains the output from the {{infer}} processor. In this NER example, there are two documents that contain the `Elastic` organization entity.

In this {{lang-ident}} example, the `ml.inference.predicted_value` contains the ISO identifier of the language with the highest probability and the `ml.inference.top_classes` fields contain the top five most probable languages and their scores:

:::{image} /explore-analyze/images/machine-learning-ml-nlp-discover-lang.png
:alt: A document from the {{lang-ident}} pipeline in the Discover app
:screenshot:
:::

To learn more about ingest pipelines and all of the other processors that you can add, refer to [Ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md).

## Common problems [ml-nlp-inference-common-problems]

If you encounter problems while using your trained model in an ingest pipeline, check the following possible causes:

1. The trained model is not deployed in your cluster. You can view its status by navigating to the **Trained models** page in the main menu, or using the [global search field](../../find-and-organize/find-apps-and-objects.md) in {{kib}}. Alternatively, use the [get trained models statistics API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models-stats). Unless you are using the built-in `lang_ident_model_1` model, you must ensure your model is successfully deployed. Refer to [Deploy the model in your cluster](ml-nlp-deploy-model.md).
2. The default input field name expected by your trained model is not present in your source document. Use the **Field Map** option in your {{infer}} processor to set the appropriate field name.
3. There are too many requests. If you are using bulk ingest, reduce the number of documents in the bulk request. If you are reindexing, use the `size` parameter to decrease the number of documents processed in each batch.

These common failure scenarios and others can be captured by adding failure processors to your pipeline. For more examples, refer to [Handling pipeline failures](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md#handling-pipeline-failures).

## Further reading [nlp-example-reading]

* [How to deploy NLP: Text Embeddings and Vector Search](https://www.elastic.co/blog/how-to-deploy-nlp-text-embeddings-and-vector-search)
* [How to deploy NLP: Named entity recognition (NER) example](https://www.elastic.co/blog/how-to-deploy-nlp-named-entity-recognition-ner-example)
* [How to deploy NLP: Sentiment Analysis Example](https://www.elastic.co/blog/how-to-deploy-nlp-sentiment-analysis-example)
