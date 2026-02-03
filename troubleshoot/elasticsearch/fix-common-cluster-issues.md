---
navigation_title: Common cluster issues
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-common-cluster-issues.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Fix common cluster issues [fix-common-cluster-issues]

Use these topics to fix common issues with {{es}} clusters.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
::: 

[](fix-watermark-errors.md)
:   Fix watermark errors that occur when a data node is critically low on disk space and has reached the flood-stage disk usage watermark.

[](circuit-breaker-errors.md)
:   {{es}} uses circuit breakers to prevent nodes from running out of JVM heap memory. If {{es}} estimates an operation would exceed a circuit breaker, it stops the operation and returns an error.

[](high-cpu-usage.md)
:   The most common causes of high CPU usage and their solutions.

[](high-jvm-memory-pressure.md)
:   High JVM memory usage can degrade cluster performance and trigger circuit breaker errors.

[](red-yellow-cluster-status.md)
:   A red or yellow cluster status indicates one or more shards are missing or unallocated. These unassigned shards increase your risk of data loss and can degrade cluster performance.

[](rejected-requests.md)
:   When {{es}} rejects a request, it stops the operation and returns an error with a `429` response code.

[](task-queue-backlog.md)
:   A backlogged task queue can prevent tasks from completing and put the cluster into an unhealthy state.

[](mapping-explosion.md)
:   A cluster in which an index or index pattern as exploded with a high count of mapping fields which causes performance look-up issues for {{es}} and {kib}.

[](hotspotting.md)
:   Hot spotting can occur in {{es}} when resource utilizations are unevenly distributed across nodes.

## Additional resources

* [Troubleshoot {{es}}](/troubleshoot/elasticsearch.md)
* [Troubleshooting overview](/troubleshoot/index.md)

