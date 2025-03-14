---
navigation_title: "{{ecloud}}"
applies_to:
  deployment:
    ess: ga
  serverless: ga
---

# Secure your {{ecloud}} organization [ec-securing-considerations]

This section covers security settings for your {{ecloud}} organization, the platform for managing {{ech}} deployments and serverless projects.

**Managed by Elastic**

As a managed service, Elastic automatically handles a [number of security features](https://www.elastic.co/cloud/security#details) with no configuration required:

- **TLS encrypted communication** is provided in the default configuration. {{es}} nodes communicate using TLS.
- **Encryption at rest**. By default, all of your {{ecloud}} resources are encrypted at rest. Note that you can choose to encrypt your {{ech}} deployments [using your own encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).
- **Cluster isolation**. {{es}} nodes run in isolated containers, configured according to the principle of least privilege, and with restrictions on system calls and allowed root operations.

**Additional organization-level security settings**

To reinforce the security of your organization, consider implementing the following measures:

- [**Organization-level SSO**](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md). Note that for {{ech}} deployments, you can also configure SSO at the [deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md).
- [**Cloud role-based access control**](/deploy-manage/users-roles/cloud-organization/manage-users.md): Define the roles of users who have access to your organization and its resources. Note that for {{ech}} deployments, you can also [manage non-cloud users and roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
- [**Cloud API keys**](/deploy-manage/api-keys/elastic-cloud-api-keys.md): Manage API keys used for programmatic access to [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud/) and [{{ecloud}} serverless](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless/) APIs.



**Additional deployment-level security settings**

While serverless projects are fully managed and secured by Elastic, additional security settings are available for you to configure individually for your {{ech}} deployments. Refer to [](secure-your-cluster-deployment.md) for more information.


In addition, multifactor authentication is mandatory for all {{ecloud}} users belonging to your organization. For more information on the available authentication methods, refer to [](/cloud-account/multifactor-authentication.md).

