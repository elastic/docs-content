---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-software-prereq.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Software prerequisites [ece-software-prereq]

To install ECE, make sure you prepare your environment with the following software. Pay special attention to what Linux kernel and Docker or Podman versions you plan to use and follow our recommendations. Our testing has shown that not all software combinations work well together.

* [Supported Linux kernel](#ece-linux-kernel)
* [Linux distributions with compatible Docker versions](#ece-linux-docker)
* [Free RAM](#ece-free-ram)
* [XFS](#ece-xfs)
* [FIPS compliance](#ece-fips)
* [Swap considerations](#ece-swap-considerations)


## Supported Linux kernel [ece-linux-kernel] 

{{ece}} requires 3.10.0-1160.31.1 or later on RHEL.

We recommend using kernel 4.15.x or later on Ubuntu.

To check your kernel version, run `uname -r`.

::::{note} 
{{ece}} is not supported on Linux distributions that use [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html) version 2.
::::



## Linux distributions with compatible Docker or Podman versions [ece-linux-docker] 

ECE requires using a supported combination of Linux distribution and Docker or Podman version, following our official Support matrix:

[https://www.elastic.co/support/matrix#elastic-cloud-enterprise](https://www.elastic.co/support/matrix#elastic-cloud-enterprise)

1. Check your operating system:

    ```sh
    cat /etc/os-release
    ```

2. Check whether Docker or Podman is installed and its version is compatible with ECE:

    ```sh
    docker --version
    ```

    ```sh
    podman --version
    ```


::::{note} 
{{ece}} does not support Amazon Linux.
::::



## Free RAM [ece-free-ram] 

ECE requires at least 8GB of free RAM. Check how much free memory you have:

```sh
free -h
```


## XFS [ece-xfs] 

XFS is required if you want to use disk space quotas for {{es}} data directories.

Disk space quotas set a limit on the amount of disk space an {{es}} cluster node can use. Currently, quotas are calculated by a static ratio of 1:32, which means that for every 1 GB of RAM a cluster is given, a cluster node is allowed to consume 32 GB of disk space.

::::{important} 
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly.
::::


## FIPS compliance [ece-fips]

:::{include} /deploy-manage/deploy/_snippets/ece-fips-message.md
:::

For more information about FIPS compliance across the {{stack}}, refer to [](/deploy-manage/security/fips.md).


## Swap considerations [ece-swap-considerations]

Unlike Elasticsearch nodes, which run with [swap disabled](/deploy-manage/deploy/self-managed/setup-configuration-memory.md), ECE hosts have different swap requirements based on their roles.

### Director hosts

Do not enable swap on director hosts. ECE director hosts run ZooKeeper, and swapping can significantly degrade ZooKeeper performance. Refer to the [ZooKeeper administrator guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html) for details.

### Allocator and other hosts

Enable swap on all ECE hosts except director hosts to improve system stability. If an allocator runs out of memory, the Linux out-of-memory (OOM) killer might terminate a random process on the host. Having swap space available provides a safeguard against sudden memory pressure and helps protect the availability of ECE services.

:::{important}
Swap should be treated as an emergency safety net only — not as a way to overcommit memory or reduce host RAM. If a container runtime process (Docker or Podman) runs on swap, it can cause allocator failures due to API timeouts (visible as errors in `allocator.log`). Always ensure allocators are not over-allocated so the OS does not routinely rely on swap.
:::

There is no specific recommendation for sizing swap, but 4 GB of swap per 32 GB of RAM has proven to be a reasonable safeguard for most ECE installations. As a baseline, ECE hosts should have at least 512 MB of swap space.

To ensure that swap remains a last-resort safeguard, set the `vm.swappiness` kernel setting to `1`, as described in the [Configure your OS](./configure-operating-system.md) preparation guides.

The method for provisioning swap space depends on your operating system and infrastructure provider. Consult your OS or cloud provider's documentation for instructions on creating a swap file or partition.
