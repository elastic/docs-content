---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_advantages_of_using_this_endpoint_before_a_cross_cluster_search.html
applies_to:
  stack:
  serverless: unavailable
products:
  - id: elasticsearch
---

# Resolve a cluster before {{ccs}} [_advantages_of_using_this_endpoint_before_a_ccs]

You can use the [`_resolve/cluster`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-cluster) endpoint before cross-cluster search to identify clusters or indices to exclude from your search.

You may want to exclude a cluster or index from a search when:

1. A remote cluster is unavailable and configured with `skip_unavailable`=`false`. Executing a {{ccs}} under those conditions will cause [the entire search to fail](/explore-analyze/cross-cluster-search.md#cross-cluster-search-failures).
2. A cluster has no matching indices, aliases or data streams for the index expression, or your user does not have permissions to search them. For example, if your index expression is `logs*,remote1:logs*` and the `remote1` cluster has no matching indices, that cluster will return no results if included in a {{ccs}}.
3. The index expression, combined with any query parameters you specify, might trigger exceptions. In these cases, the "error" field in the `_resolve/cluster` response will be present. This is also where security/permission errors will be shown.
4. A remote cluster is running an older version that does not support features needed for your search.

## Examples [resolve-cluster-api-example]

```console
GET /_resolve/cluster/my-index*,clust*:my-index*
```

The API returns the following response:

```console-result
{
  "(local)": {          <1>
    "connected": true,
    "skip_unavailable": false,
    "matching_indices": true,
    "version": {
      "number": "8.13.0",
      "build_flavor": "default",
      "minimum_wire_compatibility_version": "7.17.0",
      "minimum_index_compatibility_version": "7.0.0"
    }
  },
  "cluster_one": {
    "connected": true,         <2>
    "skip_unavailable": true,  <3>
    "matching_indices": true,  <4>
    "version": {
      "number": "8.13.0",      <5>
      "build_flavor": "default",
      "minimum_wire_compatibility_version": "7.17.0",
      "minimum_index_compatibility_version": "7.0.0"
    }
  },
  "cluster_two": {
    "connected": true,
    "skip_unavailable": false,
    "matching_indices": true,
    "version": {
      "number": "8.13.0",
      "build_flavor": "default",
      "minimum_wire_compatibility_version": "7.17.0",
      "minimum_index_compatibility_version": "7.0.0"
    }
  }
}
```

1. Each cluster has its own response section. The cluster you sent the request to is labelled as "(local)".
2. The querying cluster attempts to make a request to each remote cluster. If successful, `connected`=`true`.
3. The `skip_unavailable` setting for each remote cluster, as configured on the local cluster.
4. Indicates whether any index, alias or data stream matches the index expression specified for that cluster.
5. The Elasticsearch server version.



### Identifying potential problems with your {{ccs}} [resolve-cluster-api-error-example]

The following request shows several examples of how modifying your query can prevent search failures. Note also that a `timeout` of 5 seconds is sent, which sets the maximum time the query will wait for remote clusters to respond.

```console
GET /_resolve/cluster/not-present,clust*:my-index*,oldcluster:*?ignore_unavailable=false&timeout=5s
```

```console-result
{
  "(local)": {
    "connected": true,
    "skip_unavailable": false,
    "error": "no such index [not_present]"  <1>
  },
  "cluster_one": {
    "connected": true,
    "skip_unavailable": true,
    "matching_indices": false,    <2>
    "version": {
      "number": "8.13.0",
      "build_flavor": "default",
      "minimum_wire_compatibility_version": "7.17.0",
      "minimum_index_compatibility_version": "7.0.0"
    }
  },
  "cluster_two": {
    "connected": false,           <3>
    "skip_unavailable": false
  },
  "cluster_three": {
    "connected": false,
    "skip_unavailable": false,
    "error": "Request timed out before receiving a response from the remote cluster"  <4>
  },
  "oldcluster": {         <5>
    "connected": true,
    "skip_unavailable": false,
    "matching_indices": true
  }
}
```

1. The local cluster has no index called `not_present`. Searching against it using the specified `ignore_unavailable=false` param will return a "no such index" error. Other types of errors can show up here as well, such as security permission errors when the user does not have authorization to search the specified index.
2. The `cluster_one` remote cluster has no indices that match the pattern `my-index*`. There may be no indices that match the pattern or the index could be closed. (You can check this by using the [resolve index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index) API.)
3. The `cluster_two` remote cluster is not connected (the attempt to connect failed). Since this cluster is marked as `skip_unavailable=false`, you should probably exclude this cluster from the search by adding `-cluster_two:*` to the search index expression.
4. For `cluster_three`, the error message indicates that this remote cluster did not respond within the 5-second timeout window specified, so it is also marked as not connected.
5. The `oldcluster` remote cluster shows that it has matching indices, but no version information is included. This indicates that the cluster version predates the introduction of the `_resolve/cluster` API in 8.13.0., so you may want to exclude it from your {{ccs}}. (Note: the endpoint was able to tell there were matching indices because it fell back to using the [resolve index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index) API.)



