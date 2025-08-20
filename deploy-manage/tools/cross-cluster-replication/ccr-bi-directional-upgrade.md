---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-bi-directional-upgrade.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Bi-directional index following [ccr-bi-directional-upgrade]

In a bi-directional configuration, each cluster contains both leader and follower indices.

When upgrading clusters in this configuration, [pause all index following](ccr-pause-replication.md) and [pause auto-follow patterns](ccr-auto-follow-pause.md) prior to upgrading both clusters.

After upgrading both clusters, resume index following and resume replication of auto-follow patterns.

