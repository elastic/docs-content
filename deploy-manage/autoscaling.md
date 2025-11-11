---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-autoscaling.html
applies_to:
  deployment:
    ece: ga
    ess: ga
    eck: ga
  serverless: all
products:
  - id: elasticsearch
---

# Autoscaling

The autoscaling feature adjusts resources based on demand. A deployment can use autoscaling to scale resources as needed, ensuring sufficient capacity to meet workload requirements. In {{ece}}, {{eck}}, and {{ech}} deployments, autoscaling follows predefined policies, while in {{serverless-short}}, it is fully managed and automatic.

:::{{tip}} - Serverless handles autoscaling for you
By default, {{serverless-full}} automatically scales your {{es}} resources based on your usage. You don't need to enable autoscaling.
:::

## Cluster autoscaling

::::{admonition} Indirect use only
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::

Cluster autoscaling allows an operator to create tiers of nodes that monitor themselves and determine if scaling is needed based on an operator-defined policy. An {{es}} cluster can use the autoscaling API to report when additional resources are required. For example, an operator can define a policy that scales a warm tier based on available disk space. {{es}} monitors disk space in the warm tier. If it predicts low disk space for current and future shard copies, the autoscaling API reports that the cluster needs to scale. It remains the responsibility of the operator to add the additional resources that the cluster signals it requires.

A policy is composed of a list of roles and a list of deciders. The policy governs the nodes matching the roles. The deciders provide independent estimates of the capacity required. See [Autoscaling deciders](../deploy-manage/autoscaling/autoscaling-deciders.md) for details on available deciders.

Cluster autoscaling supports:
* Scaling machine learning nodes up and down.
* Scaling data nodes up based on storage.

## Trained model autoscaling

:::{admonition} Trained model auto-scaling for self-managed deployments
The available resources of self-managed deployments are static, so trained model autoscaling is not applicable. However, available resources are still segmented based on the settings described in this section.
:::

Trained model autoscaling automatically adjusts the resources allocated to trained model deployments based on demand. This feature is available on all cloud deployments (ECE, ECK, ECH) and {{serverless-short}}. Refer to [Trained model autoscaling](/deploy-manage/autoscaling/trained-model-autoscaling.md) for details. 

To ensure availability and avoid unnecessary scaling, trained model deployments operate with defined [cooldown periods](/deploy-manage/autoscaling/trained-model-autoscaling.md#cooldown-periods).

Trained model autoscaling supports:
* Scaling trained model deployments

::::{note}
Autoscaling is not supported on Debian 8.
::::

Find instructions on setting up and managing autoscaling, including supported environments, configuration options, and examples:

* [Autoscaling in {{ece}} and {{ech}}](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)
* [Autoscaling in {{eck}}](/deploy-manage/autoscaling/autoscaling-in-eck.md)
* [Autoscaling deciders](/deploy-manage/autoscaling/autoscaling-deciders.md)
* [Trained model autoscaling](/deploy-manage/autoscaling/trained-model-autoscaling.md)
