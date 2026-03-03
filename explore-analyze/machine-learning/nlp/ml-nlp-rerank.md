---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-rerank.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Elastic Rerank [ml-nlp-rerank]

Elastic Rerank is a state-of-the-art cross-encoder reranking model trained by Elastic that helps you improve search relevance with a few simple API calls. Elastic Rerank is Elastic’s first semantic reranking model and is available out-of-the-box in supporting Elastic deployments using the {{es}} Inference API.

Use Elastic Rerank to improve existing search-powered applications including:

* Traditional BM25 scoring
* Hybrid semantic search
* Retrieval Augmented Generation (RAG)

The model can significantly improve search result quality by reordering results based on deeper semantic understanding of queries and documents.

When reranking BM25 results, it provides an average 40% improvement in ranking quality on a diverse benchmark of retrieval tasks— matching the performance of models 11x its size.

## Availability and requirements [ml-nlp-rerank-availability]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

### Elastic Cloud Serverless [ml-nlp-rerank-availability-serverless]

Elastic Rerank is available in {{es}} Serverless projects as of November 25, 2024.

### Elastic Cloud Hosted and self-managed deployments [ml-nlp-rerank-availability-elastic-stack]

Elastic Rerank is available in Elastic Stack version 8.17+:

* To use Elastic Rerank, you must have the appropriate subscription level or the trial period activated.
* A 4GB ML node

    ::::{important}
    Deploying the Elastic Rerank model in combination with ELSER (or other hosted models) requires at minimum an 8GB ML node. The current maximum size for trial ML nodes is 4GB (defaults to 1GB).

    ::::

## Download and deploy [ml-nlp-rerank-deploy]

To download and deploy Elastic Rerank, use the [create inference API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch) to create an {{es}} service `rerank` endpoint.

::::{tip}
Refer to this [Python notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/12-semantic-reranking-elastic-rerank.ipynb) for an end-to-end example using Elastic Rerank.

::::

### Create an inference endpoint [ml-nlp-rerank-deploy-steps]

1. In {{kib}}, navigate to the **Dev Console**.
2. Create an {{infer}} endpoint with the Elastic Rerank service by running:

```console
PUT _inference/rerank/my-rerank-model
    {
      "service": "elasticsearch",
      "service_settings": {
        "adaptive_allocations": {
          "enabled": true,
          "min_number_of_allocations": 1,
          "max_number_of_allocations": 10
        },
        "num_threads": 1,
        "model_id": ".rerank-v1"
      }
    }
```

::::{note}
The API request automatically downloads and deploys the model. This example uses [autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) through adaptive allocation.
::::

::::{note}
You might see a 502 bad gateway error in the response when using the {{kib}} Console. This error usually just reflects a timeout, while the model downloads in the background. You can check the download progress in the {{ml-app}} UI. If using the Python client, you can set the `timeout` parameter to a higher value.

::::

After creating the Elastic Rerank {{infer}} endpoint, it’s ready to use with a [`text_similarity_reranker`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) retriever.

## Deploy in an air-gapped environment [ml-nlp-rerank-deploy-verify]

If you want to deploy the Elastic Rerank model in a restricted or closed network, you have two options:

* Create your own HTTP/HTTPS endpoint with the model artifacts on it
* Put the model artifacts into a directory inside the config directory on all master-eligible nodes.

### Model artifact files [ml-nlp-rerank-model-artifacts]

For the cross-platform version, you need the following files in your system:

```text
https://ml-models.elastic.co/rerank-v1.metadata.json
https://ml-models.elastic.co/rerank-v1.pt
https://ml-models.elastic.co/rerank-v1.vocab.json
```

### Using an HTTP server [_using_an_http_server_2]

INFO: If you use an existing HTTP server, note that the model downloader only supports passwordless HTTP servers.

You can use any HTTP service to deploy the model. This example uses the official Nginx Docker image to set a new HTTP download service up.

