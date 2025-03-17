---
navigation_title: "{{ece}}"
applies_to:
  deployment:
    ece: ga
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-considerations.html
---

# Secure your {{ece}} orchestrator [ece-securing-considerations]

This section covers security settings for your {{ece}} orchestrator.

**Orchestrator-level security**

- [**Enforcing SELinux with RHEL/Podman installations**](secure-your-elastic-cloud-enterprise-installation/migrate-ece-on-podman-hosts-to-selinux-enforce.md): SELinux (Security-Enhanced Linux) is a security module that enforces mandatory access controls, helping to protect systems from unauthorized access and privilege escalation.
- [**TLS certificates**](secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md): Apply security controls to network communications. With {{ece}}, you manage proxy certificates for the HTTP layer. The transport layer is managed by ECE.
- [**Platform role-based access control**](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md): Define the roles of users who have access to your organization and its resources. Note that you can also [manage non-cloud users and roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
- [**Authentication providers**](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md): Integrate with external authentication providers, including Active Directory, LDAP, and SAML.


**Additional deployment-level security settings**

Additional security settings are available for you to configure individually for each deployment orchestrated using {{ece}}. Refer to [](secure-your-cluster-deployment.md) for more information.


## Notes about {{ece}} security

### Users with admin privileges [ece_users_with_admin_privileges] 

In {{ece}}, every user who can manage your installation through the Cloud UI or the RESTful API is a user with admin privileges. This includes both the `admin` user and the `readonly` user that get created when you install ECE on your first host. Initially, only the `admin` user has the required privileges to make changes to resources on ECE.

[Role-based access control](../users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for {{ece}} allows you to connect multiple users or user groups to the platform.

All {{es}} clusters come with X-Pack security features and support role-based access control. To learn more, check [Secure Your Clusters](../users-roles/cluster-or-deployment-auth.md).


### Encryption [ece_encryption] 

{{ece}} does not implement encryption at rest out of the box. To ensure encryption at rest for all data managed by {{ece}}, the hosts running {{ece}} must be configured with disk-level encryption, such as dm-crypt. In addition, snapshot targets must ensure that data is encrypted at rest as well.

Configuring dm-crypt or similar technologies is outside the scope of the {{ece}} documentation, and issues related to disk encryption are outside the scope of support.

{{ece}} provides full encryption of all network traffic by default.

TLS is supported when interacting with the [RESTful API of {{ece}}](https://www.elastic.co/docs/api/doc/cloud-enterprise/) and for the proxy layer that routes user requests to clusters of all versions. Internally, our administrative services also ensure transport-level encryption.


### Attack vectors versus separation of roles [ece-securing-vectors] 

As covered in [Separation of Roles](../deploy/cloud-enterprise/ece-roles.md), it is important to not mix certain roles in a production environment.

Specifically, a host that is used as an allocator should hold *only* the allocator role. Allocators run the {{es}} and {{kib}} nodes that handle your workloads, which can expose a larger attack surface than the internal admin services. By separating the allocator role from other roles, you reduce any potential security exposure.

{{ece}} is designed to ensure that an allocator has access only to the keys necessary to manage the clusters that it has been assigned. If there is a compromise of {{es}} or {{kib}} combined with a zero-day or Linux kernel exploit, for example, this design ensures that the entire {{ece}} installation or clusters other than those already managed by that allocator are not affected.

Security comes in layers, and running separate services on separate infrastructure is the last layer of defense, on top of other security features like the JVM security manager, system call filtering, and running nodes in isolated containers with no shared secrets.


### Hardware isolation
$$$ece_clusters_share_the_same_resources$$$

The {{es}} clusters you create on {{ece}} share the same resources. It is currently not possible to run a specific cluster on entirely dedicated hardware not shared by other clusters.


