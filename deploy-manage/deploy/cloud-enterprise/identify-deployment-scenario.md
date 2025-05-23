---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-deploy-scenario.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Identify the deployment scenario [ece-deploy-scenario]

Before you start deploying ECE, choose the deployment scenario that best fits your use case. All deployment scenarios have 3 director nodes for [high availability](ece-ha.md).


## Small deployment [ece_small_deployment]

The type of deployment is recommended for development, test, and small-scale use cases. You need:

* 3 hosts with 128 GB RAM
* 3 availability zones

:::{image} /deploy-manage/images/cloud-enterprise-ece-pb-3.png
:alt: A small baseline installation with three hosts across three availability zones
:::

* This type of installation is **not recommended for high-traffic workloads**.
* Avoid ECE installations with **spinning disks** as these are not supported when you run allocators and control plane on the same server.
* Note that the small-size ECE installation keeps the directors and coordinators roles (ECE management services) on the same hosts as your allocators and proxies.

You can proceed with this scenario and [install ECE](./install.md).

## Medium deployment [ece_medium_deployment]

This type of deployment is recommended for many production setups. You need:

* 3 hosts with at least 32 GB RAM each for directors and coordinators (ECE management services)
* 3 hosts for allocators, each with one of the following RAM configurations:

    * 1 x 256 GB RAM
    * 2 x 128 GB RAM
    * 4 x 64 GB RAM

* 3 hosts with 16 GB RAM each for proxies
* 3 availability zones

:::{image} /deploy-manage/images/cloud-enterprise-ece-pb-6.png
:alt: A medium installation with nine to twelve hosts across three availability zones
:::

* Monitor the load on proxies and make sure the volume of user requests routed by the proxies does not affect the resources available to the ECE management services.
* Note that the large-sized {{ece}} installation separates the allocator and proxy roles from the director and coordinator roles (ECE management services).

You can proceed with this scenario and [install ECE](./install.md).

## Large deployment [ece_large_deployment]

This type of deployment is recommended for deployments with significant overall search and indexing throughput. You need:

* 3 hosts with at least 64 GB RAM each for directors and coordinators (ECE management services)
* 3 hosts for allocators, each with one of the following RAM configurations:

    * 1 x 256 GB RAM
    * 2 x 128 GB RAM
    * 4 x 64 GB RAM

* 3 hosts with 16 GB RAM each for proxies
* 3 availability zones

:::{image} /deploy-manage/images/cloud-enterprise-ece-pb-9.png
:alt: A large installation with nine to twelve hosts across three availability zones
:::

Note that the large-sized {{ece}} installation separates the allocator and proxy roles from the director and coordinator roles (ECE management services).

You can proceed with this scenario and [install ECE](./install.md).