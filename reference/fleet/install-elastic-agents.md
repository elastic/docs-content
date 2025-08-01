---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-installation.html
products:
  - id: fleet
  - id: elastic-agent
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




::::{admonition} New FIPS compatible install packages
:class: note

{applies_to}`stack: preview 9.1` FIPS compatible binaries for {{agent}}, {{fleet}}, and other ingest tools are available for download. Look for the `Linux 64-bit (FIPS)` or `Linux aarch64 (FIPS)` platform option on the product [download page](https://www.elastic.co/downloads). Get more details about FIPS compatibility for {{agent}}, {{fleet}} and other ingest tools in [FIPS mode for Ingest tools](/deploy-manage/security/fips-ingest.md).

::::


You have a few options for installing and managing an {{agent}}:

* **Install a {{fleet}}-managed {{agent}} (recommended)**

    With this approach, you install {{agent}} and use {{fleet}} in {{kib}} to define, configure, and manage your agents in a central location.

    We recommend using {{fleet}} management because it makes the management and upgrade of your agents considerably easier.

    Refer to [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md).

* **Install {{agent}} in standalone mode (advanced users)**

    With this approach, you install {{agent}} and manually configure the agent locally on the system where it’s installed. You are responsible for managing and upgrading the agents. This approach is reserved for advanced users only.

    Refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md).

