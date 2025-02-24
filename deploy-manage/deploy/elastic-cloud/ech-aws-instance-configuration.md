---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-aws-instance-configuration.html
---

# Elasticsearch Add-On for Heroku AWS instance configurations [ech-aws-instance-configuration]

Amazon EC2 (AWS) C6gd, M6gd & R6gd instances, powered by AWS Graviton2, are now available for Elastic Cloud deployments. C6gd, M6gd & R6gd VMs use the [Graviton2, ARM neoverse N1 cores](https://aws.amazon.com/about-aws/whats-new/2020/07/announcing-new-amazon-ec2-instances-powered-aws-graviton2-processors/) and provide high compute coupled with fast NVMe storage, which makes them a good fit to power Elastic workloads. In addition, Graviton2 VMs also offer more than a 20% improvement in price-performance over comparable Intel chipsets.

In addition to AWS Graviton2 instances, Amazon EC2 (AWS) C5d, M5d, I3, I3en, and D2/D3 instances are now available for Elastic Cloud deployments in all supported [AWS Cloud Regions](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-hosted/ec-regions-templates-instances.md#ec-aws_regions).

For specific AWS hardware and availability details, check the [Regional availability of instances per AWS region](ech-default-aws-configurations.md#aws-list-region) and the [AWS default provider instance configurations](ech-default-aws-configurations.md).

## VM configurations [echvm_configurations]

For the AWS infrastructure upgrade, we use the default instance type configurations provided by AWS which are unique to them.

To make it easy to identify each instance type in AWS, a new common nomenclature is introduced.

For example, Instance ID / SKU: `aws.es.datahot.i3`

|     |     |
| --- | --- |
| `aws.*` | Denotes the cloud provider, AWS in this case with Azure in future cases. |
| `\*.es.datahot.*` | Denotes that this configuration is an Elasticsearch (`es`) cluster component that serves as a data node for hot content. Other options may be `datawarm`, `datacold`, `datafrozen` for data nodes, and `kibana`, `master`, and so on for other components. |
| `*.i3` | Denotes that this configuration is running on the AWS i3 instance family. |

The new configuration naming convention aligns with the [data tiers](/manage-data/lifecycle/data-tiers.md) intended for each configuration type, replacing prior naming conventions of “highio”, “highcpu”, and so on. The following table details the new configurations for data nodes and compares them with prior naming conventions where applicable.

| New config name | Notes |
| --- | --- |
| aws.es.datahot.i3 | This configuration maintains the same type of VM configuration as used in the previous config (“aws.data.highio.i3”) but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.datahot.i3en | This is a new configuration that is similar to the “aws.data.datahot.i3” config, but with more disk space to allow for longer retention in ingest use cases, or larger catalog in search use cases. |
| aws.es.datahot.m5d | This configuration maintains the same type of VM configuration as used in the previous config (“aws.data.highcpu.m5d”) but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.datahot.m6gd | This is a new configuration that is similar to the “aws.es.datahot.m5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.es.datahot.c5d | This is a new configuration that provides double the CPU capacity compared to “aws.es.datahot.m5d” config. It is intended for high throughput ingest use cases or intensive search use cases. |
| aws.es.datahot.c6gd | This is a new configuration that is similar to the “aws.es.datahot.c5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.es.datahot.r6gd | This is a new configuration powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.es.datawarm.d2, aws.es.datacold.d2 | These configurations maintain the same type of VM configuration as used in the previous config (“aws.data.highstorage.d2”) but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.datawarm.d3, aws.es.datacold.d3 | These configurations maintain the same type of VM configuration as used in the previous config (“aws.data.highstorage.d3”) but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.datawarm.i3en, aws.es.datacold.i3en | These configurations maintain the same type of VM configuration as used in the previous config (“aws.data.highstorage.i3en”) but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.datafrozen.i3en | This configuration maintains the same type of VM configuration as defined for (“aws.es.datacold.i3en”) config. |

For a detailed price list, check the [Elastic Cloud price list](https://cloud.elastic.co/deployment-pricing-table?provider=aws). For a detailed specification of the new configurations, check [Elasticsearch Service default provider instance configurations](ech-default-aws-configurations.md).

The benefits of the new configurations are multifold:

* By providing a net new configuration of C5d instances, there is a general boost of performance related to new chipsets and faster hardware. On average the boost we witnessed in select benchmarks can reach up to 15%, however, different workloads may exhibit different improvements.
* Introducing C6gd, M6gd & R6gd instances, powered by AWS Graviton 2, provides high compute coupled with fast NVMe storage and offer more than a 20% improvement in price-performance over comparable Intel chipsets.
* The existing family types have been extended in terms of disk capacity which translates to a more cost effective infrastructure which in some cases can save up to 80% when calculating cost by disk capacity.
* There are now more instance types to choose from in the hot tier.  Rather than the traditional “highio” and “highcpu”, there are now six options to cover the hot data tier which allows to optimize cost/performance further.

In addition to data nodes for storage and search, Elasticsearch nodes also have machine learning nodes, master nodes, and coordinating nodes. These auxiliary node types along with application nodes such as APM servers, Kibana, and Enterprise search have also been upgraded to the new C5d, C6gd, M5d, and M6gd instance types. Both auxiliary node and application node configurations are based on Elasticsearch data node configuration types shown in the previous table.

| New config name | Notes |
| --- | --- |
| aws.es.master.c5d | Master nodes have been “upgraded” to use 4x the CPU with more memory and disk space as they had when based on “aws.master.r5d” config. This will help boost the overall performance and stability of clusters, as master nodes have a critical role in maintaining cluster state and controlling workloads. |
| aws.es.master.c6gd | This is a new configuration that is similar to the “aws.es.master.c5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.es.ml.m5d | ML nodes will maintain the same type of VM configuration as used in the previous config (“aws.ml.m5d”), but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.ml.m6gd | This is a new configuration that is similar to the “aws.es.ml.m5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.es.ml.c5d | This is a new configuration that is similar to the “aws.es.ml.m5d” config but with 2x more CPU per unit of RAM and more disk space. |
| aws.es.coordinating.m5d | Coordinating nodes will maintain the same type of VM configuration as used in the previous config (“aws.coordinating.m5d”), but will have a new name (and billing SKU) that is consistent with the new naming. |
| aws.es.coordinating.m6gd | This is a new configuration that is similar to the “aws.es.coordinating.m5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.kibana.c5d | Same “upgrade” for Kibana as that of master nodes. Will now use 4x the CPU with more memory and disk space.  This ensures a more performant Kibana and helps with some client side aggregation, as well as responsive UI. |
| aws.kibana.c6gd | This is a new configuration that is similar to the “aws.kibana.c5d” config but with more disk space and similar RAM:CPU ratios. It is powered by AWS Graviton2 which offers a better price-performance over comparable Intel chipsets. |
| aws.apm.c5d | Same “upgrade” for APM as that of Kibana. Will now use 4x the CPU with more memory and disk space. |
| aws.integrationsserver.c5d | Same “upgrade” for Integrations Server as that of Kibana. Will now use 4x the CPU with more memory and disk space. |
| aws.enterprisesearch.c5d | Enterprisesearch nodes have been “upgraded” to use 2x the CPU with more memory and disk space as they had when based on “aws.enterprisesearch.m5d” config. |


## Selecting the right configuration for you [echselecting_the_right_configuration_for_you]

While far from being a comprehensive guide for performance tuning, the following advice is provided for selecting the hot tier instance configuration:

| Deployment template | Hot data tier instance configuration | Notes |
| --- | --- | --- |
| Storage Optimized | aws.es.datahot.i3 | Good for most ingestion use cases with 7-10 days of data available for fast access. Also good for light search use cases without heavy indexing or CPU needs. |
| Storage Optimized (Dense) | aws.es.datahot.i3en | Ideal for ingestion use cases with more than 10 days of data available for fast access. Also, good for light search use cases with very large data sets. |
| CPU Optimized | aws.es.datahot.c5d | Suitable for ingestion use cases with 1-4 days of data available for fast access and for search use cases with indexing and querying workloads. Provides the most CPU resources per unit of RAM. |
| CPU Optimized (ARM) | aws.es.datahot.c6gd | Suitable for ingestion use cases with 1-4 days of data available for fast access and for search use cases with indexing and querying workloads. Provides the most CPU resources per unit of RAM. |
| Vector Search Optimized (ARM) | aws.es.datahot.r6gd | Optimized for applications that leverage Vector Search and/or Generative AI. Also the optimal choice for utilizing ELSER for semantic search applications. Broadly suitable for all semantic search, text embedding, image search, and other Vector Search use cases. |
| General Purpose | aws.es.datahot.m5d | Suitable for ingestion use cases with 5-7 days of data available for fast access. Also good for search workloads with less-frequent indexing and medium to high querying loads. Provides a balance of storage, memory, and CPU. |
| General Purpose (ARM) | aws.es.datahot.m6gd | Suitable for ingestion use cases with 5-7 days of data available for fast access. Also good for search workloads with less-frequent indexing and medium to high querying loads. Provides a balance of storage, memory, and CPU. |


