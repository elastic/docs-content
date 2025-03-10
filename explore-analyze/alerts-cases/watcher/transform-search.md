---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Search {{watcher-transform}}"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-search.html
---

# Search payload transform [transform-search]

A [{{watcher-transform}}](transform.md) that executes a search on the cluster and replaces the current payload in the watch execution context with the returned search response. The following snippet shows how a simple search transform can be defined on the watch level:

```js
{
  "transform" : {
    "search" : {
      "request" : {
        "body" : { "query" : { "match_all" : {} }}
      }
    }
  }
}
```
%  NOTCONSOLE

Like every other search based construct, one can make use of the full search API supported by Elasticsearch. For example, the following search {{watcher-transform}} execute a search over all events indices, matching events with `error` priority:

```js
{
  "transform" : {
    "search" : {
      "request" : {
        "indices" : [ "events-*" ],
        "body" : {
          "size" : 0,
          "query" : {
            "match" : { "priority" : "error"}
          }
        }
      }
    }
  }
}
```
%  NOTCONSOLE

## Transform search settings [transform-search-settings]

The following table lists all available settings for the search {{watcher-transform}}:

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `request.search_type` | no | query_then_fetch | The search [type](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search). |
| `request.indices` | no | all indices | One or more indices to search on. |
| `request.body` | no | `match_all` query | The body of the request. The                                                                                  [request body](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) follows                                                                                  the same structure you normally send in the body of                                                                                  a REST `_search` request. The body can be static text                                                                                  or include `mustache` [templates](how-watcher-works.md#templates). |
| `request.indices_options.expand_wildcards` | no | `open` | Determines how to expand indices wildcards. An array                                                                                  consisting of a combination of `open`, `closed`,                                                                                  and `hidden`. Alternatively a value of `none` or `all`.                                                                                  (see [multi-target syntax](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index)) |
| `request.indices_options.ignore_unavailable` | no | `true` | A boolean value that determines whether the search                                                                                  should leniently ignore unavailable indices                                                                                  (see [multi-target syntax](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index)) |
| `request.indices_options.allow_no_indices` | no | `true` | A boolean value that determines whether the search                                                                                  should leniently return no results when no indices                                                                                  are resolved (see [multi-target syntax](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index)) |
| `request.template` | no | - | The body of the search template. See                                                                                  [configure templates](how-watcher-works.md#templates) for more information. |
| `timeout` | no | 30s | The timeout for waiting for the search api call to                                                                                  return. If no response is returned within this time,                                                                                  the search {{watcher-transform}} times out and fails. This setting                                                                                  overrides the default timeouts. |

## Template support [transform-search-template]

The search {{watcher-transform}} support mustache [templates](how-watcher-works.md#templates). This can either be as part of the body definition or alternatively point to an existing template (either defined in a file or [stored](../../../solutions/search/search-templates.md#create-search-template) as a script in Elasticsearch).

For example, the following snippet shows a search that refers to the scheduled time of the watch:

```js
{
  "transform" : {
    "search" : {
      "request" : {
        "indices" : [ "logstash-*" ],
        "body" : {
          "size" : 0,
          "query" : {
            "bool" : {
              "must" : {
                "match" : { "priority" : "error"}
              },
              "filter" : [
                {
                  "range" : {
                    "@timestamp" : {
                      "gte" : "{{ctx.trigger.scheduled_time}}||-30s",
                      "lte" : "{{ctx.trigger.triggered_time}}"
                    }
                  }
                }
              ]
            }
          }
        }
      }
    }
  }
}
```
%  NOTCONSOLE

The model of the template is a union between the provided `template.params` settings and the [standard watch execution context model](how-watcher-works.md#watch-execution-context).

The following is an example of using templates that refer to provided parameters:

```js
{
  "transform" : {
    "search" : {
      "request" : {
        "indices" : [ "logstash-*" ],
        "template" : {
          "source" : {
            "size" : 0,
            "query" : {
              "bool" : {
                "must" : {
                  "match" : { "priority" : "{{priority}}"}
                },
                "filter" : [
                  {
                    "range" : {
                      "@timestamp" : {
                        "gte" : "{{ctx.trigger.scheduled_time}}||-30s",
                        "lte" : "{{ctx.trigger.triggered_time}}"
                      }
                    }
                  }
                ]
              }
            },
            "params" : {
              "priority" : "error"
            }
          }
        }
      }
    }
  }
}
```
%  NOTCONSOLE
