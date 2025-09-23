---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-select-model.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Select a trained model [ml-nlp-select-model]

Per the [Overview](ml-nlp-overview.md), there are multiple ways that you can use NLP features within the {{stack}}. After you determine which type of NLP task you want to perform, you must choose an appropriate trained model.

The simplest method is to use a model that has already been fine-tuned for the type of analysis that you want to perform. For example, there are models and data sets available for specific NLP tasks on [Hugging Face](https://huggingface.co/models). These instructions assume you’re using one of those models and do not describe how to create new models. For the current list of supported model architectures, refer to [Compatible third party models](ml-nlp-model-ref.md).

If you choose to perform {{lang-ident}} by using the `lang_ident_model_1` that is provided in the cluster, no further steps are required to import or deploy the model. You can skip to using the model in [ingestion pipelines](ml-nlp-inference.md).
