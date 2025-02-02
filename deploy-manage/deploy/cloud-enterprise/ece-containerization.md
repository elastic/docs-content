---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-containerization.html
---

# Services as Docker containers [ece-containerization]

Services are deployed as Docker containers, which simplifies the operational effort and makes it easy to provision similar environments for development and staging. Using Docker containers has the following advantages:

* **Shares of resources**

    Each cluster node is run within a Docker container to make sure that all of the nodes have access to a guaranteed share of host resources. This mitigates the *noisy neighbor effect* where one busy deployment can overwhelm the entire host. The CPU resources are relative to the size of the Elasticsearch cluster they get assigned to. For example, a cluster with 32GB of RAM gets assigned twice as many CPU resources as a cluster with 16GB of RAM.

* **Better security**

    On the assumption that any cluster can be compromised, containers are given no access to the platform. The same is true for the services: each service can read or write only those parts of the system state that are relevant to it. Even if some services are compromised, the attacker won’t get hold of the keys to the rest of them and will not compromise the whole platform.

* **Secure communication through Stunnel**

    Docker containers communicate securely with one another through Transport Layer Security, provided by [Stunnel](https://www.stunnel.org/) (as not all of the services or components support TLS natively). Tunneling all traffic between containers makes sure that it is not possible to eavesdrop, even when someone else has access to the underlying cloud or network infrastructure.
