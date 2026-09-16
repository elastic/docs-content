---
navigation_title: Tune for search speed
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
type: how-to
description: Elasticsearch performance tuning guide covering hardware setup, index design, and query optimization techniques to reduce search latency and improve throughput.
---

# Tune Elasticsearch for search speed [tune-for-search-speed]

This page provides guidance on tuning {{es}} for faster search performance. While hardware and system-level settings play an important role, the structure of your documents and the design of your queries often have the biggest impact. Use these recommendations to optimize field mappings, caching behavior, and query design for high-throughput, low-latency search at scale.

::::{note}
Search performance in {{es}} depends on a combination of factors, including how expensive individual queries are, how many searches run in parallel, the number of indices and shards involved, and the overall sharding strategy and shard size.

These variables influence how you tune the system. For example, optimizing for a small number of complex queries differs significantly from optimizing for many lightweight, concurrent searches.

Make sure to also consider your cluster's shard count, index layout, and overall data distribution when tuning for indexing speed. Refer to [](./size-shards.md) for more details about sharding strategies and recommendations.
::::

::::{tip}
This page covers three groups of recommendations. **Cluster and hardware tuning** and **Index design and maintenance** apply to all query languages, including ES|QL. **Query DSL optimizations** applies only to Query DSL queries. If you use ES|QL, also refer to [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md).
::::


## Cluster and hardware tuning [search-speed-cluster-hardware]

These recommendations apply to all {{es}} query languages and interfaces.

### Give memory to the filesystem cache [_give_memory_to_the_filesystem_cache_2]
```yaml {applies_to}
deployment:
  self: all
  eck: all
  ece: all
```

{{es}} relies heavily on the filesystem cache to make search fast. In general, make sure that at least half the available memory goes to the filesystem cache so that {{es}} can keep hot regions of the index in physical memory.

