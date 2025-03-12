# Secure the {{stack}} [secure-cluster]

The {{stack}} is comprised of many moving parts. There are the {{es}} nodes that form the cluster, plus {{ls}} instances, {{kib}} instances, {{beats}} agents, and clients all communicating with the cluster. To keep your cluster safe, adhere to the [{{es}} security principles](../../../deploy-manage/security.md).

The first principle is to run {{es}} with security enabled. Configuring security can be complicated, so we made it easy to [start the {{stack}} with security enabled and configured](../../../deploy-manage/security/security-certificates-keys.md). For any new clusters, just start {{es}} to automatically enable password protection, secure internode communication with Transport Layer Security (TLS), and encrypt connections between {{es}} and {{kib}}.

If you have an existing, unsecured cluster (or prefer to manage security on your own), you can [manually enable and configure security](../../../deploy-manage/security/manually-configure-security-in-self-managed-cluster.md) to secure {{es}} clusters and any clients that communicate with your clusters. You can also implement additional security measures, such as role-based access control, IP filtering, and auditing.

Enabling security protects {{es}} clusters by:

* [Preventing unauthorized access](../../../deploy-manage/security.md#preventing-unauthorized-access) with password protection, role-based access control, and IP filtering.
* [Preserving the integrity of your data](../../../deploy-manage/security.md#preserving-data-integrity) with SSL/TLS encryption.
* [Maintaining an audit trail](../../../deploy-manage/security.md#maintaining-audit-trail) so you know who’s doing what to your cluster and the data it stores.

::::{tip} 
If you plan to run {{es}} in a Federal Information Processing Standard (FIPS) 140-2 enabled JVM, see [FIPS 140-2](../../../deploy-manage/security/fips-140-2.md).
::::



## Preventing unauthorized access [preventing-unauthorized-access] 

To prevent unauthorized access to your {{es}} cluster, you need a way to *authenticate* users in order to validate that a user is who they claim to be. For example, making sure that only the person named *Kelsey Andorra* can sign in as the user `kandorra`. The {{es-security-features}} provide a standalone authentication mechanism that enables you to quickly password-protect your cluster.

If you’re already using LDAP, Active Directory, or PKI to manage users in your organization, the {{security-features}} integrate with those systems to perform user authentication.

In many cases, authenticating users isn’t enough. You also need a way to control what data users can access and what tasks they can perform. By enabling the {{es-security-features}}, you can *authorize* users by assigning access privileges to roles and assigning those roles to users. Using this role-based access control mechanism (RBAC), you can limit the user `kandorra` to only perform read operations on the `events` index restrict access to all other indices.

The {{security-features}} also enable you to restrict the nodes and clients that can connect to the cluster based on [IP filters](../../../deploy-manage/security/ip-traffic-filtering.md). You can block and allow specific IP addresses, subnets, or DNS domains to control network-level access to a cluster.

See [User authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md) and [User authorization](../../../deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).


## Preserving data integrity and confidentiality [preserving-data-integrity] 

A critical part of security is keeping confidential data secured. {{es}} has built-in protections against accidental data loss and corruption. However, there’s nothing to stop deliberate tampering or data interception. The {{stack-security-features}} use TLS to preserve the *integrity* of your data against tampering, while also providing *confidentiality* by encrypting communications to, from, and within the cluster. For even	greater protection, you can increase the [encryption strength](../../../deploy-manage/security/enabling-cipher-suites-for-stronger-encryption.md).

See [Configure security for the {{stack}}](../../../deploy-manage/security/security-certificates-keys.md).


## Maintaining an audit trail [maintaining-audit-trail] 

Keeping a system secure takes vigilance. By using {{stack-security-features}} to maintain an audit trail, you can easily see who is accessing your cluster and what they’re doing. You can configure the audit level, which accounts for the type of events that are logged. These events include failed authentication attempts, user access denied, node connection denied, and more. By analyzing access patterns and failed attempts to access your cluster, you can gain insights into attempted attacks and data breaches. Keeping an auditable log of the activity in your cluster can also help diagnose operational issues.

See [Enable audit logging](../../../deploy-manage/security/logging-configuration/enabling-audit-logs.md).

