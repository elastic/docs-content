---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-up-authentication.html
  - https://www.elastic.co/guide/en/kibana/current/kibana-authentication.html
applies_to:
  stack: all
products:
  - id: elasticsearch
  - id: kibana
---

# User authentication

Authentication identifies an individual. To gain access to restricted resources, a user must prove their identity, using passwords, credentials, or some other means (typically referred to as authentication tokens).

The {{stack}} authenticates users by identifying the users behind the requests that hit the cluster and verifying that they are who they claim to be. The authentication process is handled by one or more authentication services called [*realms*](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md).

You can manage and authenticate users natively, or integrate with external user management systems such as LDAP and Active Directory. If none of the built-in realms meet your needs, you can also build your own custom realm and plug it into the {{stack}}.

When {{security-features}} are enabled, depending on the realms you’ve configured, you must attach your user credentials to requests sent to {{es}}. For example, when using realms that support usernames and passwords, you can attach a [basic auth](https://en.wikipedia.org/wiki/Basic_access_authentication) header to the requests.

The {{security-features}} provide two services: the token service and the API key service. You can use these services to exchange the current authentication for a token or key. This token or key can then be used as credentials for authenticating new requests. The API key service is enabled by default. The token service is enabled by default when TLS/SSL is enabled for HTTP.

Review the following topics to learn about authentication in your {{es}} cluster.

:::{tip}
If you use {{ece}} or {{ech}}, then you can also manage authentication at the level of your [{{ece}} orchestrator](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md) or [{{ecloud}} organization](/deploy-manage/users-roles/cloud-organization.md).

If you use {{serverless-full}}, then you can only manage authentication at the [{{ecloud}} organization level](/deploy-manage/users-roles/cloud-organization.md).
:::

### Set up user authentication

* Set up an authentication method:
  * Learn about the available [realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md) that you can use to authenticate users.
  * Manage passwords for [default users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
  * Manage users using [internal realms](/deploy-manage/users-roles/cluster-or-deployment-auth/internal-authentication.md):
    * Manage users [natively](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md)
    * Configure [file-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md)
  * Integrate with external authentication providers using [external realms](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md):
    * [Active Directory](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md)
    * [JWT](/deploy-manage/users-roles/cluster-or-deployment-auth/jwt.md)
    * [Kerberos](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md)
    * [LDAP](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md)
    * [OpenID Connect](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md)
    * [SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md)
    * [PKI](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md)
    * [Implement a custom realm](/deploy-manage/users-roles/cluster-or-deployment-auth/custom.md)
* Configure [authentication mechanisms for {{kib}}](kibana-authentication.md).
* Enable [anonymous access](/deploy-manage/users-roles/cluster-or-deployment-auth/anonymous-access.md).
* Set up a [user access agreement](/deploy-manage/users-roles/cluster-or-deployment-auth/access-agreement.md).

### Advanced topics

* Learn about [internal users](/deploy-manage/users-roles/cluster-or-deployment-auth/internal-users.md), which are responsible for the operations that take place inside an {{es}} cluster.
* Learn about [service accounts](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md), which are used for integration with external services that connect to {{es}}.
* Learn about the [services used for token-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/token-based-authentication-services.md).
* Learn about the [services used by orchestrators](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.md).
* Manage [user profiles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-profiles.md).
* Learn about [user lookup technologies](/deploy-manage/users-roles/cluster-or-deployment-auth/looking-up-users-without-authentication.md).
* [Manage the user cache](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-user-cache.md).
* Manage authentication for [multiple clusters](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-authentication-for-multiple-clusters.md) using {{stack}} configuration policies ({{eck}} only)
