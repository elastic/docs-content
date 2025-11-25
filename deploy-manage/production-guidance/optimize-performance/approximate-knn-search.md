---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-knn-search.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
---

# Tune approximate kNN search [tune-knn-search]

{{es}} supports [approximate k-nearest neighbor search](../../../solutions/search/vector/knn.md#approximate-knn) for efficiently finding the *k* nearest vectors to a query vector. Since approximate kNN search works differently from other queries, there are special considerations around its performance.

Many of these recommendations help improve search speed. With approximate kNN, the indexing algorithm runs searches under the hood to create the vector index structures. So these same recommendations also help with indexing speed.


## Reduce vector memory foot-print [_reduce_vector_memory_foot_print]

The default [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-element-type) is `float`. But this can be automatically quantized during index time through [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization). Quantization will reduce the required memory by 4x, 8x, or as much as 32x, but it will also reduce the precision of the vectors and increase disk usage for the field (by up to 25%, 12.5%, or 3.125%, respectively). Increased disk usage is a result of {{es}} storing both the quantized and the unquantized vectors. For example, when int8 quantizing 40GB of floating point vectors an extra 10GB of data will be stored for the quantized vectors. The total disk usage amounts to 50GB, but the memory usage for fast search will be reduced to 10GB.

For `float` vectors with `dim` greater than or equal to `384`, using a [`quantized`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) index is highly recommended.


## Reduce vector dimensionality [_reduce_vector_dimensionality]

The speed of kNN search scales linearly with the number of vector dimensions, because each similarity computation considers each element in the two vectors. Whenever possible, it’s better to use vectors with a lower dimension. Some embedding models come in different "sizes", with both lower and higher dimensional options available. You could also experiment with dimensionality reduction techniques like PCA. When experimenting with different approaches, it’s important to measure the impact on relevance to ensure the search quality is still acceptable.


## Exclude vector fields from `_source` [_exclude_vector_fields_from_source]

{{es}} stores the original JSON document that was passed at index time in the [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md). By default, each hit in the search results contains the full document `_source`. When the documents contain high-dimensional `dense_vector` fields, the `_source` can be quite large and expensive to load. This could significantly slow down the speed of kNN search.

::::{note}
[reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex), [update](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update), and [update by query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) operations generally require the `_source` field. Disabling `_source` for a field might result in unexpected behavior for these operations. For example, reindex might not actually contain the `dense_vector` field in the new index.
::::


You can disable storing `dense_vector` fields in the `_source` through the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) mapping parameter. This prevents loading and returning large vectors during search, and also cuts down on the index size. Vectors that have been omitted from `_source` can still be used in kNN search, since it relies on separate data structures to perform the search. Before using the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) parameter, make sure to review the downsides of omitting fields from `_source`.

Another option is to use  [synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source).


## Ensure data nodes have enough memory [_ensure_data_nodes_have_enough_memory]

