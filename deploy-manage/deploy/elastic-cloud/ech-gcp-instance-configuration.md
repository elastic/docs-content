---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-gcp-instance-configuration.html
---

# Elasticsearch Add-On for Heroku GCP instance configurations [ech-gcp-instance-configuration]

Google Compute Engine (GCE) N2 general purpose VM types are now available for Elastic Cloud deployments in all supported [Google Cloud regions](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-hosted/ec-regions-templates-instances.md#ec-gcp_regions). [N2](https://cloud.google.com/compute/docs/machine-types) VMs have a better mix of vCPU, RAM, and internal disk, and are up to 50% more cost effective when compared to N1 VM types. In addition to N2, we also provide N2D VMs across the Google Cloud regions.

To learn about the GCE specific configurations, check:

* [VM configurations](#ech-gcp-vm-configurations)
* [Selecting the right configuration for you](#ech-gcp-configuration-choose)
* [GCP default provider instance configurations](ech-default-gcp-configurations.md)
* [Regional availability of instances per GCP region](ech-default-gcp-configurations.md#ech-gcp-list-region)

## VM configurations [ech-gcp-vm-configurations]

For the Google Cloud infrastructure upgrade, rather than using default baseline configurations, [custom machine types](https://cloud.google.com/custom-machine-types) unique to Google Cloud are used so individual parameters of each VM can be fine tuned to fit the right blend of RAM:CPU:Disk. To accommodate the custom configuration, a new common nomenclature is introduced to help you easily identify each VM type. This will apply eventually to AWS and Azure instances as well, as we roll out newer versions of VMs for these providers.

For example, Instance ID / SKU: `gcp.es.datahot.n2.68x10x45`

|     |     |
| --- | --- |
| `gcp.*` | Denotes the cloud provider, GCP in this case or AWS/Azure in future cases. |
| `\*.es.datahot.*` | Denotes that this configuration is an Elasticsearch (`es`) cluster component that serves as a data node for hot content. Other options may be `datawarm`, `datacold`, `datafrozen` for data nodes, and `kibana`, `master`, and so on for other components. |
| `\*.n2.*` | Denotes that this configuration is running on the GCP N2 family. |
| `*.68x10x45` | Denotes the resource configuration, delimited by “x”.<br>* The first argument (`68`) denotes the total gross RAM capacity of the instance. Normally we use 4GB of that for utilities and therefore this configuration has a “usable RAM” of 64GB.<br>* The second argument (`10`) denotes the number of vCPUs allocated to the entire machine.<br>* The third argument denotes the ratio of RAM to storage capacity as in 1:X. In this case, for each 1GB of RAM, you will have 45 GB of disk to store Elasticsearch data. |

The new configuration naming convention aligns with the [data tiers](/manage-data/lifecycle/data-tiers.md) intended for each configuration type, replacing prior naming conventions of “highio”, “highcpu”, and so on. The following table details the new configurations for data nodes and compares them with prior naming conventions where applicable.

| New config name | Notes |
| --- | --- |
| gcp.es.datahot.n2.68x10x45 | This configuration replaces “highio”, which is based on N1 with 1:30 RAM:disk and similar RAM:CPU ratios. |
| gcp.es.datahot.n2.68x10x95 | This is a new configuration that is similar to the first, but with more disk space to allow for longer retention in ingest use cases, or larger catalog in search use cases. |
| gcp.es.datahot.n2.68x16x45 | This configuration replaces “highcpu”, which is based on N1 with 1:8 RAM:disk and similar RAM:CPU ratios. |
| gcp.es.datahot.n2.68x32x45 | This is a new configuration that provides double the CPU capacity compared to “highcpu” or [68-16-1:45] configuration. It is intended for high throughput ingest use cases or intensive search use cases. |
| gcp.es.datahot.n2d.64x8x11 | This is a new configuration powered by AMD processors which offers a better price-performance compared to Intel processors. |
| gcp.es.datawarm.n2.68x10x190, gcp.es.datacold.n2.68x10x190 | These configurations replace “highstorage”, which is based on N1 with 1:160 RAM:disk and similar RAM:CPU ratios. |
| gcp.es.datafrozen.n2.68x10x95 | This configuration replaces the (short lived) gcp.es.datafrozen.n2d.64x8x95 configuration we used for the frozen cache tier. n2d was based on the AMC epyc processor but we found that the Intel-based configuration provides a slightly better cost/performance ratio. We also tweaked the RAM/CPU ratios to align to other configurations and benchmarks. |

For a detailed price list, check the [Elastic Cloud deployment pricing table](https://cloud.elastic.co/deployment-pricing-table?provider=gcp). For a detailed specification of the new configurations, check [{{ecloud}} default GCP instance configurations](ech-default-gcp-configurations.md).

The benefits of the new configurations are multifold:

1. By using newer generations of N2 machines, there is a general boost of performance related to new chipsets and faster hardware. On average the boost we witnessed in select benchmarks can reach up to 15%, however, different workloads may exhibit different improvements.
2. The existing family types have been extended in terms of disk capacity which translates to a more cost effective infrastructure which in some cases can save up to 80% when calculating cost by disk capacity.
3. There are now more instance types to choose from in the hot tier.  Rather than the traditional “highio” and “highcpu”, there are now four options to cover the hot data tier which allows to optimize cost/performance further.

In addition to data nodes for storage and search, Elasticsearch nodes also have machine learning nodes, master nodes, and coordinating nodes. These auxiliary node types along with application nodes such as APM servers and Kibana instances have also been upgraded to the new N2 instance types. Both auxiliary node and application node configurations are based on Elasticsearch data node configuration types shown in the previous table.

| New config name | Notes |
| --- | --- |
| gcp.es.master.n2.68x32x45 | Master nodes will now be based on the highest CPU rich configuration (68:32). In the past, master nodes were based on a configuration that had ¼ of the CPU for each unit of RAM (was called “highmem”). This will help boost the overall performance and stability of clusters, as master nodes have a critical role in maintaining cluster state and controlling workloads. |
| gcp.es.ml.n2.68x16x45 | ML nodes will maintain the same type of VM configuration as in the past, but will have a new name (and billing SKU) that is consistent with the rest of the naming. |
| gcp.es.ml.n2.68x32x45 | This is a new configuration that is similar to the “gcp.es.ml.n2.68x16x45” config but with 2x more CPU per unit of RAM and similar storage ratio. |
| gcp.es.coordinating.n2.68x16x45 | Same as ML nodes - no configuration change, just a new name. |
| gcp.kibana.n2.68x32x45 | Kibana nodes have been upgraded two steps up as well, to use 4x the CPU as they had when based on “highmem”. This ensures a more performant Kibana and helps with some client side aggregation, as well as responsive UI. |
| gcp.apm.n2.68x32x45 | Same upgrade for APM. Will now use 4x the CPU. |
| gcp.integrationsserver.n2.68x32x45 | Same upgrade for Integrations Server. Will now use 4x the CPU. |

## Selecting the right configuration for you [ech-gcp-configuration-choose]

While far from being a comprehensive guide for performance tuning, the following advice is provided for selecting the hot tier instance configuration:

| Deployment template | Hot data tier instance configuration | Notes |
| --- | --- | --- |
| Storage Optimized | gcp.es.datahot.n2.68x10x45 | Consider this default configuration for ingest use cases that require ~7-10 days of retention, or for light search use cases that don’t have significant index changes or CPU utilization. |
| Storage Optimized (Dense) | gcp.es.datahot.n2.68x10x95 | Consider this dense storage option for ingest use cases that have a longer retention period of the hot tier, or for light search use cases that have a significant catalog size. |
| CPU Optimized | gcp.es.datahot.n2.68x32x45 | Consider this configuration for ingest use cases that require ~1-4 days of retention, or for heavyweight search use cases that require significant and consistent indexing or high query load. |
| Vector Search Optimized | gcp.es.datahot.n2d.64x8x11 | Optimized for applications that leverage Vector Search and/or Generative AI. Also the optimal choice for utilizing ELSER for semantic search applications. Broadly suitable for all semantic search, text embedding, image search, and other Vector Search use cases. |
| General Purpose | gcp.es.datahot.n2.68x16x45 | Consider this configuration for ingest use cases that require ~5-7 days of retention, or for moderate load search use cases that require occasional indexing or medium to high query load. |


