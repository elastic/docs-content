---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/8.18/put-synonyms-set.html#put-synonyms-set-example
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Create or update synonyms set API examples [create-update-synonyms-set-api-examples]

On this page, you can find practical examples of how to create or update a synonyms set using the [Synonyms APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-synonyms). The examples below show how to create a new synonyms set, validate its rules, and explain how analyzers are reloaded automatically when the synonyms set is updated.

The following example creates a new synonyms set called `my-synonyms-set`:

```console
PUT _synonyms/my-synonyms-set
{
  "synonyms_set": [
    {
      "id": "test-1",
      "synonyms": "hello, hi"
    },
    {
      "synonyms": "bye, goodbye"
    },
    {
      "id": "test-2",
      "synonyms": "test => check"
    }
  ]
}
```

If any of the synonym rules included is not valid, the API will return an error.

```console
PUT _synonyms/my-synonyms-set
{
  "synonyms_set": [
    {
      "synonyms": "hello => hi => howdy"
    }
  ]
}
```
% TEST[catch:bad_request]

```console-result
{
  "error": {
    "root_cause": [
      {
        "type": "action_request_validation_exception",
        "reason": "Validation Failed: 1: More than one explicit mapping specified in the same synonyms rule: [hello => hi => howdy];",
        "stack_trace": ...
      }
    ],
    "type": "action_request_validation_exception",
    "reason": "Validation Failed: 1: More than one explicit mapping specified in the same synonyms rule: [hello => hi => howdy];",
    "stack_trace": ...
  },
  "status": 400
}
```
% TESTRESPONSE[s/"stack_trace": \.\.\./"stack_trace": $body.$_path/]

## Analyzer reloading [synonyms-set-analyzer-reloading]

When an existing synonyms set is updated, the [search-analyzer](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/search-analyzer) that use the synonyms set are reloaded automatically for all indices.
This would be equivalent to invoking [Reload search analyzers API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-reload-search-analyzers) for all indices that use the synonyms set.

For example, creating an index with a synonyms set and updating it:

```console-result
PUT _synonyms/my-synonyms-set
{
    "synonyms_set": [
        {
            "id": "test-1",
            "synonyms": "hello, hi"
        }
    ]
}

PUT /test-index
{
  "settings": {
    "analysis": {
      "filter": {
        "synonyms_filter": {
          "type": "synonym_graph",
          "synonyms_set": "my-synonyms-set",
          "updateable": true
        }
      },
      "analyzer": {
        "my_index_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase"]
        },
        "my_search_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "synonyms_filter"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "my_index_analyzer",
        "search_analyzer": "my_search_analyzer"
      }
    }
  }
}

PUT _synonyms/my-synonyms-set
{
    "synonyms_set": [
        {
            "id": "test-1",
            "synonyms": "hello, hi, howdy"
        }
    ]
}
```

The reloading result is included as part of the response:

```console-result
{
  "result": "updated",
  "reload_analyzers_details": {
    "_shards": {
      "total": 2,
      "successful": 1,
      "failed": 0
    },
    "reload_details": [
      {
        "index": "test-index",
        "reloaded_analyzers": [
          "my_search_analyzer"
        ],
        "reloaded_node_ids": [
          "1wYFZzq8Sxeu_Jvt9mlbkg"
        ]
      }
    ]
  }
}
```
% TESTRESPONSE[s/1wYFZzq8Sxeu_Jvt9mlbkg/$body.reload_analyzers_details.reload_details.0.reloaded_node_ids.0/]
