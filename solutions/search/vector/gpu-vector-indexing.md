---
navigation_title: GPU vector indexing
description: Accelerate HNSW index construction for dense vectors with GPU acceleration in Elasticsearch, including hardware setup, Docker configuration, monitoring, and troubleshooting.
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: unavailable
products:
  - id: elasticsearch
  - id: elastic-stack
type: how-to
---

# Accelerate dense vector indexing with a GPU in {{es}} [gpu-vector-indexing]

GPU indexing in {{es}} builds Hierarchical Navigable Small World (HNSW)
graphs with the [NVIDIA cuVS library](https://developer.nvidia.com/cuvs).
Offloading that work to a graphics processing unit (GPU) speeds up dense
vector ingest on large datasets and frees CPU resources for search and
other tasks.

## Before you begin [gpu-vector-indexing-before-you-begin]

To use GPU indexing, you need:

* An [Enterprise subscription](https://www.elastic.co/subscriptions)
* A supported NVIDIA GPU (Ampere architecture or better, compute capability
  \>= 8.0) with a minimum 8 GB of GPU memory
* GPU driver, CUDA, and
  [cuVS runtime libraries](https://docs.rapids.ai/api/cuvs/stable/build/)
  installed on the node. Refer to the
  [Elastic support matrix](https://www.elastic.co/support/matrix#vector-indexing) for
  supported CUDA and cuVS versions.
* `LD_LIBRARY_PATH` environment variable configured to include the cuVS
  libraries path and its dependencies (CUDA, rmm, and so on)
* Supported platform: Linux x86_64 only, Java 22 or later
* Supported dense vector configurations: `hnsw` and `int8_hnsw`; `float`
  element type only

## Configuration

The
[`vectors.indexing.use_gpu`](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#gpu-vector-indexing-settings)
node-level setting controls GPU vector indexing.

## Elasticsearch Docker image with GPU support

You can extend the official {{es}} Docker image with this example Dockerfile
to add the dependencies required for GPU support.

::::{warning}
This Dockerfile serves as an example implementation, and is not fully supported
like our official Docker images.
::::

This example is configured for {{es}} 9.5. To use a different {{es}} version,
update both `ELASTICSEARCH_VERSION` and `CUVS_VERSION` to a supported
combination from the
[Elastic support matrix](https://www.elastic.co/support/matrix#vector-indexing).

::::{dropdown} Example Dockerfile
:::{include} _snippets/docker-gpu-indexing.md
:::
::::

### Host requirements

The host machine running the Docker container needs
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
installed and configured.

### Build it

```sh
docker build -t es-gpu .
```

### Run it

```sh
docker run \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  -e "vectors.indexing.use_gpu=true" \
  --user elasticsearch \
  --gpus all \
  --rm -it es-gpu
```

## Monitoring

```{applies_to}
stack: ga 9.3.2
```

Use the `GET _xpack/usage` API to monitor GPU vector indexing status and usage
across all nodes in the cluster:

```console
GET _xpack/usage?filter_path=gpu_vector_indexing
```

```console-result
{
  "gpu_vector_indexing": {
    "available": true, <1>
    "enabled": true, <2>
    "index_build_count": 30, <3>
    "nodes_with_gpu": 3, <4>
    "nodes": [ <5>
      { "type": "NVIDIA L4", "memory_in_bytes": 24000000000,
        "enabled": true, "index_build_count": 10 },
      { "type": "NVIDIA L4", "memory_in_bytes": 24000000000,
        "enabled": true, "index_build_count": 10 },
      { "type": "NVIDIA A100", "memory_in_bytes": 80000000000,
        "enabled": true, "index_build_count": 10 }
    ]
  }
}
```
1. Whether the current license permits GPU indexing.
2. Whether at least one node has GPU hardware configured and has not turned it off through `vectors.indexing.use_gpu=false`.
3. Total number of GPU index builds across the cluster.
4. Number of data nodes with GPU support.
5. Per-node GPU details including type, memory, enabled status, and build count.

## Troubleshooting

By default, {{es}} uses GPU indexing for supported vector types if a
compatible GPU and required libraries are detected.
Check server logs for messages indicating whether {{es}} has detected a GPU.

If the following message appears, a GPU was successfully detected and
GPU indexing is used:
```
[o.e.x.g.GPUSupport ] [elasticsearch-0] Found compatible GPU [NVIDIA L4] (id: [0])
```
If this message doesn't appear, check for warning messages explaining why GPU
indexing isn't being used, such as an unsupported environment, missing
libraries, or an incompatible GPU.


### cuVS runtime version mismatch

If the cuVS runtime library is older than the `cuvs-java` library bundled with
{{es}}, you see a warning similar to the following:

```
GPU based vector indexing is not supported on this platform; Cannot create JDKProvider:
Version mismatch: outdated libcuvs_c (libcuvs_c [25.12.0], cuvs-java version [26.02.0])
```

Install a cuVS runtime version that's supported for your {{es}} version. Refer
to the
[Elastic support matrix](https://www.elastic.co/support/matrix#vector-indexing).


### Node fails to start with `vectors.indexing.use_gpu: true`

To enforce GPU indexing, set `vectors.indexing.use_gpu: true` in
`elasticsearch.yml`.
The node fails to start if GPU indexing isn't available. For example, if
a GPU isn't detected by {{es}}, if the runtime isn't supported, or if the
necessary dependencies aren't correctly configured.

If the node fails to start, check:
* A supported NVIDIA GPU is present
* CUDA runtime libraries and drivers are installed (check with `nvidia-smi`)
* `LD_LIBRARY_PATH` includes paths to the cuVS libraries and to their
  dependencies (for example, CUDA)
* Supported platform: Linux x86_64 with Java 22 or later


### Performance not improved with GPU indexing

If you're sure that GPU indexing is enabled but performance doesn't improve,
check the following:

* Use supported vector index types and the `float` element type.
* Use a dataset large enough to benefit from GPU acceleration.
* Check for other bottlenecks. GPU indexing accelerates HNSW graph building, but other factors can limit speedups.
  * Indexing throughput depends on how fast you can get data into {{es}}. Check network speed and client performance. Use multiple clients if needed.
  * JSON parsing can dominate the computation. Use base64 encoded vectors instead of JSON arrays.
  * Storage speed also matters. The GPU can process lots of data, so use storage that can keep up. Avoid network-attached storage, and prefer fast NVMe.
* Monitor CPU usage to confirm work is offloaded to the GPU.
* Monitor GPU usage (for example, with `nvidia-smi`).

## Next steps

- [Index dense vectors and run kNN search](knn.md)
- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) for indexing and query performance
- [Bring your own dense vectors](bring-own-vectors.md) if you already have embeddings

## Related pages

- [GPU vector indexing settings](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#gpu-vector-indexing-settings)
- [`dense_vector` field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md)
- [Dense vector search](dense-vector.md)
- [Vector search in Elasticsearch](../vector.md)
