---
navigation_title: "Named entity recognition"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-ner-example.html
---

# Named entity recognition [ml-nlp-ner-example]

You can use these instructions to deploy a [named entity recognition (NER)](ml-nlp-extract-info.md#ml-nlp-ner) model in {{es}}, test the model, and add it to an {{infer}} ingest pipeline. The model that is used in the example is publicly available on [HuggingFace](https://huggingface.co/).

## Requirements [ex-ner-requirements]

To follow along the process on this page, you must have:

* an {{es}} Cloud cluster that is set up properly to use the {{ml-features}}. Refer to [Setup and security](../setting-up-machine-learning.md).
* The [appropriate subscription](https://www.elastic.co/subscriptions) level or the free trial period activated.
* [Docker](https://docs.docker.com/get-docker/) installed.

## Deploy a NER model [ex-ner-deploy]

You can use the [Eland client](https://www.elastic.co/guide/en/elasticsearch/client/eland/current) to install the {{nlp}} model. Use the prebuilt Docker image to run the Eland install model commands. Pull the latest image with:

```shell
docker pull docker.elastic.co/eland/eland
```

After the pull completes, your Eland Docker client is ready to use.

Select a NER model from the [third-party model reference list](ml-nlp-model-ref.md#ml-nlp-model-ref-ner). This example uses an [uncased NER model](https://huggingface.co/elastic/distilbert-base-uncased-finetuned-conll03-english).

Install the model by running the `eland_import_model_hub` command in the Docker image:

```shell
docker run -it --rm docker.elastic.co/eland/eland \
    eland_import_hub_model \
      --cloud-id $CLOUD_ID \
      -u <username> -p <password> \
      --hub-model-id elastic/distilbert-base-uncased-finetuned-conll03-english \
      --task-type ner \
      --start
```

You need to provide an administrator username and its password and replace the `$CLOUD_ID` with the ID of your Cloud deployment. This Cloud ID can be copied from the deployments page on your Cloud website.

Since the `--start` option is used at the end of the Eland import command, {{es}} deploys the model ready to use. If you have multiple models and want to select which model to deploy, you can use the **{{ml-app}} > Model Management** user interface in {{kib}} to manage the starting and stopping of models.

Go to the **{{ml-app}} > Trained Models** page and synchronize your trained models. A warning message is displayed at the top of the page that says *"ML job and trained model synchronization required"*. Follow the link to *"Synchronize your jobs and trained models."* Then click **Synchronize**. You can also wait for the automatic synchronization that occurs in every hour, or use the [sync {{ml}} objects API](https://www.elastic.co/docs/api/doc/kibana/v8/group/endpoint-ml).

## Test the NER model [ex-ner-test]

Deployed models can be evaluated in {{kib}} under **{{ml-app}}** > **Trained Models** by selecting the **Test model** action for the respective model.

:::{image} ../../../images/machine-learning-ml-nlp-ner-test.png
:alt: Test trained model UI
:class: screenshot
:::

::::{dropdown} **Test the model by using the _infer API**
You can also evaluate your models by using the [_infer API](https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-trained-model.html). In the following request, `text_field` is the field name where the model expects to find the input, as defined in the model configuration. By default, if the model was uploaded via Eland, the input field is `text_field`.

```js
POST _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/_infer
{
  "docs": [
    {
      "text_field": "Elastic is headquartered in Mountain View, California."
    }
  ]
}
```

The API returns a response similar to the following:

```js
{
  "inference_results": [
    {
      "predicted_value": "[Elastic](ORG&Elastic) is headquartered in [Mountain View](LOC&Mountain+View), [California](LOC&California).",
      "entities": [
        {
          "entity": "elastic",
          "class_name": "ORG",
          "class_probability": 0.9958921231805256,
          "start_pos": 0,
          "end_pos": 7
        },
        {
          "entity": "mountain view",
          "class_name": "LOC",
          "class_probability": 0.9844731508992688,
          "start_pos": 28,
          "end_pos": 41
        },
        {
          "entity": "california",
          "class_name": "LOC",
          "class_probability": 0.9972361009811214,
          "start_pos": 43,
          "end_pos": 53
        }
      ]
    }
  ]
}
```

::::

Using the example text "Elastic is headquartered in Mountain View, California.", the model finds three entities: an organization "Elastic", and two locations "Mountain View" and "California".

## Add the NER model to an {{infer}} ingest pipeline [ex-ner-ingest]

You can perform bulk {{infer}} on documents as they are ingested by using an [{{infer}} processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/inference-processor.html) in your ingest pipeline. The novel *Les Misérables* by Victor Hugo is used as an example for {{infer}} in the following example. [Download](https://github.com/elastic/stack-docs/blob/8.5/docs/en/stack/ml/nlp/data/les-miserables-nd.json) the novel text split by paragraph as a JSON file, then upload it by using the [Data Visualizer](../../../manage-data/ingest.md#upload-data-kibana). Give the new index the name `les-miserables` when uploading the file.

Now create an ingest pipeline either in the [Stack management UI](ml-nlp-inference.md#ml-nlp-inference-processor) or by using the API:

```js
PUT _ingest/pipeline/ner
{
  "description": "NER pipeline",
  "processors": [
    {
      "inference": {
        "model_id": "elastic__distilbert-base-uncased-finetuned-conll03-english",
        "target_field": "ml.ner",
        "field_map": {
          "paragraph": "text_field"
        }
      }
    },
    {
      "script": {
        "lang": "painless",
        "if": "return ctx['ml']['ner'].containsKey('entities')",
        "source": "Map tags = new HashMap(); for (item in ctx['ml']['ner']['entities']) { if (!tags.containsKey(item.class_name)) tags[item.class_name] = new HashSet(); tags[item.class_name].add(item.entity);} ctx['tags'] = tags;"
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "description": "Index document to 'failed-<index>'",
        "field": "_index",
        "value": "failed-{{{ _index }}}"
      }
    },
    {
      "set": {
        "description": "Set error message",
        "field": "ingest.failure",
        "value": "{{_ingest.on_failure_message}}"
      }
    }
  ]
}
```

The `field_map` object of the `inference` processor maps the `paragraph` field in the *Les Misérables*  documents to `text_field` (the name of the field the model is configured to use). The `target_field` is the name of the field to write the inference results to.

The `script` processor pulls out the entities and groups them by type. The end result is lists of people, locations, and organizations detected in the input text. This painless script enables you to build visualizations from the fields that are created.

The purpose of the `on_failure` clause is to record errors. It sets the `_index` meta field to a new value, and the document is now stored there. It also sets a new field `ingest.failure` and the error message is written to this field. {{infer-cap}} can fail for a number of easily fixable reasons. Perhaps the model has not been deployed, or the input field is missing in some of the source documents. By redirecting the failed documents to another index and setting the error message, those failed inferences are not lost and can be reviewed later. When the errors are fixed, reindex from the failed index to recover the unsuccessful requests.

Ingest the text of the novel - the index `les-miserables` - through the pipeline you created:

```js
POST _reindex
{
  "source": {
    "index": "les-miserables",
    "size": 50 <1>
  },
  "dest": {
    "index": "les-miserables-infer",
    "pipeline": "ner"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.

Take a random paragraph from the source document as an example:

```js
{
    "paragraph": "Father Gillenormand did not do it intentionally, but inattention to proper names was an aristocratic habit of his.",
    "line": 12700
}
```

After the text is ingested through the NER pipeline, find the resulting document stored in {{es}}:

```js
GET /les-miserables-infer/_search
{
  "query": {
    "term": {
      "line": 12700
    }
  }
}
```

The request returns the document marked up with one identified person:

```js
(...)
"paragraph": "Father Gillenormand did not do it intentionally, but inattention to proper names was an aristocratic habit of his.",
  "@timestamp": "2020-01-01T17:38:25.000+01:00",
  "line": 12700,
  "ml": {
    "ner": {
      "predicted_value": "Father [Gillenormand](PER&Gillenormand) did not do it intentionally, but inattention to proper names was an aristocratic habit of his.",
      "entities": [
        {
          "entity": "gillenormand",
          "class_name": "PER",
          "class_probability": 0.9452480789333386,
          "start_pos": 7,
          "end_pos": 19
        }
      ],
      "model_id": "elastic__distilbert-base-uncased-finetuned-conll03-english"
    }
  },
  "tags": {
    "PER": [
      "gillenormand"
    ]
  }
(...)
```

## Visualize results [ex-ner-visual]

You can create a tag cloud to visualize your data processed by the {{infer}} pipeline. A tag cloud is a visualization that scales words by the frequency at which they occur. It is a handy tool for viewing the entities found in the data.

In {{kib}}, open **Stack management** > **{{data-sources-cap}}** from the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md), and create a new {{data-source}} from the `les-miserables-infer` index pattern.

Open **Dashboard** and create a new dashboard. Select the **Aggregation based-type > Tag cloud** visualization. Choose the new {{data-source}} as the source.

Add a new bucket with a term aggregation, select the `tags.PER.keyword` field, and increase the size to 20.

Optionally, adjust the time selector to cover the data points in the {{data-source}} if you selected a time field when creating it.

Update and save the visualization.

:::{image} ../../../images/machine-learning-ml-nlp-tag-cloud.png
:alt: Tag cloud created from Les Misérables
:class: screenshot
:::
