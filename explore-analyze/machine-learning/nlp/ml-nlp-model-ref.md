---
navigation_title: Compatible third party models
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-model-ref.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Compatible third party models [ml-nlp-model-ref]

::::{warning}
PyTorch models can execute code on your {{es}} server, exposing your cluster to potential security vulnerabilities.

**Only use models from trusted sources and never use models from unverified or unknown providers.**

The models listed on this page are all from a trusted source – Hugging Face.
::::

::::{note}
The minimum dedicated ML node size for deploying and using the {{nlp}} models is 16 GB in {{ech}} if [deployment autoscaling](../../../deploy-manage/autoscaling.md) is turned off. Turning on autoscaling is recommended because it allows your deployment to dynamically adjust resources based on demand. Better performance can be achieved by using more allocations or more threads per allocation, which requires bigger ML nodes. Autoscaling provides bigger nodes when required. If autoscaling is turned off, you must provide suitably sized nodes yourself.
::::

The {{stack-ml-features}} support transformer models with the following architectures:

* BERT
* BART
* DPR bi-encoders
* DeBERTa
* DistilBERT
* ELECTRA
* MobileBERT
* RoBERTa
* RetriBERT
* MPNet
* SentenceTransformers bi-encoders with the above transformer architectures
* XLM-RoBERTa

In general, any trained model that has a supported architecture is deployable in {{es}} by using eland. However, it is not possible to test every third party model. The following lists are therefore provided for informational purposes only and may not be current. Elastic makes no warranty or assurance that the {{ml-features}} will continue to interoperate with these third party models in the way described, or at all.

These models are listed by NLP task; for more information about those tasks, refer to [*Overview*](ml-nlp-overview.md).

**Models highlighted in bold** in the list below are recommended for evaluation purposes and to get started with the Elastic {{nlp}} features.

## Third party fill-mask models [ml-nlp-model-ref-mask]

