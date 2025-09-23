---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/test-analyzer.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Test an analyzer [test-analyzer]

The [`analyze` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-analyze) is an invaluable tool for viewing the terms produced by an analyzer. A built-in analyzer can be specified inline in the request:

```console
POST _analyze
{
  "analyzer": "whitespace",
  "text":     "The quick brown fox."
}
```

The API returns the following response:

```console-result
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "quick",
      "start_offset": 4,
      "end_offset": 9,
      "type": "word",
      "position": 1
    },
    {
      "token": "brown",
      "start_offset": 10,
      "end_offset": 15,
      "type": "word",
      "position": 2
    },
    {
      "token": "fox.",
      "start_offset": 16,
      "end_offset": 20,
      "type": "word",
      "position": 3
    }
  ]
}
```

You can also test combinations of:

* A tokenizer
* Zero or more token filters
* Zero or more character filters

```console
POST _analyze
{
  "tokenizer": "standard",
  "filter":  [ "lowercase", "asciifolding" ],
  "text":      "Is this déja vu?"
}
```

The API returns the following response:

```console-result
{
  "tokens": [
    {
      "token": "is",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "this",
      "start_offset": 3,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "deja",
      "start_offset": 8,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "vu",
      "start_offset": 13,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
```

::::{admonition} Positions and character offsets
As can be seen from the output of the `analyze` API, analyzers not only convert words into terms, they also record the order or relative *positions* of each term (used for phrase queries or word proximity queries), and the start and end *character offsets* of each term in the original text (used for highlighting search snippets).

::::


Alternatively, a [`custom` analyzer](create-custom-analyzer.md) can be referred to when running the `analyze` API on a specific index:

```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "std_folded": { <1>
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_text": {
        "type": "text",
        "analyzer": "std_folded" <2>
      }
    }
  }
}

GET my-index-000001/_analyze <3>
{
  "analyzer": "std_folded", <4>
  "text":     "Is this déjà vu?"
}

GET my-index-000001/_analyze <3>
{
  "field": "my_text", <5>
  "text":  "Is this déjà vu?"
}
```

1. Define a `custom` analyzer called `std_folded`.
2. The field `my_text` uses the `std_folded` analyzer.
3. To refer to this analyzer, the `analyze` API must specify the index name.
4. Refer to the analyzer by name.
5. Refer to the analyzer used by field `my_text`.

The API returns the following response:

```console-result
{
  "tokens": [
    {
      "token": "is",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "this",
      "start_offset": 3,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "deja",
      "start_offset": 8,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "vu",
      "start_offset": 13,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
```
