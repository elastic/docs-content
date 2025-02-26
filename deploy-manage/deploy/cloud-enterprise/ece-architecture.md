---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-architecture.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-containerization.html
---

# Service-oriented architecture [ece-architecture]

Elastic Cloud Enterprise has a service-oriented architecture that lets you:

* Scale each service separately, with different reliability and performance requirements.
* Access services through the API.
* Deploy each service independently in its own Docker container.

:::{image} ../../../images/cloud-enterprise-ece-architecture.png
:alt: Elastic Cloud Enterprise high level architecture
:::

## Control plane [ece_control_plane]

The *control plane* of ECE include the following management services:

**ZooKeeper**

* [ZooKeeper](http://zookeeper.apache.org/) is a distributed, strongly consistent data store.
* Holds essential information for ECE components: Proxy routing tables, memory capacity advertised by the allocators, changes committed through Admin Console, and so on.
* Acts as a message bus for communication between the services.
* Talks to ECE components using STunnel.
* Stores the state of the ECE installation and the state of all deployments running in ECE.

**Director**

* Manages the ZK data store and signs the CSRs (certificate signing requests) for internal clients that want to communicate with ZooKeeper.
* Maintains the stunnels used by ZooKeeper for communication and establishes quorum when new ZooKeeper nodes are created.

**Constructor**

* Works like a scheduler that monitors requests from the Admin console.
* Determines what needs to be changed, and writes the changes to ZooKeeper nodes monitored by the allocators.
* Assigns cluster nodes to allocators.
* Maximizes the utilization of underlying allocators to reduce the need to spin up extra hardware for new deployments.
* Places cluster nodes and instances within different availability zones to ensure that the deployment can survive any downtime of a whole zone. You can designate these availability zones when you install ECE.

**Cloud UI and API**

Provide web and API access for administrators to manage and monitor the ECE installation.


## Proxies [ece_proxies]

* Handle user requests, mapping deployment IDs that are passed in request URLs for the container to the actual Elasticsearch cluster nodes and other instances. The association of deployment IDs to a container is stored in ZooKeeper, cached by the proxies. In the event of ZooKeeper downtime, the platform can still service the requests to existing deployments by using the cache.
* Keep track of the state and availability of zones, if you have a highly available Elasticsearch cluster. If one of the zones goes down, the proxy will not route any requests there.
* Help with no-downtime scaling and upgrades. Before performing an upgrade, a snapshot is taken, and data is migrated to the new nodes. When the migration is complete, a proxy switches the traffic to the new nodes and disconnects the old ones.
* Multiple proxies are usually configured behind a load balancer to ensure that the system remains available.


## Allocators [ece-architecture-allocators]

* Run on all the machines that host Elasticsearch nodes and Kibana instances.
* Control the lifecycle of cluster nodes by:

    * Creating new containers and starting Elasticsearch nodes when requested
    * Restarting a node if it becomes unresponsive
    * Removing a node if it is no longer needed

* Advertise the memory capacity of the underlying host machine to ZooKeeper so that the Constructor can make an informed decision on where to deploy.

## Services as Docker containers [ece-containerization]

Services are deployed as Docker containers, which simplifies the operational effort and makes it easy to provision similar environments for development and staging. Using Docker containers has the following advantages:

* **Shares of resources**

    Each cluster node is run within a Docker container to make sure that all of the nodes have access to a guaranteed share of host resources. This mitigates the *noisy neighbor effect* where one busy deployment can overwhelm the entire host. The CPU resources are relative to the size of the Elasticsearch cluster they get assigned to. For example, a cluster with 32GB of RAM gets assigned twice as many CPU resources as a cluster with 16GB of RAM.

* **Better security**

    On the assumption that any cluster can be compromised, containers are given no access to the platform. The same is true for the services: each service can read or write only those parts of the system state that are relevant to it. Even if some services are compromised, the attacker won’t get hold of the keys to the rest of them and will not compromise the whole platform.

* **Secure communication through Stunnel**

    Docker containers communicate securely with one another through Transport Layer Security, provided by [Stunnel](https://www.stunnel.org/) (as not all of the services or components support TLS natively). Tunneling all traffic between containers makes sure that it is not possible to eavesdrop, even when someone else has access to the underlying cloud or network infrastructure.

