---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-azure-instance-configuration.html
---

# Elasticsearch Add-On for Heroku Azure instance configurations [ech-azure-instance-configuration]

Azure [Ddv4](https://docs.microsoft.com/en-us/azure/virtual-machines/ddv4-ddsv4-series/), [Edsv4](https://docs.microsoft.com/en-us/azure/virtual-machines/edv4-edsv4-series/), [Fsv2](https://docs.microsoft.com/en-us/azure/virtual-machines/fsv2-series/), and [Lsv3](https://docs.microsoft.com/en-us/azure/virtual-machines/lsv3-series/) virtual machines (VM) are now available for Elastic Cloud deployments in all supported [Azure Cloud regions](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions). These VMs provide additional combinations of compute, memory, and disk configurations to better fit your use-cases to optimize performance and cost.

To learn about the Azure specific configurations, check:

* [VM configurations](#ech-azure-vm-configurations)
* [Selecting the right configuration for you](#ech-azure-configuration-choose)
* [Azure default provider instance configurations](ech-default-azure-configurations.md)
* [Regional availability of instances per Azure region](ech-default-azure-configurations.md#ech-azure-list-region)

## VM configurations [ech-azure-vm-configurations]

For Azure, we use the default instance type configurations provided by Azure which are unique to them. To make it easy to identify each instance type in Azure, a new common nomenclature is introduced.

For example, Instance ID / SKU: `azure.es.datahot.ddv4`

|     |     |
| --- | --- |
| `azure.*` | Denotes the cloud provider, Azure in this case. |
| `\*.es.datahot.*` | Denotes that this configuration is an Elasticsearch (`es`) cluster component that serves as a data node for hot content. Other options may be `datawarm`, `datacold`, `datafrozen` for data nodes, and `kibana`, `master`, and so on for other components. |
| `*.ddv4` | Denotes that this configuration is running on the Azure Ddv4 VM series. |

The new configuration naming convention aligns with the [data tiers](/manage-data/lifecycle/data-tiers.md) intended for each configuration type, replacing prior naming conventions of “highio”, “highcpu”, and so on. The following table details the new configurations for data nodes and compares them with prior naming conventions where applicable.

| New config name | Notes |
| --- | --- |
| azure.es.datahot.edsv4 | This is a new configuration that replaces “azure.data.highio.l32sv2” or “azure.data.highio.e32sv3” config, but provides more disk space and similar RAM:CPU ratios. |
| azure.es.datahot.ddv4 | This is a new configuration that replaces “azure.data.highcpu.d64sv3” config, but provides more disk space to allow for longer retention in ingest use cases, or larger catalog in search use cases. |
| azure.es.datahot.fsv2 | This is a new configuration that provides double the CPU compared to “azure.es.datahot.ddv4” config. It is intended for high throughput ingest use cases or intensive search use cases. |
| azure.es.datahot.lsv3 | This is a new configuration powered by Intel Ice lake processor which provides similar RAM:CPU ratios as that of edsv4 but provides lower disk space. |
| azure.es.datawarm.edsv4, azure.es.datacold.edsv4 | This is a new configuration that replaces “azure.data.highstorage.e16sv3” config but provides more disk space. |
| azure.es.datafrozen.edsv4 | This is a new configuration that replaces “azure.es.datafrozen.lsv2” or “azure.es.datafrozen.esv3” config but provides more disk space. |

For a detailed price list, check the [Elastic Cloud price list](https://cloud.elastic.co/deployment-pricing-table?provider=azure). For a detailed specification of the new configurations, check [{{ecloud}} default Azure instance configurations](ech-default-azure-configurations.md).

The benefits of the new configurations are multifold:

* By providing a net new configuration of fsv2 VM series, there is a general boost of performance related to new chipsets and faster hardware.
* The new instances provide more disk capacity as compared to existing VM series which translates to a more cost effective infrastructure which can save up to 80% when calculating cost by disk capacity.
* There are now more instances to choose from in the hot tier. Rather than the traditional “highio” and “highcpu”, there are now three options to cover the hot data tier which allows to optimize cost/performance further.

In addition to data nodes for storage and search, Elasticsearch nodes also have machine learning nodes, master nodes, and coordinating nodes. These auxiliary node types along with application nodes such as APM servers, Kibana, and Enterprise search have also been upgraded to the new Fsv2 VM series. Both auxiliary node and application node configurations are based on Elasticsearch data node configuration types shown in the previous table.

| New config name | Notes |
| --- | --- |
| azure.es.master.fsv2 | Master nodes now use 4x the CPU as they had when based on “azure.master.e32sv3” config. This will help boost the overall performance and stability of clusters, as master nodes have a critical role in maintaining cluster state and controlling workloads. |
| azure.es.ml.fsv2 | ML nodes now use 2x the CPU as they had when based on “azure.ml.d64sv3” config. |
| azure.es.coordinating.fsv2 | Coordinating nodes now use 2x the CPU as they had when based on “azure.coordinating.d64sv3” config. |
| azure.kibana.fsv2 | Kibana nodes now use 4x the CPU  as they had when based on “azure.kibana.e32sv3” config. This ensures a more performant Kibana and helps with some client side aggregation, as well as responsive UI. |
| azure.apm.fsv2 | APM nodes now use 4x the CPU  as they had when based on “azure.apm.e32sv3” config. |
| azure.integrationsserver.fsv2 | Integrations Server nodes now use 4x the CPU  as they had when based on “azure.integrationsserver.e32sv3” config. |
| azure.enterprisesearch.fsv2 | Enterprisesearch Server nodes now use 2x the CPU  as they had when based on “azure.enterprisesearch.d64sv3” config. |


## Selecting the right configuration for you [ech-azure-configuration-choose]

While far from being a comprehensive guide for performance tuning, the following advice is provided for selecting the hot tier instance configuration:

| Deployment template | Hot data tier instance configuration | Notes |
| --- | --- | --- |
| Storage Optimized | azure.es.datahot.edsv4 | Good for most ingestion use cases with 7-10 days of data available for fast access. Also good for light search use cases without heavy indexing or CPU needs. |
| CPU Optimized | azure.es.datahot.fsv2 | Suitable for ingestion use cases with 1-4 days of data available for fast access and for search use cases with indexing and querying workloads. Provides the most CPU resources per unit of RAM. |
| Vector Search Optimized | azure.es.datahot.lsv3 | Optimized for applications that leverage Vector Search and/or Generative AI. Also the optimal choice for utilizing ELSER for semantic search applications. Broadly suitable for all semantic search, text embedding, image search, and other Vector Search use cases. |
| General Purpose | azure.es.datahot.ddv4 | Suitable for ingestion use cases with 5-7 days of data available for fast access. Also good for search workloads with less-frequent indexing and medium to high querying loads. Provides a balance of storage, memory, and CPU. |


