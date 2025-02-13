---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/aliases.html
---

# Aliases [aliases]

An alias points to one or more indices or data streams. Most {{es}} APIs accept an alias in place of a data stream or index name.

Aliases enable you to:

* Query multiple indices/data streams together with a single name
* Change which indices/data streams your application uses in real time
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) data without downtime


## Alias types [alias-types]

There are two types of aliases:

* A **data stream alias** points to one or more data streams.
* An **index alias** points to one or more indices.

An alias cannot point to both data streams and indices. You also cannot add a data stream’s backing index to an index alias.


## Add an alias [add-alias]

To add an existing data stream or index to an alias, use the [aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases)'s `add` action. If the alias doesn’t exist, the request creates it.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-nginx.access-prod",
        "alias": "logs"
      }
    }
  ]
}
```

The API’s `index` and `indices` parameters support wildcards (`*`). Wildcard patterns that match both data streams and indices return an error.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-*",
        "alias": "logs"
      }
    }
  ]
}
```


## Remove an alias [remove-alias]

To remove an alias, use the aliases API’s `remove` action.

```console
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "logs-nginx.access-prod",
        "alias": "logs"
      }
    }
  ]
}
```


## Multiple actions [multiple-actions]

You can use the aliases API to perform multiple actions in a single atomic operation.

For example, the `logs` alias points to a single data stream. The following request swaps the stream for the alias. During this swap, the `logs` alias has no downtime and never points to both streams at the same time.

```console
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "logs-nginx.access-prod",
        "alias": "logs"
      }
    },
    {
      "add": {
        "index": "logs-my_app-default",
        "alias": "logs"
      }
    }
  ]
}
```


## Multiple action results [multiple-action-results]

When using multiple actions, if some succeed and some fail, a list of per-action results will be returned.

Consider a similar action list to the previous example, but now with an alias `log-non-existing`, which does not yet exist. In this case, the `remove` action will fail, but the `add` action will succeed. The response will contain the list `action_results`, with a result for every requested action.

```console
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "index1",
        "alias": "logs-non-existing"
      }
    },
    {
      "add": {
        "index": "index2",
        "alias": "logs-non-existing"
      }
    }
  ]
}
```

The API returns the following result:

```console-result
{
  "acknowledged": true,
  "errors": true,
  "action_results": [
    {
      "action": {
        "type": "remove",
        "indices": [ "index1" ],
        "aliases": [ "logs-non-existing" ],
      },
      "status": 404,
      "error": {
        "type": "aliases_not_found_exception",
        "reason": "aliases [logs-non-existing] missing",
        "resource.type": "aliases",
        "resource.id": "logs-non-existing"
      }
    },
    {
      "action": {
        "type": "add",
        "indices": [ "index2" ],
        "aliases": [ "logs-non-existing" ],
      },
      "status": 200
    }
  ]
}
```

Allowing the action list to succeed partially may not provide the desired result. It may be more appropriate to set `must_exist` to `true`, which will cause the entire action list to fail if a single action fails.


## Add an alias at index creation [add-alias-at-creation]

You can also use a [component](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) or [index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to add index or data stream aliases when they are created.

```console
# Component template with index aliases
PUT _component_template/my-aliases
{
  "template": {
    "aliases": {
      "my-alias": {}
    }
  }
}

# Index template with index aliases
PUT _index_template/my-index-template
{
  "index_patterns": [
    "my-index-*"
  ],
  "composed_of": [
    "my-aliases",
    "my-mappings",
    "my-settings"
  ],
  "template": {
    "aliases": {
      "yet-another-alias": {}
    }
  }
}
```

You can also specify index aliases in [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) requests.

```console
# PUT <my-index-{now/d}-000001>
PUT %3Cmy-index-%7Bnow%2Fd%7D-000001%3E
{
  "aliases": {
    "my-alias": {}
  }
}
```


## View aliases [view-aliases]

To get a list of your cluster’s aliases, use the [get alias API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-alias) with no argument.

```console
GET _alias
```

Specify a data stream or index before `_alias` to view its aliases.

```console
GET my-data-stream/_alias
```

Specify an alias after `_alias` to view its data streams or indices.

```console
GET _alias/logs
```


## Write index [write-index]

You can use `is_write_index` to specify a write index or data stream for an alias. {{es}} routes any write requests for the alias to this index or data stream.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-nginx.access-prod",
        "alias": "logs"
      }
    },
    {
      "add": {
        "index": "logs-my_app-default",
        "alias": "logs",
        "is_write_index": true
      }
    }
  ]
}
```

If an alias points to multiple indices or data streams and `is_write_index` isn’t set, the alias rejects write requests. If an index alias points to one index and `is_write_index` isn’t set, the index automatically acts as the write index. Data stream aliases don’t automatically set a write data stream, even if the alias points to one data stream.

::::{tip}
We recommend using data streams to store append-only time series data. If you need to update or delete existing time series data, you can perform update or delete operations directly on the data stream backing index. If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. See [Manage time series data without data streams](../lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams).
::::



## Filter an alias [filter-alias]

The `filter` option uses [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md) to limit the documents an alias can access.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-index-2099.05.06-000001",
        "alias": "my-alias",
        "filter": {
          "bool": {
            "filter": [
              {
                "range": {
                  "@timestamp": {
                    "gte": "now-1d/d",
                    "lt": "now/d"
                  }
                }
              },
              {
                "term": {
                  "user.id": "kimchy"
                }
              }
            ]
          }
        }
      }
    }
  ]
}
```

::::{note}
Filters are only applied when using the [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md), and are not applied when [retrieving a document by ID](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get).
::::



## Routing [alias-routing]

Use the `routing` option to [route](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-routing-field.html) requests for an alias to a specific shard. This lets you take advantage of [shard caches](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html) to speed up searches. Data stream aliases do not support routing options.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-index-2099.05.06-000001",
        "alias": "my-alias",
        "routing": "1"
      }
    }
  ]
}
```

Use `index_routing` and `search_routing` to specify different routing values for indexing and search. If specified, these options overwrite the `routing` value for their respective operations.

```console
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-index-2099.05.06-000001",
        "alias": "my-alias",
        "search_routing": "1",
        "index_routing": "2"
      }
    }
  ]
}
```


## Remove an index [remove-index]

To remove an index, use the aliases API’s `remove_index` action.

```console
POST _aliases
{
  "actions": [
    {
      "remove_index": {
        "index": "my-index-2099.05.06-000001"
      }
    }
  ]
}
```
