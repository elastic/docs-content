---
navigation_title: Nodes
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-nodes-view.html
applies_to:
  deployment:
    ess: all
    self:
    ece:
    eck:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Nodes view in AutoOps [ec-autoops-nodes-view]

The **Nodes** view provides a thorough look into essential metrics for all monitored nodes. With this view, you can gain deeper insight into your cluster's health on a per-node basis and observe each metric over extended periods of time.

To get to the **Nodes** view, go to AutoOps in your deployment or cluster and select **Nodes** from the side navigation.

:::{image} /deploy-manage/images/cloud-autoops-node-view.png
:screenshot:
:alt: Screenshot showing the Nodes view in AutoOps
:::

## Panels in the Nodes view

The **Nodes** view shows the following panels.

### Nodes

The **Nodes** table lists all the nodes used by the {{es}} cluster, along with their name, role, and status. The elected master node is marked with a star.

### Open Events

The **Open Events** panel lists open events sorted by severity and time. When the conditions that triggered the event no longer exist, the event is automatically set to close and appear in the **Events History** panel. Closing an event does not necessarily indicate that the customer resolved the issue, but rather that AutoOps no longer detects it.

### Panels covering other monitoring areas

The following table lists all the other panels in the **Nodes** view that drill down into specific monitoring areas, along with the names and descriptions of metrics they present. 

| Area | Metrics name | Metrics description | 
| --- | --- | --- | 
| Activity | Indexing rate | Number of documents being indexed per second on all primary and replica shards hosted on the node. |
|  | Indexing latency | Average latency for indexing documents, which is the time it takes to index documents divided by the number that were indexed in all primary and replica shards hosted on the node. |
|  | Search rate | Number of search requests being executed per second on all shards hosted on the node. |
|  | Search latency | Average latency for searching, which is the time it takes to execute searches divided by the number of searches submitted to the node. |
| Host and Process | Load | Load average of the node over the last five minutes. |
|  | CPU | Percentage of the CPU usage for the {{es}} process running on the node. |
|  | Heap used in bytes | Total JVM heap memory used by the {{es}} process running on the node. |
|  | GC | Average time spent doing GC in milliseconds on the node. |
| Thread pools | Write | Number of index, bulk and write operations in the queue, as well as the total number of completed and rejected operations in those pools. |
|  | Search | Number of search operations in the queue, as well as the total number of completed and rejected operations in that pool. |
|  | Management | Number of management operations in the queue, as well as the total number of completed and rejected operations in that pool. |
|  | Snapshot | Number of snapshot operations in the queue, as well as the total number of completed and rejected operations in that pool. 
| Data | Disk usage | Amount of used disk storage on the node. |
|  | Shards count | Number of primary and replica shards hosted on the node. |
|  | Segment count | Number of segments hosted on the node. |
|  | Documents count | Number of documents hosted on the node. |
| HTTP | HTTP current open | Current number of open HTTP connections for the node. |
|  | HTTP connections open rate | Number of HTTP connections opened per second. |
| Circuit breakers | Parent Used | Estimated memory used for the parent circuit breaker. |
|  | Field Data used | Estimated memory used for the field data circuit breaker. |
|  | Request used | Estimated memory used for the request circuit breaker. |
|  | Parent tripped | Total number of times the parent circuit breaker has been triggered and prevented an out-of-memory error. |
|  | Field data tripped | Total number of times the field data circuit breaker has been triggered and prevented an-out-of memory error. |
|  | Request tripped | Total number of times the request circuit breaker has been triggered and prevented an out-of-memory error. |
| Network | Network rx bytes | Size of RX packets received by the node during internal cluster communication. |
|  | Network rx count | Total number of RX packets received by the node during internal cluster communication. |
|  | Network tx bytes | Size of TX packets sent by the node during internal cluster communication. |
|  | Network tx count | Total number of TX packets received by the node during internal cluster communication. |
| Disk | Disk read bytes | The total number of bytes read across all devices used by {{es}}. |
|  | Disk read IOPS | The total number of completed read operations across all devices used by {{es}}. |
|  | Disk write bytes | The total number of bytes written across all devices used by {{es}}. |
|  | Disk write IOPS | The total number of completed write operations across all devices used by {{es}}. |
| Activity-Additional | Merge rate | Number of merge operations being executed per second on all shards hosted on the node. |
|  | Merge latency | Average latency for merging, which is the time it takes to execute merges divided by the number of merge operations submitted to the node. |
|  | Indexing failed | Number of failed indexing operations on the node. |

