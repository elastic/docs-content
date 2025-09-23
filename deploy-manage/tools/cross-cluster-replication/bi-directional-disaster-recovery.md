---
navigation_title: Bi-directional disaster recovery
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-disaster-recovery-bi-directional-tutorial.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---



# Bi-directional disaster recovery [ccr-disaster-recovery-bi-directional-tutorial]


Learn how to set up disaster recovery between two clusters based on bi-directional {{ccr}}. The following tutorial is designed for data streams which support [update by query](../../../manage-data/data-store/data-streams/use-data-stream.md#update-docs-in-a-data-stream-by-query) and [delete by query](../../../manage-data/data-store/data-streams/use-data-stream.md#delete-docs-in-a-data-stream-by-query). You can only perform these actions on the leader index.

This tutorial works with {{ls}} as the source of ingestion. It takes advantage of a {{ls}} feature where [the {{ls}} output to {{es}}](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md) can be load balanced across an array of hosts specified. {{beats}} and {{agents}} currently do not support multiple outputs. It should also be possible to set up a proxy (load balancer) to redirect traffic without {{ls}} in this tutorial.

* Setting up a remote cluster on `clusterA` and `clusterB`.
* Setting up bi-directional cross-cluster replication with exclusion patterns.
* Setting up {{ls}} with multiple hosts to allow automatic load balancing and switching during disasters.

:::{image} /deploy-manage/images/elasticsearch-reference-ccr-bi-directional-disaster-recovery.png
:alt: Bi-directional cross cluster replication failover and failback
:::





