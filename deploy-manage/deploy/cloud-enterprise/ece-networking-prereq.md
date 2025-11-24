---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-networking-prereq.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Networking prerequisites [ece-networking-prereq]

The first host you install ECE on initially requires the ports for all roles to be open, which includes the ports for the coordinator, allocator, director, and proxy roles. After you have brought up your initial ECE installation, only the ports for the roles that the initial host continues to hold need to remain open. Before installing a host, make sure that ports 20000, 21000, and 22000 are open for the installation script checks. Port 2375 will also be utilized on each host you install ECE on for internal Docker communication.

For versions 2.4.0 and 2.4.1, IPv6 should remain enabled on any host with the Proxy role. In 2.4.2 and later, IPv6 can be disabled.

* [Inbound traffic](#ece-inbound)
* [Outbound traffic](#ece-outbound)
* [Container communication on the same host](#ece-container-communication)
* [Hosts in multiple data centers](#ece-multiple-data-centers)

## Inbound traffic [ece-inbound]

When there are multiple hosts for each role, the inbound networking and ports can be represented by the following diagram:

![ECE networking and ports](/deploy-manage/images/cloud-enterprise-ece-networking-ports.png "")

**Inbound traffic from any source**

| **Number** | **Host role** | **Inbound ports** | *Purpose* |
| --- | --- | --- | --- |
|  | All | 22 | Installation and troubleshooting SSH access only (TCP)<br> |
| 2 | Coordinator | 12300/12343, 12400/12443 | Admin API access (HTTP/HTTPS)<br> |
| 3 | Proxy | 9200, 9243 | {{es}} REST API. 9200 is plain text and 9243 is with TLS, also required by load balancers<br> |
| 3 | Proxy | 9300, 9343 | {{es}} transport client. 9300 is plain text and 9343 is with TLS, also required by load balancers<br> |
| 3 | Proxy | 9400, 9443 | {{es}} Cross Cluster Search and Cross Cluster Replication with TLS authentication (9400) or API key authentication (9443), also required by load balancers. Can be blocked if [CCR/CCS](../../remote-clusters/ece-enable-ccs.md) is not used.<br> |
| 7 | Coordinator | 12400/12443 | Cloud UI console to API  (HTTP/HTTPS)<br> |

**Inbound traffic from other ECE hosts**

| **Number** | **Host role** | **Inbound ports** | *Purpose* |
| --- | --- | --- | --- |
| 1 | Director | 2112 | ZooKeeper ensemble discovery/joining (TCP)<br> |
| 1 | Director | 12898-12908, 13898-13908 | ZooKeeper leader and election activity |
| 4 | Director | 12191-12201 | Client forwarder to ZooKeeper, one port per director (TLS tunnels)<br> |
| 5 | Allocator | 19000-19999 | {{es}} node to node and Proxy to {{es}} for CCR/CCS (Node Transport 6.x+/TLS 6.x+)<br> |
| 7 | Coordinator | 22191-22195 | Connections to initial coordinator from allocators and proxies, one port per coordinator, up to five (TCP)<br> |
| 9 | Proxy | 9200/9243, 9300/9343 | {{kib}} and {{es}} (HTTPS)<br> |
| 10 | Allocator | 18000-18999 | Constructor to {{es}} cluster (HTTPS)<br> |
| 11 | Allocator | 18000-18999/20000-20999 | Proxy to Elasticsearch/Kibana/APM Server instance (HTTPS/Transport Client 6.x+/TLS 6.x+)<br> |
|  | Allocator | 21000-21999 | APM Server (Instance Monitoring)<br> |
| 12 | Allocator | 23000-23999 | {{es}} node to node and Proxy to {{es}} for CCR/CCS using Remote Cluster Security<br> |
| 13 | Allocator | 14000 | Proxy to Allocator service endpoint (HTTPS)<br> |
| 14 | Proxy | 14043 | API to Proxy for Allocator service traffic (HTTPS)<br> |


## Outbound traffic [ece-outbound]

Open these ports for outbound traffic:

| Host role | Outbound ports | Purpose |
| --- | --- | --- |
| All | 80 | Installation script and docker.elastic.co Docker registry access (HTTP) |
| All | 443 | Installation script and docker.elastic.co Docker registry access (HTTPS) |

::::{note}
Outbound traffic must also permit connections to the [snapshot repositories](../../tools/snapshot-and-restore/cloud-enterprise.md) you intend to use. Ports depend on the snapshot repository type. Refer to the external supported providers to confirm the exact list of ports.
::::


## Container communication on the same host [ece-container-communication-on-same-host]

The following ports need to be open for containers communicating with the host and/or with each other on the same host:

| Port(s) | Purpose | Host role |
| --- | --- | --- |
| 53 | DNS resolver | All roles |
| 2180 | ZooKeeper admin port | All roles |
| 2375 | Docker admin port | All roles |
| 2191-2199 | Debug ports | Director |
| 5000-5010 | JVM/debug ports | All roles |
| 8080-8084 | Health/monitoring ports | All roles |
| 9000, 9043 | Internal proxy use | Proxy |
| 9244 | Internal proxy port | All roles |


## Hosts in multiple data centers [ece-multiple-data-centers]

A typical ECE installation should be contained within a single data center. We recommend that ECE installations not span different data centers, due to variations in networking latency and bandwidth that cannot be controlled.

Installation of ECE across multiple data centers might be feasible with sufficiently low latency and high bandwidth, with some restrictions around what we can support. Based on our experience with our hosted {{ecloud}} service, the following is required:

* A typical network latency between the data centers of less than 10ms round-trip time during pings
* A network bandwidth of at least 10 Gigabit

If you choose to deploy a single ECE installation across multiple data centers, you might need to contend with additional disruptions due to bandwidth or latency issues. Both ECE and {{es}} are designed to be resilient to networking issues, but this resiliency is intended to handle exceptions and should not be depended on as part of normal operations. If Elastic determines during a support case that an issue is related to an installation across multiple data centers, the recommended resolution will be to consolidate your installation into a single data center, with further support limited until consolidation is complete.

