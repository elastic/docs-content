---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
---

# {{cps-cap}} [cross-project-search]

**{{cps-cap}}** enables you to run a single search request across multiple projects. For example, you can use {{cps}} to filter and analyze log data stored in projects linked through {{cps-init}}.
Common use cases include centralized log analysis, cross-environment troubleshooting, and incident investigation across multiple teams or services.

## {{cps-cap}} as the default behavior for linked projects

Projects are intended to act as logical namespaces for data, not hard boundaries for querying it. You can split data into projects to organize ownership, use cases, or environments, while still expecting to search and analyze that data from a single place.

Because of this, {{cps}} is the default behavior for your linked projects.
Searches are designed to run across projects automatically, providing the same experience for querying, analysis, and insights across projects as within a single project.
Restricting search scope is always possible, but it requires an explicit choice rather than being the default.

## Prerequisites

* {{cps-cap}} requires linked projects.
<!-- To set up linked projects, refer to . -->
* To use {{cps}} with ES|QL, both the origin and linked projects must have the appropriate [subscription level](https://www.elastic.co/subscriptions).
<!-- * {{cps-cap}} requires [UIAM](TODO) set up. -->

## Project linking

In {{serverless-short}}, projects can be linked together. The project from which links are created is called the origin project, and the connected projects are referred to as linked projects.
The **origin project** is the project you are currently working in and from which you run cross-project searches.
**Linked projects** are other projects that are connected to the origin project and whose data can be searched from it.
After you link projects, searches that you run from the origin project are no longer local to the origin project by default.
**Any search initiated on the origin project automatically runs across the origin project and all its linked projects ({{cps}}).**
Project linking is not bidirectional. When you search from an origin project, the query runs against its linked projects automatically unless you explicitly change the scope.
However, searches initiated from a linked project do not run against the origin project.

You can link projects by using the Cloud UI.

<!--
TODO: screenshot
-->

1. On the home screen, select the project you want to use as the origin project and click **Manage**.
2. Click **Configure** on the **{{cps-cap}}** tile. Or click **{{cps-cap}}** in the left-hand navigation.
3. Click **Link projects**.
4. Select the project you want to link from the project list.

<!--
TODO: screenshot
-->

5. Click **Review and save**.
6. Review the selected projects. If you are satisfied, click **Save**. You can also view and copy the corresponding API request by clicking **View API request**.

<!--
TODO: screenshot
-->

When your configuration is saved, a page with the list of linked projects opens.

### Project ID and aliases

Each project has a unique project ID and a project alias.
The project alias is derived from the project name and can be modified.

The **project ID** uniquely identifies a project and is system-generated.

The **project alias** is a human-readable identifier that you can change to make a project easier to recognize and reference.

While both the project ID and project alias uniquely identify a project, {{cps}} uses project aliases in index expressions. Project aliases are intended to be user-friendly and descriptive, making search expressions easier to read and maintain.

#### Referencing the origin project

In addition to using a project alias, {{cps-init}} provides a reserved identifier, `_origin`, that always refers to the origin project of the search.
You can use `_origin` in search expressions to explicitly target the origin project, without having to reference its specific project alias. Refer to [](#search-expressions) for detailed examples and to learn more.

## Search in {{cps-init}}

This section explains how search works in {{cps-init}}, including:

* the {{cps-init}} search model
* **qualified search expressions** (for example,`logs` and `logs*`), **unqualified search expressions** (expressions with a project alias prefix, for example `project1:logs`) and how they control search scope
* how **index resolution** works across the merged project view
* how search options such as `ignore_unavailable` and `allow_no_indices` behave in {{cps-init}}
* common edge cases and examples involving mixed qualified and unqualified expressions

### {{cps-init}} search model

With {{cps-init}}, searches are resolved across all projects, not just on the origin project by default.
You explicitly need to limit the scope of your search to override this behavior. Refer to the [](#search-expressions) section to learn more.
When you refer to a resource by a name, {{cps-init}} resolves that name across the origin project and all of its linked projects.
This means that when you run a search from the origin project and refer to a searchable resource such as `logs`, the search is executed against all resources named `logs` across the origin project and its linked projects, for example:

```console
GET logs/_search
```

For each linked project, the search runs only if a resource named `logs` exists.
If a linked project does not have a `logs` resource, that project is skipped and the search continues without returning an error. No error is returned as long as at least one project has the `logs` resource.

### Unqualified and qualified search expressions [search-expressions]

{{cps-cap}} supports two types of search expressions: unqualified and qualified search expressions. The difference between them determines where a search request runs and how errors are handled.

**Unqualified search expressions** follow the {{cps}} model and represent the default, native behavior in {{cps-init}}.
**Qualified search expressions** explicitly override the default behavior, providing CCS-like semantics for controlling where a search runs and how errors are handled.

An unqualified search expression does not include a project alias prefix.
In this case, the search runs against the origin project and all its linked projects.

A qualified search expression includes additional qualifiers, such as project alias prefixes, that explicitly control the scope of the search.

For example, the following request searches only the origin project:

```console
GET _origin:logs/_search
```

For additional examples of qualified search expressions, refer to the [examples section](#cps-examples).

#### Search scope and index resolution

In {{cps}}, when projects are linked to an origin project, all their searchable resources are conceptually brought into the origin project’s search scope. For search purposes, this forms a single merged project view.

* Unqualified index expressions are resolved against this merged project view.
* Qualified index expressions are resolved independently within each project explicitly targeted by the search expression.

As a result, unqualified searches treat linked projects as part of one larger logical project, unless the search expression explicitly limits the scope.

#### `ignore_unavailable` and `allow_no_indices`

The distinction between qualified and unqualified search expressions affects how the `ignore_unavailable` and `allow_no_indices` search options are applied in {{cps}}.
When you use an **unqualified** expression, index resolution is performed against the merged project view. In this case, search options are evaluated based on whether the target resources exist in any of the searched projects, not only in the origin project.

::::{important}
The way that missing resources are interpreted differs between qualified and unqalified expressions, refer to [this section](#behavior-qualified-unqualified) for a detailed explanation.
::::

`ignore_unavailable` defaults to `false`.
When set to `false`, the request returns an error if it targets a missing resource (such as an index or data stream).
When set to `true`, missing resources are ignored and the request returns an empty result instead of an error.
For example, if the `logs` index does not exist, the following request returns an error because the default value is `false`:

```console
GET logs/_search
```

`allow_no_indices` defaults to `true`.
When set to `true`, the request succeeds and returns an empty result if it targets a missing resource.
When set to `false`, the request returns an error if any wildcard expression, index alias, or `_all` value does not resolve to an existing resource.

For example, if no indices match `logs*`, the following request returns an empty result because the default value is `true`:

```console
GET logs*/_search
```

##### Behavior with qualified and unqualified expression [behavior-qualified-unqualified]

When you use a **qualified search expression**, the default behavior of `ignore_unavailable` and `allow_no_indices` outlined above applies independently to each qualified project.

When you use an **unqualified search expression**, the behavior is different:

* As long as the targeted resources exist in at least one of the searched projects, the request succeeds, even if `ignore_unavailable` or `allow_no_indices` are set to false.
* The request returns an error only if:
  * the targeted resources are missing from all searched projects, or
  * a search expression explicitly targets a specific project and the resource is missing from that project.

##### Examples

You have two projects linked to your `origin` project: `project1` and `project2`.
Resources:

* `origin` has a `logs` index
* `project1` has a `metrics` index
* `project2` has a `books` index

**The following request succeeds**, even with `ignore_unavailable=false`:

```console
GET logs,metrics/_search?ignore_unavailable=false
```

Although `logs` is not present in `project2` and `metrics` is not present in `origin`, each index exists in at least one searched project, so the request succeeds.

If the projects have the following resources, however:

* `origin` has a `metrics` index
* `project1` has a `metrics` index
* `project2` has a `books` index

**The following request returns an error**:

```console
GET logs,metrics/_search?ignore_unavailable=false
```

In this case, the `logs` index does not exist in any of the searched projects, so the request fails.

In the next example, the request combines qualified and unqualified index expressions.
Resources:

* `origin` has a `logs` index
* `project1` has a `metrics` index
* `project2` has a `books` index

**The following request returns an error**:

```console
GET logs,project2:metrics/_search?ignore_unavailable=false
```

Because the request explicitly targets `project2` for the `metrics` index using a qualified expression and `ignore_unavailable` is set to `false`, the entire request returns an error, even though the `logs` index exists in one of the projects.

Refer to [the examples section](#cps-examples) for more.

<!--
### System and hidden indices
TODO
-->

## Tags

You can assign tags to projects and use them to control {{cps}} behavior. Tags are managed in the Elastic Cloud UI.

With tags, you can:

* route API calls to specific projects based on tag values
* include tag values in search or ES|QL results to identify which project each document came from
* filter and aggregate results using tags

The following tags are predefined:

* `_alias`: the project alias
* `_csp`: the cloud service provider
* `_id`: the project identifier
* `_organization`: the organization identifier
* `_region`: the CPS region
* `_type`: the project type (Observability, Search, Security)

Predefined tags are always start with an underscore `_`.

### Using tags in {{cps-init}}

There are two ways to use tags in {{cps-init}}:

* project routing
* queries

#### Project routing

Project routing enables you to limit a search to a subset of linked projects (the origin project and its linked projects) based on tag values.
When you use project routing, the routing decision is made before the search request is performed.
Based on the specified tags, {{cps-init}} determines which projects the query is sent to, and the search is performed only on those projects.
The `project_routing` parameter is available on all cross-project-enabled endpoints. Refer to the [](#cps-supported-apis) for a full list of endpoints.
When you specify tags in the project_routing parameter, projects that do not match the specified tags are excluded from the search entirely. The query is never run on those projects.

For example, the following API request searches the `logs` resource only on projects that have the `_alias:my_search_project` tag.

```console
GET logs/_search 
{
  "project_routing": "_alias:my_search_project"
}
```

::::{important}
Currently, project routing only supports using the `_alias` tag.
::::

<!--
Project routing supports prefix and suffix wildcards, boolean logic and groupings of terms. The tag syntax matches the Lucene syntax notation, including in ES|QL.
For example:

```console
GET logs/_search
{
  project_routing="(_region:us-* AND _csp:aws) OR _csp:gcp"
}
```
-->

Refer to [the examples section](#cps-examples) for more.

<!--
Also link to the ES|QL CPS tutorial when it's available for more ES|QL examples.
-->

#### Using project tags in queries

You can also use project tags within a search query. In this case, tags are treated as query-time metadata, not as routing criteria.
You can explicitly request project tags to be included in search results. For both `_search` and ES|QL, you must request one or more tags to include them in the response.

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
Unlike project routing, using tags inside a query does not affect which projects the query is sent to. The routing decision has already been made before the query is performed.
When tags are used in queries, they act only as queryable metadata. They do not change search scope or limit operation on specific projects.
For example, the following request aggregates results by cloud service provider:

For example:

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


<!--
## Security

A high-level overview
-->

## Supported APIs [cps-supported-apis]

The following APIs support {{cps}}:

* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [CAT count](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-cat-count)
* Datafeeds [PUT](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-put-datafeed), [GET](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-get-datafeeds), [DELETE](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-delete-datafeed)
* [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Multi search template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template)
* PIT (point in time) [close](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-close-point-in-time), [open](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-open-point-in-time)
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-reindex)
* [Resolve Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index)
* [SQL](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-sql)
* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* Search scroll [clear](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-clear-scroll), [run](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-scroll)
* [Search template](/solutions/search/search-templates.md)
* [Transforms](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-transform)

<!--
### {{cps-cap}} specific APIs

**Project routing**: `_project_routing`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)

**Project tags**: `_project/tags`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)
-->

## Limitations

### Maximum of 20 linked projects per origin project

Each origin project can have up to 20 linked projects.
A linked project can be associated with any number of origin projects.

## {{cps-cap}} examples [cps-examples]

<!--
Examples to include:

* GET logs/_search
* GET _origin:logs/_search
* GET *:logs/_search
* GET *:logs/_search?ignore_unavailable=false
...
* have example(s) of resuts
* more complex project_routing examples
* qualified search expressions and project_routing
-->