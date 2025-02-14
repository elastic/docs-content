---
navigation_title: "Cloud organization"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-organizations.html
applies:
  serverless: all
  hosted: all
---

# Cloud organization users [ec-organizations]

When you sign up to {{ecloud}}, you create an organization. This organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier.

You can perform the following tasks to control access to your Cloud organization, your Cloud Hosted deployments, and your Cloud Serverless projects:

* [Invite users to join your organization](/deploy-manage/users-roles/cloud-organization/manage-users.md)
* Assign [user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md): 
  * Manage organization-level roles and high-level access to deployments and projects. 
  * Assign project-level roles and create custom roles. ({{serverless-short}} only)
* Configure [SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) for your organization


## Should I use organization-level or deployment-level SSO? [organization-deployment-sso] 

:::{applies}
:hosted: all
:::

For {{ecloud}} Hosted deployments, you can configure SSO at the [organization level](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md), the [deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md), or both. 

The option that you choose depends on your requirements:

| Consideration | Organization-level | Deployment-level |
| --- | --- | --- |
| **Management experience** | Manage authentication and role mapping centrally for all deployments in the organization | Configure SSO for each deployment individually |
| **Authentication protocols** | SAML only | Multiple protocols, including LDAP, OIDC, and SAML |
| **Role mapping** | [Organization-level roles and instance access roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md), Serverless project [custom roles](https://docs.elastic.co/serverless/custom-roles.md) | [Built-in](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) and [custom](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) stack-level roles |
| **User experience** | Users interact with Cloud | Users interact with the deployment directly |

If you want to avoid exposing users to the {{ecloud}} UI, or have users who only interact with some deployments, then you might prefer users to interact with your deployment directly.

In some circumstances, you might want to use both organization-level and deployment-level SSO. For example, if you have a data analyst who interacts only with data in specific deployments, then you might want to configure deployment-level SSO for them. If you manage multiple tenants in a single organization, then you might want to configure organization-level SSO to administer deployments, and deployment-level SSO for the users who are using each deployment.
