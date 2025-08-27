---
navigation_title: E5
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-e5.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# E5 [ml-nlp-e5]

EmbEddings from bidirEctional Encoder rEpresentations - or E5 -  is a {{nlp}} model that enables you to perform multi-lingual semantic search by using dense vector representations. This model is recommended for non-English language documents and queries. If you want to perform semantic search on English language documents, use the [ELSER](ml-nlp-elser.md) model.

[Semantic search](../../../solutions/search/semantic-search.md) provides you search results based on contextual meaning and user intent, rather than exact keyword matches.

E5 has two versions: one cross-platform version which runs on any hardware and one version which is optimized for Intel® silicon. The **Model Management** > **Trained Models** page shows you which version of E5 is recommended to deploy based on your cluster’s hardware. However, the recommended way to use E5 is through the [{{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch) as a service which makes it easier to download and deploy the model and you don’t need to select from different versions.

Refer to the model cards of the [multilingual-e5-small](https://huggingface.co/elastic/multilingual-e5-small) and the [multilingual-e5-small-optimized](https://huggingface.co/elastic/multilingual-e5-small-optimized) models on HuggingFace for further information including licensing.

## Requirements [e5-req]

To use E5, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level for semantic search or the trial period activated.

Enabling trained model autoscaling for your E5 deployment is recommended. Refer to [*Trained model autoscaling*](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) to learn more.

## Download and deploy E5 [download-deploy-e5]

The easiest and recommended way to download and deploy E5 is to use the [{{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference).

1. In {{kib}}, navigate to the **Dev Console**.
2. Create an {{infer}} endpoint with the `elasticsearch` service by running the following API request:

```console
PUT _inference/text_embedding/my-e5-model
    {
      "service": "elasticsearch",
      "service_settings": {
        "num_allocations": 1,
        "num_threads": 1,
        "model_id": ".multilingual-e5-small"
      }
    }
```

The API request automatically initiates the model download and then deploy the model.

Refer to the `elasticsearch` [{{infer}} service documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch) to learn more about the available settings.

After you created the E5 {{infer}} endpoint, it’s ready to be used for semantic search. The easiest way to perform semantic search in the {{stack}} is to [follow the `semantic_text` workflow](../../../solutions/search/semantic-search/semantic-search-semantic-text.md).

### Alternative methods to download and deploy E5 [alternative-download-deploy-e5]

You can also download and deploy the E5 model from the **Trained models** page, from **Search** > **Indices**, or by using the trained models API in Dev Console.

::::{note}
For most cases, the preferred version is the **Intel and Linux optimized** model, it is recommended to download and deploy that version.
::::

::::{dropdown} Using the Trained Models page

#### Using the Trained Models page [trained-model-e5]

1. In {{kib}}, navigate to the **Trained Models** page from the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md). E5 can be found in the list of trained models. There are two versions available: one portable version which runs on any hardware and one version which is optimized for Intel® silicon. You can see which model is recommended to use based on your hardware configuration.
2. Click the **Add trained model** button. Select the E5 model version you want to use in the opening modal window. The model that is recommended for you based on your hardware configuration is highlighted. Click **Download**. You can check the download status on the **Notifications** page.

    :::{image} /explore-analyze/images/machine-learning-ml-nlp-e5-download.png
    :alt: Downloading E5
    :screenshot:
    :::

    Alternatively, click the **Download model** button under **Actions** in the trained model list.

3. After the download is finished, start the deployment by clicking the **Start deployment** button.
4. Provide a deployment ID, select the priority, and set the number of allocations and threads per allocation values.

    :::{image} /explore-analyze/images/machine-learning-ml-nlp-deployment-id-e5.png
    :alt: Deploying E5
    :screenshot:
    :::

5. Click Start.

::::

::::{dropdown} Using the search indices UI

#### Using the search indices UI [elasticsearch-e5]

Alternatively, you can download and deploy the E5 model to an {{infer}} pipeline using the search indices UI.

1. In {{kib}}, navigate to **Search** > **Indices**.
2. Select the index from the list that has an {{infer}} pipeline in which you want to use E5.
3. Navigate to the **Pipelines** tab.
4. Under **{{ml-app}} {{infer-cap}} Pipelines**, click the **Deploy** button in the **Improve your results with E5** section to begin downloading the E5 model. This may take a few minutes depending on your network.

    :::{image} /explore-analyze/images/machine-learning-ml-nlp-deploy-e5-es.png
    :alt: Deploying E5 in Elasticsearch
    :screenshot:
    :::

5. Once the model is downloaded, click the **Start single-threaded** button to start the model with basic configuration or select the **Fine-tune performance** option to navigate to the **Trained Models** page where you can configure the model deployment.

    :::{image} /explore-analyze/images/machine-learning-ml-nlp-start-e5-es.png
    :alt: Start E5 in Elasticsearch
    :screenshot:
    :::

When your E5 model is deployed and started, it is ready to be used in a pipeline.

::::

::::{dropdown} Using the trained models API in Dev Console

#### Using the trained models API in Dev Console [dev-console-e5]

1. In {{kib}}, navigate to the **Dev Console**.
2. Create the E5 model configuration by running the following API call:

```console
PUT _ml/trained_models/.multilingual-e5-small
    {
      "input": {
    	"field_names": ["text_field"]
      }
    }
```

    The API call automatically initiates the model download if the model is not downloaded yet.

3. Deploy the model by using the [start trained model deployment API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment) with a delpoyment ID:

```console
POST _ml/trained_models/.multilingual-e5-small/deployment/_start?deployment_id=for_search
```

::::

## Deploy the E5 model in an air-gapped environment [air-gapped-install-e5]

If you want to install E5 in an air-gapped environment, you have the following options:

* put the model artifacts into a directory inside the config directory on all master-eligible nodes (for `multilingual-e5-small` and `multilingual-e5-small-linux-x86-64`)
* install the model by using HuggingFace (for `multilingual-e5-small` model only).

### Model artifact files [e5-model-artifacts]

For the `multilingual-e5-small` model, you need the following files in your system:

```text
https://ml-models.elastic.co/multilingual-e5-small.metadata.json
https://ml-models.elastic.co/multilingual-e5-small.pt
https://ml-models.elastic.co/multilingual-e5-small.vocab.json
```

For the optimized version, you need the following files in your system:

```text
https://ml-models.elastic.co/multilingual-e5-small_linux-x86_64.metadata.json
https://ml-models.elastic.co/multilingual-e5-small_linux-x86_64.pt
https://ml-models.elastic.co/multilingual-e5-small_linux-x86_64.vocab.json
```

### Using file-based access [_using_file_based_access_3]

For a file-based access, follow these steps:

1. Download the [model artifact files](#e5-model-artifacts).
2. Put the files into a `models` subdirectory inside the `config` directory of your {{es}} deployment.
3. Point your {{es}} deployment to the model directory by adding the following line to the `config/elasticsearch.yml` file:

    ```yml
    xpack.ml.model_repository: file://${path.home}/config/models/`
    ```

4. Repeat step 2 and step 3 on all master-eligible nodes.
5. [Restart](../../../deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) the master-eligible nodes one by one.
6. Navigate to the **Trained Models** page from the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md) in {{kib}}. E5 can be found in the list of trained models.
7. Click the **Add trained model** button, select the E5 model version you downloaded in step 1 and want to deploy and click **Download**. The selected model will be downloaded from the model directory where you put in step 2.
8. After the download is finished, start the deployment by clicking the **Start deployment** button.
9. Provide a deployment ID, select the priority, and set the number of allocations and threads per allocation values.
10. Click **Start**.

### Using the HuggingFace repository [_using_the_huggingface_repository]

You can install the `multilingual-e5-small` model in a restricted or closed network by pointing the `eland_import_hub_model` script to the model’s local files.

For an offline install, the model first needs to be cloned locally, Git and [Git Large File Storage](https://git-lfs.com/) are required to be installed in your system.

1. Clone the E5 model from Hugging Face by using the model URL.

    ```bash
    git clone https://huggingface.co/intfloat/multilingual-e5-small
    ```

    The command results in a local copy of the model in the `multilingual-e5-small` directory.

2. Use the `eland_import_hub_model` script with the `--hub-model-id` set to the directory of the cloned model to install it:

    ```bash
    eland_import_hub_model \
          --url 'XXXX' \
          --hub-model-id /PATH/TO/MODEL \
          --task-type text_embedding \
          --es-username elastic --es-password XXX \
          --es-model-id multilingual-e5-small
    ```

    If you use the Docker image to run `eland_import_hub_model` you must bind mount the model directory, so the container can read the files.

    ```bash
    docker run --mount type=bind,source=/PATH/TO/MODELS,destination=/models,readonly -it --rm docker.elastic.co/eland/eland \
        eland_import_hub_model \
          --url 'XXXX' \
          --hub-model-id /models/multilingual-e5-small \
          --task-type text_embedding \
          --es-username elastic --es-password XXX \
          --es-model-id multilingual-e5-small
    ```

    Once it’s uploaded to {{es}}, the model will have the ID specified by `--es-model-id`. If it is not set, the model ID is derived from `--hub-model-id`; spaces and path delimiters are converted to double underscores `__`.

## Disclaimer [terms-of-use-e5]

Customers may add third party trained models for management in Elastic. These models are not owned by Elastic. While Elastic will support the integration with these models in the performance according to the documentation, you understand and agree that Elastic has no control over, or liability for, the third party models or the underlying training data they may utilize.

This e5 model, as defined, hosted, integrated and used in conjunction with our other Elastic Software is covered by our standard warranty.
