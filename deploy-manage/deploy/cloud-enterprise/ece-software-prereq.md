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
* [Swap considerations](#ece-swap-considerations)
* [XFS](#ece-xfs)
* [FIPS compliance](#ece-fips)


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


## Swap [ece-swap-considerations]

Swap requirements depend on the ECE roles assigned to the host:
* **Director hosts:** Do not enable swap. Directors run ZooKeeper, and swap can severely degrade ZooKeeper performance. For background, refer to the [ZooKeeper administrator guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html).
* **All other hosts, including allocators:** Enable swap. If the host runs out of memory, the Linux OOM killer can stop a random process. Swap acts as a last-resort safeguard and helps protect ECE service availability.

:::{admonition} Use swap only as an emergency safety net
A container runtime process, such as Docker or Podman, running on swap can cause allocator failures due to API timeouts. Do not rely on it to overcommit memory or reduce host RAM. Size allocator capacity so the OS does not need swap during normal operation. For allocator capacity planning, refer to [](./ece-manage-capacity.md).
:::

As a baseline, provision at least 512 MB of swap. A common safeguard is 4 GB of swap for every 32 GB of RAM.

Set `vm.swappiness` to `1` so the kernel uses swap only as a last resort. The OS preparation guides in [](./configure-operating-system.md) include this setting.

How you create swap space depends on your operating system and infrastructure provider. Use your OS or cloud provider documentation to create a swap file or partition.

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
