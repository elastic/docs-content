# Autoscaling [xpack-autoscaling]

::::{note} 
{cloud-only}
::::


The [autoscaling](../../../deploy-manage/autoscaling.md) feature enables an operator to configure tiers of nodes that self-monitor whether or not they need to scale based on an operator-defined policy. Then, via the autoscaling API, an Elasticsearch cluster can report whether or not it needs additional resources to meet the policy. For example, an operator could define a policy that a warm tier should scale on available disk space. Elasticsearch would monitor and forecast the available disk space in the warm tier, and if the forecast is such that the cluster will soon not be able to allocate existing and future shard copies due to disk space, then the autoscaling API would report that the cluster needs to scale due to disk space. It remains the responsibility of the operator to add the additional resources that the cluster signals it requires.

A policy is composed of a list of roles and a list of deciders. Nodes matching the roles are governed by the policy. The deciders provide independent estimates of the capacity required. See [Autoscaling deciders](../../../deploy-manage/autoscaling/autoscaling-deciders.md) for more information on the deciders available.

Autoscaling supports the scale-up and scale-down of dedicated {{ml}} nodes. Autoscaling also supports the scale-up of data nodes based on storage.

::::{note} 
Autoscaling is not supported on Debian 8.
::::


