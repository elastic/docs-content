---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-installation.html
---

# Install Elastic Agents [elastic-agent-installation]

::::{admonition} Restrictions
:class: important

Note the following restrictions when installing {{agent}} on your system:

* You can install only a single {{agent}} per host. Due to the fact that the {{agent}} may read data sources that are only accessible by a superuser, {{agent}} will therefore also need to be executed with superuser permissions.
* You might need to log in as a root user (or Administrator on Windows) to run the commands described here. After the {{agent}} service is installed and running, make sure you run these commands without prepending them with `./` to avoid invoking the wrong binary.
* Running {{agent}} commands using the Windows PowerShell ISE is not supported.
* See also the [resource requirements](#elastic-agent-installation-resource-requirements) described on this page.

::::


You have a few options for installing and managing an {{agent}}:

* **Install a {{fleet}}-managed {{agent}} (recommended)**

    With this approach, you install {{agent}} and use {{fleet}} in {{kib}} to define, configure, and manage your agents in a central location.

    We recommend using {{fleet}} management because it makes the management and upgrade of your agents considerably easier.

    Refer to [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).

* **Install {{agent}} in standalone mode (advanced users)**

    With this approach, you install {{agent}} and manually configure the agent locally on the system where it’s installed. You are responsible for managing and upgrading the agents. This approach is reserved for advanced users only.

    Refer to [Install standalone {{agent}}s](/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md).

* **Install {{agent}} in a containerized environment**

    You can run {{agent}} inside of a container — either with {{fleet-server}} or standalone. Docker images for all versions of {{agent}} are available from the Elastic Docker registry, and we provide deployment manifests for running on Kubernetes.

    Refer to:

    * [Run {{agent}} in a container](/reference/ingestion-tools/fleet/elastic-agent-container.md)
    * [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md)

        * [Advanced {{agent}} configuration managed by {{fleet}}](/reference/ingestion-tools/fleet/advanced-kubernetes-managed-by-fleet.md)
        * [Configuring Kubernetes metadata enrichment on {{agent}}](/reference/ingestion-tools/fleet/configuring-kubernetes-metadata.md)
        * [Run {{agent}} on GKE managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-gke-managed-by-fleet.md)
        * [Run {{agent}} on Amazon EKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-eks-managed-by-fleet.md)
        * [Run {{agent}} on Azure AKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-aks-managed-by-fleet.md)

    * [Run {{agent}} Standalone on Kubernetes](/reference/ingestion-tools/fleet/running-on-kubernetes-standalone.md)
    * [Scaling {{agent}} on {{k8s}}](/reference/ingestion-tools/fleet/scaling-on-kubernetes.md)
    * [Run {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/standalone-elastic-agent.md) — for {{eck}} users


::::{admonition} Restrictions in {{serverless-short}}
:class: important

If you are using {{agent}} with [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), note these differences from use with {{ech}} and self-managed {{es}}:

* The number of {{agents}} that may be connected to an {{serverless-full}} project is limited to 10 thousand.
* The minimum supported version of {{agent}} supported for use with {{serverless-full}} is 8.11.0.

::::



## Resource requirements [elastic-agent-installation-resource-requirements]

The {{agent}} resources consumption is influenced by the number of integration and the environment its been running on.

Using our lab environment as an example, we can observe the following resource consumption:


### CPU and RSS memory size [_cpu_and_rss_memory_size]

We tested using an AWS `m7i.large` instance type with 2 vCPUs, 8.0 GB of memory, and up to 12.5 Gbps of bandwidth. The tests ingested a single log file using both the [throughput and scale preset](/reference/ingestion-tools/fleet/elasticsearch-output.md#output-elasticsearch-performance-tuning-settings) with self monitoring enabled. These tests are representative of use cases that attempt to ingest data as fast as possible. This does not represent the resource overhead when using [{{elastic-defend}}](integration-docs://docs/reference/endpoint.md).

|     |     |     |
| --- | --- | --- |
| **Resource** | **Throughput** | **Scale** |
| **CPU*** | ~67% | ~20% |
| **RSS memory size*** | ~280 MB | ~220 MB |
| **Write network throughput** | ~3.5 MB/s | 480 KB/s |

* including all monitoring processes

Adding integrations will increase the memory used by the agent and its processes.


### Size on disk [_size_on_disk]

The disk requirements for {{agent}} vary by operating system and {{stack}} version. With version 8.14 we have significantly reduced the size of the {{agent}} binary. Further reductions are planned to be made in future releases.

| Operating system | 8.13 | 8.14 | 8.15 |
| --- | --- | --- | --- |
| **Linux** | 1800 MB | 1018 MB | 1060 MB |
| **macOS** | 1100 MB | 619 MB | 680 MB |
| **Windows** | 891 MB | 504 MB | 500 MB |

During upgrades, double the disk space is required to store the new {{agent}} binary. After the upgrade completes, the original {{agent}} is removed from disk to free up the space.
