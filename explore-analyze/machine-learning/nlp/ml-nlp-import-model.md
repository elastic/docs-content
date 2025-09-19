---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-import-model.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Import the trained model and vocabulary [ml-nlp-import-model]

::::{warning}
PyTorch models can execute code on your {{es}} server, exposing your cluster to potential security vulnerabilities.

**Only use models from trusted sources and never use models from unverified or unknown providers.**
::::

::::{important}
If you want to install a trained model in a restricted or closed network, refer to [these instructions](eland://reference/machine-learning.md#ml-nlp-pytorch-air-gapped).
::::

After you choose a model, you must import it and its tokenizer vocabulary to your cluster. When you import the model, it must be chunked and imported one chunk at a time for storage in parts due to its size.

::::{note}
Trained models must be in a TorchScript representation for use with {{stack-ml-features}}.
::::

[Eland](https://github.com/elastic/eland) is an {{es}} Python client that provides a simple script to perform the conversion of Hugging Face transformer models to their TorchScript representations, the chunking process, and upload to {{es}}; it is therefore the recommended import method. You can either install the Python Eland client on your machine or use a Docker image to build Eland and run the model import script.

## Import with the Eland client installed [ml-nlp-import-script]

1. Install the [Eland Python client](eland://reference/installation.md) with PyTorch extra dependencies.

    ```shell
    python -m pip install 'eland[pytorch]'
    ```

2. Run the `eland_import_hub_model` script to download the model from Hugging Face, convert it to TorchScript format, and upload to the {{es}} cluster. For example:

    ```
    eland_import_hub_model \
    --cloud-id <cloud-id> \ <1>
    -u <username> -p <password> \ <2>
    --hub-model-id elastic/distilbert-base-cased-finetuned-conll03-english \ <3>
    --task-type ner  <4>
    ```

    1. Specify the Elastic Cloud identifier. Alternatively, use `--url`.
    2. Provide authentication details to access your cluster. Refer to [Authentication methods](#ml-nlp-authentication) to learn more.
    3. Specify the identifier for the model in the Hugging Face model hub.
    4. Specify the type of NLP task. Supported values are `fill_mask`, `ner`, `question_answering`, `text_classification`, `text_embedding`, `text_expansion`, `text_similarity`, and `zero_shot_classification`.

For more details, refer to the [Eland documentation](eland://reference/machine-learning.md#ml-nlp-pytorch).

## Import with Docker [ml-nlp-import-docker]

If you want to use Eland without installing it, run the following command:

```bash
$ docker run -it --rm --network host docker.elastic.co/eland/eland
```

The `eland_import_hub_model` script can be run directly in the docker command:

```bash
docker run -it --rm docker.elastic.co/eland/eland \
    eland_import_hub_model \
      --url $ELASTICSEARCH_URL \
      --hub-model-id elastic/distilbert-base-uncased-finetuned-conll03-english \
      --start
```

Replace the `$ELASTICSEARCH_URL` with the URL for your {{es}} cluster. Refer to [Authentication methods](#ml-nlp-authentication) to learn more.

## Authentication methods [ml-nlp-authentication]

The following authentication options are available when using the import script:

* username/password authentication (specified with the `-u` and `-p` options):

```bash
eland_import_hub_model --url https://<hostname>:<port> -u <username> -p <password> ...
```

* username/password authentication (embedded in the URL):

```bash
eland_import_hub_model --url https://<user>:<password>@<hostname>:<port> ...
```

* API key authentication:

```bash
eland_import_hub_model --url https://<hostname>:<port> --es-api-key <api-key> ...
```
