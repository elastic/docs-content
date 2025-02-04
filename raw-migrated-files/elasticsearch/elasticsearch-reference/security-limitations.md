---
navigation_title: "Limitations"
---

# Security limitations [security-limitations]



## Plugins [_plugins] 

{{es}}'s plugin infrastructure is extremely flexible in terms of what can be extended. While it opens up {{es}} to a wide variety of (often custom) additional functionality, when it comes to security, this high extensibility level comes at a cost. We have no control over the third-party plugins' code (open source or not) and therefore we cannot guarantee their compliance with {{stack-security-features}}. For this reason, third-party plugins are not officially supported on clusters with {{security-features}} enabled.


## Changes in wildcard behavior [_changes_in_wildcard_behavior] 

{{es}} clusters with the {{security-features}} enabled apply `_all` and other wildcards to data streams, indices, and aliases the current user has privileges for, not all data streams, indices, and aliases on the cluster.


## Multi document APIs [_multi_document_apis] 

Multi get and multi term vectors API throw IndexNotFoundException when trying to access non existing indices that the user is not authorized for. By doing that they leak information regarding the fact that the data stream or index doesn’t exist, while the user is not authorized to know anything about those data streams or indices.


## Filtered index aliases [_filtered_index_aliases] 

Aliases containing filters are not a secure way to restrict access to individual documents, due to the limitations described in [Index and field names can be leaked when using aliases](../../../deploy-manage/security.md#alias-limitations). The {{stack-security-features}} provide a secure way to restrict access to documents through the [document-level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) feature.


## Field and document level security limitations [field-document-limitations] 

When a user’s role enables document or [field level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for a data stream or index:

* The user cannot perform write operations:

    * The update API isn’t supported.
    * Update requests included in bulk requests aren’t supported.

* The user cannot perform operations that effectively make contents accessible under another name, including actions from the following APIs:

    * [Clone index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-clone-index.html)
    * [Shrink index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-shrink-index.html)
    * [Split index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-split-index.html)
    * [Aliases API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html)

* The request cache is disabled for search requests if either of the following are true:

    * The role query that defines document level security is [templated](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#templating-role-query) using a [stored script](../../../explore-analyze/scripting/modules-scripting-using.md#script-stored-scripts).
    * The target indices are a mix of local and remote indices.


When a user’s role enables [document level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for a data stream or index:

* Document level security doesn’t affect global index statistics that relevancy scoring uses. This means that scores are computed without taking the role query into account. Documents that don’t match the role query are never returned.
* The `has_child` and `has_parent` queries aren’t supported as query parameters in the role definition. The `has_child` and `has_parent` queries can be used in the search API with document level security enabled.
* [Date math](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math) expressions cannot contain `now` in [range queries with date fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html#ranges-on-dates)
* Any query that makes remote calls to fetch query data isn’t supported, including the following queries:

    * `terms` query with terms lookup
    * `geo_shape` query with indexed shapes
    * `percolate` query

* If suggesters are specified and document level security is enabled, the specified suggesters are ignored.
* A search request cannot be profiled if document level security is enabled.
* The [terms enum API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-terms-enum.html) does not return terms if document level security is enabled.
* The [`multi_match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html) query does not support specifying fields using wildcards.

::::{note} 
While document-level security prevents users from viewing restricted documents, it’s still possible to write search requests that return aggregate information about the entire index. A user whose access is restricted to specific documents in an index could still learn about field names and terms that only exist in inaccessible documents, and count how many inaccessible documents contain a given term.
::::



## Index and field names can be leaked when using aliases [alias-limitations] 

Calling certain {{es}} APIs on an alias can potentially leak information about indices that the user isn’t authorized to access. For example, when you get the mappings for an alias with the `_mapping` API, the response includes the index name and mappings for each index that the alias applies to.

Until this limitation is addressed, avoid index and field names that contain confidential or sensitive information.


## LDAP realm [_ldap_realm] 

The [LDAP Realm](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md) does not currently support the discovery of nested LDAP Groups. For example, if a user is a member of `group_1` and `group_1` is a member of `group_2`, only `group_1` will be discovered. However, the [Active Directory Realm](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md) **does** support transitive group membership.


## Resource sharing check for users and API keys [can-access-resources-check] 

The result of [async search](https://www.elastic.co/guide/en/elasticsearch/reference/current/async-search.html) and [scroll](https://www.elastic.co/guide/en/elasticsearch/reference/current/scroll-api.html) requests can be retrieved later by the same user or API key that submitted the initial request. The verification process involves comparing the username, authentication realm type, and (for realms other than file or native) realm name. If you used an API key to submit the request, only that key can retrieve the results. This logic also has a few limitations:

* Two different realms can have the same name on different nodes. This is not a recommended way to configure realms, therefore the resource sharing check does not attempt to detect this inconsistency.
* Realms can be renamed. This can cause inconsistency for the resource sharing check when you submit an async search or scroll then rename the realm and try to retrieve the results. Hence, changing realm names should be handled with care since it can cause complications for more than just the resource sharing check.
* The username is dynamically computed for realms backed by certain external authentication providers. For example, the username can be derived from part of the DN in an LDAP realm. It is in theory possible that two distinct users from the external system get mapped to the same username. Our recommendation is to avoid this situation in the first place. Hence, the resource sharing check does not account for this potential discrepancy.

