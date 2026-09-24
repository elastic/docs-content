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

## Default authentication [default-cloud-authentication]

By default, {{ecloud}} provides SSO between your Cloud account and {{kib}}. When users log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and open {{kib}} from a deployment or project, they are authenticated automatically. The **Login with Cloud** option is also available on the {{kib}} login screen, so users can authenticate with their Cloud credentials even when accessing the {{kib}} endpoint directly.

No additional SSO configuration is required for this default behavior. The organization-level and deployment-level SSO options described below let you customize authentication further, for example by integrating with your own identity provider.

## Should I use organization-level or deployment-level SSO? [organization-deployment-sso] 

```{applies_to}
ess: ga
```

:::{include} _snippets/org-vs-deploy-sso.md
:::