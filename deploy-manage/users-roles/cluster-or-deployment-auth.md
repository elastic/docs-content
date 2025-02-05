---
navigation_title: "Cluster or deployment"
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters.html
  - https://www.elastic.co/guide/en/cloud/current/ec-security.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# Cluster or deployment users

To prevent unauthorized access to your Elastic resources, you need a way to identify users and validate that a user is who they claim to be (*authentication*), and control what data users can access and what tasks they can perform (*authorization*).

In this section, you’ll learn how to set up authentication and authorization at the cluster or deployment level, and learn about the underlying security technologies that Elasticsearch uses to authenticate and authorize requests internally and across services.

This section only covers direct access to and communications with an Elasticsearch cluster - sometimes known as a deployment. To learn about managing access to your {{ecloud}} organization or {{ece}} orchestrator, or to learn how to use single sign-on to access a cluster using your {{ecloud}} credentials, refer to [Manage users and roles](/deploy-manage/users-roles.md).

## Quickstart

If you plan to use native Elasticsearch user and role management, then [follow our quickstart](/deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md) to learn how to set up basic authentication and authorization features.

## Authentication

Review the following topics to learn about authentication in your Elasticsearch cluster:

### Set up user authentication

* Learn about the available [realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md) that you can use to authenticate users
* Manage passwords for [default users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.html)
* Manage users [natively](/deploy-manage/users-roles/cluster-or-deployment-auth/native.html)
* Integrate with external authentication providers using [external realms](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md):
  * [Active Directory](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.html)
  * [JWT](/deploy-manage/users-roles/cluster-or-deployment-auth/jwt.html)
  * [Kerberos](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.html)
  * [LDAP](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.html)
  * [OpenID Connect](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.html)
  * [SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.html)
  * [PKI](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.html)
  * [Implement a custom realm](/deploy-manage/users-roles/cluster-or-deployment-auth/custom.html)
* Configure [file-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.html)
* Enable [anonymous access](/deploy-manage/users-roles/cluster-or-deployment-auth/anonymous-access.html)
* Manage [user profiles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-profiles.html)
* Manage authentication for [multiple clusters](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-authentication-for-multiple-clusters.html) ({{eck}} only)
* Set up a [user access agreement](/deploy-manage/users-roles/cluster-or-deployment-auth/access-agreement.html)

### Advanced topics

* Learn about [internal users](/deploy-manage/users-roles/cluster-or-deployment-auth/internal-users.html), which are responsible for the operations that take place inside an Elasticsearch cluster.
* Learn about [service accounts](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.html), which are used for integration with external services that connect to Elasticsearch
* Learn about the [services used for token-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/token-based-authentication-services.html)
* Learn about the [services used by orchestrators](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.html) (applies to {{ece}}, {{ecloud}} Hosted, and {{eck}})
* Learn about [user lookup technologies](/deploy-manage/users-roles/cluster-or-deployment-auth/looking-up-users-without-authentication.html)
* [Manage the user cache](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-user-cache.html)

## Authorization

After a user is authenticated, use role-based access control to determine whether the user behind an incoming request is allowed to execute the request. The primary method of authorization in a cluster is role-based access control (RBAC). Review the following topics to learn about authorization in your Elasticsearch cluster.

### Set up user authorization

* [Define roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.html)
* Learn about [built-in roles](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.html)
* Learn about the [Elasticsearch](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.html) and [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.html) privileges you can assign to roles
* [Map users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.html)
* Learn how to [control access at the document and field level](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.html)

### Advanced topics

* Learn how to [delegate authorization to another realm](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-delegation.html)
* Learn how to [build a custom authorization plugin](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-plugins.html) for unsupported systems or advanced applications
* Learn how to [submit requests on behalf of other users](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.html)
* Learn about [attribute-based access control](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.html#attributes)

::::{tip}
User roles are also used to control access to [spaces](/deploy-manage/manage-spaces.md). 
::::