---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability.html
---

# Backup, high availability, and resilience tools [high-availability]

Your data is important to you. Keeping it safe and available is important to Elastic. Sometimes your cluster may experience hardware failure or a power loss. To help you plan for this, {{es}} offers a number of features to achieve high availability despite failures. Depending on your deployment type, you might need to provision servers in different zones or configure external repositories to meet your organization’s availability needs.

* **[Design for resilience](production-guidance/availability-and-resilience.md)**

    Distributed systems like Elasticsearch are designed to keep working even if some of their components have failed. An Elasticsearch cluster can continue operating normally if some of its nodes are unavailable or disconnected, as long as there are enough well-connected nodes to take over the unavailable node’s responsibilities.

    If you’re designing a smaller cluster, you might focus on making your cluster resilient to single-node failures. Designers of larger clusters must also consider cases where multiple nodes fail at the same time.

* **[Cross-cluster replication](tools/cross-cluster-replication.md)**

    To effectively distribute read and write operations across nodes, the nodes in a cluster need good, reliable connections to each other. To provide better connections, you typically co-locate the nodes in the same data center or nearby data centers.

    Co-locating nodes in a single location exposes you to the risk of a single outage taking your entire cluster offline. To maintain high availability, you can prepare a second cluster that can take over in case of disaster by implementing {{ccr}} (CCR).

    CCR provides a way to automatically synchronize indices from a leader cluster to a follower cluster. This cluster could be in a different data center or even a different content from the leader cluster. If the primary cluster fails, the secondary cluster can take over.

    ::::{tip} 
    You can also use CCR to create secondary clusters to serve read requests in geo-proximity to your users.
    ::::

* **[Snapshots](tools/snapshot-and-restore.md)**

    Take snapshots of your cluster that can be restored in case of failure.


