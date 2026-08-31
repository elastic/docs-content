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

{{es}} supports [approximate k-nearest neighbor search](../../../solutions/search/vector/knn/approximate-knn.md) for efficiently finding the *k* nearest vectors to a query vector. Since approximate kNN search works differently from other queries, there are special considerations around its performance.

Many of these recommendations help improve search speed. With approximate kNN, the indexing algorithm runs searches under the hood to create the vector index structures. So these same recommendations also help with indexing speed.


## Reduce vector memory foot-print [_reduce_vector_memory_foot_print]

The default [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-element-type) is `float`. But this can be automatically quantized during index time through [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization). Quantization will reduce the required memory by 4x, 8x, or as much as 32x, but it will also reduce the precision of the vectors and increase disk usage for the field (by up to 25%, 12.5%, or 3.125%, respectively). Increased disk usage is a result of {{es}} storing both the quantized and the unquantized vectors. For example, when int8 quantizing 40GB of floating point vectors an extra 10GB of data will be stored for the quantized vectors. The total disk usage amounts to 50GB, but the memory usage for fast search will be reduced to 10GB.

For `float` vectors with `dim` greater than or equal to `384`, using a [`quantized`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) index is highly recommended.


## Reduce vector dimensionality [_reduce_vector_dimensionality]

The speed of kNN search scales linearly with the number of vector dimensions, because each similarity computation considers each element in the two vectors. Whenever possible, it’s better to use vectors with a lower dimension. Some embedding models come in different "sizes", with both lower and higher dimensional options available. You could also experiment with dimensionality reduction techniques like PCA. When experimenting with different approaches, it’s important to measure the impact on relevance to ensure the search quality is still acceptable.


## Exclude vector fields from `_source` [_exclude_vector_fields_from_source]

{{es}} stores the original JSON document that was passed at index time in the [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md). By default, each hit in the search results contains the full document `_source`. When the documents contain high-dimensional `dense_vector` fields, the `_source` can be quite large and expensive to load. This could significantly slow down the speed of kNN search.

::::{note}
:applies_to: { "stack": "ga 9.2+" }
New indices already exclude vector fields from `_source` by default, with automatic rehydration for reindex and recovery operations.
::::


### Exclude and rehydrate automatically
```{applies_to}
stack: ga 9.2+
```

For vector fields specifically, prefer the [`index.mapping.exclude_source_vectors`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) index setting over the generic `excludes` mapping parameter. Vectors excluded through this setting are rehydrated automatically, so reindex, update, and recovery continue to work as expected. To retrieve vector values in a specific search response, use the `fields` option. 

This setting is enabled by default for indices created on 9.2+. 

### Exclude without rehydration

::::{note}
[reindex]({{es-apis}}operation/operation-reindex), [update]({{es-apis}}operation/operation-update), and [update by query]({{es-apis}}operation/operation-update-by-query) operations generally require the `_source` field. Disabling `_source` for a field through the generic `excludes` parameter (unlike `index.mapping.exclude_source_vectors` above) does **not** support rehydration, and might result in unexpected behavior for these operations. For example, reindex might not actually contain the `dense_vector` field in the new index.
::::


You can also disable storing `dense_vector` fields in the `_source` through the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) mapping parameter. This prevents loading and returning large vectors during search, and also cuts down on the index size. Vectors that have been omitted from `_source` can still be used in kNN search, since it relies on separate data structures to perform the search. Before using the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) parameter, make sure to review the downsides of omitting fields from `_source`.

Another option is to use  [synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source).

## Ensure data nodes have enough capacity [_ensure_data_nodes_have_enough_memory]

