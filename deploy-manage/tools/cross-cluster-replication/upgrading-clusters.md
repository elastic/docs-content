---
navigation_title: Upgrading clusters
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-upgrading.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---



# Upgrading clusters [ccr-upgrading]


Clusters that are actively using {{ccr}} require a careful approach to upgrades. The following conditions could cause index following to fail during rolling upgrades:

* Clusters that have not yet been upgraded will reject new index settings or mapping types that are replicated from an upgraded cluster.
* Nodes in a cluster that has not been upgraded will reject index files from a node in an upgraded cluster when index following tries to fall back to file-based recovery. This limitation is due to Lucene not being forward compatible.

The approach to running a rolling upgrade on clusters where {{ccr}} is enabled differs based on uni-directional and bi-directional index following.



