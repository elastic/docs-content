---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-deployment-templates.html
---

# Deployment templates [ece-deployment-templates]

Deployment templates deploy the Elastic Stack on virtual hardware. Each template has a different blend of RAM, storage, and vCPU. This allows you to configure the Elastic Stack for different use cases, giving your deployments the resources they need.

The components of the Elastic Stack that we support as part of a deployment are called *instances* and include:

* Elasticsearch data tiers and master nodes
* Machine Learning (ML) nodes
* Kibana instances
* APM and Fleet instances
* Enterprise Search instances

Elastic Cloud Enterprise comes with some deployment templates already built in, but you can [create new deployment templates](ece-configuring-ece-create-templates.md) to address a particular use case you might have. To make the most out of your hardware, we also recommend that you [configure deployment templates](configure-deployment-templates.md), so that ECE knows where to deploy components of the Elastic Stack.

The deployment templates available are:

* **Default template**

    A template to get you started and for backwards compatibility with existing deployments.

    The default template is suitable for search and general all-purpose workloads that don’t require more specialized resources.

    Existing deployments that were created in an ECE version before 2.0 are switched to this template automatically, if you edit their deployment configuration. The template is fully backwards compatible and enables you to add Elastic Stack features such as machine learning and dedicated master nodes to existing deployments.

    ::::{tip}
    To use this template effectively, you must [tag your allocators](ece-configuring-ece-tag-allocators.md) and [edit the default instance configurations](ece-configuring-ece-instance-configurations-edit.md), so that ECE knows where to host the Elastic Stack products that are part of your deployment.
    ::::

* **Cross-cluster search template**

    This template manages remote connections for running Elasticsearch queries across multiple deployments and indices. These federated searches make it possible to break up large deployments into smaller, more resilient Elasticsearch clusters. You can organize deployments by departments or projects for example, but still have the ability to aggregate query results and get visibility into your Elastic Cloud Enterprise infrastructure. You can add remote connections either when you create your deployment or when you customize it. To know more about cross-cluster search, check [Enable cross-cluster search](https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs.html).

* **Elastic Security template**

    Use this template to prevent, collect, detect, and respond to threats for unified protection across your infrastructure. Check the [**Elastic Security**](../../../solutions/security.md) documentation for more information.

* **Elastic Enterprise Search template**

    Default deployment template for Elastic Enterprise Search. Check the [**Enterprise Search**](https://www.elastic.co/guide/en/enterprise-search/current/index.html) documentation for more information.

* **Elastic Observability template**

    This template allows you to consolidate your logs, metrics, application traces, and system availability with purpose-built UIs. Check the [**Elastic Observability**](../../../solutions/observability/get-started/what-is-elastic-observability.md) documentation for more information.



## Instance configurations [ece-getting-started-instance-configurations]

For instances to run well when they are used in your Elastic Cloud Enterprise deployment, they need the right hardware that supports their intended purpose. For that, Elastic Cloud Enterprise uses *instance configurations*. Instance configurations match the Elastic Stack components to allocators for deployment, and indicate how memory and storage resources get sized relative to each other, and what sizes are available. For example: If you have a logging use case that needs lots of storage space, you probably want your instance configuration to use at least some storage with large spindle drives rather than fast but more expensive SSD storage.

To determine where ECE should place specific components of the Elastic Stack for deployment, instance configurations match suitable allocators by filtering for tags with queries. You can edit instance configurations to change what allocators get matched by the queries, which in turn changes what components of the Elastic Stack get hosted on matching allocators when creating or changing a deployment.

Elastic Cloud Enterprise comes with a number of [default instance configurations](ece-configuring-ece-instance-configurations-default.md) built in, but just like new templates, you can [create instance configurations](ece-configuring-ece-instance-configurations-create.md) if you need additional ones.

