---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
description: Learn how cross-project search (CPS) enables you to search across multiple Serverless projects from a single request.
---

# {{cps-cap}} [cross-project-search]

::::{include} /deploy-manage/_snippets/cps-definition.md
::::

From the origin project, you can run queries, build dashboards, and configure alerting rules that include data from all linked projects. Results are filtered by each user's permissions across projects.

{{cps-cap}} relies on linking projects within your {{ecloud}} organization. After you link projects together, searches from the origin project automatically run across all linked projects.

This overview explains how {{cps}} works, including project linking and security.
For prerequisites, compatibility requirements, architecture planning, and scope defaults, refer to [](/deploy-manage/cross-project-search-config.md).

For details on how search, tags, and project routing work in {{cps-init}}, refer to the following pages:

* [Search in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-search.md): Learn how search expressions, search options, and index resolution work.
* [Tags in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-tags.md): Learn about predefined and custom project tags and how to use them in queries.
* [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md): Learn how to route searches to specific projects based on tag values.
* [Manage {{cps-init}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md): Control which projects are searched as you work in Discover, Dashboards, and other {{kib}} apps.

## {{cps-cap}} as the default behavior for linked projects

::::{include} /explore-analyze/cross-project-search/_snippets/cps-default-search-behavior.md
::::

## Project linking

In {{serverless-short}}, projects can be linked together.

::::{include} /deploy-manage/_snippets/cps-origin-linked-definitions.md
::::

After you link projects, searches that you run from the origin project are no longer scoped to the origin project by default.
**Any search initiated on the origin project automatically runs across the origin project and all its linked projects ({{cps}}).**

When you search from an origin project, the query runs against its linked projects automatically unless you explicitly change the query scope by using [project routing expressions](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) or [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions).

Project linking is not bidirectional. Searches initiated from a linked project do **not** run against the origin project. If you need bidirectional search, link the projects twice, in both directions.

You can link projects by using the {{ecloud}} UI. For step-by-step instructions, refer to [Link projects for {{cps}}](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md).

### Project IDs and aliases

Each project has a unique project ID and a project alias.
The project alias is derived from the project name and can be modified.

The **project ID** uniquely identifies a project and is system-generated.

The [**project alias**](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-connection-aliases) is a human-readable identifier derived from the project's connection alias. If you want to change the project alias, you must update the connection alias of the linked project.

While both the project ID and project alias uniquely identify a project, {{cps}} uses project aliases in index expressions. Project aliases are intended to be user-friendly and descriptive, making search expressions easier to read and maintain.

#### Referencing the origin project

In addition to using a project alias, {{cps-init}} provides a reserved identifier, `_origin`, that always refers to the origin project of the search.
You can use `_origin` in search expressions to explicitly target the origin project, without having to reference its specific project alias. Refer to [Qualified and unqualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) for detailed examples and to learn more.

## Excluding indices and projects

You can exclude specific indices or projects from a {{cps}} by prefixing a pattern with a dash (`-`).
This enables you to start with a broad search scope and narrow it down by removing specific indices or projects from the results.

### How exclusion works

Exclusion follows these rules:

* A leading `-` on a pattern signals exclusion. The dash can be placed on the index part or on the project part of an expression, each with different requirements.
Placing the dash on the **index** part (for example, `linked-project-1:-my-index` or `linked-project-1:-*`) works for any index pattern and can be used on its own.
Placing the dash on the **project** part (for example, `*,-linked-project-1:*`) requires a preceding inclusion pattern and only works when the index part is the `*` wildcard. For example, `*,-linked-project-1:*` is valid, but `*,-linked-project-1:my-index` is not.
You cannot prefix both the project and the index with a dash in the same expression (for example, `-linked-project-1:-*` is invalid).
* An exclusion pattern only affects patterns that appear **before** it in the expression.
Patterns listed **after** the exclusion are not affected by it (for example, in `*,-*,my-index`, the exclusion `-*` removes everything matched by the first `*`, but `my-index` comes after the exclusion and is still included).
* You can use multiple exclusion patterns in a single expression.

### Exclusion examples

The following examples assume an origin project with two linked projects: `linked-project-1` and `linked-project-2`.

`*,-linked-project-1:*`
:   Searches everything across all projects, then excludes all indices on the `linked-project-1` project. The search runs on the origin project and `linked-project-2` only.

`*,linked-project-1:-my-index`
:   Searches everything across all projects, then excludes only the `my-index` index on the `linked-project-1` project. All other indices on `linked-project-1` and all indices on the origin project and `linked-project-2` are still included.

`*,-my-index*,-logs`
:   Searches everything, then applies two exclusion patterns. Indices matching `my-index*` and the `logs` index are excluded from the results from all projects.

`*,linked-project-1:-*`
:   Excludes all indices on the `linked-project-1` project. This is functionally equivalent to `*,-linked-project-1:*`.

`*,-*`
:   Matches all indices across all projects, then excludes all of them. The result is an empty scope.

`*,-*,my-index`
:   Matches all indices, then excludes all indices. Because the exclusion only affects patterns before it, the `my-index` pattern that follows is unaffected and `my-index` is still included in the search.

## Security

This section gives you a high-level overview of how security works in {{cps}}.

:::{include} /explore-analyze/cross-project-search/_snippets/cps-security.md
:::

### How access is evaluated

:::{include} /explore-analyze/cross-project-search/_snippets/cps-access-evaluation.md
:::

**Example**

You have read access to the `logs` index in project 1, but no access to the `logs` index in project 2.
If you run `GET logs/_search`:

* documents from the `logs` index in project 1 are returned
* the `logs` index in project 2 is not accessible and is excluded from the results. No error is returned. The query succeeds, but results only include data from projects where your role grants access.

## Supported APIs [cps-supported-apis]

The following APIs support {{cps}}:

* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [Count](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-count) and [CAT count](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-cat-count)
* [ES|QL query](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-esql-queryv) and [ES|QL async query](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-esql-async-query)
* [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Multi search template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template)
* PIT (point in time) [close](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-close-point-in-time), [open](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-open-point-in-time)
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-reindex)
* [Resolve Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index)
* [SQL](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-sql)
* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* [Search a vector tile](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-search-mvt)
* Search scroll [clear](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-clear-scroll), [run](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-scroll)
* [Search template](/solutions/search/search-templates.md)

