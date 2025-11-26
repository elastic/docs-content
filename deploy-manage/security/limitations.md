---
navigation_title: Limitations
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-limitations.html
applies_to:
  deployment:
    self: all
    eck: all
    ess: all
    ece: all
products:
  - id: elasticsearch
---

# Security limitations [security-limitations]

Review the following {{es}} security limitations. Depending on your organization's security requirements, you might want to restrict, adjust, or find workaround or alternatives for some of these features and resources.

## Plugins [_plugins]

{{es}}'s plugin infrastructure is extremely flexible in terms of what can be extended. While it opens up {{es}} to a wide variety of (often custom) additional functionality, when it comes to security, this high extensibility level comes at a cost. We have no control over the third-party plugins' code (open source or not) and therefore we cannot guarantee their compliance with {{stack-security-features}}. For this reason, third-party plugins are not officially supported on clusters with {{security-features}} enabled.


## Changes in wildcard behavior [_changes_in_wildcard_behavior]

{{es}} clusters with the {{security-features}} enabled apply `_all` and other wildcards to data streams, indices, and aliases the current user has privileges for, not all data streams, indices, and aliases on the cluster.


## Multi document APIs [_multi_document_apis]

Multi get and multi term vectors API throw `IndexNotFoundException` when trying to access non existing indices that the user is not authorized for. By doing that they leak information regarding the fact that the data stream or index doesn’t exist, while the user is not authorized to know anything about those data streams or indices.


## Filtered index aliases [_filtered_index_aliases]

Aliases containing filters are not a secure way to restrict access to individual documents, due to the limitations described in [Index and field names can be leaked when using aliases](#alias-limitations). The {{stack-security-features}} provide a secure way to restrict access to documents through the [document-level security](/deploy-manage/users-roles/controlling-access-at-document-field-level.md) feature.


## Field and document level security limitations [field-document-limitations]

::::{include} /deploy-manage/_snippets/field-doc-sec-limitations.md
::::

## Index and field names can be leaked when using aliases [alias-limitations]

Calling certain {{es}} APIs on an alias can potentially leak information about indices that the user isn’t authorized to access. For example, when you get the mappings for an alias with the `_mapping` API, the response includes the index name and mappings for each index that the alias applies to.

Until this limitation is addressed, avoid index and field names that contain confidential or sensitive information.


## LDAP realm [_ldap_realm]

The [LDAP Realm](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md) does not currently support the discovery of nested LDAP Groups. For example, if a user is a member of `group_1` and `group_1` is a member of `group_2`, only `group_1` will be discovered. However, the [Active Directory Realm](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md) **does** support transitive group membership.


## Resource sharing check for users and API keys [can-access-resources-check]

The result of [async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) and [scroll](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-scroll) requests can be retrieved later by the same user or API key that submitted the initial request. The verification process involves comparing the username, authentication realm type, and (for realms other than file or native) realm name. If you used an API key to submit the request, only that key can retrieve the results. This logic also has a few limitations:

* Two different realms can have the same name on different nodes. This is not a recommended way to configure realms, therefore the resource sharing check does not attempt to detect this inconsistency.
* Realms can be renamed. This can cause inconsistency for the resource sharing check when you submit an async search or scroll then rename the realm and try to retrieve the results. Hence, changing realm names should be handled with care since it can cause complications for more than just the resource sharing check.
* The username is dynamically computed for realms backed by certain external authentication providers. For example, the username can be derived from part of the DN in an LDAP realm. It is in theory possible that two distinct users from the external system get mapped to the same username. Our recommendation is to avoid this situation in the first place. Hence, the resource sharing check does not account for this potential discrepancy.