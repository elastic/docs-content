---
navigation_title: Overview
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-overview.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Overview of NLP with Elastic machine learning [ml-nlp-overview]

{{nlp-cap}} (NLP) refers to the way in which we can use software to understand natural language in spoken word or written text.

## NLP in the {{stack}} [nlp-elastic-stack]

Elastic offers a wide range of possibilities to leverage natural language processing.

You can **integrate NLP models from different providers** such as Cohere, HuggingFace, or OpenAI and use them as a service through the [semantic_text](../../../solutions/search/semantic-search/semantic-search-semantic-text.md) workflow. You can also use [ELSER](ml-nlp-elser.md) (the retrieval model trained by Elastic) and [E5](ml-nlp-e5.md) in the same way.

The [{{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) enables you to use the same services with a more complex workflow, for greater control over your configurations settings. This [tutorial](../../elastic-inference/inference-api.md) walks you through the process of using the various services with the {{infer}} API.

You can **upload and manage NLP models** using the Eland client and the [{{stack}}](ml-nlp-deploy-models.md). Find the  [list of recommended and compatible models here](ml-nlp-model-ref.md). Refer to [*Examples*](ml-nlp-examples.md) to learn more about how to use {{ml}} models deployed in your cluster.

You can **store embeddings in your {{es}} vector database** if you generate [dense vector](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) or [sparse vector](elasticsearch://reference/elasticsearch/mapping-reference/sparse-vector.md) model embeddings outside of {{es}}.

## What is NLP? [what-is-nlp]

Classically, NLP was performed using linguistic rules, dictionaries, regular expressions, and {{ml}} for specific tasks such as automatic categorization or summarization of text. In recent years, however, deep learning techniques have taken over much of the NLP landscape. Deep learning capitalizes on the availability of large scale data sets, cheap computation, and techniques for learning at scale with less human involvement. Pre-trained language models that use a transformer architecture have been particularly successful. For example, BERT is a pre-trained language model that was released by Google in 2018. Since that time, it has become the inspiration for most of today’s modern NLP techniques. The {{stack}} {{ml}} features are structured around BERT and transformer models. These features support BERT’s tokenization scheme (called WordPiece) and transformer models that conform to the standard BERT model interface. For the current list of supported architectures, refer to [Compatible third party models](ml-nlp-model-ref.md).

To incorporate transformer models and make predictions, {{es}} uses libtorch, which is an underlying native library for PyTorch. Trained models must be in a TorchScript representation for use with {{stack}} {{ml}} features.

As in the cases of [classification](../data-frame-analytics/ml-dfa-classification.md) and [{{regression}}](../data-frame-analytics/ml-dfa-regression.md), after you deploy a model to your cluster, you can use it to make predictions (also known as *{{infer}}*) against incoming data. You can perform the following NLP operations:

* [Extract information](ml-nlp-extract-info.md)
* [Classify text](ml-nlp-classify-text.md)
* [Search and compare text](ml-nlp-search-compare.md)

To delve deeper into Elastic’s {{ml}} research and development, explore the [ML research](https://www.elastic.co/search-labs/blog/categories/ml-research) section within Search Labs.
