# Securing your deployment [ec-security]

The security of Elasticsearch Service is described on the [{{ecloud}} security](https://www.elastic.co/cloud/security) page. In addition to the security provided by {{ecloud}}, you can take the following steps to secure your deployments:

* Prevent unauthorized access with password protection and role-based access control:

    * Reset the [`elastic` user password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Use third-party authentication providers and services like [SAML](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md), [OpenID Connect](../../../deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md) to provide dynamic [role mappings](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) for role based or attribute based access control.
    * Use {{kib}} Spaces and roles to [secure access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).
    * Authorize and authenticate service accounts for {{beats}} by [granting access using API keys](https://www.elastic.co/guide/en/beats/filebeat/current/beats-api-keys.html).
    * Roles can provide full, or read only, access to your data and can be created in Kibana or directly in Elasticsearch. Check [defining roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for full details.


* Block unwanted traffic with [traffic filter](../../../deploy-manage/security/traffic-filtering.md).
* Secure your settings with the Elasticsearch [keystore](../../../deploy-manage/security/secure-settings.md).

In addition, we also enable encryption at rest (EAR) by default. Elasticsearch Service supports EAR for both the data stored in your clusters and the snapshots we take for backup, on all cloud platforms and across all regions.


## Should I use organization-level or deployment-level SSO? [ec_should_i_use_organization_level_or_deployment_level_sso] 

You can also integrate SAML SSO [at the organization level](../../../deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md). The option that you choose depends on your requirements:

| Consideration | Organization-level | Deployment-level |
| --- | --- | --- |
| **Management experience** | Manage authentication and role mapping centrally for all deployments in the organization | Configure SSO for each deployment individually |
| **Authentication protocols** | SAML only | Multiple protocols, including LDAP, OIDC, and SAML |
| **Role mapping** | [Organization-level roles and instance access roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md), Serverless project [custom roles](https://docs.elastic.co/serverless/custom-roles.html) | [Built-in](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) and [custom](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) stack-level roles |
| **User experience** | Users interact with Cloud | Users interact with the deployment directly |

If you want to avoid exposing users to the {{ecloud}} UI, or have users who only interact with some deployments, then you might prefer users to interact with your deployment directly.

In some circumstances, you might want to use both organization-level and deployment-level SSO. For example, if you have a data analyst who interacts only with data in specific deployments, then you might want to configure deployment-level SSO for them. If you manage multiple tenants in a single organization, then you might want to configure organization-level SSO to administer deployments, and deployment-level SSO for the users who are using each deployment.

