---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-domain.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Security domains [security-domain]

Security domains are a method of grouping multiple [realms](authentication-realms.md) under the same domain so that the {{stack}} can recognize when a single user authenticates with these realms. Users can authenticate with any of the realms in the domain group, and have access to the same set of resources regardless of which realm they authenticated with.

For example, a single [user profile](user-profiles.md) is associated with a user, enabling preferences, notifications, and other user data to be shared across realms. The user can view results from an asynchronous search request or a scrolling search across realms. If the user has the necessary privileges, they can also view and manage API keys across realms.

## Resource sharing across domains [security-domain-resource-sharing]

Some types of resources in {{es}} are owned by a single user, such as [async search contexts](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit), [API keys](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), and [user profiles](user-profiles.md). When a user creates a resource, {{es}} captures the user’s username and realm information as part of the resource’s metadata. Likewise, if a user updates a resource, such as an API key, {{es}} automatically re-captures the user’s current realm information.

When a user later attempts to access the resource, {{es}} compares the captured username and realm information against those from the accessing user. {{es}} will deny access unless both the realm and username match. If {{es}} detects that a username from two different realms is attempting to access a resource, {{es}} assumes that these users are distinct and doesn’t allow resources to be shared between those users.

However, there are cases where the same user can authenticate with multiple realms and needs to share the same set of resources across realms. For example, an [LDAP realm](ldap.md) and a [SAML realm](saml.md) can be backed by the same directory service. Additionally, [authorization delegation](authorization-delegation.md) allows one realm to delegate authorization to another realm. If both realms authenticate users with the same username, it’s reasonable to treat these users as the same user from a resource ownership perspective.

Security domains make resource sharing across realms possible by grouping those realms under the same domain. {{es}} always enforces the privileges that are associated with the currently authenticated user, which remains true with security domains. Security domains don’t bypass [user authorization](user-roles.md) when resource sharing requires them. For example, a user requires the `manage_own_api_key` privilege to manage their own API keys. If that user doesn’t have this privilege when authenticating with one realm, they won’t be able to manage API keys while authenticating with another realm.

### Managing roles across realms [security-domain-realm-roles]

{{es}} provides multiple ways to consistently apply roles across realms. For example, you can use [authorization delegation](authorization-delegation.md) to ensure that a user is assigned the same roles from multiple realms. You can also manually configure multiple realms that are backed by the same directory service. Though it’s possible to configure different [roles](user-roles.md#roles) for the same user when authenticating with different realms, it is not recommended.



## Configure a security domain [security-domain-configure]

::::{important}
:name: security-domain-warning

Security domains are an advanced feature that requires careful configuration. Misconfiguration or misuse can lead to unexpected behaviors.

::::


Security domains must be configured consistently across all nodes in cluster. Inconsistent configuration can lead to issues such as:

* Duplicated user profiles
* Different ownership of resources depending on the authenticating node’s configuration

To configure a security domain:

1. Add a security domain configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) in the `xpack.security.authc.domains` namespace:

    ```yaml
    xpack:
      security:
        authc:
          domains:
            my_domain:
              realms: [ 'default_native', 'saml1' ] <1>
    ```

    1. This configuration defines a security domain called `my_domain`, which contains two realms named `default_native` and `saml1`.


    The specified realms must be defined in `elasticsearch.yml`, but do not need to be enabled.

    ::::{note}
    The [file realm](file-based.md) and [native realm](native.md) are automatically enabled as `default_file` and `default_native`, respectively, without any explicit configuration. You can list these realms under domains even when they are not explicitly defined in `elasticsearch.yml`.
    ::::

2. Restart {{es}}.

    ::::{important}
    {{es}} can fail to start if the domain configuration is invalid. Invalid configurations include:

    * The same realm is configured under multiple domains.
    * Any undefined realm, synthetic realm, or the reserved realm is configured to be under a domain.

    ::::

3. Apply the same configuration across all nodes in the cluster before performing operations related to security domains, including creating and managing resources such as [user profiles](user-profiles.md), [API keys](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), and [async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit).

    When adding realms to a security domain, avoid authenticating with a newly-added realm until changes are fully applied to all nodes.



## Removing realms from a security domain [security-domain-remove-realm]

Removing realms from a security domain can lead to unexpected behaviors and is not recommended. Resources created or updated before the removal can be owned by different users depending on the resource type:

* [User profiles](user-profiles.md) are owned by the user for whom the profile was last [activated](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-activate-user-profile). For users whose realms are no longer in the same domain as the owner user, a new user profile will be created for them next time the activate user profile API is called.
* An API key is owned by the user who originally [created](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) or last [updated](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-api-key) it. Users, including the original creator of the API key, will lose ownership if their realms are no longer in the same domain as those of the current API key owner.
* Resources such as async search contexts are owned by the user who originally created them.

Instead of removing realms, consider disabling them and keeping them as part of the security domain. Under all circumstances, resource sharing across realms is only possible between users with the same username.


