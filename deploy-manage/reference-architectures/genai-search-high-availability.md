---
applies_to:
  deployment:
    self: all
    ess: all
    ece: all
    eck: all
---

# GenAI search - High Availability

This reference architecture represents a production-grade, high-availability GenAI Search architecture built on Elasticsearch. It is intended to show physical deployment architecture, logical integration points, and highlight important best practices for enabling a retrieval layer for grounding generative AI responses.

Elasticsearch can combine lexical search, dense and sparse vector search, temporal and geospatial filtering, and hybrid ranking techniques. These capabilities form the foundation for Retrieval Augmented Generation (RAG), agentic workflows, and AI-assisted applications.

Below is a multi-availability-zone deployment designed for continuous availability, fault tolerance, and predictable performance under sustained query and ingestion load. It applies to both time-series and non-time-series use cases and supports a broad set of GenAI patterns including assistants, autonomous agents, observability copilots for SRE’s, and SOC analysis platforms.

Elasticsearch supports multiple vector search execution models and optimizations, allowing this architecture to balance recall, latency, and cost based on workload requirements.

- **BBQ (Better Binary Quantization)** is Elastic’s patented quantization technology that dramatically reduces vector memory footprint while preserving high recall, enabling large-scale in-memory vector search at lower cost.  
- **DiskBBQ** extends BBQ by efficiently paging vector data from disk, providing predictable performance even when the full vector working set does not fit in memory and enabling cost-efficient scaling for very large corpora.  
- **HNSW** is used where maximum recall and lowest tail latency are required and sufficient memory is available to keep vector indexes resident in RAM.  
- **ACORN** further optimizes filtered vector search by reducing unnecessary graph traversals, making it especially effective for high-selectivity queries common in security, observability, and multi-tenant environments.

Together, these approaches allow the architecture to be tuned precisely for different latency, recall, update, and cost constraints without changing the overall system design.

## Search AI use case

The GenAI Search – High Availability architecture is intended for organizations that:

* Require high-performance, low-latency information retrieval across large and diverse datasets, with queries returning highly relevant results at scale.  
* Need lexical, semantic, hybrid, or multimodal search (including text, code, images, video, and geospatial retrieval).  
* Employ Retrieval Augmented Generation (RAG) and Agentic Workflows where grounding generative models in the most relevant documents is essential.  
* Depend on advanced search features such as faceting, filtering, highlighting, personalization, and metadata-aware retrieval.  
* Operate in secure or multi-tenant environments where document and field level security and tenant-aware index design ensure compliance without sacrificing performance.  
* Use Elasticsearch as a short- and long-term memory system for LLM agents, enabling session recall, personalization, and optimized token usage through techniques like time-decayed scoring or constant\_keyword partitioning.  
* Power observability copilots and SOC assistants that summarize alerts, logs, and metrics in plain language, correlate across incidents, and accelerate root cause analysis with semantically grounded responses.

## Architecture

:::{image} /deploy-manage/images/genai-search-ha-logical-diagram.png
:alt: GenAI Search high availability logical diagram
:::

:::{image} /deploy-manage/images/genai-search-ha-physical-diagram.png
:alt: GenAI Search high availability physical diagram
:::

