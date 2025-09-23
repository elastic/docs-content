---
navigation_title: API quick reference
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-apis.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# NLP API quick reference [ml-nlp-apis]

All the trained models endpoints have the following base:

```js
/_ml/trained_models/
```

* [Create trained model aliases](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model-alias)
* [Create trained model definition part](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model-definition-part)
* [Create trained models](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model)
* [Delete trained models](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-delete-trained-model)
* [Get trained models](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models)
* [Get trained models statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models-stats)
* [Infer trained model](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-infer-trained-model)
* [Start trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment)
* [Stop trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-stop-trained-model-deployment)
* [Update trained model aliases](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model-alias)

You can also integrate NLP models from different providers such as Cohere, HuggingFace, or OpenAI and use them as a service through the {{infer}} API.

The {{infer}} APIs have the following base:

```js
/_inference/
```

* [Create inference endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put)
* [Delete inference endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-delete)
* [Get inference endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get)
* [Perform inference](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-inference)
