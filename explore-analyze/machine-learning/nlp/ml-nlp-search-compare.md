---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-search-compare.html
---

# Search and compare text [ml-nlp-search-compare]

The {{stack-ml-features}} can generate embeddings, which you can use to search in unstructured text or compare different pieces of text.

* [Text embedding](#ml-nlp-text-embedding)
* [Text similarity](#ml-nlp-text-similarity)

## Text embedding [ml-nlp-text-embedding]

Text embedding is a task which produces a mathematical representation of text called an embedding. The {{ml}} model turns the text into an array of numerical values (also known as a *vector*). Pieces of content with similar meaning have similar representations. This means it is possible to determine whether different pieces of text are either semantically similar, different, or even opposite by using a mathematical similarity function.

This task is responsible for producing only the embedding. When the embedding is created, it can be stored in a [dense_vector](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field and used at search time. For example, you can use these vectors in a [k-nearest neighbor (kNN) search](../../../solutions/search/vector/knn.md) to achieve semantic search capabilities.

The following is an example of producing a text embedding:

```js
{
    docs: [{"text_field": "The quick brown fox jumps over the lazy dog."}]
}
...
```

The task returns the following result:

```js
...
{
    "predicted_value": [0.293478, -0.23845, ..., 1.34589e2, 0.119376]
    ...
}
...
```

## Text similarity [ml-nlp-text-similarity]

The text similarity task estimates how similar two pieces of text are to each other and expresses the similarity in a numeric value. This is commonly referred to as cross-encoding. This task is useful for ranking document text when comparing it to another provided text input.

You can provide multiple strings of text to compare to another text input sequence. Each string is compared to the given text sequence at inference time and a prediction of similarity is calculated for every string of text.

```js
{
  "docs":[{ "text_field": "Berlin has a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers."}, {"text_field": "New York City is famous for the Metropolitan Museum of Art."}],
  "inference_config": {
    "text_similarity": {
      "text": "How many people live in Berlin?"
    }
  }
}
```

In the example above, every string in the `docs` array is compared individually to the text provided in the `text_similarity`.`text` field and a predicted similarity is calculated for both as the API response shows:

```js
...
{
    "predicted_value": 7.235751628875732
},
{
    "predicted_value": -11.562295913696289
}
...
```