### {{product.painless}} scripting [cps-painless-scripting]

The [{{product.painless}} execute API](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md) (`POST _scripts/painless/_execute`) does not search across linked projects. Unlike the search APIs listed above, the execute API resolves index names against the **origin project only**.

When testing scripts with the execute API in a {{cps}} environment:

* To target a specific linked project, prefix the index with the project alias: `projectAlias:myindex`.
* To explicitly target the origin project, use `_origin:myindex`.
    * An unqualified index name like `logs` is equivalent to `_origin:logs` — it targets the origin project only.
* Only a single index is accepted. Wildcards and [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) are not supported.
* Requests to linked projects are subject to the same [security model](/explore-analyze/cross-project-search.md#security) as other {{cps}} requests.

For additional information, refer to the [{{product.painless}} execute API reference](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md).

### {{cps-cap}} specific APIs

**Project routing**: `_project_routing`

* [Create or update project routing expressions](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-project-create-many-routing)
* [Get a project routing expression](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-project-get-routing)
* [Delete a project routing expression](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-project-delete-routing)

**Project tags**: `_project/tags`

* [Get tags](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-project-tags)

## Identifying the location of a document [cps-identify-documents]

To determine whether a document comes from the origin project or a linked project, examine the `_index` field.

Documents from linked projects include the linked project's alias as a prefix, separated by a colon:

```
my-linked-project-abc123:.ds-logs-generic.otel-default-2026.03.02-000001
```

Origin documents have no prefix:

```
.ds-logs-generic.otel-default-2026.03.02-000001
```

In {{esql}}, the `_index` field is not returned by default. To include it, use the `METADATA` keyword:

```esql
FROM logs-* METADATA _index
| WHERE @timestamp > "2026-03-16T15:15:00Z"
| KEEP @timestamp, _index, message
```

## Limitations [cps-limitations]

::::{include} /deploy-manage/_snippets/cps-limitations-core.md
::::

For a [complete list of limitations](/deploy-manage/cross-project-search-config.md#cps-limitations), including restrictions for Elastic Observability and {{elastic-sec}} projects, as well as administrator-focused details including compatibility, architecture patterns, and feature impacts, refer to [](/deploy-manage/cross-project-search-config.md).

To check whether {{cps}} is available in a specific {{kib}} app, refer to the [availability table](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-availability).

## {{cps-cap}} examples [cps-examples]

The following examples show how {{cps}} resolves index names and routes queries when you use unqualified expressions, qualified expressions, and project routing.

### Unqualified search expressions

In the following example, an origin project and a linked project both contain an index named `my-index`.

```console
GET /my-index/_search
{
  "size": 2,
  "query": {
    "match_all": {}
  }
}
```

The request will return a response similar to this:

```console

{
  "took": 34,
  "timed_out": false,
  "num_reduce_phases": 3,
  "_shards": {
    "total": 12,
    "successful": 12,
    "skipped": 0,
    "failed": 0
  },
  "_clusters": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "running": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "_origin": {
        "status": "successful",
        "indices": "my-index",
        "took": 21,
        "timed_out": false,
        "_shards": {
          "total": 6,
          "successful": 6,
          "skipped": 0,
          "failed": 0
        }
      },
      "linked_project": {
        "status": "successful",
        "indices": "my-index",
        "took": 5,
        "timed_out": false,
        "_shards": {
          "total": 6,
          "successful": 6,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "linked_project:my-index",
        "_id": "IH-mupwBMZyy2F9u2IQz",
        "_score": 1.0,
        "_source": {
          "project": "linked"
        }
      },
      {
        "_index": "my-index",
        "_id": "u0SnupwBaOrMOsBImb7G",
        "_score": 1.0,
        "_source": {
          "project": "origin"
        }
      }
    ]
  }
}
```

In this example, both the origin project and a linked project contain an index named `my-index`:

```console
POST /_query
{
 "query": "FROM my-index",
  "include_execution_metadata": true
}
```
The query will return a response similar to this:

```console
{
  "took": 39,
  "is_partial": false,
  "completion_time_in_millis": 1772659251830,
  "documents_found": 2,
  "values_loaded": 4,
  "start_time_in_millis": 1772659251791,
  "expiration_time_in_millis": 1773091251753,
  "columns": [
    {
      "name": "project",
      "type": "text"
    },
    {
      "name": "project.keyword",
      "type": "keyword"
    }
  ],
  "values": [
    [
      "origin",
      "origin"
    ],
    [
      "linked",
      "linked"
    ]
  ],
  "_clusters": {
    "total": 2,
    "successful": 2,
    "running": 0,
    "skipped": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "_origin": {
        "status": "successful",
        "indices": "my-index",
        "took": 39,
        "_shards": {
          "total": 6,
          "successful": 6,
          "skipped": 0,
          "failed": 0
        }
      },
      "linked_project": {
        "status": "successful",
        "indices": "my-index",
        "took": 23,
        "_shards": {
          "total": 6,
          "successful": 6,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  }
}
```
These requests don’t include a project prefix. The `my-index` index is searched in the origin project and in the linked project.

### Qualified search expressions

Search limited to the `origin` project:

::::{tab-set}

:::{tab-item} _search
```console
GET _origin:my-index/_search
```
:::

:::{tab-item} ES|QL
```console
POST /_query
{
  "query": "FROM _origin:my-index | LIMIT 10"
}
```
:::

::::

The requests include the `_origin` prefix. Only the origin project is searched.

Search across all projects using a wildcard expression:

::::{tab-set}

:::{tab-item} _search
```console
GET *:my-index/_search
```
:::

:::{tab-item} ES|QL
```console
POST /_query
{
  "query": "FROM *:my-index | LIMIT 10"
}
```
:::

::::

The requests explicitly target all projects using the `*:` prefix.
The `my-index` index is evaluated separately in each project.
The index `my-index` must exist in every project, otherwise [the search returns an error](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions).

### Project routing examples

In the following example, there is an origin project and a linked project. The origin project contains one index, `my-index`. The linked project contains two indices: `my-index` and `logs`.

The following request searches all indices on projects whose alias starts with "lin".

::::{tab-set}

:::{tab-item} _search
```console
GET /*/_search
{
  "project_routing":"_alias:lin*",
  "query": {
    "match_all": {}
  }
}
```
:::

:::{tab-item} ES|QL
```console
GET /_query
{
  "query": "SET project_routing=\"_alias:lin*\"; FROM * METADATA _index",
  "include_execution_metadata":true
}
```
:::

::::

The request will return a response similar to this:

::::{tab-set}

:::{tab-item} _search
```console
{
  "took": 60,
  "timed_out": false,
  "_shards": {
    "total": 12,
    "successful": 12,
    "skipped": 0,
    "failed": 0
  },
  "_clusters": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "running": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "linked_project": {
        "status": "successful",
        "indices": "*",
        "took": 11,
        "timed_out": false,
        "_shards": {
          "total": 12,
          "successful": 12,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "linked_project:my-index",
        "_id": "ytm_v5wB1c8L_6vBSeM6",
        "_score": 1.0,
        "_source": {
          "project": "linked"
        }
      },
      {
        "_index": "linked_project:logs",
        "_id": "y9m_v5wB1c8L_6vBW-Mu",
        "_score": 1.0,
        "_source": {
          "project": "linked-logs-data"
        }
      }
    ]
  }
}
```
:::

:::{tab-item} ES|QL
```console
{
  "took": 54,
  "is_partial": false,
  "completion_time_in_millis": 1772740419771,
  "documents_found": 2,
  "values_loaded": 6,
  "start_time_in_millis": 1772740419717,
  "expiration_time_in_millis": 1773172419734,
  "columns": [
    {
      "name": "project",
      "type": "text"
    },
    {
      "name": "project.keyword",
      "type": "keyword"
    },
    {
      "name": "_index",
      "type": "keyword"
    }
  ],
  "values": [
    [
      "linked-logs-data",
      "linked-logs-data",
      "linked_project:logs"
    ],
    [
      "linked",
      "linked",
      "linked_project:my-index"
    ]
  ],
  "_clusters": {
    "total": 1,
    "successful": 1,
    "running": 0,
    "skipped": 0,
    "partial": 0,
    "failed": 0,
    "details": {
      "linked_project": {
        "status": "successful",
        "indices": "*",
        "took": 35,
        "_shards": {
          "total": 12,
          "successful": 12,
          "skipped": 0,
          "failed": 0
        }
      }
    }
  }
}
```
:::

::::

#### Project routing with named project routing expressions

First, create the named expression:

```console
PUT /_project_routing/origin-only
{
  "expression": "_alias:_origin"
}
```

Then, query it:

::::{tab-set}

:::{tab-item} _search
```console
GET /my*/_search
{
  "project_routing": "@origin-only",
  "query": {
    "match_all": {}
  }
}
```
:::

:::{tab-item} ES|QL
```console
GET /_query
{
  "project_routing": "@origin-only",
  "query": "FROM *",
  "include_execution_metadata": true
}
```
:::

::::

#### Project routing and qualified expressions

In the first example, both the project routing rule and the qualified index expression limit the search to the linked project:

```console
GET /linked_project:my*/_search
{
  "project_routing": "_alias:lin*",
  "query": {
    "match_all": {}
  }
}
```

In the next example, the project routing rule and the qualified index expression target different projects which causes a conflict:

```console
GET /_origin:*,linked_project:*/_search
{
  "project_routing": "@origin-only",
  "query": {
    "match_all": {}
  }
}
```

This request returns an error:

```console
{
  "error": {
    "root_cause": [
      {
        "type": "no_matching_project_exception",
        "reason": "No such project: [linked_project] with project routing [@origin-only]"
      }
    ],
    "type": "no_matching_project_exception",
    "reason": "No such project: [linked_project] with project routing [@origin-only]"
  },
  "status": 404
}
```