By default, {{es}} automatically sets its [Java Virtual Machine (JVM) heap size](/deploy-manage/deploy/self-managed/important-settings-configuration.md#heap-size-settings) to follow this best practice. However, in self-managed or {{eck}} deployments, you have the flexibility to allocate even more memory to the filesystem cache, which can lead to performance improvements depending on your workload.

::::{note}
On Linux, the filesystem cache uses any memory not actively used by applications. To allocate memory to the cache, ensure that enough system memory remains available and isn't consumed by {{es}} or other processes.
::::

### Avoid page cache thrashing by using modest readahead values on Linux [_avoid_page_cache_thrashing_by_using_modest_readahead_values_on_linux]
```yaml {applies_to}
deployment:
  self: all
  eck: all
  ece: all
```

Search can cause a lot of randomized read I/O. When the underlying block device has a high readahead value, there might be a lot of unnecessary read I/O, especially when files use memory mapping (see [storage types](elasticsearch://reference/elasticsearch/index-settings/store.md#file-system)).

Most Linux distributions use a sensible readahead value of `128KiB` for a single plain device, however, when using software raid, Logical Volume Manager (LVM), or dm-crypt the resulting block device (backing {{es}} [path.data](../../deploy/self-managed/important-settings-configuration.md#path-settings)) might end up with a very large readahead value (in the range of several MiB). This usually results in severe page (filesystem) cache thrashing adversely affecting search (or [update]({{es-apis}}group/endpoint-document)) performance.

You can check the current value in `KiB` using `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`. Consult the documentation of your distribution on how to alter this value (for example with a `udev` rule to persist across reboots, or via [blockdev --setra](https://man7.org/linux/man-pages/man8/blockdev.8.html) as a transient setting). We recommend a value of `128KiB` for readahead.

::::{warning}
`blockdev` expects values in 512 byte sectors whereas `lsblk` reports values in `KiB`. As an example, to temporarily set readahead to `128KiB` for `/dev/nvme0n1`, specify `blockdev --setra 256 /dev/nvme0n1`.
::::

You can't adjust the disk readahead in {{ech}}, as the Linux kernel controls it. However, you can modify it in {{ece}}, Kubernetes, or self-managed nodes.

### Use faster hardware [search-use-faster-hardware]

If your searches are I/O-bound, consider increasing the size of the filesystem cache (see [Give memory to the filesystem cache](#_give_memory_to_the_filesystem_cache_2)) or using faster storage. Each search involves a mix of sequential and random reads across multiple files, and there might be many searches running concurrently on each shard, so solid-state drives (SSDs) tend to perform better than spinning disks.

If your searches are CPU-bound, consider using a larger number of faster CPUs.

::::{note}
In {{ech}} and {{ece}}, you can choose the underlying hardware by selecting different hardware profiles or deployment templates. Refer to [ECH → Manage hardware profiles](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) and [ECE → Manage deployment templates](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md) for more details.
::::

#### Local versus remote storage [_local_vs_remote_storage_2]
```yaml {applies_to}
deployment:
  self: all
  eck: all
  ece: all
```

{{es}} clusters using directly-attached local storage generally perform better than those using remote storage. Direct storage typically provides lower latency for I/O operations, which is more critical for most {{es}} workloads than the high throughput that remote storage can often achieve.

Some remote storage performs very poorly, especially under the kind of load that {{es}} imposes. However, on certain workloads and with careful tuning, it's sometimes possible to achieve acceptable performance using remote storage too. Before committing to a particular storage architecture, benchmark your system with a realistic workload to determine whether it meets your performance goals. If you can't achieve the performance you expect, work with the vendor of your storage system to identify suitable tuning parameter values.

::::{note}
For {{eck}} deployments refer to the [ECK storage recommendations](/deploy-manage/deploy/cloud-on-k8s/storage-recommendations.md) for a complete overview of storage options in Kubernetes, along with their implications and best practices. In Kubernetes, remote storage solutions are commonly used and well-supported.
::::

### Warm up the filesystem cache [_warm_up_the_filesystem_cache]

When the machine running {{es}} restarts, the filesystem cache is empty, so it takes some time before the operating system loads hot regions of the index into memory so that search operations are fast. You can explicitly tell the operating system which files to load into memory eagerly depending on the file extension using the [`index.store.preload`](elasticsearch://reference/elasticsearch/index-settings/preloading-data-into-file-system-cache.md) setting.

::::{warning}
Preloading data into the filesystem cache makes search *slower* if the total size of the preloaded data exceeds available RAM. Use with caution.
::::


### Replicas might help with throughput, but not always [_replicas_might_help_with_throughput_but_not_always]

In addition to improving resiliency, replicas can help improve throughput. For instance, if you have a single-shard index and three nodes, you need to set the number of replicas to two to have three copies of your shard in total so that all nodes handle requests.

Now imagine that you have a two-shards index and two nodes. In one case, the number of replicas is zero, meaning that each node holds a single shard. In the second case the number of replicas is one, meaning that each node has two shards. Which setup performs best in terms of search performance? Usually, the setup with fewer shards per node in total performs better. The reason is that it gives a greater share of the available filesystem cache to each shard, and the filesystem cache is probably Elasticsearch's number one performance factor. At the same time, beware that a setup without replicas is subject to failure in case of a single node failure, so there's a trade-off between throughput and availability.

So what's the right number of replicas? If you have a cluster that has `num_nodes` nodes, `num_primaries` primary shards *in total* and if you want to be able to cope with `max_failures` node failures at once at most, then the right number of replicas for you is `max(max_failures, ceil(num_nodes / num_primaries) - 1)`.


### Use `preference` to optimize cache utilization [preference-cache-optimization]

There are multiple caches that can help with search performance, such as the [filesystem cache](https://en.wikipedia.org/wiki/Page_cache), the [request cache](/deploy-manage/distributed-architecture/shard-request-cache.md) or the [query cache](elasticsearch://reference/elasticsearch/configuration-reference/node-query-cache-settings.md). Yet all these caches are maintained at the node level, meaning that if you run the same request twice in a row, have one replica or more and use [round-robin](https://en.wikipedia.org/wiki/Round-robin_DNS), the default routing algorithm, then those two requests go to different shard copies, preventing node-level caches from helping.

Since it's common for users of a search application to run similar requests one after another, for instance to analyze a narrower subset of the index, using a preference value that identifies the current user or session helps optimize cache usage.


### Default search timeout [_default_search_timeout]

By default, search requests don't time out. You can set a default timeout using the [`search.default_search_timeout`](/solutions/search/the-search-api.md#search-timeout) cluster setting.

### Avoid high open search contexts [_open_search_contexts]

When a [search executes](/deploy-manage/distributed-architecture/reading-and-writing-documents.md#_basic_read_model), it opens a search context on each shard, which acts as a form of read lock. This context exists during the search request, or for [scroll searches]({{es-apis}}operation/operation-scroll) during their designated timeout period. High scroll request search contexts can cause [high JVM memory pressure](/troubleshoot/elasticsearch/high-jvm-memory-pressure.md). 

To check for `open_contexts`, poll the [node stats API]({{es-apis}}/operation/operation-nodes-stats):

```console
GET _nodes/stats/indices/search
```

This value can rise when the [task queue backlog](/troubleshoot/elasticsearch/task-queue-backlog.md) reports a high amount of pending searches. If not, your [scroll search timeouts](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md#scroll-search-results) might be set too high. [Clear scrolls](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md#clear-scroll) as soon as they're no longer needed to release the context retention.


## Index design and maintenance [search-speed-index-design]

These recommendations apply to all {{es}} query languages, including ES|QL. They affect how data is stored and structured at index time, and benefit any query that runs against the index.

### Document modeling [_document_modeling]

Model documents so that search-time operations are as cheap as possible.

In particular, avoid joins. [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) can make queries several times slower and [parent-child](elasticsearch://reference/elasticsearch/mapping-reference/parent-join.md) relations can make queries hundreds of times slower. So if the same questions can be answered without joins by denormalizing documents, you can expect significant speedups.


### Search as few fields as possible [search-as-few-fields-as-possible]

The more fields a [`query_string`](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md) or [`multi_match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-multi-match-query.md) query targets, the slower it is. A common technique to improve search speed over multiple fields is to copy their values into a single field at index time, and then use this field at search time. You can automate this with the [`copy-to`](elasticsearch://reference/elasticsearch/mapping-reference/copy-to.md) directive of mappings without having to change the source of documents. Here is an example of an index containing movies that optimizes queries that search over both the name and the plot of the movie by indexing both values into the `name_and_plot` field.

```console
PUT movies
{
  "mappings": {
    "properties": {
      "name_and_plot": {
        "type": "text"
      },
      "name": {
        "type": "text",
        "copy_to": "name_and_plot"
      },
      "plot": {
        "type": "text",
        "copy_to": "name_and_plot"
      }
    }
  }
}
```

:::{note}
In the previous example, `name` and `plot` are still indexed individually alongside `name_and_plot`, which adds storage overhead for each source field. If you don't need to search those fields individually, you can avoid this by setting `"index": false` on them. See [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md) for more on using `copy_to` to reduce per-field mapping overhead.
:::

### Pre-index data [_pre_index_data]

Leverage patterns in your queries to optimize the way data is indexed. For instance, if all your documents have a `price` field and most queries run [`range`](elasticsearch://reference/aggregations/search-aggregations-bucket-range-aggregation.md) aggregations on a fixed list of ranges, you can make this aggregation faster by pre-indexing the ranges into the index and using a [`terms`](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) aggregation.

For instance, if documents look like:

```console
PUT index/_doc/1
{
  "designation": "spoon",
  "price": 13
}
```

and search requests look like:

```console
GET index/_search
{
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 10 },
          { "from": 10, "to": 100 },
          { "from": 100 }
        ]
      }
    }
  }
}
```

Then enrich documents with a `price_range` field at index time, mapping it as a [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md):

```console
PUT index
{
  "mappings": {
    "properties": {
      "price_range": {
        "type": "keyword"
      }
    }
  }
}

PUT index/_doc/1
{
  "designation": "spoon",
  "price": 13,
  "price_range": "10-100"
}
```

Then search requests can aggregate this new field rather than running a `range` aggregation on the `price` field.

```console
GET index/_search
{
  "aggs": {
    "price_ranges": {
      "terms": {
        "field": "price_range"
      }
    }
  }
}
```

### Consider mapping identifiers as `keyword` [map-ids-as-keyword]

Not all numeric data needs to be mapped as a [numeric](elasticsearch://reference/elasticsearch/mapping-reference/number.md) field data type. {{es}} optimizes numeric fields, such as `integer` or `long`, for [`range`](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) queries. However, [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) fields are better for [`term`](elasticsearch://reference/query-languages/query-dsl/query-dsl-term-query.md) and other [term-level](elasticsearch://reference/query-languages/query-dsl/term-level-queries.md) queries.

Identifiers, such as an International Standard Book Number (ISBN) or a product ID, are rarely used in `range` queries. However, they're often retrieved using term-level queries.

Consider mapping a numeric identifier as a `keyword` if:

* You don't plan to search for the identifier data using [`range`](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) queries.
* Fast retrieval is important. `term` query searches on `keyword` fields are often faster than `term` searches on numeric fields.

If you're unsure which to use, you can use a [multi-field](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) to map the data as both a `keyword` *and* a numeric data type.


### Use `constant_keyword` to speed up filtering [faster-filtering-with-constant-keyword]

There is a general rule that the cost of a filter is mostly a function of the number of matched documents. Imagine that you have an index containing cycles. There are many bicycles and many searches perform a filter on `cycle_type: bicycle`. This very common filter is unfortunately also very costly since it matches most documents. One efficient approach is to avoid running this filter: move bicycles to their own index and filter bicycles by searching this index instead of adding a filter to the query.

Unfortunately this can make client-side logic tricky, which is where `constant_keyword` helps. By mapping `cycle_type` as a `constant_keyword` with value `bicycle` on the index that contains bicycles, clients can keep running the exact same queries as they used to run on the monolithic index and {{es}} does the right thing on the bicycles index by ignoring filters on `cycle_type` if the value is `bicycle` and returning no hits otherwise.

Example mappings:

```console
PUT bicycles
{
  "mappings": {
    "properties": {
      "cycle_type": {
        "type": "constant_keyword",
        "value": "bicycle"
      },
      "name": {
        "type": "text"
      }
    }
  }
}

PUT other_cycles
{
  "mappings": {
    "properties": {
      "cycle_type": {
        "type": "keyword"
      },
      "name": {
        "type": "text"
      }
    }
  }
}
```

We're splitting our index in two: one that contains only bicycles, and another one that contains other cycles: unicycles, tricycles, and so on. At search time, we need to search both indices, but we don't need to modify queries.

```console
GET bicycles,other_cycles/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "description": "dutch"
        }
      },
      "filter": {
        "term": {
          "cycle_type": "bicycle"
        }
      }
    }
  }
}
```

On the `bicycles` index, {{es}} ignores the `cycle_type` filter and rewrites the search request to the following query:

```console
GET bicycles,other_cycles/_search
{
  "query": {
    "match": {
      "description": "dutch"
    }
  }
}
```

On the `other_cycles` index, {{es}} quickly figures out that `bicycle` doesn't exist in the terms dictionary of the `cycle_type` field and returns a search response with no hits.

This is a powerful way of making queries cheaper by putting common values in a dedicated index. This idea can also combine across multiple fields: for instance if you track the color of each cycle and your `bicycles` index ends up with a majority of black bikes, you can split it into a `bicycles-black` and a `bicycles-other-colors` index.

`constant_keyword` isn't strictly required for this optimization: it's also possible to update the client-side logic to route queries to the relevant indices based on filters. However `constant_keyword` does this transparently and allows you to decouple search requests from the index topology in exchange for very little overhead.

`constant_keyword` shard-skipping also applies to ES|QL queries: {{es}} runs a `can_match` phase with pushed-down filters, and `constant_keyword` allows entire shards to skip before execution begins.

### Use index sorting to speed up conjunctions [_use_index_sorting_to_speed_up_conjunctions]

[Index sorting](elasticsearch://reference/elasticsearch/index-settings/sorting.md) can make conjunctions faster at the cost of slightly slower indexing. Read more about it in the [index sorting documentation](elasticsearch://reference/elasticsearch/index-settings/sorting-conjunctions.md).

Index sorting also benefits ES|QL queries. When the query sort order is congruent with the index sort, Lucene stops scanning each segment early, which significantly reduces the number of documents scanned.

### Faster phrase queries with `index_phrases` [faster-phrase-queries]

The [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) field has an [`index_phrases`](elasticsearch://reference/elasticsearch/mapping-reference/index-phrases.md) option that indexes two-term word combinations (shingles) and is automatically leveraged by query parsers to run phrase queries that don't have a slop. If your use-case involves running lots of phrase queries, this can speed up queries significantly.

This optimization also applies to ES|QL `MATCH_PHRASE` calls, which emit standard phrase queries internally.

::::{note}
If your field uses [`match_only_text`](elasticsearch://reference/elasticsearch/mapping-reference/match-only-text.md) instead of `text`, phrase queries run slower because positions are read from `_source` rather than the index. `index_phrases` has no effect on `match_only_text` fields.
::::

### Force-merge read-only indices [_force_merge_read_only_indices]

Indices that are read-only might benefit from being [merged down to a single segment]({{es-apis}}operation/operation-indices-forcemerge). This is typically the case with time-based indices: only the index for the current time frame gets new documents while older indices are read-only. Shards that have been force-merged into a single segment can use more efficient data structures to perform searches.

::::{important}
Don't force-merge indices to which you're still writing, or to which you plan to write again in the future. Instead, rely on the automatic background merge process to perform merges as needed to keep the index running smoothly. If you continue to write to a force-merged index then its performance might become much worse.
::::


## Query DSL optimizations [search-speed-query-dsl]

The following recommendations apply only to [Query DSL](elasticsearch://reference/query-languages/querydsl.md) queries. If you use ES|QL or another query interface, refer to [Other query languages](#search-speed-other-languages) in this guide.

### Avoid scripts [_avoid_scripts]

If possible, avoid using [script](../../../explore-analyze/scripting.md)-based sorting, scripts in aggregations, and the [`script_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) query. See [Scripts, caching, and search speed](../../../explore-analyze/scripting/scripts-search-speed.md).


### Search rounded dates [_search_rounded_dates]

Queries on date fields that use `now` are typically not cacheable since the range that matches changes all the time. However switching to a rounded date is often acceptable in terms of user experience, and has the benefit of making better use of the query cache.

For example, the following query:

```console
PUT index/_doc/1
{
  "my_date": "2016-05-11T16:30:55.328Z"
}

GET index/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "range": {
          "my_date": {
            "gte": "now-1h",
            "lte": "now"
          }
        }
      }
    }
  }
}
```

can be replaced with the following query:

```console
GET index/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "range": {
          "my_date": {
            "gte": "now-1h/m",
            "lte": "now/m"
          }
        }
      }
    }
  }
}
```

In that case we rounded to the minute, so if the current time is `16:31:29`, the range query matches everything whose value of the `my_date` field is between `15:31:00` and `16:31:59`. And if several users run a query that contains this range in the same minute, the query cache helps speed things up a bit. The longer the interval that's used for rounding, the more the query cache can help, but beware that too aggressive rounding might also hurt user experience.

::::{note}
It might be tempting to split ranges into a large cacheable part and smaller not cacheable parts to use the query cache, as shown in the following example:
::::


```console
GET index/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "bool": {
          "should": [
            {
              "range": {
                "my_date": {
                  "gte": "now-1h",
                  "lte": "now-1h/m"
                }
              }
            },
            {
              "range": {
                "my_date": {
                  "gt": "now-1h/m",
                  "lt": "now/m"
                }
              }
            },
            {
              "range": {
                "my_date": {
                  "gte": "now/m",
                  "lte": "now"
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

However such practice sometimes makes the query run slower since the overhead introduced by the `bool` query might defeat the savings from better using the query cache.

::::{note}
ES|QL applies its own equivalent date-rounding optimization automatically during query planning.
::::


### Faster prefix queries with `index_prefixes` [faster-prefix-queries]

The [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) field has an [`index_prefixes`](elasticsearch://reference/elasticsearch/mapping-reference/index-prefixes.md) option that indexes term prefixes within a configurable length range (two to five characters by default) and is automatically leveraged by query parsers to run prefix queries. If your use-case involves running lots of prefix queries, this can speed up queries significantly.


### Warm up global ordinals [_warm_up_global_ordinals]

[Global ordinals](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md) are a data structure that optimizes the performance of aggregations. {{es}} calculates them lazily and stores them in the JVM heap as part of the [field data cache](elasticsearch://reference/elasticsearch/configuration-reference/field-data-cache-settings.md). For fields that are heavily used for bucketing aggregations, you can tell {{es}} to construct and cache the global ordinals before requests arrive. Do this carefully because it increases heap usage and can make [refreshes]({{es-apis}}operation/operation-indices-refresh) take longer. Update the option dynamically on an existing mapping by setting the [eager global ordinals](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md) mapping parameter:

```console
PUT index
{
  "mappings": {
    "properties": {
      "foo": {
        "type": "keyword",
        "eager_global_ordinals": true
      }
    }
  }
}
```

::::{note}
Query DSL `terms`, `composite`, `significant_terms`, and `diversified_sampler` aggregations use global ordinals. ES|QL `STATS BY` uses a separate grouping implementation and doesn't benefit from eager global ordinals.
::::


### Tune your queries with the Search Profiler [_tune_your_queries_with_the_search_profiler]

The [Profile API](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md) provides detailed information about how each component of your queries and aggregations impacts the time it takes to process the request.

The [Search Profiler](../../../explore-analyze/query-filter/tools/search-profiler.md) in {{kib}} helps you navigate and analyze the profile results and gives you insight into how to tune your queries to improve performance and reduce load.

Because the Profile API itself adds significant overhead to the query, this information is best used to understand the relative cost of the various query components. It doesn't provide a reliable measure of actual processing time.

::::{note}
ES|QL has its own profiling mechanism. Set `"profile": true` in the ES|QL request body. Refer to [Profile API responses](elasticsearch://reference/query-languages/esql/esql-query-performance.md#profile-api-responses) in the ES|QL performance guide.
::::


## Other query languages [search-speed-other-languages]

The sections above cover optimizations for all query languages and for Query DSL specifically. For guidance specific to other query languages, refer to the following resources.

### Optimize {{esql}} queries [_optimize_esql_queries]

For {{esql}}-specific performance guidance, including common anti-patterns and techniques for reducing scan size, refer to [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md).

### Event Query Language (EQL)

For Event Query Language (EQL)-specific performance guidance, including how functions affect search performance and when to pre-index data, refer to [How functions impact search performance](elasticsearch://reference/query-languages/eql/eql-syntax.md#eql-how-functions-impact-search-performance).
