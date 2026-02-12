---
applies_to:
  deployment:
    self: ga all
    ess: ga all
    ece: ga all
    eck: ga all
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-hosted
---

# GenAI Search - High Availability

This reference architecture represents a production-grade, high-availability GenAI search architecture built on {{es}}. It is intended to show physical deployment architecture, logical integration points, and highlight important best practices for enabling a retrieval layer for grounding generative AI responses.

{{es}} can combine [lexical search](/solutions/search/full-text.md), [dense](/solutions/search/vector/dense-vector.md) and [sparse vector search](/solutions/search/vector/sparse-vector.md), temporal and geospatial filtering, and hybrid ranking techniques. These capabilities form the foundation for [Retrieval Augmented Generation (RAG)](/solutions/search/rag.md), [agentic workflows](/explore-analyze/ai-features/elastic-agent-builder.md), and AI-assisted applications.

## GenAI search use cases

The GenAI search – high availability architecture is intended for organizations that:

- Require high-performance, low-latency information retrieval across large and diverse datasets, supporting {{nlp}} workloads and returning highly relevant results at scale.
- Need lexical, vector, semantic, temporal, hybrid, or multimodal search (including text, code, images, video, and geospatial retrieval).  
- Employ generative AI applications such as assistants, agents, and agentic workflows using Retrieval Augmented Generation (RAG) and/or the Model Context Protocol (MCP), where grounding generative models in the most relevant documents is essential. 
- Integrate with foundation models (such as Azure OpenAI, Anthropic, and Amazon Bedrock) and apply re-ranking techniques to optimize relevance.
- Depend on advanced search features such as faceting, filtering, highlighting, personalization, and metadata-aware retrieval.  
- Operate in secure or multi-tenant environments where document and field level security and tenant-aware index design ensure compliance without sacrificing performance.  
- Use {{es}} as a short- and long-term memory system for LLM agents, enabling session recall, personalization, and optimized token usage through techniques like time-decayed scoring or `constant_keyword` partitioning.  
- Power observability copilots and SOC assistants that summarize alerts, logs, and metrics in plain language, correlate across incidents, and accelerate root cause analysis with semantically grounded responses.
- Integrate with common large language model (LLM) development frameworks, including LlamaIndex, LangChain, and LangSmith.

## Vector search optimization

{{es}} supports multiple vector search execution models and optimizations, allowing this architecture to balance recall, latency, and cost based on workload requirements.

