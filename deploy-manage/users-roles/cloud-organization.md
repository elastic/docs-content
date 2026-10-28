---
navigation_title: Cloud organization
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-organizations.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
---

# Cloud organization users [ec-organizations]

When you sign up to {{ecloud}}, you create an organization. This organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier.

You can perform the following tasks to control access to your Cloud organization, your {{ech}} deployments, and your {{serverless-full}} projects:

* [Manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md): Invite users to join your organization and manage existing users.
* Assign [user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md): 
  * Manage organization-level roles and high-level access to deployments and projects. 
  * If you have {{serverless-full}} projects, assign project-level roles and create custom roles.
* Configure [SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) for your organization.

You can also control programmatic access to {{ecloud}}, your deployments, and your projects using [API keys](/deploy-manage/api-keys.md).

:::{tip}
If you're using {{ech}}, then you can also manage users and control access [at the deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md).
:::

## Access to deployments and projects [default-cloud-authentication]

Organization members can open {{kib}} in their {{ech}} deployments and {{serverless-full}} projects directly from the {{ecloud}} Console, or use the **Login with Cloud** option on the {{kib}} login screen. No additional authentication setup is required.

Users must be granted a [cloud resource access role](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_instance_access_roles) for the deployment or project. For {{serverless-short}} projects, the [access level](/deploy-manage/users-roles/cloud-organization/user-roles.md#access) must also include {{kib}} and {{es}}. Access to the {{ecloud}} Console alone does not grant access to the project itself.

To configure additional authentication methods at the deployment level, such as SAML, OIDC, or LDAP, refer to [deployment-level authentication](/deploy-manage/users-roles/cluster-or-deployment-auth.md).

## Should I use organization-level or deployment-level SSO? [organization-deployment-sso] 

```{applies_to}
ess: ga
```

:::{include} _snippets/org-vs-deploy-sso.md
:::