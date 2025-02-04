---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-considerations.html
---

# Secure your Elastic Cloud Enterprise installation [ece-securing-considerations]

Elastic Cloud Enterprise can run on shared and less secure environments, but you should be aware of some limitations when deploying our product.


### Users with admin privileges [ece_users_with_admin_privileges] 

In Elastic Cloud Enterprise 3.8.1, every user who can manage your installation through the Cloud UI or the RESTful API is a user with admin privileges. This includes both the `admin` user and the `readonly` user that get created when you install ECE on your first host. Initially, only the `admin` user has the required privileges to make changes to resources on ECE.

[Role-based access control](../users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for Elastic Cloud Enterprise allows you to connect multiple users or user groups to the platform.

All Elasticsearch clusters come with X-Pack security features and support role-based access control. To learn more, check [Secure Your Clusters](../users-roles/cluster-or-deployment-auth.md).


### Clusters share the same resources [ece_clusters_share_the_same_resources] 

The Elasticsearch clusters you create on Elastic Cloud Enterprise share the same resources. It is currently not possible to run a specific cluster on entirely dedicated hardware not shared by other clusters.


### Encryption [ece_encryption] 

Elastic Cloud Enterprise does not implement encryption at rest out of the box. To ensure encryption at rest for all data managed by Elastic Cloud Enterprise, the hosts running Elastic Cloud Enterprise must be configured with disk-level encryption, such as dm-crypt. In addition, snapshot targets must ensure that data is encrypted at rest as well.

Configuring dm-crypt or similar technologies is outside the scope of the Elastic Cloud Enterprise documentation, and issues related to disk encryption are outside the scope of support.

Elastic Cloud Enterprise provides full encryption of all network traffic by default when using Elasticsearch 6.0 or higher.

TLS is supported when interacting with the RESTful API of Elastic Cloud Enterprise and for the proxy layer that routes user requests to clusters of all versions. Internally, our administrative services also ensure transport-level encryption.

In Elasticsearch versions lower than 6.0, traffic between nodes in a cluster and between proxies and the clusters is *not* encrypted.


## Attack vectors versus separation of roles [ece-securing-vectors] 

As covered in [Separation of Roles](../deploy/cloud-enterprise/ece-roles.md), it is important to not mix certain roles in a production environment.

Specifically, a host that is used as an allocator should hold *only* the allocator role. Allocators run the Elasticsearch and Kibana nodes that handle your workloads, which can expose a larger attack surface than the internal admin services. By separating the allocator role from other roles, you reduce any potential security exposure.

Elastic Cloud Enterprise is designed to ensure that an allocator has access only to the keys necessary to manage the clusters that it has been assigned. If there is a compromise of Elasticsearch or Kibana combined with a zero-day or Linux kernel exploit, for example, this design ensures that the entire Elastic Cloud Enterprise installation or clusters other than those already managed by that allocator are not affected.

Security comes in layers, and running separate services on separate infrastructure is the last layer of defense, on top of other security features like the JVM security manager, system call filtering, and running nodes in isolated containers with no shared secrets.

