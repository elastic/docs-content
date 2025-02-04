---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-software-prereq.html
---

# Software prerequisites [ece-software-prereq]

To install ECE, make sure you prepare your environment with the following software. Pay special attention to what Linux kernel and Docker or Podman versions you plan to use and follow our recommendations. Our testing has shown that not all software combinations work well together.

* [Supported Linux kernel](#ece-linux-kernel)
* [Linux distributions with compatible Docker versions](#ece-linux-docker)
* [Free RAM](#ece-free-ram)
* [XFS](#ece-xfs)


## Supported Linux kernel [ece-linux-kernel] 

Elastic Cloud Enterprise requires 3.10.0-1160.31.1 or later on RHEL.

We recommend using kernel 4.15.x or later on Ubuntu.

To check your kernel version, run `uname -r`.

::::{note} 
Elastic Cloud Enterprise is not supported on Linux distributions that use [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.md) version 2.
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
Elastic Cloud Enterprise does not support Amazon Linux.
::::



## Free RAM [ece-free-ram] 

ECE requires at least 8GB of free RAM. Check how much free memory you have:

```sh
free -h
```


## XFS [ece-xfs] 

XFS is required if you want to use disk space quotas for Elasticsearch data directories.

Disk space quotas set a limit on the amount of disk space an Elasticsearch cluster node can use. Currently, quotas are calculated by a static ratio of 1:32, which means that for every 1 GB of RAM a cluster is given, a cluster node is allowed to consume 32 GB of disk space.

::::{important} 
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly.
::::