* [BERT base model](https://huggingface.co/bert-base-uncased)
* [DistilRoBERTa base model](https://huggingface.co/distilroberta-base)
* [MPNet base model](https://huggingface.co/microsoft/mpnet-base)
* [RoBERTa large model](https://huggingface.co/roberta-large)

## Third party named entity recognition models [ml-nlp-model-ref-ner]

* [BERT base NER](https://huggingface.co/dslim/bert-base-NER)
* [**DistilBERT base cased finetuned conll03 English**](https://huggingface.co/elastic/distilbert-base-cased-finetuned-conll03-english)
* [DistilRoBERTa base NER conll2003](https://huggingface.co/philschmid/distilroberta-base-ner-conll2003)
* [**DistilBERT base uncased finetuned conll03 English**](https://huggingface.co/elastic/distilbert-base-uncased-finetuned-conll03-english)
* [DistilBERT fa zwnj base NER](https://huggingface.co/HooshvareLab/distilbert-fa-zwnj-base-ner)

## Third party question answering models [ml-nlp-model-ref-question-answering]

* [BERT large model (uncased) whole word masking finetuned on SQuAD](https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad)
* [DistilBERT base cased distilled SQuAD](https://huggingface.co/distilbert-base-cased-distilled-squad)
* [Electra base squad2](https://huggingface.co/deepset/electra-base-squad2)
* [TinyRoBERTa squad2](https://huggingface.co/deepset/tinyroberta-squad2)

## Third party sparse embedding models [ml-nlp-model-ref-sparse-embedding]

Sparse embedding models should be configured with the `text_expansion` task type.

* [SPLADE-v3-DistilBERT](https://huggingface.co/naver/splade-v3-distilbert)
* [aken12/splade-japanese-v3](https://huggingface.co/aken12/splade-japanese-v3)
* [hotchpotch/japanese-splade-v2](https://huggingface.co/hotchpotch/japanese-splade-v2)

## Third party text embedding models [ml-nlp-model-ref-text-embedding]

Text Embedding models are designed to work with specific scoring functions for calculating the similarity between the embeddings they produce. Examples of typical scoring functions are: `cosine`, `dot product` and `euclidean distance` (also known as `l2_norm`).

The embeddings produced by these models should be indexed in {{es}} using the [dense vector field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) with an appropriate [similarity function](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) chosen for the model.

To find similar embeddings in {{es}} use the efficient [Approximate k-nearest neighbor (kNN)](../../../solutions/search/vector/knn.md#approximate-knn) search API with a text embedding as the query vector. Approximate kNN search uses the similarity function defined in the dense vector field mapping is used to calculate the relevance. For the best results the function must be one of the suitable similarity functions for the model.

Using `SentenceTransformerWrapper`:

* [All DistilRoBERTa v1](https://huggingface.co/sentence-transformers/all-distilroberta-v1) Suitable similarity functions:	`dot_product`, `cosine`, `l2_norm`
* [All MiniLM L12 v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2) Suitable similarity functions:	`dot_product`, `cosine`, `l2_norm`
* [**All MPNet base v2**](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) Suitable similarity functions:	`dot_product`, `cosine`, `l2_norm`
* [Facebook dpr-ctx_encoder multiset base](https://huggingface.co/sentence-transformers/facebook-dpr-ctx_encoder-multiset-base) Suitable similarity functions:	`dot_product`
* [Facebook dpr-question_encoder single nq base](https://huggingface.co/sentence-transformers/facebook-dpr-question_encoder-single-nq-base) Suitable similarity functions:	`dot_product`
* [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) Suitable similarity functions:	`cosine`
* [msmarco DistilBERT base tas b](https://huggingface.co/sentence-transformers/msmarco-distilbert-base-tas-b) Suitable similarity functions:	`dot_product`
* [msmarco MiniLM L12 v5](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) Suitable similarity functions:	`dot_product`, `cosine`, `l2_norm`
* [paraphrase mpnet base v2](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2) Suitable similarity functions:	`cosine`

Using `DPREncoderWrapper`:

* [ance dpr-context multi](https://huggingface.co/castorini/ance-dpr-context-multi)
* [ance dpr-question multi](https://huggingface.co/castorini/ance-dpr-question-multi)
* [bpr nq-ctx-encoder](https://huggingface.co/castorini/bpr-nq-ctx-encoder)
* [bpr nq-question-encoder](https://huggingface.co/castorini/bpr-nq-question-encoder)
* [dpr-ctx_encoder single nq base](https://huggingface.co/facebook/dpr-ctx_encoder-single-nq-base)
* [dpr-ctx_encoder multiset base](https://huggingface.co/facebook/dpr-ctx_encoder-multiset-base)
* [dpr-question_encoder single nq base](https://huggingface.co/facebook/dpr-question_encoder-single-nq-base)
* [dpr-question_encoder multiset base](https://huggingface.co/facebook/dpr-question_encoder-multiset-base)

## Third party text classification models [ml-nlp-model-ref-text-classification]

* [BERT base uncased emotion](https://huggingface.co/nateraw/bert-base-uncased-emotion)
* [DehateBERT mono english](https://huggingface.co/Hate-speech-CNERG/dehatebert-mono-english)
* [DistilBERT base uncased emotion](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion)
* [DistilBERT base uncased finetuned SST-2](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)
* [FinBERT](https://huggingface.co/ProsusAI/finbert)
* [Twitter roBERTa base for Sentiment Analysis](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)

## Third party text similarity models [ml-nlp-model-ref-text-similarity]

You can use these text similarity models for [semantic re-ranking](../../../solutions/search/ranking/semantic-reranking.md#semantic-reranking-in-es).

* [ms marco TinyBERT L2 v2](https://huggingface.co/cross-encoder/ms-marco-TinyBERT-L-2-v2)
* [ms marco MiniLM L6 v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)
* [BAAI/bge-reranker-base](https://huggingface.co/BAAI/bge-reranker-base)

## Third party zero-shot text classification models [ml-nlp-model-ref-zero-shot]

* [BART large mnli](https://huggingface.co/facebook/bart-large-mnli)
* [DistilBERT base model (uncased)](https://huggingface.co/typeform/distilbert-base-uncased-mnli)
* [**DistilBart MNLI**](https://huggingface.co/valhalla/distilbart-mnli-12-6)
* [MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices](https://huggingface.co/typeform/mobilebert-uncased-mnli)
* [NLI DistilRoBERTa base](https://huggingface.co/cross-encoder/nli-distilroberta-base)
* [NLI RoBERTa base](https://huggingface.co/cross-encoder/nli-roberta-base)
* [SqueezeBERT](https://huggingface.co/typeform/squeezebert-mnli)

## Expected model output [_expected_model_output]

Models used for each NLP task type must output tensors of a specific format to be used in the Elasticsearch NLP pipelines.

Here are the expected outputs for each task type.

### Fill mask expected model output [_fill_mask_expected_model_output]

Fill mask is a specific kind of token classification; it is the base training task of many transformer models.

For the Elastic stack’s fill mask NLP task to understand the model output, it must have a specific format. It needs to be a float tensor with `shape(<number of sequences>, <number of tokens>, <vocab size>)`.

Here is an example with a single sequence `"The capital of [MASK] is Paris"` and with vocabulary `["The", "capital", "of", "is", "Paris", "France", "[MASK]"]`.

Should output:

```json
 [
   [
     [ 0, 0, 0, 0, 0, 0, 0 ], // The
     [ 0, 0, 0, 0, 0, 0, 0 ], // capital
     [ 0, 0, 0, 0, 0, 0, 0 ], // of
     [ 0.01, 0.01, 0.3, 0.01, 0.2, 1.2, 0.1 ], // [MASK]
     [ 0, 0, 0, 0, 0, 0, 0 ], // is
     [ 0, 0, 0, 0, 0, 0, 0 ] // Paris
   ]
]
```

The predicted value here for `[MASK]` is `"France"` with a score of 1.2.

### Named entity recognition expected model output [_named_entity_recognition_expected_model_output]

Named entity recognition is a specific token classification task. Each token in the sequence is scored related to a specific set of classification labels. For the Elastic Stack, we use Inside-Outside-Beginning (IOB) tagging. Elastic supports any NER entities as long as they are IOB tagged. The default values are: "O", "B_MISC", "I_MISC", "B_PER", "I_PER", "B_ORG", "I_ORG", "B_LOC", "I_LOC".

The `"O"` entity label indicates that the current token is outside any entity. `"I"` indicates that the token is inside an entity. `"B"` indicates the beginning of an entity. `"MISC"` is a miscellaneous entity. `"LOC"` is a location. `"PER"` is a person. `"ORG"` is an organization.

The response format must be a float tensor with `shape(<number of sequences>, <number of tokens>, <number of classification labels>)`.

Here is an example with a single sequence `"Waldo is in Paris"`:

```json
 [
   [
//    "O", "B_MISC", "I_MISC", "B_PER", "I_PER", "B_ORG", "I_ORG", "B_LOC", "I_LOC"
     [ 0,  0,         0,       0.4,     0.5,     0,       0.1,     0,       0 ], // Waldo
     [ 1,  0,         0,       0,       0,       0,       0,       0,       0 ], // is
     [ 1,  0,         0,       0,       0,       0,       0,       0,       0 ], // in
     [ 0,  0,         0,       0,       0,       0,       0,       0,       1.0 ] // Paris
   ]
]
```

### Text embedding expected model output [_text_embedding_expected_model_output]

Text embedding allows for semantic embedding of text for dense information retrieval.

The output of the model must be the specific embedding directly without any additional pooling.

Eland does this wrapping for the aforementioned models. But if supplying your own, the model must output the embedding for each inferred sequence.

### Text classification expected model output [_text_classification_expected_model_output]

With text classification (for example, in tasks like sentiment analysis), the entire sequence is classified. The output of the model must be a float tensor with `shape(<number of sequences>, <number of classification labels>)`.

Here is an example with two sequences for a binary classification model of "happy" and "sad":

```json
 [
   [
//     happy, sad
     [ 0,     1], // first sequence
     [ 1,     0] // second sequence
   ]
]
```

### Zero-shot text classification expected model output [_zero_shot_text_classification_expected_model_output]

Zero-shot text classification allows text to be classified for arbitrary labels not necessarily part of the original training. Each sequence is combined with the label given some hypothesis template. The model then scores each of these combinations according to `[entailment, neutral, contradiction]`. The output of the model must be a float tensor with `shape(<number of sequences>, <number of labels>, 3)`.

Here is an example with a single sequence classified against 4 labels:

```json
 [
   [
//     entailment, neutral, contradiction
     [ 0.5,        0.1,     0.4], // first label
     [ 0,          0,       1], // second label
     [ 1,          0,       0], // third label
     [ 0.7,        0.2,     0.1] // fourth label
   ]
]
```
