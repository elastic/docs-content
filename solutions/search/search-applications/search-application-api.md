---
navigation_title: "Search API and templates"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-application-api.html
applies_to:
  stack: beta
  serverless: beta
---



# Search API and templates [search-application-api]


Your [search applications](../search-applications.md) use [search templates](../search-templates.md) to perform searches. Templates help reduce complexity by exposing only template parameters, while using the full power of {{es}}'s query DSL to formulate queries. Templates may be set when creating or updating a search application, and can be customized. This template can be edited or updated at any time using the [Put Search Application API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-put) API call.

In a nutshell, you create search templates with parameters instead of specific hardcoded search values. At search time, you pass in the actual values for these parameters, enabling customized searches without rewriting the entire query structure. Search Application templates:

* Simplify query requests
* Reduce request size
* Ensure security and performance, as the query is predefined and can’t be changed arbitrarily

This document provides information and sample templates to get you started using [search applications](../search-applications.md) for additional use cases. These templates are designed to be easily modified to meet your needs. Once you’ve created a search application with a template, you can search your search application using this template.

::::{tip}
Search templates use the [Mustache](https://mustache.github.io/) templating language. Mustache variables are typically enclosed in double curly brackets like this: `{{my-var}}`.

Learn more by reading about [search templates](../search-templates.md).

::::



## Default template example [search-application-api-default-template]

If no template is stored with a search application, a minimal [default search template](#search-application-api-default-template) will be applied at search time. The default template implements a simple search use case.

To create a search application with the default template, issue a [create or update Search Application](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-put) request without specifying a template:

```console
PUT _application/search_application/my_search_application
{
  "indices": ["index1", "index2"]
}
```
%  TEST[warning:Using default search application template which is subject to change. We recommend storing a template to avoid breaking changes.]

You can then use the [get search application](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-get) API call to view your newly created search application, which will also include the default template that was created for you:

```console
GET _application/search_application/my_search_application
```
%  TEST[continued]
%  TEST[warning:Using default search application template which is subject to change. We recommend storing a template to avoid breaking changes.]

In this case, the response would be:

```console-result
{
  "name": "my_search_application",
  "indices": [
    "index1",
    "index2"
  ],
  "updated_at_millis": 1715802354482,
  "template": {
    "script": {
      "source": """{
  "query": {
    "query_string": {
        "query": "{{query_string}}",
        "default_field": "{{default_field}}"
        }
    }
}
""",
      "lang": "mustache",
      "params": {
        "default_field": "*",
        "query_string": "*"
      }
    }
  }
}
```
%  TESTRESPONSE[s/"updated_at_millis": 1715802354482/"updated_at_millis": $body.$_path/]

The default template is very minimal:

```console-result
{
  "template": {
    "script": {
      "source": {
        "query": {
          "query_string": {
            "query": "{{query_string}}",
            "default_field": "{{default_field}}"
          }
        }
      },
      "params": {
        "query_string": "*",
        "default_field": "*"
      }
    }
  }
}
```
%  TEST[skip:This is not a console result but NOTCONSOLE annotation by itself still fails the test]

This may be useful for initial exploration of search templates, but you’ll likely want to update this.

::::{note}
This template does not support additional parameters, including `from`, `size` or `boost`. If you need to use these, you can customize the template associated with your search application accordingly to include them as parameters.
::::


You can see the parameters and their default values by viewing the template, but it also may be valuable to view the query that will be generated if you [search your search application](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-search) with various parameters.

You can use the [render search application query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-render-query) to view the query this template would generate, including with default parameters. For example, searching the search application with no parameters:

```console
POST _application/search_application/my_search_application/_render_query
```
%  TEST[continued]

will return:

```console-result
{
  "query": {
    "query_string": {
      "query": "*",
      "default_field": "*",
      "fields": []
    }
  }
}
```
%  TEST[continued]

This uses the default parameters that were defined with the template. You can also specify one or more parameters to the render call, for example:

```console
POST _application/search_application/my_search_application/_render_query
{
  "params": {
    "query_string": "rock climbing"
  }
}
```
%  TEST[continued]

will return:

```console-result
{
  "query": {
    "query_string": {
      "query": "rock climbing",
      "default_field": "*",
      "fields": []
    }
  }
}
```
%  TEST[continued]

In this case, the `{{query_string}}` parameter has been replaced with the value `rock climbing`, and the `{{default_field}}` parameter was not specified so used the default value of `*`.

When you actually perform a search with no parameters, it will execute the underlying query that the render call returned. In this case, a search with no parameters will return all results, in a similar manner to a parameterless call to `/_search`.

```console
POST _application/search_application/my_search_application/_search
```
%  TEST[continued]

Searching with the `query_string` and/or `default_field` parameters will perform a [`query_string`](elasticsearch://reference/query-languages/query-dsl-query-string-query.md) query.

::::{warning}
The default template is subject to change in future versions of the Search Applications feature.

::::


Try some of the other examples in this document to experiment with specific use cases, or try creating your own!


## Searching a search application [search-application-api-searching]


### Template search [search-application-api-searching-templates]

The simplest way to interact with a search application is to use the search template that’s created and stored with it. Each search application has a single template associated with it, which defines search criteria, parameters and defaults.

You send search requests to a search application using the [Search Application Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-search).

With the default template, a search looks like this:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "query_string": "kayaking"
  }
}
```
%  TEST[continued]

In this example, we’ve overridden the `query_string` parameter’s default value of `*`. Since we didn’t specify `default_field` the value of this parameter will still be `*`.


### Alias search [search-application-api-searching-alias]

If you don’t want to set up a search template for your search application, an alias will be created with the same name as your search application. This may be helpful when experimenting with specific search queries that you want to use when building your search application’s search template.

If your search application’s name is `my_search_application`, your alias will be `my_search_application`. You can search this using the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search).


### Cross cluster search [search-application-cross-cluster-search]

Search applications do not currently support {{ccs}} because it is not possible to add a remote cluster’s index or index pattern to an index alias.

::::{note}
You should use the Search Applications management APIs to update your application and *not* directly use {{es}} APIs such as the alias API. For example, use [PUT Search Application](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-put) with the `indices` parameter. This will automatically keep the associated alias up to date and ensure that indices are added to the search application correctly.

::::



## Search template examples [search-application-api-examples]

We have created a number of examples to explore specific use cases. Use these as a starting point for creating your own search templates.


### Text search example [search-application-api-bm25-template]

The following template supports a `multi_match` search over specified fields and boosts:

```console
PUT _application/search_application/my_search_application
{
  "indices": ["index1", "index2"],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
      {
        "query": {
          "multi_match": {
            "query": "{{query_string}}",
            "fields": [{{#text_fields}}"{{name}}^{{boost}}",{{/text_fields}}]
          }
        },
        "explain": "{{explain}}",
        "from": "{{from}}",
        "size": "{{size}}"
      }
      """,
      "params": {
        "query_string": "*",
        "text_fields": [
          {"name": "title", "boost": 10},
          {"name": "description", "boost": 5}
        ],
        "explain": false,
        "from": 0,
        "size": 10
      }
    }
  }
}
```

A search query using this template might look like this:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "size": 5,
    "query_string": "mountain climbing",
    "text_fields": [
          {"name": "title", "boost": 10},
          {"name": "description", "boost": 2},
          {"name": "state", "boost": 1}
     ]
  }
}
```
%  TEST[continued]

The `text_fields` parameters can be overridden with new/different fields and boosts to experiment with the best configuration for your use case. This template also supports pagination and `explain` via parameters.


### Text search + ELSER with RRF [search-application-api-rrf-template]

This example supports the [reciprocal rank fusion (RRF)]](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) method for combining BM25 and [ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md) searches. Reciprocal Rank Fusion consistently improves the combined results of different search algorithms. It outperforms all other ranking algorithms, and often surpasses the best individual results, without calibration.

```console
PUT _application/search_application/my-search-app
{
  "indices": [
    "index1"
  ],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
      {
        "retriever": {
          "rrf": {
            "retrievers": [
              {{#text_fields}}
              {
                "standard": {
                  "query": {
                    "match": {
                      "{{.}}": "{{query_string}}"
                    }
                  }
                }
              },
              {{/text_fields}}
              {{#elser_fields}}
              {
                "standard": {
                  "query": {
                    "sparse_vector": {
                      "field": "ml.inference.{{.}}_expanded.predicted_value",
                      "inference_id": "<elser_inference_id>",
                      "query": "{{query_string}}"
                    }
                  }
                }
              },
              {{/elser_fields}}
            ],
            "rank_window_size": {{rrf.rank_window_size}},
            "rank_constant": {{rrf.rank_constant}}
          }
        }
      }
      """,
      "params": {
        "elser_fields": ["title", "meta_description"],
        "text_fields": ["title", "meta_description"],
        "query_string": "",
        "rrf": {
          "rank_window_size": 100,
          "rank_constant": 60
        }
      }
    }
  }
}
```

::::{note}
Replace `<elser_model_id>` with the model ID of your ELSER deployment.
::::


A sample query for this template will look like the following example:

```console
POST _application/search_application/my-search-app/_search
{
  "params": {
    "query_string": "What is the most popular brand of coffee sold in the United States?",
    "elser_fields": ["title", "meta_description"],
    "text_fields": ["title", "meta_description"],
    "rrf": {
      "rank_window_size": 50,
      "rank_constant": 25
    }
  }
}
```
%  TEST[skip:ELSER requires inference]


### Text search + ELSER [search-application-api-catchall-template]

The Elastic Learned Sparse EncodeR ([ELSER](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md)) improves search relevance through text-expansion, which enables semantic search. This experimental template requires ELSER to be enabled for one or more fields. Refer to [Semantic search with ELSER](/solutions/search/semantic-search/semantic-search-elser-ingest-pipelines.md) for more information on how to use ELSER. In this case, ELSER is enabled on the `title` and `description` fields.

This example provides a single template that you can use for various search application scenarios: text search, ELSER, or all of the above. It also provides a simple default `query_string` query if no parameters are specified.

```console
PUT _application/search_application/my_search_application
{
  "indices": [
    "index1",
    "index2"
  ],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
      {
        "query": {
          "bool": {
            "should": [
              {{#text}}
              {
                "multi_match": {
                  "query": "{{query_string}}",
                  "fields": [{{#text_fields}}"{{name}}^{{boost}}",{{/text_fields}}],
                  "boost": "{{text_query_boost}}"
                }
              },
              {{/text}}
              {{#elser}}
              {{#elser_fields}}
              {
                "sparse_vector": {
                  "field": "ml.inference.{{.}}_expanded.predicted_value",
                  "inference_id": "<elser_inference_id>",
                  "query": "{{query_string}}"
                }
              },
              {{/elser_fields}}
              { "bool": { "must": [] } },
              {{/elser}}
              {{^text}}
              {{^elser}}
              {
                "query_string": {
                  "query": "{{query_string}}",
                  "default_field": "{{default_field}}",
                  "default_operator": "{{default_operator}}",
                  "boost": "{{text_query_boost}}"
                }
              },
              {{/elser}}
              {{/text}}
              { "bool": { "must": [] } }
              ],
            "minimum_should_match": 1
          }
        },
        "min_score": "{{min_score}}",
        "explain": "{{explain}}",
        "from": "{{from}}",
        "size": "{{size}}"
      }
      """,
      "params": {
        "text": false,
        "elser": false,
        "elser_fields": [
          {"name": "title", "boost": 1},
          {"name": "description", "boost": 1}
        ],
        "text_fields": [
          {"name": "title", "boost": 10},
          {"name": "description", "boost": 5},
          {"name": "state", "boost": 1}
        ],
        "query_string": "*",
        "text_query_boost": 4,
        "default_field": "*",
        "default_operator": "OR",
        "explain": false,
        "from": 0,
        "size": 10,
        "min_score": 0
      }
    }
  }
}
```

A text search query using this template might look like this:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "text": true,
    "size": 5,
    "query_string": "mountain climbing",
    "text_fields": [
          {"name": "title", "boost": 10},
          {"name": "description", "boost": 5},
          {"name": "state", "boost": 1}
     ]
  }
}
```
%  TEST[skip:ELSER requires inference]

An ELSER search query using this template will look like the following example:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "elser": true,
    "query_string": "where is the best mountain climbing?",
    "elser_fields": [
      {"name": "title", "boost": 1},
      {"name": "description", "boost": 1}
    ]
  }
}
```
%  TEST[skip:ELSER requires inference]

A combined text search and ELSER search query using this template will look like the following example:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "elser": true,
    "text": true,
    "query_string": "where is the best mountain climbing?",
    "elser_fields": [
      {"name": "title", "boost": 1},
      {"name": "description", "boost": 1}
    ],
    "text_query_boost": 4,
    "min_score": 10
  }
}
```
%  TEST[skip:ELSER requires inference]

::::{tip}
Text search results and ELSER search results are expected to have significantly different scores in some cases, which makes ranking challenging. To find the best search result mix for your dataset, we suggest experimenting with the boost values provided in the example template:

* `text_query_boost` to boost the BM25 query as a whole
* [`boost`](elasticsearch://reference/query-languages/query-dsl-query-string-query.md#_boosting) fields to boost individual text search fields
* [`min_score`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-min_score) parameter to omit significantly low confidence results

The above boosts should be sufficient for many use cases, but there are cases when adding a [rescore](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#rescore) query or [index boost](elasticsearch://reference/elasticsearch/rest-apis/search-multiple-data-streams-indices.md#index-boost) to your template may be beneficial. Remember to update your search application to use the new template using the [put search application command](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-put).

::::


Finally, a parameterless search using this template would fall back to a default search returning all documents:

```console
POST _application/search_application/my_search_application/_search
```
%  TEST[continued]


### ELSER search [search-application-api-elser-template]

This example supports a streamlined version of ELSER search.

```console
PUT _application/search_application/my_search_application
{
  "indices": [
    "index1",
    "index2"
    ],
    "template": {
      "script": {
        "lang": "mustache",
        "source": """
        {
          "query": {
            "bool": {
              "should": [
                {{#elser_fields}}
                {
                  "sparse_vector": {
                      "field": "ml.inference.{{.}}_expanded.predicted_value",
                      "inference_id": "<elser_inference_id>",
                      "query": "{{query_string}}"
                    }
                },
                {{/elser_fields}}
                ]
            }
          },
          "min_score": "{{min_score}}"
        }
        """,
        "params": {
          "query_string": "*",
          "min_score": "10",
          "elser_fields": [
            {
              "name": "title"
            },
            {
              "name": "description"
            }
            ]
        }
      }
    }
}
```

::::{note}
Replace `<elser_model_id>` with the model ID of your ELSER deployment.
::::


A sample query for this template will look like the following example:

```console
POST _application/search_application/my_search_application/_search
  {
    "params": {
      "query_string": "Where is the best place for mountain climbing?"
    }
  }
```
%  TEST[skip:ELSER requires inference]


### kNN search [search-applications-knn-template]

This example supports [k-nearest neighbor (kNN) search](../vector/knn.md).

A template supporting exact kNN search will look like the following example:

```console
PUT _application/search_application/my_search_application
{
  "indices": [
    "index1"
  ],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
        {
          "query": {
            "script_score": {
              "query": {
                "bool": {
                  "filter": {
                    "range": {
                      "{{field}}": {
                        "{{operator}}": {{value}}
                      }
                    }
                  }
                }
              },
              "script": {
                "source": "cosineSimilarity({{#toJson}}query_vector{{/toJson}}, '{{dense_vector_field}}') + 1.0"
              }
            }
          }
        }
        """,
      "params": {
        "field": "price",
        "operator": "gte",
        "value": 1000,
        "dense_vector_field": "product-vector",
        "query_vector": []
      }
    }
  }
}
```

A search query using this template will look like the following example:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "field": "price",
    "operator": "gte",
    "value": 500
  }
}
```
%  TEST[continued]

A template supporting approximate kNN search will look like the following example:

```console
PUT _application/search_application/my_search_application
{
  "indices": [
    "index1"
  ],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
      {
          "knn": {
            "field": "{{knn_field}}",
            "query_vector": {{#toJson}}query_vector{{/toJson}},
            "k": "{{k}}",
            "num_candidates": {{num_candidates}}
          },
          "fields": {{#toJson}}fields{{/toJson}}
      }
      """,
      "params": {
        "knn_field": "image-vector",
        "query_vector": [],
        "k": 10,
        "num_candidates": 100,
        "fields": ["title", "file-type"]
      }
    }
  }
}
```

A search query using this template will look like the following example:

```console
POST _application/search_application/my_search_application/_search
{
  "params": {
    "knn_field": "image-vector",
        "query_vector": [-5, 9, -12],
        "k": 10,
        "num_candidates": 100,
        "fields": ["title", "file-type"]
  }
}
```
%  TEST[continued]

