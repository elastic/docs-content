---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
---

# Cross-project search [cross-project-search]

**{{cps-cap}}** enables you to run a single search request across multiple projects. For example, you can use {{cps}} to filter and analyze log data stored in projects connected through {{cps-init}}.
Common use cases include centralized log analysis, cross-environment troubleshooting, and incident investigation across multiple teams or services.

## Prerequisites

* {{cps-cap}} requires linked projects. To set up linked projects, refer to [**TODO**]().
* To use {{cps}} with ES|QL, both the origin and linked projects must have the appropriate [subscription level](https://www.elastic.co/subscriptions).
* {{cps-cap}} requires [UIAM](TODO) set up.

## Project linking

In {{cps-init}}, projects have one of two roles: origin projects and linked projects.
An **origin project** is a project that you link other projects to.
A **linked project** is a project that is connected to an origin project.
After linking projects, you can run queries from the origin project that also search the linked projects ({{cps}}).
Project linking is not bidirectional. When you search from an origin project, the query runs against its linked projects as well.
However, searches initiated from a linked project do not run against the origin project.

You can link projects by using the Cloud UI.

%%TODO: screenshot%%

1. On the home screen, select the project you want to use as the origin project and click **Manage**.
2. Click **Configure** on the **{{cps-cap}}** tile. Or click **{{cps-cap}}** in the left-hand navigation.
3. Click **Link projects**.
4. Select the project you want to link from the project list.

%%TODO: screenshot%%

5. Click **Review and save**.
6. Review the selected projects. If you are satisfied, click **Save**. You can also view and copy the corresponding API request by clicking **View API request**.

%%TODO: screenshot%%

Your configuration is saved, a page with the list of linked projects opens.

## Search in {{cps-init}}

### Flat-world search

If a project has linked projects, any search initiated on the origin project is automatically performed on the origin project and all of its linked projects.
This behavior is referred to as flat-world search.
For example, the following request searches the `logs` indices in the origin project and in every linked project by default:

```console
GET logs/_search
```

For each linked project, the search runs only if an index named `logs` exists.
If a linked project does not have a `logs` index, that project is skipped and the search continues without returning an error.

### Unqualified and qalified search expressions

{{cps-cap}} supports two types of search expressions: unqualified and qualified search expressions. The difference between them determines where a search request runs.

An **unqualified** search expression does not include a project prefix or tags. When you use an unqualified expression, the search is executed according to the flat-world search model.
In this case, the search runs against the origin project and all of its linked projects.

A **qualified** search expression includes additional qualifiers, such as project prefixes or tags, that explicitly control the scope of the search.

Qualified search expressions enables you to:

* restrict the search to the origin project only
* narrow the search to specific linked projects
* limit the search to projects that match certain tags

For example, the following request searches only the origin project:

```console
GET _origin:logs/_search
```

For additional examples of qualified search expressions, refer to the [examples section](#cps-examples).

#### Search scope and index resolution

In {{cps}}, when projects are linked to an origin project, all of their searchable resources are conceptually brought into the origin project’s search scope. For search purposes, this forms a single merged project view.

* Unqualified index expressions are resolved against this merged project view.
* Qualified index expressions are resolved independently within each qualified project.

As a result, unqualified searches treat linked projects as part of one larger logical project, unless the search expression explicitly limits the scope.

#### `ignore_unavaliable` and `allow_no_indices`

The distinction between qualified and unqualified index expressions affects how the `ignore_unavailable` and `allow_no_indices` search options are applied.
When you use an **unqualified** index expression, the merged project view is taken into account. In this case, these options are evaluated based on whether the target indices exist in any of the linked projects, not only in the origin project.

`ignore_unavaliable` defaults to `false`. If it `false`, the request returns an error if it targets a missing resource (for example, and index or a datastream).

`allow_no_indices` defaults to `true`. 

## Tags

## Security

%%A high-level overview%%

## Supported APIs [cps-supported-apis]

The following APIs support {{cps}}:

* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [CAT count](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-cat-count)
* Datafeeds [PUT](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-put-datafeed), [GET](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-get-datafeeds), [DELETE](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-delete-datafeed)
* [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Multi search template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template)
* [Painless execute API](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md)
* PIT (point in time) [close](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-close-point-in-time), [open](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-open-point-in-time)
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-reindex)
* [Resolve Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index)
* [SQL](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-sql)
* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* Search scroll [clear](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-clear-scroll), [run](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-scroll)
* [Search template](/solutions/search/search-templates.md)
* [Transforms](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-transform)

### {{cps-cap}} specific APIs

**Project routing**: `_project_routing`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)

**Project tags**: `_project/tags`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)

## Limitations

### Maximum of 20 linked projects per origin project

Each origin project can have up to 20 linked projects.
A linked project can be associated with any number of origin projects.

## {{cps-cap}} examples [cps-examples]