{{es}} uses either the Hierarchical Navigable Small World ([HNSW](https://arxiv.org/abs/1603.09320)) algorithm or the Disk Better Binary Quantization ([DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) algorithm for approximate kNN search.

HNSW is a graph-based algorithm which only works efficiently when most vector data is held in memory. You should ensure that data nodes have at least enough RAM to hold the vector data and index structures.

DiskBBQ is a clustering algorithm which can scale efficiently often on less memory than HNSW. Where HNSW typically performs poorly without sufficient memory to fit the entire structure in RAM, DiskBBQ scales linearly when using less available memory than the total index size. You can start with enough RAM to hold the vector data and index structures but, in most cases, you should be able to reduce your RAM allocation and still maintain good performance. All centroids should stay resident. Extra headroom to cache about 5–10% of the posting lists (cluster vectors) is enough for reasonable performance when queries access largely overlapping clusters.

A `dense_vector` field stores more than the values you index. On disk, {{es}} keeps the raw vectors (for rescoring and reindex), any quantized copy used for approximate search, and the search structure (an HNSW graph, or DiskBBQ centroids and clusters). Off-heap RAM is only the working set that must stay in the operating system's filesystem cache, which is separate from the Java heap.

Use the calculator to estimate disk and off-heap RAM. [Vector files](#vector-files-off-heap-ram) and the formulas explain what those totals include.

### Vector sizing calculator [vector-sizing-calculator]

Use this calculator to estimate disk and off-heap RAM for a `dense_vector` field. The RAM total is the working set that must stay in the filesystem cache. Disk includes every persisted structure, including raw vectors that stay on disk when you use quantization.

:::{vector-sizing-calculator}
:::

These estimates are a planning baseline. Real usage depends on your data, indexing settings, query patterns, merges, deletes, and rescoring options. [Vector files](#vector-files-off-heap-ram) lists the Lucene files behind the totals. [Estimate off-heap RAM](#_estimate_off_heap_ram) and [Estimate disk usage](#_estimate_disk_usage) show the formulas.

### Vector files [vector-files-off-heap-ram]

Each structure is a Lucene file (also reported under `off_heap.*_size_bytes` in [index stats]({{es-apis}}operation/operation-indices-stats)). Metadata files (`.vem`, `.vemf`, `.vemq`, `.vemb`) are small and you do not need to preload them.

The **Off-heap RAM** column is whether that file is part of the working set you size in the [calculator](#vector-sizing-calculator) and in [Estimate off-heap RAM](#_estimate_off_heap_ram):

- **Yes**: must stay in the filesystem cache. Include it in the RAM estimate.
- **Partial**: optional headroom; only touched parts are paged in.
- **No**: not in the working set. Lives on disk, read on demand.

::::{tab-set}

:::{tab-item} HNSW

| Component | File | Off-heap RAM | What it is |
| --- | --- | --- | --- |
| Raw vectors | `.vec` | Yes if unquantized; otherwise No | Full-precision vectors. Scanned during search when there is no quantization; otherwise kept on disk for optional rescoring. |
| Quantized vectors | `.veq` (int8 or int4) or `.veb` (BBQ) | Yes | Present only with quantization. A field uses one of these files, not both. |
| HNSW graph | `.vex` | Yes | Proximity graph that HNSW walks at search time. |

:::

:::{tab-item} Flat

| Component | File | Off-heap RAM | What it is |
| --- | --- | --- | --- |
| Raw vectors | `.vec` | Yes if unquantized; otherwise No | Full-precision vectors. Scanned during search when there is no quantization; otherwise kept on disk for optional rescoring. |
| Quantized vectors | `.veq` (int8 or int4) or `.veb` (BBQ) | Yes | Present only with quantization. A field uses one of these files, not both. |

:::

:::{tab-item} DiskBBQ

```{applies_to}
stack: ga 9.3+
```

| Component | File | Off-heap RAM | What it is |
| --- | --- | --- | --- |
| Raw vectors | `.vec` | No | Full-precision vectors kept on disk for optional rescoring. |
| Centroids | `.cenivf` | Yes | Cluster centroids DiskBBQ uses to pick which clusters to visit. |
| Clusters | `.clivf` | Partial | Quantized vectors grouped into clusters. Only clusters a query visits are paged in. |

:::

::::

### Estimate off-heap RAM [_estimate_off_heap_ram]

Disk and off-heap RAM are two different numbers, and they can differ by a lot. Disk is every structure persisted for the field. Off-heap RAM is the working set that must stay in the operating system's filesystem cache for fast, stable query latency. Vector data is memory-mapped, so it lives in the OS page cache, separate from the Java heap.

Provision at least the off-heap RAM figure per copy, plus headroom. Once the working set no longer fits in cache, queries start reading from disk and latency climbs sharply. For quantized indices the raw vectors stay on disk (read only for optional rescoring), so they count toward disk but not toward the required off-heap RAM.

**What should stay in RAM, by index type:**

- `flat`: the raw vectors.
- `hnsw`: the raw vectors and the graph.
- `int8_flat` / `int4_flat` / `bbq_flat`: the quantized codes only.
- `int8_hnsw` / `int4_hnsw` / `bbq_hnsw`: the quantized codes and the graph.
- `bbq_disk` (DiskBBQ): all centroids. Extra headroom to cache about 5–10% of the posting lists is a good target; the rest of the postings and the raw vectors stay on disk. This is why DiskBBQ can serve far more vectors per GiB of RAM.

Those structures are the files marked **Yes** (and **Partial** for DiskBBQ cluster headroom) in [Vector files](#vector-files-off-heap-ram).

#### Vector data in RAM

The amount of vector data held in off-heap RAM depends on the `element_type` and `quantization`. When quantization is enabled, only the smaller quantized vectors need to be in RAM. The raw vectors are accessed from disk only during rescoring.

| `element_type` | `quantization` | RAM per vector |
| --- | --- | --- |
| `float` | none | `num_dimensions × 4` |
| `float` | `int8` | `num_dimensions + 16` |
| `float` | `int4` | `⌈num_dimensions / 2⌉ + 16` |
| `float` | `bbq` | `⌈num_dimensions / 64⌉ × 8 + 14` |
| `bfloat16` | none | `num_dimensions × 2` |
| `bfloat16` | `int8` | `num_dimensions + 16` |
| `bfloat16` | `int4` | `⌈num_dimensions / 2⌉ + 16` |
| `bfloat16` | `bbq` | `⌈num_dimensions / 64⌉ × 8 + 14` |
| `byte` | none | `num_dimensions` |
| `bit` | none | `⌈num_dimensions / 8⌉` |

```{math}
\begin{align*}
vector\ RAM = num\_vectors \times RAM\ per\ vector
\end{align*}
```

#### Index structure in RAM

::::{tab-set}

:::{tab-item} HNSW

The HNSW graph must be fully loaded in memory for efficient search. The default value for `m` is `16`.

```{math}
\begin{align*}
HNSW\ RAM = num\_vectors \times 4 \times m
\end{align*}
```

Total off-heap RAM for HNSW:

```{math}
\begin{align*}
total\ RAM = vector\ RAM + HNSW\ RAM
\end{align*}
```

Example with unquantized `hnsw`, `element_type: float`, `m` set to `16`, and `1,000,000` vectors of `1024` dimensions:

```{math}
\begin{align*}
estimated\ bytes &= (1,000,000 \times 4 \times 16) + (1,000,000 \times 4 \times 1024) \\
&= 64,000,000 + 4,096,000,000 \\
&= 4,160,000,000 \\
&= 3.87GB
\end{align*}
```

:::

:::{tab-item} Flat

The flat index has no graph structure. Only vector data needs to be in RAM.

```{math}
\begin{align*}
total\ RAM = vector\ RAM
\end{align*}
```

:::

:::{tab-item} DiskBBQ

```{applies_to}
stack: ga 9.3+
```

DiskBBQ keeps all centroids resident. Extra headroom to cache about 5–10% of the posting lists (cluster vectors) is a good target. Use the centroid and cluster formulas in [Index structure on disk](#_index_structure_on_disk).

```{math}
\begin{align*}
required\ RAM &= centroid\ bytes \\
with\ headroom &\approx centroid\ bytes + 0.05 \times cluster\ bytes
\end{align*}
```

Start with all centroids plus about 5% of the posting lists in RAM and tune based on benchmark results. The useful fraction depends on your query patterns: queries that access overlapping clusters benefit from caching more.

:::

::::

Data nodes should also leave a buffer for other ways that RAM is needed. For example your index might also include text fields and numerics, which also benefit from using filesystem cache. Run benchmarks with your dataset to confirm there is enough memory for good search performance. Nightly examples include the [`so_vector`](https://elasticsearch-benchmarks.elastic.co/#tracks/so_vector) and [`dense_vector`](https://elasticsearch-benchmarks.elastic.co/#tracks/dense_vector) tracks.

### Estimate disk usage [_estimate_disk_usage]

Disk usage for a `dense_vector` field is three parts: raw vectors, quantized vectors if you use quantization, and the search structure.

#### Raw vector storage

Raw (unquantized) vectors are always stored on disk, including when quantization is enabled. Size depends on `element_type`:

| `element_type` | Bytes per dimension | Disk per vector |
| --- | --- | --- |
| `float` | 4 | `num_dimensions × 4` |
| `bfloat16` | 2 | `num_dimensions × 2` |
| `byte` | 1 | `num_dimensions` |
| `bit` | 1/8 | `⌈num_dimensions / 8⌉` |

```{math}
\begin{align*}
raw\ vector\ bytes = num\_vectors \times bytes\_per\_vector
\end{align*}
```

#### Quantized vector storage

When quantization is enabled, {{es}} stores both the raw vectors and a quantized copy. That increases total disk usage and reduces off-heap RAM. Quantized vector storage applies to `float` and `bfloat16` only. The extra 14 or 16 bytes per vector are a small correction the quantizer stores so it can rescore accurately.

| `quantization` | Bytes per vector |
| --- | --- |
| `int8` | `num_dimensions + 16` |
| `int4` | `⌈num_dimensions / 2⌉ + 16` |
| `bbq` | `⌈num_dimensions / 64⌉ × 8 + 14` |

```{math}
\begin{align*}
estimated\ bytes = num\_vectors \times bytes\ per\ vector
\end{align*}
```

#### Index structure on disk [_index_structure_on_disk]

Overhead depends on the search algorithm. The default for HNSW `m` is `16`. The default for DiskBBQ `vectors_per_cluster` is `384`.

| Index type | Component | Estimated bytes |
| --- | --- | --- |
| `hnsw` | Graph (`.vex`) | `num_vectors × 4 × m` |
| `flat` | — | `0` |
| `bbq_disk` {applies_to}`stack: ga 9.3+` | Centroids (`.cenivf`) | `⌈num_vectors / vectors_per_cluster⌉ × (num_dimensions + 16)` |
| `bbq_disk` | Clusters (`.clivf`), `num_dimensions` 384 or more | `num_vectors × 2 × (⌈num_dimensions / 8⌉ + 16)` |
| `bbq_disk` | Clusters (`.clivf`), `num_dimensions` less than 384 | `num_vectors × 2 × (⌈num_dimensions / 2⌉ + 16)` |

For DiskBBQ, add centroid bytes and cluster bytes. The `× 2` on cluster vectors is a conservative upper bound: a vector may be written to a second cluster. Real cluster storage is between 1× and 2×.

#### Total disk per replica

```{math}
\begin{align*}
total\ disk = raw\ vector\ bytes + quantized\ disk + index\ structure\ bytes
\end{align*}
```

Each shard replica holds a full copy. Multiply the per-replica figure by `1 + number of replicas` for cluster-wide disk. To check the size of vector data in an existing index, use the [Analyze index disk usage]({{es-apis}}operation/operation-indices-disk-usage) API.


## Warm up the filesystem cache [dense-vector-preloading]

If the machine running {{es}} is restarted, the filesystem cache will be empty, so it will take some time before the operating system loads hot regions of the index into memory so that search operations are fast. You can explicitly tell the operating system which files should be loaded into memory eagerly depending on the file extension using the [`index.store.preload`](elasticsearch://reference/elasticsearch/index-settings/preloading-data-into-file-system-cache.md) setting.

::::{warning}
Loading data into the filesystem cache eagerly on too many indices or too many files will make search *slower* if the filesystem cache is not large enough to hold all the data. Use with caution.
::::

Preload only the files that must stay in RAM. [Vector files](#vector-files-off-heap-ram) lists those files per index type (Off-heap RAM **Yes**). For quantized HNSW or flat, that is the quantized codes (`.veq` or `.veb`) plus the HNSW graph (`.vex`). For DiskBBQ, preload the centroids (`.cenivf`). Do not preload raw vectors (`.vec`); paging them in can evict those index structures from the cache.

You can gather additional detail about the specific files by using the [stats endpoint]({{es-apis}}operation/operation-indices-stats), which displays information about the index and fields.

For example, for DiskBBQ, the response might look like this:

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


## Accelerate indexing with GPU [_use_gpu_accelerated_indexing]
```{applies_to}
stack: ga 9.4
```
For indexing-heavy workloads on large vector datasets, GPU acceleration can significantly speed up HNSW index construction and reduce the cost of merging segments into larger ones. See [GPU accelerated vector indexing](/solutions/search/vector/gpu-vector-indexing.md) for supported configurations and setup.


## Avoid heavy indexing during searches [_avoid_heavy_indexing_during_searches]

Actively indexing documents can have a negative impact on approximate kNN search performance, since indexing threads steal compute resources from search. When indexing and searching at the same time, {{es}} also refreshes frequently, which creates several small segments. This also hurts search performance, since approximate kNN search is slower when there are more segments.

When possible, it’s best to avoid heavy indexing during approximate kNN search. If you need to reindex all the data, perhaps because the vector embedding model changed, then it’s better to reindex the new documents into a separate index rather than update them in-place. This helps avoid the slowdown mentioned above, and prevents expensive merge operations due to frequent document updates.


## Avoid page cache thrashing by using modest readahead values on Linux [_avoid_page_cache_thrashing_by_using_modest_readahead_values_on_linux_2]

Search can cause a lot of randomized read I/O. When the underlying block device has a high readahead value, there may be a lot of unnecessary read I/O done, especially when files are accessed using memory mapping (see [storage types](elasticsearch://reference/elasticsearch/index-settings/store.md#file-system)).

Most Linux distributions use a sensible readahead value of `128KiB` for a single plain device, however, when using software raid, LVM or dm-crypt the resulting block device (backing {{es}} [path.data](../../deploy/self-managed/important-settings-configuration.md#path-settings)) may end up having a very large readahead value (in the range of several MiB). This usually results in severe page (filesystem) cache thrashing adversely affecting search (or [update]({{es-apis}}group/endpoint-document)) performance.

You can check the current value in `KiB` using `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`. Consult the documentation of your distribution on how to alter this value (for example with a `udev` rule to persist across reboots, or via [blockdev --setra](https://man7.org/linux/man-pages/man8/blockdev.8.html) as a transient setting). We recommend a value of `128KiB` for readahead.

::::{warning}
`blockdev` expects values in 512 byte sectors whereas `lsblk` reports values in `KiB`. As an example, to temporarily set readahead to `128KiB` for `/dev/nvme0n1`, specify `blockdev --setra 256 /dev/nvme0n1`.
::::


## Use on-disk rescoring when the vector data does not fit in RAM
```{applies_to}
stack: preview 9.3
serverless: unavailable
```
If you use quantized indices and your nodes don't have enough off-heap RAM to store all vector data in memory, then you might experience high query latencies. Vector data includes the HNSW graph, quantized vectors, and raw float vectors.

In these scenarios, on-disk rescoring can significantly reduce query latency. Enable it by setting the `on_disk_rescore: true` option on your vector indices. Your data must be re-indexed or force-merged to use the new setting in subsequent searches.