* **Install {{agent}} in a containerized environment**

    You can run {{agent}} inside of a container — either with {{fleet-server}} or standalone. Docker images for all versions of {{agent}} are available from the Elastic Docker registry, and we provide deployment manifests for running on Kubernetes.

    Refer to:

    * [Run {{agent}} in a container](/reference/fleet/elastic-agent-container.md)
    * [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/fleet/running-on-kubernetes-managed-by-fleet.md)

        * [Advanced {{agent}} configuration managed by {{fleet}}](/reference/fleet/advanced-kubernetes-managed-by-fleet.md)
        * [Configuring Kubernetes metadata enrichment on {{agent}}](/reference/fleet/configuring-kubernetes-metadata.md)
        * [Run {{agent}} on GKE managed by {{fleet}}](/reference/fleet/running-on-gke-managed-by-fleet.md)
        * [Run {{agent}} on Amazon EKS managed by {{fleet}}](/reference/fleet/running-on-eks-managed-by-fleet.md)
        * [Run {{agent}} on Azure AKS managed by {{fleet}}](/reference/fleet/running-on-aks-managed-by-fleet.md)

    * [Run {{agent}} Standalone on Kubernetes](/reference/fleet/running-on-kubernetes-standalone.md)
    * [Scaling {{agent}} on {{k8s}}](/reference/fleet/scaling-on-kubernetes.md)
    * [Run {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/standalone-elastic-agent.md) — for {{eck}} users


::::{admonition} Restrictions in {{serverless-short}}
:class: important

If you are using {{agent}} with [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), note these differences from use with {{ech}} and self-managed {{es}}:

* The number of {{agents}} that may be connected to an {{serverless-full}} project is limited to 10 thousand.
* The minimum supported version of {{agent}} supported for use with {{serverless-full}} is 8.11.0.

::::

::::{admonition} Applying {{agent}} configurations dynamically
When you set up {{agent}}, you might not yet have all input configuration details available. To solve this problem, the input configuration accepts variables and conditions that get evaluated at runtime using information from the running environment, allowing you to apply configurations dynamically. To learn more, refer to [Variables and conditions in input configurations](./dynamic-input-configuration.md).
::::

## {{agent}} installation flavors [elastic-agent-installation-flavors]

{{agent}} distribution packages are offered in multiple flavors. This gives you control over the set of components included in the package and the size of the package footprint when it's installed.

### Flavors for regular package installs

#### Basic flavor [elastic-agent-basic-flavor-regular]

The basic {{agent}} flavor is installed by default using the `elastic-agent install` command with an agent package: `.zip`, .`tar.gz`, `.deb`, `.rpm`, or `.msi`. This flavor includes only the following components:

* `agentbeat` - used to implement all [{{beats}}](beats://reference/index.md)-based integrations.
* `endpoint-security` - used to implement [{{elastic-defend}}](../../solutions/security/configure-elastic-defend.md).
* `pf-host-agent` - used to collect profiling data from hosts as part of Elastic [Universal Profiling](../../solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md).

This basic package is suitable for most use cases and it offers a reduced size on disk.

#### Servers flavor [elastic-agent-servers-flavor-regular]

The servers {{agent}} flavor is installed using the `elastic-agent install --install-servers` command, or for RPM and DEB packages the `ELASTIC_AGENT_FLAVOR=servers` environment variable. In addition to components included in the basic flavor, this flavor also includes:

* `apm-server` - implements the Elastic [APM Server](/solutions/observability/apm/get-started.md).
* `cloudbeat` - implements [Cloud Security Posture Management (CSPM)](../../solutions/security/cloud/cloud-security-posture-management.md) integrations.
* `fleet-server`, implements [Fleet Server](../fleet/fleet-server.md) for managing {{agents}}.
* `pf-elastic-symbolizer` - a server side component of Elastic [Universal Profiling](../../solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md).
* `pf-elastic-collector` - a server side component of Elastic [Universal Profiling](../../solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md).

Beginning in version 9.0, for {{agents}} to have the full functionality that was supported by default in pre-9.x versions, you need to install the servers {{agent}} flavor.

### Flavors for container package installs

#### Basic flavor [elastic-agent-basic-flavor-container]

For containerized environments, the basic {{agent}} flavor is installed using the `elastic-agent-slim` command with an agent container package. This flavor contains the same set of components described in [Basic flavor](#elastic-agent-basic-flavor-regular) above.

#### Servers flavor [elastic-agent-servers-flavor-container]

For containerized environments, the servers {{agent}} flavor is installed using the default `elastic-agent` command with an agent container package. This flavor contains the same set of components described in [Servers flavor](#elastic-agent-servers-flavor-regular) above.

{applies_to}`stack: ga 9.1` The servers {{agent}} flavor also includes the [journald](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) dependencies necessary to use the [journald input](beats://reference/filebeat/filebeat-input-journald.md).

#### Complete flavor [elastic-agent-complete-flavor]

For containerized environments, the complete {{agent}} flavor is installed using the `elastic-agent-complete` command with an agent container package. This flavor includes all of the components in the servers flavor, and also includes additional dependencies to run browser monitors through Elastic Synthetics. Refer to [Synthetic monitoring via Elastic Agent and Fleet](/solutions/observability/synthetics/get-started.md) for more information.

The complete {{agent}} flavor also includes the [journald](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) dependencies necessary to use the [journald input](beats://reference/filebeat/filebeat-input-journald.md).

## Resource requirements [elastic-agent-installation-resource-requirements]

The {{agent}} resources consumption is influenced by the number of integration and the environment its been running on.

Using our lab environment as an example, we can observe the following resource consumption:


### CPU and RSS memory size [_cpu_and_rss_memory_size]

We tested using an AWS `m7i.large` instance type with 2 vCPUs, 8.0 GB of memory, and up to 12.5 Gbps of bandwidth. The tests ingested a single log file using both the [throughput and scale preset](/reference/fleet/elasticsearch-output.md#output-elasticsearch-performance-tuning-settings) with self monitoring enabled. These tests are representative of use cases that attempt to ingest data as fast as possible. This does not represent the resource overhead when using [{{elastic-defend}}](integration-docs://reference/endpoint/index.md).

| Resource | Throughput | Scale |
| --- | --- | --- |
| **CPU**[^1^](#footnote-1) | ~67% | ~20% |
| **RSS memory size**[^1^](#footnote-1) | ~280 MB | ~220 MB |
| **Write network throughput** | ~3.5 MB/s | 480 KB/s |

^1^ $$$footnote-1$$$ including all monitoring processes

Adding integrations will increase the memory used by the agent and its processes.


### Size on disk [_size_on_disk]

The disk requirements for {{agent}} vary by operating system and {{stack}} version.

| Operating system | 8.13 | 8.14 | 8.15 | 8.18 | 9.0 |
| --- | --- | --- | --- |
| **Linux** | 1800 MB | 1018 MB | 1060 MB | 1.5 GB | 1.5 GB |
| **macOS** | 1100 MB | 619 MB | 680 MB | 775 MB | 775 MB |
| **Windows** | 891 MB | 504 MB | 500 MB | 678 MB | 705 MB |

During upgrades, double the disk space is required to store the new {{agent}} binary. After the upgrade completes, the original {{agent}} is removed from disk to free up the space.
