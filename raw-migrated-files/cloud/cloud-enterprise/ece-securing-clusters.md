# Secure your clusters [ece-securing-clusters]

Elastic Cloud Enterprise supports most of the security features that are part of the Elastic Stack. These features are designed to:

* Prevent unauthorized access with password protection and role-based access control:

    * Reset the [`elastic` user password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Use third-party authentication providers like [SAML](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md), [LDAP](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md), [Active Directory](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md), [OpenID Connect](../../../deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md) to provide dynamic [role mappings](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) for role based or attribute based access control.
    * Use {{kib}} Spaces and roles to [secure access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).
    * Authorize and authenticate service accounts for {{beats}} by [granting access using API keys](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/beats-api-keys.md).


* Block unwanted traffic with [traffic filter](../../../deploy-manage/security/traffic-filtering.md).
* Secure your settings with the Elasticsearch [keystore](../../../deploy-manage/security/secure-settings.md).










