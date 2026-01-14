---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autoops.html
applies_to:
  deployment:
    eck: ga 3.3
products:
  - id: cloud-kubernetes
---

# AutoOps [k8s-autoops]

This section describes how to configure and deploy AutoOps with ECK.

* [Configuration](configuration-autoops.md)

    * [AutoOps configuration](configuration-autoops.md#k8s-autoops-configuring-autoops)
    * [Connecting to AutoOps](configuration-autoops.md#k8s-autoops-connecting-to-autoops)
    * [Selecting {{es}} clusters](configuration-autoops.md#k8s-autoops-selecting-clusters)

::::{note}
AutoOps on ECK is available starting from ECK 3.3.0. Your {{es}} cluster must be on a [supported {{es}} version](https://www.elastic.co/support/eol) (7.17.x and above) and on an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an active self-managed trial.
::::

