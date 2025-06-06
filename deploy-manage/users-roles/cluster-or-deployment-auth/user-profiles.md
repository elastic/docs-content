---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/user-profile.html
applies_to:
  deployment:
    ess:
    ece:
    eck:
products:
  - id: elasticsearch
---

# User profiles [user-profile]

::::{admonition} Indirect use only
The user profile feature is designed only for use by {{kib}} and Elastic’s {{observability}}, and {{elastic-sec}} solutions. Individual users and external applications should not call this API directly. Elastic reserves the right to change or remove this feature in future releases without prior notice.
::::


Because the {{stack}} supports externally-managed users (such as users who authenticate via SAML, or users stored in an LDAP directory), there’s a distinction between *users* and their *profile*.

*Users* refer to the entities that authenticate requests to the {{stack}}. Each user has a username and a set of privileges (represented by [roles](user-roles.md#roles)) that determine which types of requests they can issue. Users can be ephemeral; they might exist only for the duration of a request to an {{es}} API or for the lifetime of a session in {{kib}}. These users cannot be retrieved after the session ends, and can’t store preferences across sessions.

*User profiles* provide persistent and stable representations of users. A user profile exists even if the user is offline, so their profile persists across sessions. The unique identifier assigned to each profile doesn’t change throughout the lifetime of a deployment, providing a stable way of referring to the associated user. Each profile has a unique identifier, is searchable, and can store user data such as format and notification preferences.

The capability of uniquely referring to users regardless of whether they’re actively online is a critical function that underpins important features like personalization and collaboration in {{kib}}.

## User profiles in {{kib}} [_user_profiles_in_kib]

A user profile is the persistent record that the {{stack}} stores for each interactive user that authenticates to {{kib}}.

When a user logs in to {{kib}}, a profile is automatically created for the user, or an existing profile is updated to reflect the user’s active session. By using the unique ID of the user profile, {{kib}} can store user-level data such as preferences separately for each user, which is key to fine-grained levels of customization. {{kib}} uses this unique ID to route messages and notifications to a distinct user, regardless of whether they’re logged in.

### Usernames and user profiles [_usernames_and_user_profiles]

You can use the same username across multiple realms for a single user. In {{es}}, it’s possible for two different realms to authenticate users with the same username and different roles. {{es}} doesn’t assume that these users are the same person, and treats them as separate individuals with distinct user profiles by default.

::::{note} 
For use cases where one individual can authenticate against multiple realms, you can use the [security domain](security-domains.md) feature so that these distinct users are considered to be the same identity and share a single user profile.
::::




## Create and manage user profiles [_create_and_manage_user_profiles]

To create a new user profile or update an existing one, use the [activate user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-activate-user-profile). When you submit a request, {{es}} attempts to locate an existing profile document for the specified user. If one doesn’t exist, {{es}} creates a new profile document.

In either case, the profile document captures the user’s `full_name`, `email`, `roles`, and `realms`, and also includes the profile unique ID and timestamp of the operation. You can retrieve a user profile with the [get user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-user-profile) by including the profile’s unique ID (`uid`).

In addition to the user’s basic information, you can add data to a profile document with the [update user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-update-user-profile-data). For example, you can add user-specific preferences as part of the profile data.

Use the [suggest user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-suggest-user-profiles) to retrieve profiles that match given criteria. This API is designed to support user-suggestions, in collaboration with features such as those found in {{kib}}. However, the suggest user profile API is not intended to provide a general-purpose search API.

Lastly, you can use the [has privileges API for user profiles](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-has-privileges-user-profile) to check the privileges of multiple users by specifying their profiles' unique IDs. This can be used in conjunction with the suggest user profile API in order to restrict the suggestions only to users that have the necessary permissions to actually perform the action in the context.


## Limitations [_limitations_10]

* Creating a new user profile requires a user’s authentication details (`username` and `password` or its [OAuth2 access token](token-based-authentication-services.md)). This means that a user must authenticate at least one time to create a user profile. Users who have never authenticated to {{kib}} (or another profile-aware application) won’t have a user profile, and the [suggest user profile API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-suggest-user-profiles) won’t return any results for those users.
* User profiles are meant for interactive users, such as a human user who interacts with {{kib}}. Therefore, user profiles don’t support API keys or [service accounts](service-accounts.md).

    ::::{note} 
    [OAuth2 tokens](token-based-authentication-services.md) that represent an interactive end-user are supported.
    ::::



