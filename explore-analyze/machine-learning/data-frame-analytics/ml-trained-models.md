---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-trained-models.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Trained models [ml-trained-models]

When you use a {{dfanalytics-job}} to perform {{classification}} or {{reganalysis}}, it creates a {{ml}} model that is trained and tested against a labeled data set. When you are satisfied with your trained model, you can use it to make predictions against new data. For example, you can use it in the processor of an ingest pipeline or in a pipeline aggregation within a search query. For more information about this process, see [Introduction to supervised learning](ml-dfa-overview.md#ml-supervised-workflow) and [{{infer}} for {{classification}}](ml-dfa-classification.md#ml-inference-class) and [{{regression}}](ml-dfa-regression.md#ml-inference-reg).

In {{kib}}, you can view and manage your trained models in **{{stack-manage-app}}** > **Alerts and Insights** > **{{ml-app}}** and **{{ml-app}}** > **Model Management**.

Alternatively, you can use APIs like [get trained models](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) and [delete trained models](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-delete-trained-model).

## Deploying trained models [deploy-dfa-trained-models]

### Models trained by {{dfanalytics}} [_models_trained_by_dfanalytics]

1. To deploy {{dfanalytics}} model in a pipeline, navigate to the **Trained models** page in the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md) in {{kib}}.

2. Find the model you want to deploy in the list and click **Deploy model** in the **Actions** menu.

:::{image} /explore-analyze/images/machine-learning-ml-dfa-trained-models-ui.png
:alt: The trained models UI in {{kib}}
:screenshot:
:::

3. Create an {{infer}} pipeline to be able to use the model against new data through the pipeline. Add a name and a description or use the default values.

:::{image} /explore-analyze/images/machine-learning-ml-dfa-inference-pipeline.png
:alt: Creating an inference pipeline
:screenshot:
:::

4. Configure the pipeline processors or use the default settings.

:::{image} /explore-analyze/images/machine-learning-ml-dfa-inference-processor.png
:alt: Configuring an inference processor
:screenshot:
:::

5. Configure to handle ingest failures or use the default settings.
6. (Optional) Test your pipeline by running a simulation of the pipeline to confirm it produces the anticipated results.
7. Review the settings and click **Create pipeline**.

The model is deployed and ready to use through the {{infer}} pipeline.

### Models trained by other methods [_models_trained_by_other_methods]

You can also supply trained models that are not created by {{dfanalytics-job}} but adhere to the appropriate [JSON schema](https://github.com/elastic/ml-json-schemas). Likewise, you can use third-party models to perform natural language processing (NLP) tasks. If you want to use these trained models in the {{stack}}, you must store them in {{es}} documents by using the [create trained models API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model). For more information about NLP models, refer to [*Deploy trained models*](../nlp/ml-nlp-deploy-models.md).

## Exporting and importing models [export-import]

Models trained in Elasticsearch are portable and can be transferred between clusters. This is particularly useful when models are trained in isolation from the cluster where they are used for inference. The following instructions show how to use [`curl`](https://curl.se/) and [`jq`](https://stedolan.github.io/jq/) to export a model as JSON and import it to another cluster.

1. Given a model *name*, find the model *ID*. You can use `curl` to call the [get trained model API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) to list all models with their IDs.

```bash
    curl -s -u username:password \
      -X GET "http://localhost:9200/_ml/trained_models" \
        | jq . -C \
        | more
```

    If you want to show just the model IDs available, use `jq` to select a subset.

```bash
    curl -s -u username:password \
      -X GET "http://localhost:9200/_ml/trained_models" \
        | jq -C -r '.trained_model_configs[].model_id'
```

```bash
    flights1-1607953694065
    flights0-1607953585123
    lang_ident_model_1
```

    In this example, you are exporting the model with ID `flights1-1607953694065`.

2. Using `curl` from the command line, again use the [get trained models API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) to export the entire model definition and save it to a JSON file.

```bash
    curl -u username:password \
      -X GET "http://localhost:9200/_ml/trained_models/flights1-1607953694065?exclude_generated=true&include=definition&decompress_definition=false" \
        | jq '.trained_model_configs[0] | del(.model_id)' \
        > flights1.json
```

A few observations:

  * Exporting models requires using `curl` or a similar tool that can **stream** the model over HTTP into a file. If you use the {{kib}} Console, the browser might be unresponsive due to the size of exported models.
  * Note the query parameters that are used during export. These parameters are necessary to export the model in a way that it can later be imported again and used for inference.
  * You must unnest the JSON object by one level to extract just the model definition. You must also remove the existing model ID in order to not have ID collisions when you import again. You can do these steps using `jq` inline or alternatively it can be done to the resulting JSON file after downloading using `jq` or other tools.

3. Import the saved model using `curl` to upload the JSON file to the [created trained model API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model). When you specify the URL, you can also set the model ID to something new using the last path part of the URL.

```bash
    curl -u username:password \
      -H 'Content-Type: application/json' \
      -X PUT "http://localhost:9200/_ml/trained_models/flights1-imported" \
      --data-binary @flights1.json
```

::::{note}

* Models exported from the [get trained models API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) are limited in size by the [http.max_content_length](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) global configuration value in {{es}}. The default value is `100mb` and may need to be increased depending on the size of model being exported.
* Connection timeouts can occur, for example, when model sizes are very large or your cluster is under load. If needed, you can increase [timeout configurations](https://ec.haxx.se/usingcurl/usingcurl-timeouts) for `curl` (for example, `curl --max-time 600`) or your client of choice.

::::

If you also want to copy the {{dfanalytics-job}} to the new cluster, you can export and import jobs in the **{{stack-manage-app}}** app in {{kib}}. Refer to [Exporting and importing {{ml}} jobs](../setting-up-machine-learning.md#move-jobs).

## Importing an external model to the {{stack}} [import-external-model-to-es]

It is possible to import a model to your {{es}} cluster even if the model is not trained by Elastic {{dfanalytics}}. Eland supports [importing models](eland://reference/machine-learning.md) directly through its APIs. See the latest [Eland documentation](https://eland.readthedocs.io/en/latest/index.html) for more information on supported model types and other details of using Eland to import models with.
