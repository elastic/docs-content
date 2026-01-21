---
navigation_title: Failback when clusterA comes back
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_failback_when_clustera_comes_back_2.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Bi-directional recovery: Failback when clusterA comes back [_failback_when_clustera_comes_back_2]

1. You can simulate this by turning `cluster A` back on.
2. Data ingested to `cluster B` during `cluster A` 's downtime will be automatically replicated.

    * data streams on cluster A

        * 150 documents in `logs-generic-default-replicated_from_clusterb`
        * 50 documents in `logs-generic-default`

    * data streams on cluster B

        * 50 documents in `logs-generic-default-replicated_from_clustera`
        * 150 documents in `logs-generic-default`

3. If you have {{ls}} running at this time, you will also observe traffic is sent to both clusters.

