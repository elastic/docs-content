---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-setup.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Set up an enrich processor [enrich-setup]

To set up an enrich processor, follow these steps:

1. Check the [prerequisites](#enrich-prereqs).
2. [Add enrich data](#create-enrich-source-index).
3. [Create an enrich policy](#create-enrich-policy).
4. [Execute the enrich policy](#execute-enrich-policy).
5. [Add an enrich processor to an ingest pipeline](#add-enrich-processor).
6. [Ingest and enrich documents](#ingest-enrich-docs).

Once you have an enrich processor set up, you can [update your enrich data](#update-enrich-data) and [update your enrich policies](#update-enrich-policies).

::::{important}
The enrich processor performs several operations and may impact the speed of your ingest pipeline. We recommend [node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md) co-locating ingest and data roles to minimize remote search operations.

We strongly recommend testing and benchmarking your enrich processors before deploying them in production.

We do not recommend using the enrich processor to append real-time data. The enrich processor works best with reference data that doesn’t change frequently.

::::



### Prerequisites [enrich-prereqs]

To use enrich policies, you must have:

* `read` index privileges for any indices used
* The `enrich_user` [built-in role](elasticsearch://reference/elasticsearch/roles.md)

## Add enrich data [create-enrich-source-index]

To begin, add documents to one or more source indices. These documents should contain the enrich data you eventually want to add to incoming data.

You can manage source indices just like regular {{es}} indices using the [document](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document) and [index](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-indices) APIs.

You also can set up [{{beats}}](beats://reference/index.md), such as a [{{filebeat}}](beats://reference/filebeat/filebeat-installation-configuration.md), to automatically send and index documents to your source indices. See [Getting started with {{beats}}](beats://reference/index.md).


## Create an enrich policy [create-enrich-policy]

After adding enrich data to your source indices, use the [create enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-put-policy) or [Index Management in {{kib}}](/manage-data/data-store/index-basics.md#manage-enrich-policies) to create an enrich policy.

::::{warning}
Once created, you can’t update or change an enrich policy. See [Update an enrich policy](#update-enrich-policies).

::::



## Execute the enrich policy [execute-enrich-policy]

Once the enrich policy is created, you need to execute it using the [execute enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) or [Index Management in {{kib}}](/manage-data/data-store/index-basics.md#manage-enrich-policies) to create an [enrich index](data-enrichment.md#enrich-index).

:::{image} /manage-data/images/elasticsearch-reference-enrich-policy-index.svg
:alt: enrich policy index
:::

The *enrich index* contains documents from the policy’s source indices. Enrich indices always begin with `.enrich-*`, are read-only, and are [force merged](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge).

::::{warning}
Enrich indices should only be used by the [enrich processor](elasticsearch://reference/enrich-processor/enrich-processor.md) or the [{{esql}} `ENRICH` command](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-enrich). Avoid using enrich indices for other purposes.

::::



## Add an enrich processor to an ingest pipeline [add-enrich-processor]

Once you have source indices, an enrich policy, and the related enrich index in place, you can set up an ingest pipeline that includes an enrich processor for your policy.

:::{image} /manage-data/images/elasticsearch-reference-enrich-processor.svg
:alt: enrich processor
:::

Define an [enrich processor](elasticsearch://reference/enrich-processor/enrich-processor.md) and add it to an ingest pipeline using the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline).

When defining the enrich processor, you must include at least the following:

* The enrich policy to use.
* The field used to match incoming documents to the documents in your enrich index.
* The target field to add to incoming documents. This target field contains the match and enrich fields specified in your enrich policy.

You also can use the `max_matches` option to set the number of enrich documents an incoming document can match. If set to the default of `1`, data is added to an incoming document’s target field as a JSON object. Otherwise, the data is added as an array.

See [Enrich](elasticsearch://reference/enrich-processor/enrich-processor.md) for a full list of configuration options.

You also can add other [processors](elasticsearch://reference/enrich-processor/index.md) to your ingest pipeline.


## Ingest and enrich documents [ingest-enrich-docs]

You can now use your ingest pipeline to enrich and index documents.

:::{image} /manage-data/images/elasticsearch-reference-enrich-process.svg
:alt: enrich process
:::

Before implementing the pipeline in production, we recommend indexing a few test documents first and verifying enrich data was added correctly using the [get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get).


## Update an enrich index [update-enrich-data]

Once created, you cannot update or index documents to an enrich index. Instead, update your source indices and [execute](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) the enrich policy again. This creates a new enrich index from your updated source indices. The previous enrich index will be deleted with a delayed maintenance job that executes by default every 15 minutes.

If wanted, you can [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) or [update](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) any already ingested documents using your ingest pipeline.


## Update an enrich policy [update-enrich-policies]

Once created, you can’t update or change an enrich policy. Instead, you can:

1. Create and [execute](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) a new enrich policy.
2. Replace the previous enrich policy with the new enrich policy in any in-use enrich processors or {{esql}} queries.
3. Use the [delete enrich policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-delete-policy) API or [Index Management in {{kib}}](/manage-data/data-store/index-basics.md#manage-enrich-policies) to delete the previous enrich policy.


## Enrich components [ingest-enrich-components]

The enrich coordinator is a component that manages and performs the searches required to enrich documents on each ingest node. It combines searches from all enrich processors in all pipelines into bulk [multi-searches](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch).

The enrich policy executor is a component that manages the executions of all enrich policies. When an enrich policy is executed, this component creates a new enrich index and removes the previous enrich index. The enrich policy executions are managed from the elected master node. The execution of these policies occurs on a different node.


## Node Settings [ingest-enrich-settings]

The `enrich` processor has node settings for enrich coordinator and enrich policy executor.

The enrich coordinator supports the following node settings:

`enrich.cache_size`
:   Maximum size of the cache that caches searches for enriching documents. The size can be specified in three units: the raw number of cached searches (e.g. `1000`), an absolute size in bytes (e.g. `100Mb`), or a percentage of the max heap space of the node (e.g. `1%`). Both for the absolute byte size and the percentage of heap space, {{es}} does not guarantee that the enrich cache size will adhere exactly to that maximum, as {{es}} uses the byte size of the serialized search response which is is a good representation of the used space on the heap, but not an exact match. Defaults to `1%`. There is a single cache for all enrich processors in the cluster.

`enrich.coordinator_proxy.max_concurrent_requests`
:   Maximum number of concurrent [multi-search requests](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch) to run when enriching documents. Defaults to `8`.

`enrich.coordinator_proxy.max_lookups_per_request`
:   Maximum number of searches to include in a [multi-search request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch) when enriching documents. Defaults to `128`.

The enrich policy executor supports the following node settings:

`enrich.fetch_size`
:   Maximum batch size when reindexing a source index into an enrich index. Defaults to `10000`.

`enrich.max_force_merge_attempts`
:   Maximum number of [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) attempts allowed on an enrich index. Defaults to `3`.

`enrich.cleanup_period`
:   How often {{es}} checks whether unused enrich indices can be deleted. Defaults to `15m`.

`enrich.max_concurrent_policy_executions`
:   Maximum number of enrich policies to execute concurrently. Defaults to `50`.


