---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-hardware-prereq.html
---

# Hardware prerequisites [ece-hardware-prereq]

ECE has specific hardware requirements for memory and storage.

* [Memory](#ece-memory)
* [Storage](#ece-storage)
* [SSD Storage](#ece-ssd)

::::{note}
For ECE 3.5.0 and prior versions, the host machines you use must support the x86-64 instruction set. From ECE 3.5.1 and newer versions, ARM based architecture (`aarch64`) is also supported.
::::


::::{warning}
ECE installations with **spinning disks** are not supported when you run allocators and ECE management services on the same server.
::::



## Memory [ece-memory]

| **Memory** | Coordinators | Directors | Proxies | Allocators |
| --- | --- | --- | --- | --- |
| Minimum to install | 8 GB RAM | 8 GB RAM | 8 GB RAM | 8 GB RAM<br> |
| Minimum recommended | 16 GB RAM | 8 GB RAM | 8 GB RAM | 128 GB to 256 GB RAM1<br> |
| **Small deployment**2 | 32 GB RAM | 32 GB RAM | 16 GB RAM | 128 GB RAM<br> |
| **Medium deployment**2 | 32 GB RAM | 32 GB RAM | 16 GB RAM | 256 GB RAM<br> |
| **Large deployment**3 | 128 GB RAM | 128 GB RAM | 16 GB RAM | 256 GB RAM<br> |

1 Allocators must be sized to support your Elasticsearch clusters and Kibana instances. We recommend host machines that provide between 128 GB and 256 GB of memory. While smaller hosts might not pack larger Elasticsearch clusters and Kibana instances as efficiently, larger hosts might provide fewer CPU resources per GB of RAM on average. For example, running 64 * 2GB nodes on a 128GB host with 16 vCPUs means that each node will get 2/128 of the total CPU time. This is 1/4 core on average, and might not be sufficient. We recommend inspecting both what is the expected number and size of the nodes you plan to run on your hosts in order to understand which hardware will work best in your environment.

2 For high availability, requires three hosts each of the capacities indicated, spread across three availability zones.

3 For high availability, requires three hosts each of the capacities indicated (except for allocators), spread across three availability zones. For allocators, requires three or more hosts of the capacity indicated, spread across three availability zones.

The size of your ECE deployment has a bearing on the JVM heap sizes that you should specify during installation. To learn more, check [JVM Heap Sizes](ece-jvm.md).


## Storage [ece-storage]

| **Storage** | Coordinators | Directors | Proxies | Allocators |
| --- | --- | --- | --- | --- |
| Minimum to install | 10 GB | 10 GB | 15 GB | 10 GB |
| Minimum recommended | 1:4 RAM-to-storage ratio1 | 1:4 RAM-to-storage ratio1 | 1:4 RAM-to-storage ratio1 | Enough storage to support the RAM-to-storage ratio2 |

1 Control-plane services usually require about 1:4 RAM-to-storage ratio, this may vary.

2 For example, if you use a host with 256 GB of RAM and the default ratio of 1:32, your host must provide 8192 GB of disk space.


## SSD storage [ece-ssd]

The ECE management services provided by the coordinators and directors require fast SSD storage to work correctly. For smaller deployments that co-locate the ECE management services with proxies and allocators on the same hosts, you must use fast SSD storage for your entire deployment. If SSD-only storage is not feasible, [some of the ECE management services need to be separated](ece-roles.md).

::::{note}
When using SSDs on an external (shared) storage system, please check with your storage vendor whether TRIM [should be disabled](https://www.elastic.co/blog/is-your-elasticsearch-trimmed) on the ECE hosts to avoid unnecessary stress on the storage system.
::::
