---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html
applies_to:
  stack:
  serverless:
---

# Cross-cluster search [modules-cross-cluster-search]

**{{ccs-cap}}** lets you run a single search request against one or more remote clusters. For example, you can use a {{ccs}} to filter and analyze log data stored on clusters in different data centers.


## Supported APIs [ccs-supported-apis]

The following APIs support {{ccs}}:

* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Search template](search-templates.md)
* [Multi search template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [Painless execute API](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md)
* [Resolve Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index)
* [preview] [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)
* [preview] [SQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-sql-query)
* [preview] [Vector tile search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-mvt)
* [preview] [ES|QL](../../explore-analyze/query-filter/languages/esql-cross-clusters.md)


## Prerequisites [_prerequisites]

* {{ccs-cap}} requires remote clusters. To set up remote clusters, see [*Remote clusters*](../../deploy-manage/remote-clusters.md).

    To ensure your remote cluster configuration supports {{ccs}}, see [Supported {{ccs}} configurations](#ccs-supported-configurations).

* For full {{ccs}} capabilities, the local and remote cluster must be on the same [subscription level](https://www.elastic.co/subscriptions).
* The local coordinating node must have the [`remote_cluster_client`](../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#remote-node) node role.

* If you use [sniff mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode), the local coordinating node must be able to connect to seed and gateway nodes on the remote cluster.

    We recommend using gateway nodes capable of serving as coordinating nodes. The seed nodes can be a subset of these gateway nodes.


* If you use [proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode), the local coordinating node must be able to connect to the configured `proxy_address`. The proxy at this address must be able to route connections to gateway and coordinating nodes on the remote cluster.
* {{ccs-cap}} requires different security privileges on the local cluster and remote cluster. See [Configure privileges for {{ccs}}](../../deploy-manage/remote-clusters/remote-clusters-cert.md#remote-clusters-privileges-ccs) and [*Remote clusters*](../../deploy-manage/remote-clusters.md).


## {{ccs-cap}} examples [ccs-example]


### Remote cluster setup [ccs-remote-cluster-setup]

The following [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API request adds three remote clusters: `cluster_one`, `cluster_two`, and `cluster_three`.

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster_one": {
          "seeds": [
            "35.238.149.1:9300"
          ],
          "skip_unavailable": true
        },
        "cluster_two": {
          "seeds": [
            "35.238.149.2:9300"
          ],
          "skip_unavailable": false
        },
        "cluster_three": {  <1>
          "seeds": [
            "35.238.149.3:9300"
          ]
        }
      }
    }
  }
}
```

1. Since `skip_unavailable` was not set on `cluster_three`, it uses the default of `true`. See the [Optional remote clusters](#skip-unavailable-clusters) section for details.
%  TEST[setup:host]
%  TEST[s/35.238.149.\d+:930\d+/${transport_host}/]


### Search a single remote cluster [ccs-search-remote-cluster]

In the search request, you specify data streams and indices on a remote cluster as `<remote_cluster_name>:<target>`.

The following [search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) API request searches the `my-index-000001` index on a single remote cluster, `cluster_one`.

```console
GET /cluster_one:my-index-000001/_search
{
  "size": 1,
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```
%  TEST[continued]
%  TEST[setup:my_index]

The API returns the following response. Note that when you search one or more remote clusters, a `_clusters` section is included to provide information about the search on each cluster.

```console-result
{
  "took": 150,
  "timed_out": false,
  "_shards": {
    "total": 12,
    "successful": 12,
    "failed": 0,
    "skipped": 0
  },
  "_clusters": {
    "total": 1,  <1>
    "successful": 1,
    "skipped": 0,
    "running": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "cluster_one": {  <2>
        "status": "successful",
        "indices": "my-index-000001", <3>
        "took": 148,  <4>
        "timed_out": false,
        "_shards": {  <5>
          "total": 12,
          "successful": 12,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  },
  "hits": {
    "total" : {
        "value": 1,
        "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "cluster_one:my-index-000001", <6>
        "_id": "0",
        "_score": 1,
        "_source": {
          "user": {
            "id": "kimchy"
          },
          "message": "GET /search HTTP/1.1 200 1070000",
          "http": {
            "response":
              {
                "status_code": 200
              }
          }
        }
      }
    ]
  }
}
```

1. This section of counters shows all possible cluster search states and how many cluster searches are currently in that state. The clusters can be one of the following statuses: **running**, **successful** (searches on all shards were successful), **partial** (searches on at least one shard of the cluster was successful and at least one failed), **skipped** (the search failed on a cluster marked with `skip_unavailable`=`true`) or **failed** (the search failed on a cluster marked with `skip_unavailable`=`false`).
2. The `_clusters/details` section shows metadata about the search on each cluster.
3. The index expression supplied by the user. If you provide a wildcard such as `logs-*`, this section will show the value with the wildcard, not the concrete indices being searched.
4. How long (in milliseconds) the sub-search took on that cluster.
5. The shard details for the sub-search on that cluster.
6. The search response body includes the name of the remote cluster in the `_index` parameter.
%  TESTRESPONSE[s/"took": 150/"took": "$body.took"/]
%  TESTRESPONSE[s/"max_score": 1/"max_score": "$body.hits.max_score"/]
%  TESTRESPONSE[s/"_score": 1/"_score": "$body.hits.hits.0._score"/]
%  TESTRESPONSE[s/"total": 12/"total": "$body._shards.total"/]
%  TESTRESPONSE[s/"successful": 12/"successful": "$body._shards.successful"/]
%  TESTRESPONSE[s/"skipped": 0/"skipped": "$body._shards.skipped"/]
%  TESTRESPONSE[s/"took": 148/"took": "$body._clusters.details.cluster_one.took"/]


### Search multiple remote clusters [ccs-search-multi-remote-cluster]

The following [search](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search) API request searches the `my-index-000001` index on three clusters:

* The local ("querying") cluster, with 10 shards
* Two remote clusters, `cluster_one`, with 12 shards and `cluster_two` with 6 shards.

```console
GET /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_search
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```
%  TEST[continued]

The API returns the following response:

```console-result
{
  "took": 150,
  "timed_out": false,
  "num_reduce_phases": 4,
  "_shards": {
    "total": 28,
    "successful": 28,
    "failed": 0,
    "skipped": 0
  },
  "_clusters": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "running": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "(local)": {            <1>
        "status": "successful",
        "indices": "my-index-000001",
        "took": 21,
        "timed_out": false,
        "_shards": {
          "total": 10,
          "successful": 10,
          "skipped": 0,
          "failed": 0
        }
      },
      "cluster_one": {
        "status": "successful",
        "indices": "my-index-000001",
        "took": 48,
        "timed_out": false,
        "_shards": {
          "total": 12,
          "successful": 12,
          "skipped": 0,
          "failed": 0
        }
      },
      "cluster_two": {
        "status": "successful",
        "indices": "my-index-000001",
        "took": 141,
        "timed_out": false,
        "_shards": {
          "total" : 6,
          "successful" : 6,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  },
  "hits": {
    "total" : {
        "value": 3,
        "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "my-index-000001", <2>
        "_id": "0",
        "_score": 2,
        "_source": {
          "user": {
            "id": "kimchy"
          },
          "message": "GET /search HTTP/1.1 200 1070000",
          "http": {
            "response":
              {
                "status_code": 200
              }
          }
        }
      },
      {
        "_index": "cluster_one:my-index-000001", <3>
        "_id": "0",
        "_score": 1,
        "_source": {
          "user": {
            "id": "kimchy"
          },
          "message": "GET /search HTTP/1.1 200 1070000",
          "http": {
            "response":
              {
                "status_code": 200
              }
          }
        }
      },
      {
        "_index": "cluster_two:my-index-000001", <4>
        "_id": "0",
        "_score": 1,
        "_source": {
          "user": {
            "id": "kimchy"
          },
          "message": "GET /search HTTP/1.1 200 1070000",
          "http": {
            "response":
              {
                "status_code": 200
              }
          }
        }
      }
    ]
  }
}
```

1. The local (querying) cluster is identified as "(local)".
2. This document’s `_index` parameter doesn’t include a cluster name. This means the document came from the local cluster.
3. This document came from `cluster_one`.
4. This document came from `cluster_two`.
%  TESTRESPONSE[s/"took": 150/"took": "$body.took"/]
%  TESTRESPONSE[s/"max_score": 1/"max_score": "$body.hits.max_score"/]
%  TESTRESPONSE[s/"_score": 1/"_score": "$body.hits.hits.0._score"/]
%  TESTRESPONSE[s/"_score": 2/"_score": "$body.hits.hits.1._score"/]
%  TESTRESPONSE[s/"total": 28/"total": "$body._shards.total"/]
%  TESTRESPONSE[s/"successful": 28/"successful": "$body._shards.successful"/]
%  TESTRESPONSE[s/"total": 10/"total": "$body._clusters.details.(local)._shards.total"/]
%  TESTRESPONSE[s/"successful": 10/"successful": "$body._clusters.details.(local)._shards.successful"/]
%  TESTRESPONSE[s/"took": 21/"took": "$body._clusters.details.(local).took"/]
%  TESTRESPONSE[s/"total": 12/"total": "$body._clusters.details.cluster_one._shards.total"/]
%  TESTRESPONSE[s/"successful": 12/"successful": "$body._clusters.details.cluster_one._shards.successful"/]
%  TESTRESPONSE[s/"took": 48/"took": "$body._clusters.details.cluster_one.took"/]
%  TESTRESPONSE[s/"total" : 6/"total": "$body._clusters.details.cluster_two._shards.total"/]
%  TESTRESPONSE[s/"successful" : 6/"successful": "$body._clusters.details.cluster_two._shards.successful"/]
%  TESTRESPONSE[s/"took": 141/"took": "$body._clusters.details.cluster_two.took"/]


## Using async search for {{ccs}} with ccs_minimize_roundtrips=true [ccs-async-search-minimize-roundtrips-true]

Remote clusters can be queried asynchronously using the [async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) API. A {{ccs}} accepts a [`ccs_minimize_roundtrips`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-ccs_minimize_roundtrips) parameter. For asynchronous searches it defaults to `false`. (Note: for synchronous searches it defaults to `true`.) See [Considerations for choosing whether to minimize roundtrips in a {{ccs}}](#ccs-min-roundtrips) to learn more about this option.

The following request does an asynchronous search of the `my-index-000001` index using `ccs_minimize_roundtrips=true` against three clusters (same ones as the previous example).

```console
POST /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_async_search?ccs_minimize_roundtrips=true
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```
%  TEST[continued]
%  TEST[s/ccs_minimize_roundtrips=true/ccs_minimize_roundtrips=true&wait_for_completion_timeout=100ms&keep_on_completion=true/]

The API returns the following response:

```console-result
{
  "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=", <1>
  "is_partial": true,
  "is_running": true,
  "start_time_in_millis": 1685563581380,
  "expiration_time_in_millis": 1685995581380,
  "response": {
    "took": 1020,
    "timed_out": false,
    "num_reduce_phases": 0,
    "_shards": {
      "total": 10,     <2>
      "successful": 0,
      "failed": 0,
      "skipped": 0
    },
    "_clusters": {    <3>
      "total" : 3,
      "successful" : 0,
      "skipped": 0,
      "running": 3,
      "partial": 0,
      "failed": 0,
      "details": {
        "(local)": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false
        },
        "cluster_one": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false
        },
        "cluster_one": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false
        }
      }
    },
    "hits": {
      "total" : {
          "value": 0,
          "relation": "eq"
      },
      "max_score": null,
      "hits": []
    }
  }
}
```

1. The async search id.
2. When `ccs_minimize_roundtrips` = `true` and searches on the remote clusters are still running, this section indicates the number of shards in scope for the local cluster only and any clusters that have finished their search so far. This will be updated to include the total number of shards across all clusters only when the search is completed. When `ccs_minimize_roundtrips`= `false`, the total shard count across all clusters is known up front and will be correct.
3. The `_clusters` section indicates that 3 clusters are in scope for the search and all are currently in the "running" state.
%  TEST[skip: hard to reproduce initial state]

If you query the [get async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) endpoint while the query is still running, you will see an update in the `_clusters` and `_shards` section of the response as each cluster finishes its search.

If you set `ccs_minimize_roundtrips=false`, then you will also see partial aggregation results from shards (from any cluster) that have finished, but no results are shown in "hits" section until the search has completed.

If you set `ccs_minimize_roundtrips=true`, then you will also see partial results in the "hits" and "aggregations" section of the response from all clusters that have completed so far. (Note: you can also see partial aggregation results from the local cluster even before it finishes.) The example below shows the `ccs_minimize_roundtrips=true` case.

```console
GET /_async_search/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=
```
%  TEST[continued s/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=/${body.id}/]

Response:

```console-result
{
  "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
  "is_partial": true,
  "is_running": true,
  "start_time_in_millis": 1685564911108,
  "expiration_time_in_millis": 1685996911108,
  "response": {
    "took": 11164,
    "timed_out": false,
    "terminated_early": false,
    "_shards": {
      "total": 22,
      "successful": 22,  <1>
      "skipped": 0,
      "failed": 0
    },
    "_clusters": {
      "total": 3,
      "successful": 2,  <2>
      "skipped": 0,
      "running": 1,
      "partial": 0,
      "failed": 0,
      "details": {
        "(local)": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 2034,
          "timed_out": false,
          "_shards": {
            "total": 10,
            "successful": 10,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_one": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 9039,
          "timed_out": false,
          "_shards": {
            "total": 12,
            "successful": 12,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_two": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false
        }
      }
    },
    "hits": {
      "total": {
        "value": 542,  <3>
        "relation": "eq"
      },
      "max_score": 1.7232,
      "hits": [...list of hits here...]
    }
  }
}
```

1. Searches on all shards of the local cluster and remote `cluster_one` cluster have completed.
2. Since two clusters have completed the search, the "successful" clusters entry is set to 2 and "running" clusters entry is reduced to 1. The `_clusters` response metadata will be updated as each cluster finishes.
3. Number of hits from the completed searches so far. Final hits are not shown until searches on all clusters have been completed and merged. Thus, the "hits" section can change as you call this endpoint until the search is completely done.


After searches on all the clusters have completed, querying the [get async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) endpoint will show the final status of the `_clusters` and `_shards` section as well as the hits and any aggregation results.

```console
GET /_async_search/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=
```
%  TEST[continued s/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=/${body.id}/]

Response:

```console-result
{
  "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
  "is_partial": false,
  "is_running": false,
  "start_time_in_millis": 1685564911108,
  "expiration_time_in_millis": 1685996911108,
  "completion_time_in_millis": 1685564938727,  <1>
  "response": {
    "took": 27619,
    "timed_out": false,
    "num_reduce_phases": 4,
    "_shards": {
      "total": 28,
      "successful": 28,  <2>
      "skipped": 0,
      "failed": 0
    },
    "_clusters": {
      "total": 3,
      "successful": 3,   <3>
      "skipped": 0,
      "running": 0,
      "partial": 0,
      "failed": 0,
      "details": {
        "(local)": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 2034,
          "timed_out": false,
          "_shards": {
            "total": 10,
            "successful": 10,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_one": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 9039,
          "timed_out": false,
          "_shards": {
            "total": 12,
            "successful": 12,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_two": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 27550,
          "timed_out": false,
          "_shards": {
            "total": 6,
            "successful": 6,
            "skipped": 0,
            "failed": 0
          }
        }
      }
    },
    "hits": {
      "total": {
        "value": 1067,
        "relation": "eq"
      },
      "max_score": 1.8293576,
      "hits": [...list of hits here...]
    }
  }
}
```

1. Once the search has finished, the completion_time is present.
2. The `_shards` section is now updated to show that 28 total shards were searched across all clusters and that all were successful.
3. The `_clusters` section shows that searches on all 3 clusters were successful.
%  TESTRESPONSE[s/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=/$body.id/]
%  TESTRESPONSE[s/"is_partial": true/"is_partial": $body.is_partial/]
%  TESTRESPONSE[s/"is_running": true/"is_running": $body.is_running/]
%  TESTRESPONSE[s/1685564911108/$body.start_time_in_millis/]
%  TESTRESPONSE[s/1685996911108/$body.expiration_time_in_millis/]
%  TESTRESPONSE[s/1685564938727/$body.completion_time_in_millis/]
%  TESTRESPONSE[s/"took": 27619/"took": "$body.response.took"/]
%  TESTRESPONSE[s/"took": 2034/"took": "$body.$_path"/]
%  TESTRESPONSE[s/"took": 9039/"took": "$body.$_path"/]
%  TESTRESPONSE[s/"took": 27550/"took": "$body.$_path"/]
%  TESTRESPONSE[s/"total": 28/"total": $body.response._shards.total/]
%  TESTRESPONSE[s/"successful": 28/"successful": $body.response._shards.successful/]
%  TESTRESPONSE[s/"successful": 3/"successful": $body.response._clusters.successful/]
%  TESTRESPONSE[s/"value": 1067/"value": "$body.response.hits.total.value"/]
%  TESTRESPONSE[s/"relation": "eq"/"relation": "$body.response.hits.total.relation"/]
%  TESTRESPONSE[s/"max_score": 1.8293576/"max_score": "$body.response.hits.max_score"/]
%  TESTRESPONSE[s/"hits": […​list of hits here…​]/"hits": $body.response.hits.hits/]
%  TESTRESPONSE[s/"total": \d+/"total": $body.$_path/]
%  TESTRESPONSE[s/"successful": \d+/"successful": $body.$_path/]


## {{ccs-cap}} failures [cross-cluster-search-failures]

Failures during a {{ccs}} can result in one of two conditions:

1. partial results (2xx HTTP status code)
2. a failed search (4xx or 5xx HTTP status code)

Failure details will be present in the search response in both cases.

A search will be failed if a cluster marked with `skip_unavailable`=`false` is unavailable, disconnects during the search, or has search failures on all shards. In all other cases, failures will result in partial results.

Search failures on individual shards will be present in both the `_shards` section and the `_clusters` section of the response.

A failed search will have an additional top-level `errors` entry in the response.

Here is an example of a search with partial results due to a failure on one shard of one cluster. The search would be similar to ones shown previously. The `_async_search/status` endpoint is used here to show the completion status and not show the hits.

```console
GET /_async_search/status/FmpwbThueVB4UkRDeUxqb1l4akIza3cbWEJyeVBPQldTV3FGZGdIeUVabXBldzoyMDIw
```
%  TEST[continued s/FmpwbThueVB4UkRDeUxqb1l4akIza3cbWEJyeVBPQldTV3FGZGdIeUVabXBldzoyMDIw/${body.id}/]

Response:

```console-result
{
  "id": "FmpwbThueVB4UkRDeUxqb1l4akIza3cbWEJyeVBPQldTV3FGZGdIeUVabXBldzoyMDIw",
  "is_partial": true,  <1>
  "is_running": false,
  "start_time_in_millis": 1692106901478,
  "expiration_time_in_millis": 1692538901478,
  "completion_time_in_millis": 1692106903547,
  "response": {
    "took": 2069,
    "timed_out": false,
    "num_reduce_phases": 4,
    "_shards": {
      "total": 28,
      "successful": 27,
      "skipped": 0,
      "failed": 1,
      "failures": [   <2>
        {
          "shard": 1,
          "index": "cluster_two:my-index-000001",
          "node": "LMpUnAu0QEeCUMfg_56sAg",
          "reason": {
            "type": "query_shard_exception",
            "reason": "failed to create query: [my-index-000001][1] exception message here",
            "index_uuid": "4F2VWx8RQSeIhUE-nksvCQ",
            "index": "cluster_two:my-index-000001",
            "caused_by": {
              "type": "runtime_exception",
              "reason": "runtime_exception: [my-index-000001][1] exception message here"
            }
          }
        }
      ]
    },
    "_clusters": {
      "total": 3,
      "successful": 2,
      "skipped": 0,
      "running": 0,
      "partial": 1,   <3>
      "failed": 0,
      "details": {
        "(local)": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 1753,
          "timed_out": false,
          "_shards": {
            "total": 10,
            "successful": 10,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_one": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 2054,
          "timed_out": false,
          "_shards": {
            "total": 12,
            "successful": 12,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_two": {
          "status": "partial",   <4>
          "indices": "my-index-000001",
          "took": 2039,
          "timed_out": false,
          "_shards": {
            "total": 6,
            "successful": 5,
            "skipped": 0,
            "failed": 1   <5>
          },
          "failures": [  <6>
            {
              "shard": 1,
              "index": "cluster_two:my-index-000001",
              "node": "LMpUnAu0QEeCUMfg_56sAg",
              "reason": {
                "type": "query_shard_exception",
                "reason": "failed to create query: [my-index-000001][1] exception message here",
                "index_uuid": "4F2VWx8RQSeIhUE-nksvCQ",
                "index": "cluster_two:my-index-000001",
                "caused_by": {
                  "type": "runtime_exception",
                  "reason": "runtime_exception: [my-index-000001][1] exception message here"
                }
              }
            }
          ]
        }
      }
    },
    "hits": {
    }
  }
}
```

1. The search results are marked as partial, since at least one shard search failed.
2. The `_shards` section includes shard failure info.
3. Clusters that have partial results are still marked as "partial". They are marked with status "skipped" (or "failed") only if no data was returned from the search.
4. The `partial` status has been applied to the cluster with partial results.
5. The failed shard count is shown.
6. The shard failures are listed under the cluster/details entry also.
%  TEST[skip: hard to reproduce failure results]

Here is an example where both `cluster_one` and `cluster_two` lost connectivity during a {{ccs}}. Since `cluster_one` is marked as `skip_unavailable`=`true`, its status is `skipped` and since `cluster_two` is marked as `skip_unavailable`=`false`, its status is `failed`. Since there was a `failed` cluster, a top level `error` is also present and this returns an HTTP status of 500 (not shown).

If you want the search to still return results even when a cluster is unavailable, set `skip_unavailable`=`true` for all the remote clusters.

```console
GET /_async_search/FjktRGJ1Y2w1U0phLTRhZnVyeUZ2MVEbWEJyeVBPQldTV3FGZGdIeUVabXBldzo5NzA4
```
%  TEST[continued s/FjktRGJ1Y2w1U0phLTRhZnVyeUZ2MVEbWEJyeVBPQldTV3FGZGdIeUVabXBldzo5NzA4/${body.id}/]

Response:

```console-result
{
  "id": "FjktRGJ1Y2w1U0phLTRhZnVyeUZ2MVEbWEJyeVBPQldTV3FGZGdIeUVabXBldzo5NzA4",
  "is_partial": true,
  "is_running": false,
  "start_time_in_millis": 1692112102650,
  "expiration_time_in_millis": 1692544102650,
  "completion_time_in_millis": 1692112106177,
  "response": {
    "took": 3527,
    "timed_out": false,
    "terminated_early": false,
    "_shards": {
      "total": 10,   <1>
      "successful": 10,
      "skipped": 0,
      "failed": 0
    },
    "_clusters": {
      "total": 3,
      "successful": 1,
      "skipped": 1,
      "running": 0,
      "partial": 0,
      "failed": 1,
      "details": {
        "(local)": {
          "status": "successful",
          "indices": "my-index-000001",
          "took": 1473,
          "timed_out": false,
          "_shards": {
            "total": 10,
            "successful": 10,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_one": {
          "status": "skipped",   <2>
          "indices": "my-index-000001",
          "timed_out": false,
          "failures": [
            {
              "shard": -1,
              "index": null,
              "reason": {
                "type": "node_disconnected_exception",   <3>
                "reason": "[myhostname1][35.238.149.1:9300][indices:data/read/search] disconnected"
              }
            }
          ]
        },
        "cluster_two": {
          "status": "failed",   <4>
          "indices": "my-index-000001",
          "timed_out": false,
          "failures": [
            {
              "shard": -1,
              "index": null,
              "reason": {
                "type": "node_disconnected_exception",
                "reason": "[myhostname2][35.238.149.2:9300][indices:data/read/search] disconnected"
              }
            }
          ]
        }
      }
    },
    "hits": {
    },
  }
  "error": {  <5>
    "type": "status_exception",
    "reason": "error while executing search",
    "caused_by": {
      "type": "node_disconnected_exception",
      "reason": "[myhostname2][35.238.149.2:9300][indices:data/read/search] disconnected"
    }
  }
}
```

1. The shard accounting will often be only partial when errors like this occur, since we need to be able to get shard info from remote clusters on each search.
2. `cluster_one` disconnected during the search and it returned no results. Since it is marked in the remote cluster configuration as `skip_unavailable`=`true`, its status is "skipped", which will not fail the entire search.
3. The failures list shows that the remote cluster node disconnected from the querying cluster.
4. `cluster_two` status is "failed", since it is marked in the remote cluster configuration as `skip_unavailable`=`false`.
5. A top level `error` entry is included when there is a "failed" cluster.
%  TEST[skip: hard to reproduce failure results]


## Excluding clusters or indices from a {{ccs}} [exclude-problematic-clusters]

If you use a wildcard to include a large list of clusters and/or indices, you can explicitly exclude one or more clusters or indices with a `-` minus sign in front of the cluster or index.

To exclude an entire cluster, you would put the minus sign in front of the cluster alias, such as: `-mycluster:*`. When excluding a cluster, you must use `*` in the index position or an error will be returned.

To exclude a specific remote index, you would put the minus sign in front of the index, such as `mycluster:-myindex`.

**Exclude a remote cluster**

Here’s how you would exclude `cluster_three` from a {{ccs}} that uses a wildcard to specify a list of clusters:

```console
POST /my-index-000001,cluster*:my-index-000001,-cluster_three:*/_async_search  <1>
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```

1. The `cluster*` notation would naturally include `cluster_one`, `cluster_two` and `cluster_three`. To exclude `cluster_three` use a `-` before the cluster name along with a simple wildcard `*` in the index position. This indicates that you do not want the search to make any contact with `cluster_three`.
%  TEST[continued]
%  TEST[s/ccs_minimize_roundtrips=true/ccs_minimize_roundtrips=true&wait_for_completion_timeout=100ms&keep_on_completion=true/]

**Exclude a remote index**

Suppose you want to search all indices matching `my-index-*` but you want to exclude `my-index-000001` on `cluster_three`. Here’s how you could do that:

```console
POST /my-index-000001,cluster*:my-index-*,cluster_three:-my-index-000001/_async_search  <1>
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```

1. This will **not** exclude `cluster_three` from the search. It will still be contacted and told to search any indexes matching `my-index-*` except for `my-index-000001`.
%  TEST[continued]
%  TEST[s/ccs_minimize_roundtrips=true/ccs_minimize_roundtrips=true&wait_for_completion_timeout=100ms&keep_on_completion=true/]


## Using async search for {{ccs}} with ccs_minimize_roundtrips=false [ccs-async-search-minimize-roundtrips-false]

The `_shards` and `_clusters` section of the response behave differently when `ccs_minimize_roundtrips` is `false`.

Key differences are:

1. The `_shards` section total count will be accurate immediately as the total number of shards is gathered from all clusters before the search starts.
2. The `_shards` section will be incrementally updated as searches on individual shards complete, whereas when minimizing roundtrips, the shards section will be updated as searches on shards complete on the local cluster and then as each remote cluster reports back its full search results.
3. The `_cluster` section starts off listing all of its shard counts, since they are also obtained before the query phase begins.

Example using the same setup as in the previous section (`ccs_minimize_roundtrips=true`):

```console
POST /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_async_search?ccs_minimize_roundtrips=false
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  },
  "_source": ["user.id", "message", "http.response.status_code"]
}
```
%  TEST[continued]
%  TEST[s/ccs_minimize_roundtrips=false/ccs_minimize_roundtrips=false&wait_for_completion_timeout=2s&keep_on_completion=true/]

The API returns the following response if the query takes longer than the `wait_for_completion_timeout` duration (see [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)).

```console-result
{
  "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
  "is_partial": true,
  "is_running": true,
  "start_time_in_millis": 1685563581380,
  "expiration_time_in_millis": 1685995581380,
  "response": {
    "took": 1020,
    "timed_out": false,
    "_shards": {
      "total": 28,     <1>
      "successful": 0,
      "failed": 0,
      "skipped": 0
    },
    "_clusters": {
      "total" : 3,
      "successful": 0,
      "skipped": 0,
      "running": 3,    <2>
      "partial": 0,
      "failed": 0,
      "details": {    <3>
        "(local)": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false,
          "_shards": {
            "total": 10,
            "successful": 0,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_one": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false,
          "_shards": {
            "total": 12,
            "successful": 0,
            "skipped": 0,
            "failed": 0
          }
        },
        "cluster_two": {
          "status": "running",
          "indices": "my-index-000001",
          "timed_out": false,
          "_shards": {
            "total": 6,
            "successful": 0,
            "skipped": 0,
            "failed": 0
          }
        }
      }
    },
    "hits": {
      "total" : {
          "value": 0,
          "relation": "eq"
      },
      "max_score": null,
      "hits": []
    }
  }
}
```

1. All shards from all clusters in scope for the search are listed here. Watch this section and/or the _clusters section for updates to monitor search progress.
2. From the `_clusters` section we can see that all the clusters are in "running" state.
3. The `_clusters` section shows that shard information was successfully gathered from all 3 clusters and the total shard count on each cluster is listed.
%  TEST[skip: hard to reproduce intermediate results]


## Optional remote clusters [skip-unavailable-clusters]

By default, a {{ccs}} fails if a remote cluster in the request is unavailable or returns an error where the search on all shards failed. Use the `skip_unavailable` cluster setting to mark a specific remote cluster as either optional or required for {{ccs}}.

::::{important}
In Elasticsearch 8.15, the default value for `skip_unavailable` was changed from `false` to `true`. Before Elasticsearch 8.15, if you want a cluster to be treated as optional for a {{ccs}}, then you need to set that configuration. From Elasticsearch 8.15 forward, you need to set the configuration in order to make a cluster required for the {{ccs}}.
::::


If `skip_unavailable` is `true`, a {{ccs}}:

* Skips the remote cluster if its nodes are unavailable during the search. The response’s `_clusters.skipped` value contains a count of any skipped clusters and the `_clusters.details` section of the response will show a `skipped` status.
* Ignores errors returned by the remote cluster, such as errors related to unavailable shards or indices. This can include errors related to search parameters such as [`allow_no_indices`](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index) and [`ignore_unavailable`](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index).
* Ignores the [`allow_partial_search_results`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-allow_partial_search_results) parameter and the related `search.default_allow_partial_results` cluster setting when searching the remote cluster. This means searches on the remote cluster may return partial results.

You can modify the `skip_unavailable` setting by editing the `cluster.remote.<cluster_alias>` settings in the elasticsearch.yml config file. For example:

```
cluster:
    remote:
        cluster_one:
            seeds: 35.238.149.1:9300
            skip_unavailable: false
        cluster_two:
            seeds: 35.238.149.2:9300
            skip_unavailable: true
```

Or you can set the cluster.remote settings via the [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API as shown [here](#ccs-remote-cluster-setup).

When a remote cluster configured with `skip_unavailable: true` (such as `cluster_two` above) is disconnected or unavailable during a {{ccs}}, {{es}} won’t include matching documents from that cluster in the final results and the search will be considered successful (HTTP status 200 OK).

If at least one shard from a cluster provides search results, those results will be used and the search will return partial data. This is true regardless of the `skip_unavailable` setting of the remote cluster. (If doing {{ccs}} using async search, the `is_partial` field will be set to `true` to indicate partial results.)


## How {{ccs}} handles network delays [ccs-network-delays]

Because {{ccs}} involves sending requests to remote clusters, any network delays can impact search speed. To avoid slow searches, {{ccs}} offers two options for handling network delays:

[Minimize network roundtrips](#ccs-min-roundtrips)
:   By default, {{es}} reduces the number of network roundtrips between remote clusters. This reduces the impact of network delays on search speed. However, {{es}} can’t reduce network roundtrips for large search requests, such as those including a [scroll](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md#scroll-search-results) or [inner hits](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md).

    See [Considerations for choosing whether to minimize roundtrips in a {{ccs}}](#ccs-min-roundtrips) to learn how this option works.


[Don’t minimize network roundtrips](#ccs-unmin-roundtrips)
:   For search requests that include a scroll or inner hits, {{es}} sends multiple outgoing and ingoing requests to each remote cluster. You can also choose this option by setting the [`ccs_minimize_roundtrips`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) parameter to `false`. While typically slower, this approach may work well for networks with low latency.

    See [Don’t minimize network roundtrips](#ccs-unmin-roundtrips) to learn how this option works.


::::{note}
The [vector tile search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-mvt) always minimizes network roundtrips and doesn’t include the `ccs_minimize_roundtrips` parameter.
::::


::::{note}
The [Approximate kNN search](vector/knn.md#approximate-knn) doesn’t support minimizing network roundtrips, and sets the parameter `ccs_minimize_roundtrips` to `false`.
::::



### Considerations for choosing whether to minimize roundtrips in a {{ccs}} [ccs-min-roundtrips]

Advantages of minimizing roundtrips:

1. For cross-cluster searches that query a large number of shards, the minimize roundtrips option typically provides much better performance. This is especially true if the clusters being searched have high network latency (e.g., distant geographic regions).
2. When doing an async {{ccs}}, the `GET _async_search/<search_id>` endpoint will provide both top hits and aggregations from all clusters that have reported back results even while the search is still running on other clusters. In other words, it provides "incremental" partial results as the search progresses. Note that if the local cluster is included in the search, it has special handling in that it can show partial aggregations (but not partial top hits) while the search on the local cluster is still running.

Not minimizing roundtrips when using async-search allows you to get back incremental results of any aggregations in your query as individual shards complete (rather than whole clusters) while the search is still running, but top hits are not shown until the search has completed on all clusters.

By default, synchronous searches minimize roundtrips, while asynchronous searches do not. You can override the default by using the `ccs_minimize_roundtrips` parameter, setting it to either `true` or `false`, as shown in several examples earlier in this document.


### Minimize network roundtrips [ccs-min-roundtrips-true]

Here’s how {{ccs}} works when you minimize network roundtrips.

1. You send a {{ccs}} request to your local cluster. A coordinating node in that cluster receives and parses the request.

    ![ccs min roundtrip client request](../../images/elasticsearch-reference-ccs-min-roundtrip-client-request.svg "")

2. The coordinating node sends a single search request to each cluster, including the local cluster. Each cluster performs the search request independently, applying its own cluster-level settings to the request.

    ![ccs min roundtrip cluster search](../../images/elasticsearch-reference-ccs-min-roundtrip-cluster-search.svg "")

3. Each remote cluster sends its search results back to the coordinating node.

    ![ccs min roundtrip cluster results](../../images/elasticsearch-reference-ccs-min-roundtrip-cluster-results.svg "")

4. After collecting results from each cluster, the coordinating node returns the final results in the {{ccs}} response.

    ![ccs min roundtrip client response](../../images/elasticsearch-reference-ccs-min-roundtrip-client-response.svg "")



### Don’t minimize network roundtrips [ccs-unmin-roundtrips]

Here’s how {{ccs}} works when you don’t minimize network roundtrips.

1. You send a {{ccs}} request to your local cluster. A coordinating node in that cluster receives and parses the request.

    ![ccs min roundtrip client request](../../images/elasticsearch-reference-ccs-min-roundtrip-client-request.svg "")

2. The coordinating node sends a "search shards" transport layer request to each remote cluster to have them to perform a "can match" search to determine which shards on each cluster should be searched.

    ![ccs min roundtrip cluster search](../../images/elasticsearch-reference-ccs-min-roundtrip-cluster-search.svg "")

3. Each remote cluster sends its response back to the coordinating node. This response contains information about the indices and shards the {{ccs}} request will be executed on.

    ![ccs min roundtrip cluster results](../../images/elasticsearch-reference-ccs-min-roundtrip-cluster-results.svg "")

4. The coordinating node sends a search request to each shard, including those in its own cluster. Each shard performs the search request independently.

    ::::{warning}
    When network roundtrips aren’t minimized, the search is executed as if all data were in the coordinating node’s cluster. We recommend updating cluster-level settings that limit searches, such as `action.search.shard_count.limit`, `pre_filter_shard_size`, and `max_concurrent_shard_requests`, to account for this. If these limits are too low, the search may be rejected.

    ::::


    ![ccs dont min roundtrip shard search](../../images/elasticsearch-reference-ccs-dont-min-roundtrip-shard-search.svg "")

5. Each shard sends its search results back to the coordinating node.

    ![ccs dont min roundtrip shard results](../../images/elasticsearch-reference-ccs-dont-min-roundtrip-shard-results.svg "")

6. After collecting results from each cluster, the coordinating node returns the final results in the {{ccs}} response.

    ![ccs min roundtrip client response](../../images/elasticsearch-reference-ccs-min-roundtrip-client-response.svg "")



## Supported {{ccs}} configurations [ccs-supported-configurations]

In 8.0+, Elastic supports searches from a local cluster to a remote cluster running:

* The previous minor version.
* The same version.
* A newer minor version in the same major version.

Elastic also supports searches from a local cluster running the last minor version of a major version to a remote cluster running any minor version in the following major version. For example, a local 7.17 cluster can search any remote 8.x cluster.

$$$ccs-version-compatibility$$$

|     |     |
| --- | --- |
|  | Remote cluster version |
| Local cluster version | 6.8 | 7.1–7.16 | 7.17 | 8.0 | 8.1 | 8.2 | 8.3 | 8.4 | 8.5 | 8.6 | 8.7 | 8.8 | 8.9 | 8.10 | 8.11 | 8.12 | 8.13 | 8.14 | 8.15 | 8.16 | 8.17 |
| 6.8 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") |
| 7.1–7.16 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") |
| 7.17 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.0 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.1 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.2 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.3 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.4 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.5 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.6 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.7 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.8 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.9 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.10 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.11 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.12 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.13 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.14 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.15 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.16 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.17 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |

::::{important}
For the [EQL search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search), the local and remote clusters must use the same {{es}} version if they have versions prior to 7.17.7 (included) or prior to 8.5.1 (included).
::::


For example, a local 8.0 cluster can search a remote 7.17 or any remote 8.x cluster. However, a search from a local 8.0 cluster to a remote 7.16 or 6.8 cluster is not supported.

Only features that exist across all searched clusters are supported. Using a feature with a remote cluster where the feature is not supported will result in undefined behavior.

A {{ccs}} using an unsupported configuration may still work. However, such searches aren’t tested by Elastic, and their behavior isn’t guaranteed.


### Ensure {{ccs}} support [ensure-ccs-support]

The simplest way to ensure your clusters support {{ccs}} is to keep each cluster on the same version of {{es}}. If you need to maintain clusters with different versions, you can:

* Maintain a dedicated cluster for {{ccs}}. Keep this cluster on the earliest version needed to search the other clusters. For example, if you have 7.17 and 8.x clusters, you can maintain a dedicated 7.17 cluster to use as the local cluster for {{ccs}}.
* Keep each cluster no more than one minor version apart. This lets you use any cluster as the local cluster when running a {{ccs}}.


### {{ccs-cap}} during an upgrade [ccs-during-upgrade]

You can still search a remote cluster while performing a rolling upgrade on the local cluster. However, the local coordinating node’s "upgrade from" and "upgrade to" version must be compatible with the remote cluster’s gateway node.

::::{warning}
Running multiple versions of {{es}} in the same cluster beyond the duration of an upgrade is not supported.
::::


For more information about upgrades, see [Upgrading {{es}}](../../deploy-manage/upgrade/deployment-or-cluster.md).
