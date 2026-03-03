---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
description: Learn about project tags in cross-project search (CPS), including predefined and custom tags, and how to use them in search queries.
---

# Tags in {{cps-init}} [cps-tags]

You can assign [tags](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-tags) to projects and use them to control {{cps}} behavior.

For an overview of {{cps}} concepts, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md).

{{cps-init}} supports two kinds of project tags:

* Predefined tags, which are provided by Elastic and describe built-in project metadata.
* Custom tags, which you define and manage to organize projects according to your own needs. These tags are managed in the {{ecloud}} UI.

Only custom tags can be added, modified, or removed. Predefined tags are always available and cannot be changed.

With tags, you can:

* route API calls to specific projects based on tag values
* include tag values in search or ES|QL results to identify which project each document came from
* filter and aggregate results using tags

The following tags are predefined:

* `_alias`: the project alias
* `_csp`: the cloud service provider
* `_id`: the project identifier
* `_organization`: the organization identifier
* `_region`: the Cloud region where the project is located
* `_type`: the project type (Observability, Search, Security)

Predefined tags always start with an underscore `_`.

## Using tags in {{cps-init}}

There are two ways to use tags in {{cps-init}}:

* [Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md): limit a search to a subset of projects based on tag values. The routing decision is made before the search is performed.
* [Queries](#tag-queries): include tag values in search results, or use them to filter, sort, and aggregate results.

## Using tags in queries [tag-queries]

You can also use project tags within a search query. In this case, tags are treated as query-time metadata fields, not as routing criteria.
You can explicitly request project tags to be included in search results. For both `_search` and ES|QL, you must request one or more tags to include them in the response.

::::{note}
The `_project.` prefix is required when using tags in search or ES|QL queries to disambiguate project metadata from Lucene fields.
It is optional when using tags for project routing.
::::

For example, with the `_search` endpoint:

```console
GET logs/_search
{
  "fields": ["*", "_project.mytag", "_project._region"]
}
```

For example, with ES|QL:

```console
GET /_query
{
  "query": "FROM logs METADATA _project._csp, _project._region | ..."
}
```

In both cases, the returned documents include the requested project metadata, which lets you identify which project each document originated from.

You can also use project tags in queries to filter, sort, or aggregate search results.
Unlike project routing, using tags inside a query does not affect which projects the query is sent to. It only affects which results are returned. The routing decision has already been made before the query is performed. 

For example, the following request aggregates results by cloud service provider:

```console
GET foo/_search
{
 "query": { ... }
 "aggs": {
    "myagg": {
      "terms": {
        "field": "_project._csp"
      }
    }
  }
}
```

When you use project tags in ES|QL, you must explicitly include them in the METADATA clause.
This is required not only to return tag values in the results, but also to use them in the query for filtering, sorting, or aggregation.

For example, the following ES|QL query counts documents per project alias:

```console
FROM logs* METADATA _project._alias | STATS COUNT(*) by _project._alias
```
<!--
Include a link to the ES|QL CPS tutorial.
-->
