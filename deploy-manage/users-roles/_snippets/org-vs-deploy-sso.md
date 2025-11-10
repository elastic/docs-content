For {{ech}} deployments, you can configure SSO at the [organization level](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md), the [deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md), or both.

The option that you choose depends on your requirements:

| Consideration | Organization-level | Deployment-level |
| --- | --- | --- |
| **Management experience** | Manage authentication and role mapping centrally for all deployments in the organization | Configure SSO for each deployment individually |
| **Authentication protocols** | SAML only | Multiple protocols, including LDAP, OIDC, and SAML |
| **Role mapping** | [Organization-level roles and cloud resource access roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md), Serverless project [custom roles](/deploy-manage/users-roles/serverless-custom-roles.md) | [Built-in](elasticsearch://reference/elasticsearch/roles.md) and [custom](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) stack-level roles |
| **User experience** | Users interact with Cloud | Users interact with the deployment directly |

If you want to avoid exposing users to the {{ecloud}} Console, or have users who only interact with some deployments, then you might prefer users to interact with your deployment directly.

In some circumstances, you might want to use both organization-level and deployment-level SSO. For example, if you have a data analyst who interacts only with data in specific deployments, then you might want to configure deployment-level SSO for them. If you manage multiple tenants in a single organization, then you might want to configure organization-level SSO to administer deployments, and deployment-level SSO for the users who are using each deployment.