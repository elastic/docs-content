---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-autoscaling.html
applies_to:
  deployment:
    ece: ga
    ess: ga
    eck: ga
---

# Autoscaling

::::{admonition} Indirect use only 
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::

The autoscaling feature allows an operator to create tiers of nodes. These nodes monitor themselves to decide if they need to scale, based on an operator-defined policy. An Elasticsearch cluster can use the autoscaling API to report if it needs more resources to meet the policy. For example, an operator could define a policy that a warm tier should scale on available disk space. Elasticsearch monitors disk space in the warm tier. If it predicts low disk space for current and future shard copies, the autoscaling API will report that the cluster needs to scale. It remains the responsibility of the operator to add the additional resources that the cluster signals it requires.

:::{{tip}} - Serverless handles autoscaling for you
By default, {{serverless-full}} automatically scales your {{es}} resources based on your usage. You don't need to enable autoscaling.
:::

A policy is composed of a list of roles and a list of deciders. The policy governs the nodes matching the roles. The deciders provide independent estimates of the capacity required. See [Autoscaling deciders](../deploy-manage/autoscaling/autoscaling-deciders.md) for details on available deciders.

Autoscaling supports:
* Scaling machine learning nodes up and down.
* Scaling data nodes up based on storage.

::::{note} 
Autoscaling is not supported on Debian 8.
::::