{{es}} uses either the Hierarchical Navigable Small World([HNSW](https://arxiv.org/abs/1603.09320)) algorithm or the Disk Better Binary Quantization ([DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) algorithm for approximate kNN search. 

HNSW is a graph-based algorithm which only works efficiently when most vector data is held in memory. You should ensure that data nodes have at least enough RAM to hold the vector data and index structures.

DiskBBQ is a clustering algorithm which can scale effeciently often on less memory than HNSW.  Where HNSW typically performs poorly without sufficient memory to fit the entire structure in RAM, DiskBBQ scales linearly when using less available memory than the total index size. You can start with enough RAM to hold the vector data and index structures but, in most cases, you should be able to reduce your RAM allocation and still maintain good performance. In testing as little as 1-5% of the index structure size (centroids and quantized vector data) loaded in off-heap RAM is necessary for reasonable performance for each set of queries that accesses largely overlapping clusters.  

To check the size of the vector data, you can use the [Analyze index disk usage](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-disk-usage) API.

Here are estimates for different element types and quantization levels:

* `element_type: float`: `num_vectors * num_dimensions * 4`
* `element_type: float` with `quantization: int8`: `num_vectors * (num_dimensions + 4)`
* `element_type: float` with `quantization: int4`: `num_vectors * (num_dimensions/2 + 4)`
* `element_type: float` with `quantization: bbq`: `num_vectors * (num_dimensions/8 + 14)`
* `element_type: byte`: `num_vectors * num_dimensions`
* `element_type: bit`: `num_vectors * (num_dimensions/8)`

If utilizing HNSW, the graph must also be in memory, to estimate the required bytes use `num_vectors * 4 * HNSW.m`. The default value for `HNSW.m` is 16, so by default `num_vectors * 4 * 16`.

If utilizing DiskBBQ, a fraction of the clusters and centroids will need to be in memory.  When doing this estimation it makes more sense to include both the index structure and the quantized vectors together as the structures are dependent. To estimate the total bytes we compute the cost of the centroids as `num_clusters * num_dimensions * 4 + num_clusters * (num_dimensions + 14)` plus the cost of the quantized vectors within the clusters as `num_vectors * ((num_dimensions/8 + 14 + 2) * 2)` where `num_clusters` is defined as `num_vectors / vectors_per_cluster` which by default will be `num_vectors / 384`

Note that the required RAM is for the filesystem cache, which is separate from the Java heap.

The data nodes should also leave a buffer for other ways that RAM is needed. For example your index might also include text fields and numerics, which also benefit from using filesystem cache. It’s recommended to run benchmarks with your specific dataset to ensure there’s a sufficient amount of memory to give good search performance. You can find [here](https://elasticsearch-benchmarks.elastic.co/#tracks/so_vector) and [here](https://elasticsearch-benchmarks.elastic.co/#tracks/dense_vector) some examples of datasets and configurations that we use for our nightly benchmarks.


## Warm up the filesystem cache [dense-vector-preloading]

If the machine running {{es}} is restarted, the filesystem cache will be empty, so it will take some time before the operating system loads hot regions of the index into memory so that search operations are fast. You can explicitly tell the operating system which files should be loaded into memory eagerly depending on the file extension using the [`index.store.preload`](elasticsearch://reference/elasticsearch/index-settings/preloading-data-into-file-system-cache.md) setting.

::::{warning}
Loading data into the filesystem cache eagerly on too many indices or too many files will make search *slower* if the filesystem cache is not large enough to hold all the data. Use with caution.
::::

The following file extensions are used for the approximate kNN search: Each extension is broken down by the quantization types.

* {applies_to}`stack: ga 9.3` `cenivf` for DiskBBQ to store centroids
* {applies_to}`stack: ga 9.3` `clivf` for DiskBBQ to store clusters of quantized vectors
* `vex` for the HNSW graph
* `vec` for all non-quantized vector values. This includes all element types: `float`, `byte`, and `bit`.
* `veq` for quantized vectors indexed with [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): `int4` or `int8`
* `veb` for binary vectors indexed with [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): `bbq`
* `vem`, `vemf`, `vemq`, and `vemb` for metadata, usually small and not a concern for preloading

Generally, if you are using a quantized index, you should only preload the relevant quantized values and index structures such as the HNSW graph. Preloading the raw vectors is not necessary and might be counterproductive.

Additional detail can be gathered about the specific files by using the [stats endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats), which will display information about the index and fields.

For example, for DiskBBQ, you might see something like this:

```console
GET my_index/_stats?filter_path=indices.my_index.primaries.dense_vector

{
    "indices": {
        "my_index": {
            "primaries": {
                "dense_vector": {
                    "value_count": 3,
                    "off_heap": {
                        "total_size_bytes": 249,
                        "total_veb_size_bytes": 0,
                        "total_vec_size_bytes": 36,
                        "total_veq_size_bytes": 0,
                        "total_vex_size_bytes": 0,
                        "total_cenivf_size_bytes": 111,
                        "total_clivf_size_bytes": 102,
                        "fielddata": {
                            "my_vector": {
                                "cenivf_size_bytes": 111,
                                "clivf_size_bytes": 102,
                                "vec_size_bytes": 36
                            }
                        }
                    }
                }
            }
        }
    }
}
```


## Reduce the number of index segments [_reduce_the_number_of_index_segments]

{{es}} shards are composed of segments, which are internal storage elements in the index. For approximate kNN search, {{es}} stores the vector values of each segment as a separate HNSW graph, so kNN search must check each segment. The recent parallelization of kNN search made it much faster to search across multiple segments, but still kNN search can be up to several times faster if there are fewer segments. By default, {{es}} periodically merges smaller segments into larger ones through a background [merge process](elasticsearch://reference/elasticsearch/index-settings/merge.md). If this isn’t sufficient, you can take explicit steps to reduce the number of index segments.


### Increase maximum segment size [_increase_maximum_segment_size]

{{es}} provides many tunable settings for controlling the merge process. One important setting is `index.merge.policy.max_merged_segment`. This controls the maximum size of the segments that are created during the merge process. By increasing the value, you can reduce the number of segments in the index. The default value is `5GB`, but that might be too small for larger dimensional vectors. Consider increasing this value to `10GB` or `20GB` can help reduce the number of segments.


### Create large segments during bulk indexing [_create_large_segments_during_bulk_indexing]

A common pattern is to first perform an initial bulk upload, then make an index available for searches. Instead of force merging, you can adjust the index settings to encourage {{es}} to create larger initial segments:

* Ensure there are no searches during the bulk upload and disable [`index.refresh_interval`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-refresh-interval-setting) by setting it to `-1`. This prevents refresh operations and avoids creating extra segments.
* Give {{es}} a large indexing buffer so it can accept more documents before flushing. By default, the [`indices.memory.index_buffer_size`](elasticsearch://reference/elasticsearch/configuration-reference/indexing-buffer-settings.md) is set to 10% of the heap size. With a substantial heap size like 32GB, this is often enough. To allow the full indexing buffer to be used, you should also increase the limit [`index.translog.flush_threshold_size`](elasticsearch://reference/elasticsearch/index-settings/translog.md).


## Avoid heavy indexing during searches [_avoid_heavy_indexing_during_searches]

Actively indexing documents can have a negative impact on approximate kNN search performance, since indexing threads steal compute resources from search. When indexing and searching at the same time, {{es}} also refreshes frequently, which creates several small segments. This also hurts search performance, since approximate kNN search is slower when there are more segments.

When possible, it’s best to avoid heavy indexing during approximate kNN search. If you need to reindex all the data, perhaps because the vector embedding model changed, then it’s better to reindex the new documents into a separate index rather than update them in-place. This helps avoid the slowdown mentioned above, and prevents expensive merge operations due to frequent document updates.


## Avoid page cache thrashing by using modest readahead values on Linux [_avoid_page_cache_thrashing_by_using_modest_readahead_values_on_linux_2]

Search can cause a lot of randomized read I/O. When the underlying block device has a high readahead value, there may be a lot of unnecessary read I/O done, especially when files are accessed using memory mapping (see [storage types](elasticsearch://reference/elasticsearch/index-settings/store.md#file-system)).

Most Linux distributions use a sensible readahead value of `128KiB` for a single plain device, however, when using software raid, LVM or dm-crypt the resulting block device (backing {{es}} [path.data](../../deploy/self-managed/important-settings-configuration.md#path-settings)) may end up having a very large readahead value (in the range of several MiB). This usually results in severe page (filesystem) cache thrashing adversely affecting search (or [update](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document)) performance.

You can check the current value in `KiB` using `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`. Consult the documentation of your distribution on how to alter this value (for example with a `udev` rule to persist across reboots, or via [blockdev --setra](https://man7.org/linux/man-pages/man8/blockdev.8.html) as a transient setting). We recommend a value of `128KiB` for readahead.

::::{warning}
`blockdev` expects values in 512 byte sectors whereas `lsblk` reports values in `KiB`. As an example, to temporarily set readahead to `128KiB` for `/dev/nvme0n1`, specify `blockdev --setra 256 /dev/nvme0n1`.
::::


## Use Direct IO when the vector data does not fit in RAM
```{applies_to}
stack: preview 9.1
serverless: unavailable
```
If your indices are of type `bbq_hnsw` and your nodes don't have enough off-heap RAM to store all vector data in memory, you may see very high query latencies. Vector data includes the HNSW graph, quantized vectors, and raw float32 vectors.

In these scenarios, direct IO can significantly reduce query latency. Enable it by setting the JVM option `vector.rescoring.directio=true` on all vector search nodes in your cluster.

Only use this option if you're experiencing very high query latencies on indices of type `bbq_hnsw`. Otherwise, enabling direct IO may increase your query latencies.
