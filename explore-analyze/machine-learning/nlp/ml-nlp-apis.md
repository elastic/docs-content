---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-apis.html
---

# API quick reference [ml-nlp-apis]

All the trained models endpoints have the following base:

```js
/_ml/trained_models/
```

* [Create trained model aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-trained-models-aliases.html)
* [Create trained model definition part](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-trained-model-definition-part.html)
* [Create trained models](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-trained-models.html)
* [Delete trained models](https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-trained-models.html)
* [Get trained models](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-trained-models.html)
* [Get trained models statistics](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-trained-models-stats.html)
* [Infer trained model](https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-trained-model.html)
* [Start trained model deployment](https://www.elastic.co/guide/en/elasticsearch/reference/current/start-trained-model-deployment.html)
* [Stop trained model deployment](https://www.elastic.co/guide/en/elasticsearch/reference/current/stop-trained-model-deployment.html)
* [Update trained model aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-trained-models-aliases.html)

You can also integrate NLP models from different providers such as Cohere, HuggingFace, or OpenAI and use them as a service through the {{infer}} API.

The {{infer}} APIs have the following base:

```js
/_inference/
```

* [Create inference endpoint](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-inference-api.html)
* [Delete inference endpoint](https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-inference-api.html)
* [Get inference endpoint](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-inference-api.html)
* [Perform inference](https://www.elastic.co/guide/en/elasticsearch/reference/current/post-inference-api.html)
