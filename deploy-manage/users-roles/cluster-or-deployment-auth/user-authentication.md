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
