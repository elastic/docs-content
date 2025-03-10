---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Search input"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input-search.html
---

# Search input [input-search]

Use the `search` input to load the results of an Elasticsearch search request into the execution context when the watch is triggered. See [Search Input Attributes](#search-input-attributes) for all of the supported attributes.

In the search input’s `request` object, you specify:

* The indices you want to search
* The [search type](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* The search request body

The search request body supports the full Elasticsearch Query DSL—​it’s the same as the body of an Elasticsearch `_search` request.

For example, the following input retrieves all `event` documents from the `logs` index:

```js
"input" : {
  "search" : {
    "request" : {
      "indices" : [ "logs" ],
      "body" : {
        "query" : { "match_all" : {}}
      }
    }
  }
}
```
%  NOTCONSOLE

You can use date math and wildcards when specifying indices. For example, the following input loads the latest VIXZ quote from today’s daily quotes index:

```js
{
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "<stock-quotes-{now/d}>" ],
        "body" : {
          "size" : 1,
          "sort" : {
            "timestamp" : { "order" : "desc"}
          },
          "query" : {
            "term" : { "symbol" : "vix"}
          }
        }
      }
    }
  }
}
```
%  NOTCONSOLE

## Extracting specific fields [_extracting_specific_fields]

You can specify which fields in the search response you want to load into the watch payload with the `extract` attribute. This is useful when a search generates a large response and you are only interested in particular fields.

For example, the following input loads only the total number of hits into the watch payload:

```js
"input": {
    "search": {
      "request": {
        "indices": [ ".watcher-history*" ]
      },
      "extract": [ "hits.total.value" ]
    }
  },
```
%  NOTCONSOLE

## Using Templates [_using_templates]

The `search` input supports [search templates](../../../solutions/search/search-templates.md). For example, the following snippet references the indexed template called `my_template` and passes a value of 23 to fill in the template’s `value` parameter:

```js
{
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "logs" ],
        "template" : {
          "id" : "my_template",
          "params" : {
            "value" : 23
          }
        }
      }
    }
  }
  ...
}
```
%  NOTCONSOLE

## Applying conditions [_applying_conditions]

The `search` input is often used in conjunction with the [`script`](condition-script.md) condition. For example, the following snippet adds a condition to check if the search returned more than five hits:

```js
{
  "input" : {
    "search" : {
      "request" : {
        "indices" : [ "logs" ],
        "body" : {
          "query" : { "match_all" : {} }
        }
      }
    }
  },
  "condition" : {
    "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
  }
  ...
}
```
%  NOTCONSOLE

## Accessing the search results [_accessing_the_search_results]

Conditions, transforms, and actions can access the search results through the watch execution context. For example:

* To load all of the search hits into an email body, use `ctx.payload.hits`.
* To reference the total number of hits, use `ctx.payload.hits.total`.
* To access a particular hit, use its zero-based array index. For example, to get the third hit, use `ctx.payload.hits.hits.2`.
* To get a field value from a particular hit, use `ctx.payload.hits.hits.<index>.fields.<fieldname>`. For example, to get the message field from the first hit, use `ctx.payload.hits.hits.0.fields.message`.

::::{note}
The total number of hits in the search response is returned as an object in the response. It contains a `value`, the number of hits, and a `relation` that indicates if the value is accurate (`"eq"`) or a lower bound of the total hits that match the query (`"gte"`). You can set `track_total_hits` to true in the search request to tell Elasticsearch to always track the number of hits accurately.
::::

## Search Input Attributes [search-input-attributes]

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `request.search_type` | no | `query_then_fetch` | The [type](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) of search request to perform.                                                                                    Valid values are: `dfs_query_then_fetch` and `query_then_fetch`.                                                                                    The Elasticsearch default is `query_then_fetch`. |
| `request.indices` | no | - | The indices to search. If omitted, all indices are searched, which is the                                                                                    default behaviour in Elasticsearch. |
| `request.body` | no | - | The body of the request. The [request body](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)                                                                                    follows the same structure you normally send in the body of a REST `_search`                                                                                    request. The body can be static text or include `mustache` [templates](how-watcher-works.md#templates). |
| `request.template` | no | - | The body of the search template. See [configure templates](how-watcher-works.md#templates)                                                                                    for more information. |
| `request.indices_options.expand_wildcards` | no | `open` | How to expand wildcards. Valid values are: `all`, `open`, `closed`, and `none`                                                                                    See [`expand_wildcards`](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index) for more information. |
| `request.indices_options.ignore_unavailable` | no | `true` | Whether the search should ignore unavailable indices. See                                                                                    [`ignore_unavailable`](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index) for more information. |
| `request.indices_options.allow_no_indices` | no | `true` | Whether to allow a search where a wildcard indices expression results in no                                                                                    concrete indices. See [allow_no_indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index)                                                                                    for more information. |
| `extract` | no | - | A array of JSON keys to extract from the search response and load as the payload.                                                                                    When a search generates a large response, you can use `extract` to select the                                                                                    relevant fields instead of loading the entire response. |
| `timeout` | no | 1m | The timeout for waiting for the search api call to return. If no response is                                                                                    returned within this time, the search input times out and fails. This setting                                                                                    overrides the default search operations timeouts. |

You can reference the following variables in the execution context when specifying the request `body`:

| Name | Description |
| --- | --- |
| `ctx.watch_id` | The id of the watch that is currently executing. |
| `ctx.execution_time` | The time execution of this watch started. |
| `ctx.trigger.triggered_time` | The time this watch was triggered. |
| `ctx.trigger.scheduled_time` | The time this watch was supposed to be triggered. |
| `ctx.metadata.*` | Any metadata associated with the watch. |