1. Download the [model artifact files](#ml-nlp-rerank-model-artifacts).
2. Put the files into a subdirectory of your choice.
3. Run the following commands:

    ```shell
    export ELASTIC_ML_MODELS="/path/to/models"
    docker run --rm -d -p 8080:80 --name ml-models -v ${ELASTIC_ML_MODELS}:/usr/share/nginx/html nginx
    ```

    Don’t forget to change `/path/to/models` to the path of the subdirectory where the model artifact files are located.

    These commands start a local Docker image with an Nginx server with the subdirectory containing the model files. As the Docker image has to be downloaded and built, the first start might take a longer period of time. Subsequent runs start quicker.

4. Verify that Nginx runs properly by visiting the following URL in your browser:

    ```text
    http://{IP_ADDRESS_OR_HOSTNAME}:8080/rerank-v1.metadata.json
    ```

    If Nginx runs properly, you see the content of the metdata file of the model.

5. Point your {{es}} deployment to the model artifacts on the HTTP server by adding the following line to the `config/elasticsearch.yml` file:

    ```yml
    xpack.ml.model_repository: http://{IP_ADDRESS_OR_HOSTNAME}:8080
    ```

    If you use your own HTTP or HTTPS server, change the address accordingly. It is important to specificy the protocol ("http://" or "https://"). Ensure that all master-eligible nodes can reach the server you specify.

6. Repeat step 5 on all master-eligible nodes.
7. [Restart](../../../deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) the master-eligible nodes one by one.
8. Create an inference endpoint to deploy the model per [these steps](#ml-nlp-rerank-deploy-steps).

The HTTP server is only required for downloading the model. After the download has finished, you can stop and delete the service. You can stop the Docker image used in this example by running the following command:

```shell
docker stop ml-models
```

### Using file-based access [_using_file_based_access_2]

For a file-based access, follow these steps:

1. Download the [model artifact files](#ml-nlp-rerank-model-artifacts).
2. Put the files into a `models` subdirectory inside the `config` directory of your {{es}} deployment.
3. Point your {{es}} deployment to the model directory by adding the following line to the `config/elasticsearch.yml` file:

    ```yml
    xpack.ml.model_repository: file://${path.home}/config/models/
    ```

4. Repeat step 2 and step 3 on all master-eligible nodes.
5. [Restart](../../../deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) the master-eligible nodes one by one.
6. Create an inference endpoint to deploy the model per [these steps](#ml-nlp-rerank-deploy-steps).

## Limitations [ml-nlp-rerank-limitations]

* English language only
* Maximum context window of 512 tokens

    When using the [`semantic_text` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md), text is divided into chunks. By default, each chunk contains 250 words (approximately 400 tokens). Be cautious when increasing the chunk size - if the combined length of your query and chunk text exceeds 512 tokens, the model won’t have access to the full content.

    When the combined inputs exceed the 512 token limit, a balanced truncation strategy is used. If both the query and input text are longer than 255 tokens each then both are truncated, otherwise the longest is truncated.

## Performance considerations [ml-nlp-rerank-perf-considerations]

It’s important to note that if you rerank to depth `n` then you will need to run `n` inferences per query. This will include the document text and will therefore be significantly more expensive than inference for query embeddings. Hardware can be scaled to run these inferences in parallel, but we would recommend shallow reranking for CPU inference: no more than top-30 results. You may find that the preview version is cost prohibitive for high query rates and low query latency requirements. We plan to address performance issues for GA.

## Model specifications [ml-nlp-rerank-model-specs]

* Purpose-built for English language content
* Relatively small: 184M parameters (86M backbone + 98M embedding layer)
* Matches performance of billion-parameter reranking models
* Built directly into {{es}} - no external services or dependencies needed

## Model architecture [ml-nlp-rerank-arch-overview]

Elastic Rerank is built on the [DeBERTa v3](https://arxiv.org/abs/2111.09543) language model architecture.

The model employs several key architectural features that make it particularly effective for reranking:

* **Disentangled attention mechanism** enables the model to:
  * Process word content and position separately
  * Learn more nuanced relationships between query and document text
  * Better understand the semantic importance of word positions and relationships

* **ELECTRA-style pre-training** uses:
  * A GAN-like approach to token prediction
  * Simultaneous training of token generation and detection
  * Enhanced parameter efficiency compared to traditional masked language modeling

## Training process [ml-nlp-rerank-arch-training]

Here is an overview of the Elastic Rerank model training process:

* **Initial relevance extraction**
  * Fine-tunes the pre-trained DeBERTa [CLS] token representation
  * Uses a GeLU activation and dropout layer
  * Preserves important pre-trained knowledge while adapting to the reranking task

* **Trained by distillation**
  * Uses an ensemble of bi-encoder and cross-encoder models as a teacher
  * Bi-encoder provides nuanced negative example assessment
  * Cross-encoder helps differentiate between positive and negative examples
  * Combines strengths of both model types

### Training data [ml-nlp-rerank-arch-data]

The training data consists of:

* Open domain Question-Answering datasets
* Natural document pairs (like article headings and summaries)
* 180,000 synthetic query-passage pairs with varying relevance
* Total of approximately 3 million queries

The data preparation process includes:

* Basic cleaning and fuzzy deduplication
* Multi-stage prompting for diverse topics (on the synthetic portion of the training data only)
* Varied query types:
  * Keyword search
  * Exact phrase matching
  * Short and long natural language questions

### Negative sampling [ml-nlp-rerank-arch-sampling]

The model uses an advanced sampling strategy to ensure high-quality rankings:

* Samples from top 128 documents per query using multiple retrieval methods
* Uses five negative samples per query - more than typical approaches
* Applies probability distribution shaped by document scores for sampling
* Deep sampling benefits:
  * Improves model robustness across different retrieval depths
  * Enhances score calibration
  * Provides better handling of document diversity

### Training optimization [ml-nlp-rerank-arch-optimization]

The training process incorporates several key optimizations:

Uses cross-entropy loss function to:

* Model relevance as probability distribution
* Learn relationships between all document scores
* Fit scores through maximum likelihood estimation

Implemented parameter averaging along optimization trajectory:

* Eliminates need for traditional learning rate scheduling and provides improvement in the final model quality

## Performance [ml-nlp-rerank-performance]

Elastic Rerank shows significant improvements in search quality across a wide range of retrieval tasks.

### Overview [ml-nlp-rerank-performance-overview]

* Average 40% improvement in ranking quality when reranking BM25 results
* 184M parameter model matches performance of 2B parameter alternatives
* Evaluated across 21 different datasets using the BEIR benchmark suite

### Key benchmark results [ml-nlp-rerank-performance-benchmarks]

* Natural Questions: 90% improvement
* MS MARCO: 85% improvement
* Climate-FEVER: 80% improvement
* FiQA-2018: 76% improvement

For detailed benchmark information, including complete dataset results and methodology, refer to the [Introducing Elastic Rerank blog](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-2).

## Further resources [ml-nlp-rerank-resources]

**Documentation**:

* [Semantic re-ranking in {{es}} overview](../../../solutions/search/ranking/semantic-reranking.md#semantic-reranking-in-es)
* [Inference API example](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch)

**Blogs**:

* [Part 1](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-1)
* [Part 2](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-2)
* [Part 3](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-3)

**Python notebooks**:

* [End-to-end example using Elastic Rerank in Python](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/12-semantic-reranking-elastic-rerank.ipynb)