:::::{important}
This architecture employs a single uniform hot/content data tier, as most search and generative AI workloads require very low latency across the full corpus, regardless of data age. However, disk-based vectro storage methods such as DiskBBQ (Elastic’s [patented evolution of IVF](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) offer a memory-efficient alternative to HNSW that can support larger datasets on lower-cost tiers (IoT telemetry, financial transaction logs, etc)
:::::

The physical deployment architecture for Gen AI applications is built around a resilient Elasticsearch cluster deployed across three availability zones (AZ). For production-grade deployments, two AZs are the minimum, with three AZs strongly recommended to maximize high availability and fault tolerance. In Elastic Cloud, shards are automatically distributed across zones, ensuring that primaries and replicas never reside in the same AZ. 

In self-managed deployments, shard allocation awareness and forced awareness should be configured to achieve the same resiliency. Kibana instances are deployed in each AZ to not become a single point of failure. And, in some use cases, it should be fronted by a load balancer. For example, Elastic MCP server is a foundational component of Agent Builder. It enables agentic workflows via API using natural language to query Elasticsearch. As a result, high volume programmatic access is likely required and should be balanced across multiple nodes.

All data nodes host both primary and replica shards, with replicas contributing both to redundancy and to query throughput. High-performance SSD-backed storage is recommended, along with memory-rich nodes to support vector indexes, hybrid lexical+vector search, and high concurrent load. Machine learning nodes are also distributed across zones to support optional embedding generation using self-hosted models such as Elastic’s Jina text embedding models. 

In addition, the Elastic Inference Service (EIS) is provided as part of Elastic Cloud, which uses GPU’s for high speed vector embedding generation. Finally, snapshots are stored externally for disaster recovery, with Snapshot Lifecycle Management (SLM) handling automation.

## Recommended Hardware Specifications

The following recommendations assist with clusters that are self-deployed on-prem or self-deployed in a cloud provider. With Elastic Cloud Hosted, you can deploy clusters in AWS, Azure, or Google Cloud. Available hardware types and configurations vary across providers, but each offers instance families that meet the performance needs of search and generative AI applications. 

For details, see our documentation on [Elastic Cloud Hosted hardware](https://www.elastic.co/docs/reference/cloud/cloud-hosted/hardware) for AWS, Azure, and GCP. The “Physical” column in the table below provides guidance when self-deploying Elasticsearch in your own data center, based on equivalent CPU, RAM, and storage profiles. 

Elastic has performance-tested hardware profiles across the major cloud providers to identify the optimal balance for each node type. Significantly deviating from these tested ratios may appear to reduce costs, but typically leads to degraded performance, query latency spikes, or search scalability.

Dedicated ML nodes are needed when inference is performed within the cluster, such as running ELSER or [custom transformer models](https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-model-ref) locally. These nodes should be dedicated and provisioned with sufficient memory to load models into RAM. When inference is offloaded to an LLM or embedding model external to the cluster (e.g., [Elastic Inference Service](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm), Azure OpenAI, Anthropic, or Bedrock), dedicated ML nodes are not required.

| Type | AWS | Azure | GCP | Physical |
| :---- | :---- | :---- | :---- | :---- |
| hot | c6gd | f32sv2 | N2 | 16-32 vCPU **64-256 GB RAM\*** 2-6 TB NVMe SSD |
| ml | m6gd | f16sv2 | N2 | 16-32 vCPU 64 GB RAM 256 GB SSD |
| master | c5d | f16sv2 | N2 | 4 vCPU 16 GB RAM 256 GB SSD |
| kibana | c6gd | f16sv2 | N2 | 8-16 vCPU 8 GB RAM 256 GB SSD |

## Important Hybrid Retrieval Considerations

- Over-fetch on both retrieval paths. Increase size, use RRF with a larger rank\_window\_size, and raise num\_candidates on knn so ANN does not miss critical neighbors. Then trim results to find the best recall vs. latency balance.
- Keep minimum\_should\_match loose, and rely on proper analyzers and multi-fields (text, .keyword, shingles/ngrams). Hybrid cannot recover documents BM25 never retrieves. 
- The easiest framework for executing hybrid search on Elastic is [retrievers](https://www.elastic.co/docs/solutions/search/retrievers-overview) or [ES|QL FORK and FUSE](https://www.elastic.co/docs/solutions/search/esql-for-search#fork-and-fuse).

## Important Vector Search Considerations

### Storage and Memory

Approximate nearest-neighbor (ANN) algorithms are dominated by irregular, latency-bound memory access rather than arithmetic. As a result, all vector distance computations occur in off-heap RAM and CPU. To make large-scale in-memory vector search feasible, Elasticsearch supports [many quantization techniques](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector#dense-vector-params) for up to a 32x reduction in vector footprint in ram, and defaults to HNSW with [Better Binary Quantization](https://www.elastic.co/search-labs/blog/better-binary-quantization-lucene-elasticsearch). BBQ is Elastic’s patented approach for maximizing recall with a low vector memory footprint.

Two options exist to optimize off-heap available memory. One, increase the ram per node, or Two, slightly decrease the heap per node. For option 2, ensure you benchmark with a tool like [Elastic Rally](https://esrally.readthedocs.io/en/stable/) to ensure the decreased heap will be sufficient for peak workloads. 

When vector quantization is enabled, Elasticsearch stores both the original float32 vectors and their quantized representations on disk. Retaining the float32 vectors preserves flexibility for re-ranking, re-indexing, and future model changes. Only the quantized vectors are loaded into memory for search. 

- Use HNSW when you are optimizing for 99%+ recall and absolute lowest tail latency, and you can afford the RAM/off-heap footprint (and you’re not constantly updating the index).
- Use DiskBBQ when you’re cost/memory sensitive, your recall target is more like “\~95%” and you want performance that doesn’t drop when the working set no longer fits RAM.
- Use BBQ Flat: (BBQ without HNSW) when filters reduce comparisons to \< \~100k vectors; typically lowest operational complexity.

### Vector Sizing

- For the sizing formulas [please see this page](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/approximate-knn-search#_ensure_data_nodes_have_enough_memory). Use the formulas to calculate the disk needs. 
- For HNSW, the same amount of ram will be required as the vector index storage. 
- For DiskBBQ, you can provision as little as 5% of disk storage as RAM, as DiskBBQ swaps to disk effectively, but query performance will improve significantly with more data you can fit into RAM.

### Generating Vector Embeddings

- If generating embeddings on Elastic ML nodes, capacity can be autoscaled using Elastic Cloud Hosted (ECH) or Elastic Cloud for Kubernetes on-prem.  
- Elastic provides [world class vector models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md) from Jina AI that can be used for NLP embeddings, and a re-ranker that can be either self-hosted on ML nodes or used through [Elastic Inference Service](https://www.elastic.co/docs/explore-analyze/elastic-inference/eis).  
- Embeddings can also be generated with [Elastic’s inference API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put) from many external model providers or internal or externally hosted foundation models.

### kNN Search Performance Tuning

- **Recall:** General guidance is to start with defaults → measure → [increasenum\_candidates](https://www.elastic.co/search-labs/blog/elasticsearch-knn-and-num-candidates-strategies) (oversample) → optionally add a [re-ranker](https://www.elastic.co/search-labs/blog/elastic-semantic-reranker-part-2).
- **Runtime:** Please see [this guide](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/approximate-knn-search) to understand all the vector search performance optimizations to ensure high speed search. 

### Updating vector data

Updating dense or sparse vector data can be more resource-intensive than updating keyword-based fields, since embeddings often need to be regenerated. For applications with frequent document updates, plan for additional indexing throughput and consider whether embeddings should be pre-computed, updated asynchronously, or generated on demand.

## Important General Considerations

### Hybrid Retrieval

### Multi-AZ deployment

Three availability zones is ideal, but at least two availability zones are recommended to ensure resiliency. This helps guarantee that there will be data nodes available in the event of an AZ failure. Elastic Cloud automatically distributes replicas across zones, while self-managed clusters should use shard allocation awareness to achieve the same.

### Shard management

Proper shard management is foundational to maintaining performance at scale. This includes ensuring an even distribution of shards across nodes, choosing an appropriate shard size, and managing shard counts as the cluster grows. For detailed guidance, refer to [*Size your shards*](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards).  

- Recommendations for time series data can be found in the Hot/Frozen architecture.  
- **Size shards intentionally:** estimate total index size and choose primaries that land in the **\~10–50 GB, \<200M docs** range. This is the natural shard count for a catalog; don’t add shards unless search metrics demand it.  
- **Plan scale at creation:** catalogs don’t roll over, so set shard math up front. If growth is possible, configure routing shards so the index can be **split later by clean multiples** (read-only \+ extra IO/disk required).  
- **Scale with replicas, not primaries:** increase **replicas** first to improve search throughput and availability. Replicas increase concurrency by spreading queries across shard copies; **fan-out is still driven by primary shard count**.

### Snapshots

Regular backups are essential when indexing business-critical or auditable data. Snapshots provide recoverability in case of data corruption or accidental deletion. For production workloads, configure automated snapshots through Snapshot Lifecycle Management (SLM) and integrate them with Index Lifecycle Management (ILM) policies.

### Kibana, MCP, and Agent Builder

- If deploying outside of Elastic Cloud, ensure Kibana is configured for High Availability to avoid a single point of failure. Deploying Kibana across multiple availability zones also improves resiliency for management and user access.  
- Ensure telemetry is collected from Kibana nodes if MCP server is used. This allows for proper capacity planning if usage is extensive.  
- For self-deployed clusters, use a proxy in front of multiple Kibana nodes to avoid a single point of failure. Elastic Cloud Hosted has a single point of connection that is proxied.

### Data tiering

A uniform hot tier is strongly recommended for the majority of search use cases. Disk-based vector methods like using DiskBBQ (Elastic’s [patented evolution of IVF](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) offer a memory-efficient alternative to HNSW that can support larger datasets on lower-cost tiers (IoT telemetry, financial transaction logs, etc)

[How many nodes of each do you need?](https://www.elastic.co/docs/deploy-manage/reference-architectures/hotfrozen-high-availability#hot-frozen-estimate)

It depends on:

- The type of data being ingested (such as logs, metrics, traces)  
- The retention period of searchable data (such as 30 days, 90 days, 1 year)  
- The amount of data you need to ingest each day  
- The number of dashboards, queries, query types and how frequent they are run.

You can [contact us](https://www.elastic.co/contact) for an estimate and recommended configuration based on your specific scenario.

## [**Resources and references**](https://www.elastic.co/docs/deploy-manage/reference-architectures/hotfrozen-high-availability#hot-frozen-resources)

* [Elasticsearch \- Vector Search Documentation](https://www.elastic.co/docs/solutions/search/vector)  
* [Elasticsearch \- Get ready for production](https://www.elastic.co/docs/deploy-manage/production-guidance/elasticsearch-in-production-environments)  
* [Elastic Cloud Hosted \- Preparing a deployment for production](https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/cloud-hosted)  
* [Size your shards](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards)