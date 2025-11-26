Field and document security is subject to the following limitations:

### Document level security limitations

When a user's role enables [document level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for a data stream or index:

* Document level security doesn’t affect global index statistics that relevancy scoring uses. This means that scores are computed without taking the role query into account. Documents that don’t match the role query are never returned.
* The `has_child` and `has_parent` queries aren’t supported as query parameters in the role definition. The `has_child` and `has_parent` queries can be used in the search API with document level security enabled.
* [Date math](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math) expressions cannot contain `now` in [range queries with date fields](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md#ranges-on-dates).
* Any query that makes remote calls to fetch query data isn’t supported, including the following queries:

    * `terms` query with terms lookup
    * `geo_shape` query with indexed shapes
    * `percolate` query

* If suggesters are specified and document level security is enabled, the specified suggesters are ignored.
* A search request cannot be profiled if document level security is enabled.
* The [terms enum API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-terms-enum) does not return terms if document level security is enabled.
* The [`multi_match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-multi-match-query.md) query does not support specifying fields using wildcards.

:::{note}
While document-level security prevents users from viewing restricted documents, it’s still possible to write search requests that return aggregate information about the entire index. A user whose access is restricted to specific documents in an index could still learn about field names and terms that only exist in inaccessible documents, and count how many inaccessible documents contain a given term.
:::

### Field level security limitations

When a user's role enables document or [field level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for a data stream or index:

* The user cannot perform write operations:

    * The update API isn’t supported.
    * Update requests included in bulk requests aren’t supported.

* The user cannot perform operations that effectively make contents accessible under another name, including actions from the following APIs:

    * [Clone index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clone)
    * [Shrink index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink)
    * [Split index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-split)
    * [Aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases)

* The request cache is disabled for search requests if either of the following are true:

    * The role query that defines document level security is [templated](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#templating-role-query) using a [stored script](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md).
    * The target indices are a mix of local and remote indices.
