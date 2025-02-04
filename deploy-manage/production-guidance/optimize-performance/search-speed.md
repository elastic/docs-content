---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html
---

# Search speed [tune-for-search-speed]


## Give memory to the filesystem cache [_give_memory_to_the_filesystem_cache_2] 

Elasticsearch heavily relies on the filesystem cache in order to make search fast. In general, you should make sure that at least half the available memory goes to the filesystem cache so that Elasticsearch can keep hot regions of the index in physical memory.


## Avoid page cache thrashing by using modest readahead values on Linux [_avoid_page_cache_thrashing_by_using_modest_readahead_values_on_linux] 

Search can cause a lot of randomized read I/O. When the underlying block device has a high readahead value, there may be a lot of unnecessary read I/O done, especially when files are accessed using memory mapping (see [storage types](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-store.html#file-system)).

Most Linux distributions use a sensible readahead value of `128KiB` for a single plain device, however, when using software raid, LVM or dm-crypt the resulting block device (backing Elasticsearch [path.data](../../deploy/self-managed/important-settings-configuration.md#path-settings)) may end up having a very large readahead value (in the range of several MiB). This usually results in severe page (filesystem) cache thrashing adversely affecting search (or [update](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)) performance.

You can check the current value in `KiB` using `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`. Consult the documentation of your distribution on how to alter this value (for example with a `udev` rule to persist across reboots, or via [blockdev --setra](https://man7.org/linux/man-pages/man8/blockdev.8.md) as a transient setting). We recommend a value of `128KiB` for readahead.

::::{warning} 
`blockdev` expects values in 512 byte sectors whereas `lsblk` reports values in `KiB`. As an example, to temporarily set readahead to `128KiB` for `/dev/nvme0n1`, specify `blockdev --setra 256 /dev/nvme0n1`.
::::



## Use faster hardware [search-use-faster-hardware] 

If your searches are I/O-bound, consider increasing the size of the filesystem cache (see above) or using faster storage. Each search involves a mix of sequential and random reads across multiple files, and there may be many searches running concurrently on each shard, so SSD drives tend to perform better than spinning disks.

If your searches are CPU-bound, consider using a larger number of faster CPUs.


### Local vs. remote storage [_local_vs_remote_storage_2] 

Directly-attached (local) storage generally performs better than remote storage because it is simpler to configure well and avoids communications overheads.

Some remote storage performs very poorly, especially under the kind of load that {{es}} imposes. However, with careful tuning, it is sometimes possible to achieve acceptable performance using remote storage too. Before committing to a particular storage architecture, benchmark your system with a realistic workload to determine the effects of any tuning parameters. If you cannot achieve the performance you expect, work with the vendor of your storage system to identify the problem.


## Document modeling [_document_modeling] 

Documents should be modeled so that search-time operations are as cheap as possible.

In particular, joins should be avoided. [`nested`](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html) can make queries several times slower and [parent-child](https://www.elastic.co/guide/en/elasticsearch/reference/current/parent-join.html) relations can make queries hundreds of times slower. So if the same questions can be answered without joins by denormalizing documents, significant speedups can be expected.


## Search as few fields as possible [search-as-few-fields-as-possible] 

The more fields a [`query_string`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html) or [`multi_match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html) query targets, the slower it is. A common technique to improve search speed over multiple fields is to copy their values into a single field at index time, and then use this field at search time. This can be automated with the [`copy-to`](https://www.elastic.co/guide/en/elasticsearch/reference/current/copy-to.html) directive of mappings without having to change the source of documents. Here is an example of an index containing movies that optimizes queries that search over both the name and the plot of the movie by indexing both values into the `name_and_plot` field.

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


## Pre-index data [_pre_index_data] 

You should leverage patterns in your queries to optimize the way data is indexed. For instance, if all your documents have a `price` field and most queries run [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-range-aggregation.html) aggregations on a fixed list of ranges, you could make this aggregation faster by pre-indexing the ranges into the index and using a [`terms`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) aggregations.

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

Then documents could be enriched by a `price_range` field at index time, which should be mapped as a [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html):

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

And then search requests could aggregate this new field rather than running a `range` aggregation on the `price` field.

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


## Consider mapping identifiers as `keyword` [map-ids-as-keyword] 

Not all numeric data should be mapped as a [numeric](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html) field data type. {{es}} optimizes numeric fields, such as `integer` or `long`, for [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) queries. However, [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) fields are better for [`term`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html) and other [term-level](https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html) queries.

Identifiers, such as an ISBN or a product ID, are rarely used in `range` queries. However, they are often retrieved using term-level queries.

Consider mapping a numeric identifier as a `keyword` if:

* You don’t plan to search for the identifier data using [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) queries.
* Fast retrieval is important. `term` query searches on `keyword` fields are often faster than `term` searches on numeric fields.

If you’re unsure which to use, you can use a [multi-field](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html) to map the data as both a `keyword` *and* a numeric data type.


## Avoid scripts [_avoid_scripts] 

If possible, avoid using [script](../../../explore-analyze/scripting.md)-based sorting, scripts in aggregations, and the [`script_score`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html) query. See [Scripts, caching, and search speed](../../../explore-analyze/scripting/scripts-search-speed.md).


## Search rounded dates [_search_rounded_dates] 

Queries on date fields that use `now` are typically not cacheable since the range that is being matched changes all the time. However switching to a rounded date is often acceptable in terms of user experience, and has the benefit of making better use of the query cache.

For instance the below query:

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

could be replaced with the following query:

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

In that case we rounded to the minute, so if the current time is `16:31:29`, the range query will match everything whose value of the `my_date` field is between `15:31:00` and `16:31:59`. And if several users run a query that contains this range in the same minute, the query cache could help speed things up a bit. The longer the interval that is used for rounding, the more the query cache can help, but beware that too aggressive rounding might also hurt user experience.

::::{note} 
It might be tempting to split ranges into a large cacheable part and smaller not cacheable parts in order to be able to leverage the query cache, as shown below:
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

However such practice might make the query run slower in some cases since the overhead introduced by the `bool` query may defeat the savings from better leveraging the query cache.


## Force-merge read-only indices [_force_merge_read_only_indices] 

Indices that are read-only may benefit from being [merged down to a single segment](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-forcemerge.html). This is typically the case with time-based indices: only the index for the current time frame is getting new documents while older indices are read-only. Shards that have been force-merged into a single segment can use simpler and more efficient data structures to perform searches.

::::{important} 
Do not force-merge indices to which you are still writing, or to which you will write again in the future. Instead, rely on the automatic background merge process to perform merges as needed to keep the index running smoothly. If you continue to write to a force-merged index then its performance may become much worse.
::::



## Warm up global ordinals [_warm_up_global_ordinals] 

[Global ordinals](https://www.elastic.co/guide/en/elasticsearch/reference/current/eager-global-ordinals.html) are a data structure that is used to optimize the performance of aggregations. They are calculated lazily and stored in the JVM heap as part of the [field data cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-fielddata.html). For fields that are heavily used for bucketing aggregations, you can tell {{es}} to construct and cache the global ordinals before requests are received. This should be done carefully because it will increase heap usage and can make [refreshes](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-refresh.html) take longer. The option can be updated dynamically on an existing mapping by setting the [eager global ordinals](https://www.elastic.co/guide/en/elasticsearch/reference/current/eager-global-ordinals.html) mapping parameter:

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


## Warm up the filesystem cache [_warm_up_the_filesystem_cache] 

If the machine running Elasticsearch is restarted, the filesystem cache will be empty, so it will take some time before the operating system loads hot regions of the index into memory so that search operations are fast. You can explicitly tell the operating system which files should be loaded into memory eagerly depending on the file extension using the [`index.store.preload`](https://www.elastic.co/guide/en/elasticsearch/reference/current/preload-data-to-file-system-cache.html) setting.

::::{warning} 
Loading data into the filesystem cache eagerly on too many indices or too many files will make search *slower* if the filesystem cache is not large enough to hold all the data. Use with caution.
::::



## Use index sorting to speed up conjunctions [_use_index_sorting_to_speed_up_conjunctions] 

[Index sorting](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-index-sorting.html) can be useful in order to make conjunctions faster at the cost of slightly slower indexing. Read more about it in the [index sorting documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-index-sorting-conjunctions.html).


## Use `preference` to optimize cache utilization [preference-cache-optimization] 

There are multiple caches that can help with search performance, such as the [filesystem cache](https://en.wikipedia.org/wiki/Page_cache), the [request cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html) or the [query cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-cache.html). Yet all these caches are maintained at the node level, meaning that if you run the same request twice in a row, have 1 replica or more and use [round-robin](https://en.wikipedia.org/wiki/Round-robin_DNS), the default routing algorithm, then those two requests will go to different shard copies, preventing node-level caches from helping.

Since it is common for users of a search application to run similar requests one after another, for instance in order to analyze a narrower subset of the index, using a preference value that identifies the current user or session could help optimize usage of the caches.


## Replicas might help with throughput, but not always [_replicas_might_help_with_throughput_but_not_always] 

In addition to improving resiliency, replicas can help improve throughput. For instance if you have a single-shard index and three nodes, you will need to set the number of replicas to 2 in order to have 3 copies of your shard in total so that all nodes are utilized.

Now imagine that you have a 2-shards index and two nodes. In one case, the number of replicas is 0, meaning that each node holds a single shard. In the second case the number of replicas is 1, meaning that each node has two shards. Which setup is going to perform best in terms of search performance? Usually, the setup that has fewer shards per node in total will perform better. The reason for that is that it gives a greater share of the available filesystem cache to each shard, and the filesystem cache is probably Elasticsearch’s number 1 performance factor. At the same time, beware that a setup that does not have replicas is subject to failure in case of a single node failure, so there is a trade-off between throughput and availability.

So what is the right number of replicas? If you have a cluster that has `num_nodes` nodes, `num_primaries` primary shards *in total* and if you want to be able to cope with `max_failures` node failures at once at most, then the right number of replicas for you is `max(max_failures, ceil(num_nodes / num_primaries) - 1)`.


## Tune your queries with the Search Profiler [_tune_your_queries_with_the_search_profiler] 

The [Profile API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-profile.html) provides detailed information about how each component of your queries and aggregations impacts the time it takes to process the request.

The [Search Profiler](../../../explore-analyze/query-filter/tools/search-profiler.md) in {{kib}} makes it easy to navigate and analyze the profile results and give you insight into how to tune your queries to improve performance and reduce load.

Because the Profile API itself adds significant overhead to the query, this information is best used to understand the relative cost of the various query components. It does not provide a reliable measure of actual processing time.


## Faster phrase queries with `index_phrases` [faster-phrase-queries] 

The [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) field has an [`index_phrases`](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-phrases.html) option that indexes 2-shingles and is automatically leveraged by query parsers to run phrase queries that don’t have a slop. If your use-case involves running lots of phrase queries, this can speed up queries significantly.


## Faster prefix queries with `index_prefixes` [faster-prefix-queries] 

The [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) field has an [`index_prefixes`](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-prefixes.html) option that indexes prefixes of all terms and is automatically leveraged by query parsers to run prefix queries. If your use-case involves running lots of prefix queries, this can speed up queries significantly.


## Use `constant_keyword` to speed up filtering [faster-filtering-with-constant-keyword] 

There is a general rule that the cost of a filter is mostly a function of the number of matched documents. Imagine that you have an index containing cycles. There are a large number of bicycles and many searches perform a filter on `cycle_type: bicycle`. This very common filter is unfortunately also very costly since it matches most documents. There is a simple way to avoid running this filter: move bicycles to their own index and filter bicycles by searching this index instead of adding a filter to the query.

Unfortunately this can make client-side logic tricky, which is where `constant_keyword` helps. By mapping `cycle_type` as a `constant_keyword` with value `bicycle` on the index that contains bicycles, clients can keep running the exact same queries as they used to run on the monolithic index and Elasticsearch will do the right thing on the bicycles index by ignoring filters on `cycle_type` if the value is `bicycle` and returning no hits otherwise.

Here is what mappings could look like:

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

We are splitting our index in two: one that will contain only bicycles, and another one that contains other cycles: unicycles, tricycles, etc. Then at search time, we need to search both indices, but we don’t need to modify queries.

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

On the `bicycles` index, Elasticsearch will simply ignore the `cycle_type` filter and rewrite the search request to the one below:

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

On the `other_cycles` index, Elasticsearch will quickly figure out that `bicycle` doesn’t exist in the terms dictionary of the `cycle_type` field and return a search response with no hits.

This is a powerful way of making queries cheaper by putting common values in a dedicated index. This idea can also be combined across multiple fields: for instance if you track the color of each cycle and your `bicycles` index ends up having a majority of black bikes, you could split it into a `bicycles-black` and a `bicycles-other-colors` indices.

The `constant_keyword` is not strictly required for this optimization: it is also possible to update the client-side logic in order to route queries to the relevant indices based on filters. However `constant_keyword` makes it transparently and allows to decouple search requests from the index topology in exchange of very little overhead.


## Default search timeout [_default_search_timeout] 

By default, search requests don’t time out. You can set a timeout using the [`search.default_search_timeout`](../../../solutions/search/querying-for-search.md#search-timeout) setting.

