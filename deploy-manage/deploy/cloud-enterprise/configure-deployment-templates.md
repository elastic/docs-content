---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-templates.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Manage deployment templates [ece-configuring-ece-templates]

Deployment templates combine components of the {{stack}}, such as {{es}} nodes and {{kib}} instances, for different use cases. Compared to a one-size-fits-all approach to deploying the {{stack}}, templates provide much greater flexibility and ensure that your deployments have the resources they need to support your use cases. To make the most of deployment templates, you must configure ECE for them.

After installing or upgrading to ECE version 2.0 or later:

1. [Tag your allocators](ece-configuring-ece-tag-allocators.md) to tell ECE what kind of hardware you have available for {{stack}} deployments.
2. [Edit the default instance configurations](ece-configuring-ece-instance-configurations-edit.md) to match components of the {{stack}} to your tagged allocators.

If you do not perform these steps, {{ece}} will behave just as it did in versions before 2.0 and deploy the {{stack}} wherever there is space on allocators.

Have a use case that isn’t addressed by the ECE default templates? You can also:

* [Create your own instance configurations](ece-configuring-ece-instance-configurations-create.md) to match components of the {{stack}} to allocators, tailoring what resources they get and what sizes they support.
* [Create your own deployment templates](ece-configuring-ece-create-templates.md) to solve your own use cases better.


## Basic concepts [ece_basic_concepts] 

With ECE version 2.0, a number of new concepts got introduced. Here’s how allocator tags, instance configurations, and deployment templates relate to each other:

Allocator tag
:   Indicates what kind of hardware resources you have available. Used by instance configurations to find suitable allocators.

Instance configuration
:   Matches components of the {{stack}} to allocators for deployment and tailors how memory and storage resources get sized relative to each other, and what sizes are available. Used as a building block for deployment templates.

Deployment template
:   Solves a specific use case with the {{stack}}, such as a search or a logging use case. ECE provides some deployment templates out of the box to get you started, or you can create your own.











