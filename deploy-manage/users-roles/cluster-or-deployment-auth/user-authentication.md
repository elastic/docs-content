---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-up-authentication.html
  - https://www.elastic.co/guide/en/kibana/current/kibana-authentication.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# User authentication

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/347

% Scope notes: reference ECE SSO, cloud SSO

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/setting-up-authentication.md
% - [ ] ./raw-migrated-files/kibana/kibana/kibana-authentication.md
%      Notes: this is a good overview

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$pki-authentication$$$

$$$anonymous-authentication$$$

$$$basic-authentication$$$

$$$embedded-content-authentication$$$

$$$http-authentication$$$

$$$kerberos$$$

$$$multiple-authentication-providers$$$

$$$oidc$$$

$$$saml$$$

$$$token-authentication$$$



Review the following topics to learn about authentication in your Elasticsearch cluster:

### Set up user authentication

* Learn about the available [realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md) that you can use to authenticate users
* Manage passwords for [built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md)
* Manage users [natively](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md)
* Integrate with external authentication providers using [external realms](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md):
  * [Active Directory](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md)
  * [JWT](/deploy-manage/users-roles/cluster-or-deployment-auth/jwt.md)
  * [Kerberos](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md)
  * [LDAP](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md)
  * [OpenID Connect](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md)
  * [SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md)
  * [PKI](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md)
  * [Implement a custom realm](/deploy-manage/users-roles/cluster-or-deployment-auth/custom.md)
* Configure [file-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md)
* Enable [anonymous access](/deploy-manage/users-roles/cluster-or-deployment-auth/anonymous-access.md)
* Set up a [user access agreement](/deploy-manage/users-roles/cluster-or-deployment-auth/access-agreement.md)

### Advanced topics

* Learn about [internal users](/deploy-manage/users-roles/cluster-or-deployment-auth/internal-users.md), which are responsible for the operations that take place inside an Elasticsearch cluster.
* Learn about [service accounts](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md), which are used for integration with external services that connect to Elasticsearch
* Learn about the [services used for token-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/token-based-authentication-services.md)
* Learn about the [services used by orchestrators](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.md) (applies to {{ece}}, {{ech}}, and {{eck}})
* Manage [user profiles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-profiles.md)
* Learn about [user lookup technologies](/deploy-manage/users-roles/cluster-or-deployment-auth/looking-up-users-without-authentication.md)
* [Manage the user cache](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-user-cache.md)
* Manage authentication for [multiple clusters](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-authentication-for-multiple-clusters.md) using {{stack}} configuration policies ({{eck}} only)
