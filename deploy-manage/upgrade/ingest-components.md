---
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
---
# Upgrade your ingest components

Once you've successfully [upgraded your deployment or cluster](/deploy-manage/upgrade/deployment-or-cluster.md), the final step is to update your ingest components and clients in the following order: 

1. {{agent}}: [Upgrade instructions](../../reference/fleet/upgrade-elastic-agent.md)
2. {{beats}}: [Upgrade instructions](beats://reference/libbeat/upgrading.md)
3. {{ls}}: [Upgrade instructions](logstash://reference/upgrading-logstash.md)
4. Custom clients 