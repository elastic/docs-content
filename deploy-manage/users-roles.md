---
navigation_title: Users and roles
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/project-settings-access.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
  serverless: all
products:
  - id: cloud-serverless
---

# Users and roles

To prevent unauthorized access to your Elastic resources, you need a way to identify users and validate that a user is who they claim to be (*authentication*), and control what data users can access and what tasks they can perform (*authorization*).

The methods that you use to authenticate users and control access depends on the way Elastic is deployed. 

::::{note}
Preventing unauthorized access is only one element of a complete security strategy. To secure your Elastic environment, you can also do the following:
 
* Restrict the nodes and clients that can connect to the cluster using [network security](/deploy-manage/security/network-security.md) policies. 
* Take steps to maintain your data integrity and confidentiality by [encrypting HTTP and inter-node communications](/deploy-manage/security/secure-cluster-communications.md), as well as [encrypting your data at rest](/deploy-manage/security/data-security.md).
* Maintain an [audit trail](/deploy-manage/security/logging-configuration/security-event-audit-logging.md) for security-related events.
* Control access to dashboards and other saved objects in your UI using [{{kib}} spaces](/deploy-manage/manage-spaces.md). 
* Connect your cluster to a [remote cluster](/deploy-manage/remote-clusters.md) to enable cross-cluster replication and search.
* Manage [API keys](/deploy-manage/api-keys.md) used for programmatic access to Elastic.
::::

## Cloud organization level

```{applies_to}
deployment:
  ess: all
serverless: all
```

If you’re using {{ecloud}}, then you can perform the following tasks to control access to your Cloud organization, your Cloud Hosted deployments, and your Cloud Serverless projects:

* [Invite users to join your organization](/deploy-manage/users-roles/cloud-organization/manage-users.md)
* Assign [user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md): 
  * Manage organization-level roles and high-level access to deployments and projects. 
  * Assign project-level roles and [create custom roles](/deploy-manage/users-roles/serverless-custom-roles.md). ({{serverless-short}} only)
* Configure [SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) for your organization

::::{tip}
For {{ech}} deployments, you can configure SSO at the organization level, the deployment level, or both. Refer to [Cloud organization users](/deploy-manage/users-roles/cloud-organization.md#organization-deployment-sso) for more information.
::::

{{ech}} deployments can also use [cluster-level authentication and authorization](/deploy-manage/users-roles/cluster-or-deployment-auth.md). Cluster-level auth features are not available for {{serverless-full}}.

## Orchestrator level

```{applies_to}
deployment:
  ece: all
```

Control access to your {{ece}} [orchestrator](/deploy-manage/deploy/cloud-enterprise/deploy-an-orchestrator.md) and deployments. 

* [Manage passwords for default users](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-system-passwords.md)
* [Manage orchestrator users and roles](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md):
  * [Using native users](/deploy-manage/users-roles/cloud-enterprise-orchestrator/native-user-authentication.md)
  * By integrating with external authentication providers:
    * [Active Directory](/deploy-manage/users-roles/cloud-enterprise-orchestrator/active-directory.md)
    * [LDAP](/deploy-manage/users-roles/cloud-enterprise-orchestrator/ldap.md)
    * [SAML](/deploy-manage/users-roles/cloud-enterprise-orchestrator/saml.md)
* [Configure single sign-on to deployments](/deploy-manage/users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.md) for orchestrator users

  ::::{tip}
  For {{ece}} deployments, you can configure SSO at the orchestrator level, the deployment level, or both.
  ::::

{{ece}} deployments can also use [cluster-level authentication and authorization](/deploy-manage/users-roles/cluster-or-deployment-auth.md).

:::{note}
You can't manage users and roles for {{eck}} clusters at the orchestrator level. {{eck}} deployments use cluster-level authentication and authorization only.
:::

## Project level

```{applies_to}
serverless: all
```

As an extension of the [predefined cloud resource access roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_instance_access_roles) offered for {{serverless-short}} projects, you can create custom roles at the project level to provide more granular control, and provide users with only the access they need within specific projects.

[Learn more about custom roles for {{serverless-full}} projects](/deploy-manage/users-roles/serverless-custom-roles.md).

## Cluster or deployment level

```{applies_to}
deployment:
  ece: all
  ess: all
  eck: all
  self: all
```

Set up authentication and authorization at the cluster or deployment level, and learn about the underlying security technologies that {{es}} uses to authenticate and authorize requests internally and across services.

### User authentication

Set up methods to identify users to the {{es}} cluster.

Key tasks for managing user authentication include:

* [Managing default users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md)
* [Managing users natively](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md)
* [Integrating with external authentication providers](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md)

You can also learn the basics of {{es}} authentication, learn about accounts used to communicate within an {{es}} cluster and across services, and perform advanced tasks.

[View all user authentication docs](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md)

### User authorization

After a user is authenticated, use role-based access control to determine whether the user behind an incoming request is allowed to execute the request.

Key tasks for managing user authorization include: 

* Assigning [built-in roles](elasticsearch://reference/elasticsearch/roles.md) or [defining your own](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* [Mapping users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md)
* [Setting up field- and document-level security](/deploy-manage/users-roles/controlling-access-at-document-field-level.md)

You can also learn the basics of {{es}} authorization, and perform advanced tasks.

::::{tip}
User roles are also used to control access to [{{kib}} spaces](/deploy-manage/manage-spaces.md).
:::: 

[View all user authorization docs](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md)
