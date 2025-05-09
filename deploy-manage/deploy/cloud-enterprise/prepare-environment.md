---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-prereqs.html
---

# Prepare your environment [ece-prereqs]

In this section you'll find all the prerequisites and environment preparations required to properly plan and install {{ece}} (ECE).

## Requirements [ece-prepare-requirements]

In {{ece}}, an ECE host is the server, virtual machine, or cloud instance where the ECE software is installed. An ECE installation consists of a cluster of multiple hosts, forming the platform where {{stack}} applications are orchestrated.

To prepare your hosts for installation, the following prerequisites **must** be met:

::::{important}
These prerequisites are critical to establish a supported ECE configuration. Using unsupported combinations can cause a number of either intermediate or potentially permanent issues with your ECE environment, such as failures to create [system deployments](system-deployments-configuration.md), failures to upgrade workload deployments, proxy timeouts, data loss, and more. If upgrading ECE, read [upgrade your installation](../../upgrade/orchestrator/upgrade-cloud-enterprise.md) for guidance.
::::

* [Hardware prerequisites](ece-hardware-prereq.md)
* [Software prerequisites](ece-software-prereq.md)
* [System configuration prerequisites](ece-sysconfig.md)
* [Networking prerequisites](ece-networking-prereq.md)
* [Users and permissions prerequisites](ece-users-permissions.md)

## Best practices and recommendations [ece-prepare-recommendations]

Follow these best practices to properly prepare your ECE installation:

* [High availability](ece-ha.md) - For production and mission-critical systems, high availability **must** be considered
* [Separation of roles](ece-roles.md) - To group components on ECE and prevent conflicting workloads, consider role separation
* [Load balancers](ece-load-balancers.md) - Using a load balancer is **strongly recommended**
* [JVM heap sizes](ece-jvm.md) - Configure the proper JVM heap size based on your use cases
* [Wildcard DNS record](ece-wildcard-dns.md) - Configure your own wildcard DNS record for production systems
* [Manage installation capacity](ece-manage-capacity.md) - Configure your memory, CPU quotas, processors and storage properly