- [Better Binary Quantization (BBQ)](/reference/elasticsearch/mapping-reference/bbq.md) is Elastic’s patented quantization technology that dramatically reduces vector memory footprint while preserving high recall, enabling large-scale in-memory vector search at lower cost.  
- [DiskBBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md#bbq-disk) extends BBQ by efficiently paging vector data from disk, providing predictable performance even when the full vector working set does not fit in memory and enabling cost-efficient scaling for very large corpora.  
- [HNSW](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md#bbq-hnsw) is used where maximum recall and lowest tail latency are required and sufficient memory is available to keep vector indexes resident in RAM.  
- [ACORN](https://www.elastic.co/search-labs/blog/elasticsearch-9-1-bbq-acorn-vector-search) further optimizes filtered vector search by reducing unnecessary graph traversals, making it especially effective for high-selectivity queries common in security, observability, and multi-tenant environments.

Together, these approaches allow the architecture to be tuned precisely for different latency, recall, update, and cost constraints without changing the overall system design.

## Architecture

Below is a multi-availability-zone deployment designed for continuous availability, fault tolerance, and predictable performance under sustained query and ingestion load. It applies to both time-series and non-time-series use cases and supports a broad set of GenAI patterns including assistants, autonomous agents, observability copilots for SRE’s, and SOC analysis platforms.

:::{image} /deploy-manage/images/genai-search-ha-logical-diagram.png
:alt: GenAI Search high availability logical diagram
:::

:::{image} /deploy-manage/images/genai-search-ha-physical-diagram.png
:alt: GenAI Search high availability physical diagram
:::

:::::{important}
This architecture employs a single uniform hot/content data tier, as most search and generative AI workloads require very low latency across the full corpus, regardless of data age. However, disk-based vector storage methods such as [DiskBBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md#bbq-disk) (Elastic’s [patented evolution of IVF](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) offer a memory-efficient alternative to HNSW that can support larger datasets on lower-cost tiers, such as IoT telemetry, financial transaction logs.
:::::

The physical deployment architecture for GenAI applications is built around a resilient {{es}} cluster deployed across three availability zones (AZ). For production-grade deployments, two AZs are the minimum, with three AZs strongly recommended to maximize high availability and fault tolerance. In {{ecloud}}, shards are automatically distributed across zones, ensuring that primaries and replicas never reside in the same AZ. 

In self-managed deployments, [shard allocation awareness](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) and forced awareness should be configured to achieve the same resiliency. {{kib}} instances are deployed in each AZ to not become a single point of failure. And, in some use cases, it should be fronted by a load balancer. For example, Elastic MCP server is a foundational component of Agent Builder. It enables agentic workflows via API using natural language to query {{es}}. As a result, high volume programmatic access is likely required and should be balanced across multiple nodes.

All data nodes host both primary and replica shards, with replicas contributing both to redundancy and to query throughput. High-performance SSD-backed storage is recommended, along with memory-rich nodes to support vector indexes, hybrid lexical and vector search, and high concurrent load. {{ml-cap}} nodes are also distributed across zones to support optional embedding generation using self-hosted models such as Elastic’s Jina text embedding models. 

In addition, the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) is provided as part of {{ecloud}}, which uses GPU’s for high speed vector embedding generation. Finally, snapshots are stored externally for disaster recovery, with Snapshot Lifecycle {{manage-app}} ({{slm-init}}) handling automation.

## Recommended hardware specifications

The following recommendations assist with clusters that are self-deployed on-prem or self-deployed in a cloud provider. With {{ech}}, you can deploy clusters in {{aws}}, Azure, or Google Cloud. Available hardware types and configurations vary across providers, but each offers instance families that meet the performance needs of search and generative AI applications. 

For details, refer to our documentation on [{{ech}} hardware](/reference/cloud/cloud-hosted/hardware.md) for {{aws}}, Azure, and GCP. The "Physical" column in the table below provides guidance when self-deploying {{es}} in your own data center, based on equivalent CPU, RAM, and storage profiles. 

Elastic has performance-tested hardware profiles across the major cloud providers to identify the optimal balance for each node type. Significantly deviating from these tested ratios may appear to reduce costs, but typically leads to degraded performance, query latency spikes, or search scalability.

Dedicated ML nodes are needed when {{infer}} is performed within the cluster, such as running [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) or [custom transformer models](/explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md) locally. These nodes should be dedicated and provisioned with sufficient memory to load models into RAM. When {{infer}} is offloaded to an LLM or embedding model external to the cluster (for example, [Elastic {{infer-cap}} Service](/reference/kibana/connectors-kibana/elastic-managed-llm.md), Azure OpenAI, Anthropic, or Bedrock), dedicated ML nodes are not required.

| Type | {{aws}} | Azure | GCP | Physical |
| :---- | :---- | :---- | :---- | :---- |
| hot | c6gd | f32sv2 | N2 | 16-32 vCPU **64-256 GB RAM\*** 2-6 TB NVMe SSD |
| ml | m6gd | f16sv2 | N2 | 16-32 vCPU 64 GB RAM 256 GB SSD |
| master | c5d | f16sv2 | N2 | 4 vCPU 16 GB RAM 256 GB SSD |
| kibana | c6gd | f16sv2 | N2 | 8-16 vCPU 8 GB RAM 256 GB SSD |

## Important considerations

### Vector search considerations

#### Storage and memory

Approximate nearest-neighbor (ANN) algorithms are dominated by irregular, latency-bound memory access rather than arithmetic. As a result, all vector distance computations occur in off-heap RAM and CPU. To make large-scale in-memory vector search feasible, {{es}} supports [many quantization techniques](/reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for up to a 32x reduction in vector footprint in RAM, and defaults to HNSW with [Better Binary Quantization](https://www.elastic.co/search-labs/blog/better-binary-quantization-lucene-elasticsearch). BBQ is Elastic’s patented approach for maximizing recall with a low vector memory footprint.

To increase off-heap memory available for vector search, you have the following options:

- Increase RAM per node to expand the off-heap working set.
- Slightly reduce the JVM heap size per node to free additional off-heap memory. If you choose this approach, benchmark (for example with [Elastic Rally](https://esrally.readthedocs.io/en/stable/)) to confirm the smaller heap remains sufficient under peak workload.

When vector quantization is enabled, {{es}} stores both the original `float32` vectors and their quantized representations on disk. Retaining the `float32` vectors preserves flexibility for re-ranking, re-indexing, and future model changes. Only the quantized vectors are loaded into memory for search. 

- Use [HNSW](/reference/elasticsearch/mapping-reference/bbq.md#bbq-hnsw) when you are optimizing for 99%+ recall and absolute lowest tail latency, and you can afford the RAM/off-heap footprint (and you’re not constantly updating the index).
- Use [DiskBBQ](/reference/elasticsearch/mapping-reference/bbq.md#bbq-disk) when you’re cost/memory sensitive, your recall target is more like “\~95%” and you want performance that doesn’t drop when the working set no longer fits RAM.
- Use [BBQ flat](/reference/elasticsearch/mapping-reference/bbq.md#bbq-flat): (BBQ without HNSW) when filters reduce comparisons to \< \~100k vectors; typically lowest operational complexity.

#### Vector sizing

- To learn about sizing formulas refer to [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md#_ensure_data_nodes_have_enough_memory). Use the formulas to calculate the disk needs. 
- For HNSW, the same amount of ram will be required as the vector index storage. 
- For DiskBBQ, you can provision as little as 5% of disk storage as RAM, as DiskBBQ swaps to disk effectively, but query performance will improve significantly with more data you can fit into RAM.

#### Generating vector embeddings

- If generating embeddings on Elastic ML nodes, capacity can be autoscaled using {{ech}} (ECH) or {{eck}} on-prem.  
- Elastic provides [world class vector models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md) from Jina AI that can be used for NLP embeddings, and a re-ranker that can be either self-hosted on ML nodes or used through [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference.md/eis).  
- Embeddings can also be generated with [Elastic’s {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put) from many external model providers or internal or externally hosted foundation models.

#### kNN search performance tuning

- **Recall:** General guidance is to start with defaults → measure → [increasenum\_candidates](https://www.elastic.co/search-labs/blog/elasticsearch-knn-and-num-candidates-strategies) (oversample) → optionally add a [re-ranker](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-2).
- **Runtime:** Refer to [this guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) to understand all the vector search performance optimizations to ensure high speed search. 

#### Updating vector data

Updating dense or sparse vector data can be more resource-intensive than updating keyword-based fields, since embeddings often need to be regenerated. For applications with frequent document updates, plan for additional indexing throughput and consider whether embeddings should be pre-computed, updated asynchronously, or generated on demand.

### General considerations

#### Hybrid Retrieval

- Over-fetch on both retrieval paths. Increase size, use RRF with a larger `rank_window_size`, and raise `num_candidates` on knn so ANN does not miss critical neighbors. Then trim results to find the best recall vs. latency balance.
- Keep `minimum_should_match` loose, and rely on proper analyzers and multi-fields (text, .keyword, shingles/ngrams). Hybrid cannot recover documents BM25 never retrieves. 
- The easiest framework for executing hybrid search on Elastic is [retrievers](/solutions/search/retrievers-overview.md) or [{{esql}} FORK and FUSE](/solutions/search/esql-for-search.md#fork-and-fuse).

#### Multi-AZ deployment

Three availability zones is ideal, but at least two availability zones are recommended to ensure resiliency. This helps guarantee that there will be data nodes available in the event of an AZ failure. {{ecloud}} automatically distributes replicas across zones, while self-managed clusters should use shard allocation awareness to achieve the same.

#### Shard management

Proper shard management is foundational to maintaining performance at scale. This includes ensuring an even distribution of shards across nodes, choosing an appropriate shard size, and managing shard counts as the cluster grows. For detailed guidance, refer to [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md).  

- Recommendations for time series data can be found in the [Hot/Frozen architecture](/reference-architectures/genai-search-high-availability.md#general-considerations).  
- **Size shards intentionally:** estimate total index size and choose primaries that land in the **\~10–50 GB, \<200M docs** range. This is the natural shard count for a catalog; don’t add shards unless search metrics demand it.  
- **Plan scale at creation:** catalogs don’t roll over, so set shard math up front. If growth is possible, configure routing shards so the index can be **split later by clean multiples** (read-only \+ extra IO/disk required).  
- **Scale with replicas, not primaries:** increase **replicas** first to improve search throughput and availability. Replicas increase concurrency by spreading queries across shard copies; **fan-out is still driven by primary shard count**.

#### Snapshots

Regular backups are essential when indexing business-critical or auditable data. Snapshots provide recoverability in case of data corruption or accidental deletion. For production workloads, configure automated snapshots through Snapshot Lifecycle {{manage-app}} ({{slm-init}}) and integrate them with Index Lifecycle {{manage-app}} ({{ilm-init}}) policies.

#### {{kib}}, MCP, and Agent Builder

- If deploying outside of {{ecloud}}, ensure {{kib}} is configured for High Availability to avoid a single point of failure. Deploying {{kib}} across multiple availability zones also improves resiliency for management and user access.  
- Ensure telemetry is collected from {{kib}} nodes if MCP server is used. This allows for proper capacity planning if usage is extensive.  
- For self-deployed clusters, use a proxy in front of multiple {{kib}} nodes to avoid a single point of failure. {{ech}} has a single point of connection that is proxied.

#### Data tiering

A uniform hot tier is strongly recommended for the majority of search use cases. Disk-based vector methods like using DiskBBQ (Elastic’s [patented evolution of IVF](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) offer a memory-efficient alternative to HNSW that can support larger datasets on lower-cost tiers (IoT telemetry, financial transaction logs, etc)

[How many nodes of each do you need?](/deploy-manage/reference-architectures/hotfrozen-high-availability.md#hot-frozen-estimate)

It depends on:

- The type of data being ingested (such as logs, metrics, traces)  
- The retention period of searchable data (such as 30 days, 90 days, 1 year)  
- The amount of data you need to ingest each day  
- The number of dashboards, queries, query types and how frequent they are run.

You can [contact us](https://www.elastic.co/contact) for an estimate and recommended configuration based on your specific scenario.

## [**Resources and references**](/deploy-manage/reference-architectures/hotfrozen-high-availability.md#hot-frozen-resources)

* [{{es}} \- Vector Search Documentation](/solutions/search/vector.md)  
* [{{es}} \- Get ready for production](/deploy-manage/production-guidance/elasticsearch-in-production-environments.md)  
* [{{ech}} \- Preparing a deployment for production](deploy-manage/deploy/elastic-cloud/cloud-hosted.md)  
* [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md)