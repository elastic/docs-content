---
navigation_title: Common cluster issues
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-common-cluster-issues.html
---

% add other cluster topics if it makes sense (already in toc)
% or keep a "common issues" page and create new cluster section index page

# Fix common cluster issues [fix-common-cluster-issues]

This guide describes how to fix common errors and problems with {{es}} clusters.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](https://www.elastic.co/guide/en/cloud/current/ec-autoops.html).

::::


[Watermark errors](fix-watermark-errors.md)
:   Fix watermark errors that occur when a data node is critically low on disk space and has reached the flood-stage disk usage watermark.

[Circuit breaker errors](circuit-breaker-errors.md)
:   {{es}} uses circuit breakers to prevent nodes from running out of JVM heap memory. If Elasticsearch estimates an operation would exceed a circuit breaker, it stops the operation and returns an error.

[High CPU usage](high-cpu-usage.md)
:   The most common causes of high CPU usage and their solutions.

[High JVM memory pressure](high-jvm-memory-pressure.md)
:   High JVM memory usage can degrade cluster performance and trigger circuit breaker errors.

[Red or yellow cluster status](red-yellow-cluster-status.md)
:   A red or yellow cluster status indicates one or more shards are missing or unallocated. These unassigned shards increase your risk of data loss and can degrade cluster performance.

[Rejected requests](rejected-requests.md)
:   When {{es}} rejects a request, it stops the operation and returns an error with a `429` response code.

[Task queue backlog](task-queue-backlog.md)
:   A backlogged task queue can prevent tasks from completing and put the cluster into an unhealthy state.

[Diagnose unassigned shards](diagnose-unassigned-shards.md)
:   There are multiple reasons why shards might get unassigned, ranging from misconfigured allocation settings to lack of disk space.

[Troubleshooting an unstable cluster](../../deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md#cluster-fault-detection-troubleshooting)
:   A cluster in which nodes leave unexpectedly is unstable and can create several issues.

[Mapping explosion](mapping-explosion.md)
:   A cluster in which an index or index pattern as exploded with a high count of mapping fields which causes performance look-up issues for Elasticsearch and Kibana.

[Hot spotting](hotspotting.md)
:   Hot spotting may occur in {{es}} when resource utilizations are unevenly distributed across nodes.


