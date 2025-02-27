# Securing your deployment [ec-security]

The security of {{ech}} is described on the [{{ecloud}} security](https://www.elastic.co/cloud/security) page. In addition to the security provided by {{ecloud}}, you can take the following steps to secure your deployments:

* Prevent unauthorized access with password protection and role-based access control:

    * Reset the [`elastic` user password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Use third-party authentication providers and services like [SAML](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md), [OpenID Connect](../../../deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md) to provide dynamic [role mappings](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) for role based or attribute based access control.
    * Use {{kib}} Spaces and roles to [secure access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).
    * Authorize and authenticate service accounts for {{beats}} by [granting access using API keys](asciidocalypse://docs/beats/docs/reference/filebeat/beats-api-keys.md).
    * Roles can provide full, or read only, access to your data and can be created in Kibana or directly in Elasticsearch. Check [defining roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for full details.


* Block unwanted traffic with [traffic filter](../../../deploy-manage/security/traffic-filtering.md).
* Secure your settings with the Elasticsearch [keystore](../../../deploy-manage/security/secure-settings.md).

In addition, we also enable encryption at rest (EAR) by default. {{ech}} supports EAR for both the data stored in your clusters and the snapshots we take for backup, on all cloud platforms and across all regions.


## Should I use organization-level or deployment-level SSO? [ec_should_i_use_organization_level_or_deployment_level_sso] 

% added to `deploy-manage/users-roles/cloud-organization.md` by Shaina

