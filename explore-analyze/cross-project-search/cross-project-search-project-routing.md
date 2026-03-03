---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
description: Learn how to use project routing to limit cross-project search (CPS) queries to specific projects based on tag values.
---

# Project routing [cps-project-routing]

Project routing enables you to limit a search to a subset of projects, including the origin project and linked projects, based on tag values.

When you use project routing, the routing decision is made before the search request is performed.
Based on the specified tags, {{cps-init}} determines which projects the query is sent to, and the search is performed only on those projects.

For an overview of {{cps}} concepts, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md). For details on available tags, refer to [Tags in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-tags.md).

The `project_routing` parameter is available on all {{cps-init}}-enabled endpoints. Refer to the [supported APIs](/explore-analyze/cross-project-search.md#cps-supported-apis) for a full list of endpoints.

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

Refer to [the examples section](/explore-analyze/cross-project-search.md#cps-examples) for more.

<!--
Also link to the ES|QL CPS tutorial when it's available for more ES|QL examples.
-->

## Using named project routing expressions [named-routing-expressions]

You can define named project routing expressions and reference them in the `project_routing` parameter of any {{cps}}-enabled endpoint that supports project routing.

Named expressions enable you to assign a reusable name to a routing expression. This makes complex routing rules easier to reference and reuse across multiple requests.

To reference a named project routing expression in a `project_routing` parameter, prefix its name with the `@` character.

For example, the following [`_search` API](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-search) request and [ES|QL query](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-esql-query) search the `logs` resource only on projects that match the `@custom-expression` routing rule.

::::{tab-set}

:::{tab-item} API request
```console
GET logs/_search
{
"project_routing": "@custom-expression",
"query": { ... }
}
```
:::

:::{tab-item} ES|QL
```console
SET project_routing="@custom-expression";
FROM logs 
| STATS COUNT(*)
```
:::

::::

### Creating and managing named project routing expressions

You can use the `_project_routing` API to create and manage named project routing expressions.

::::{note}
Named project routing expressions are project-specific. An expression can be used only in the project where it was created.
::::

The following request creates a named expression called `origin-only`:

```console
PUT _project_routing/origin-only
{
    "expression" : "_alias:origin"
}
```

<!--
The following request creates a named expression called `aws-us-only`:

```console
PUT _project_routing/aws-us-only
{
    "expression" : "_csp:aws AND _region:us*"
}
```
-->

You can also create multiple named expressions in a single request:

```console
PUT _project_routing
{
"origin-only": { "expression": "_alias:origin" },
"linked-security": { "expression": "_alias:*sec*" }
}
```

<!--
```console
PUT _project_routing
{
   "aws-us-only": { "expression": "_csp:aws AND _region:us*" },
   "aws-eu-only": { "expression": "_csp:aws AND _region:eu*" }
}
```
-->

The GET `_project_routing` endpoint retrieves information about named expressions.

To retrieve all named expressions:

```console
GET _project_routing
```

To retrieve a specific named expression:

```console
GET _project_routing/origin-only
```

To delete a named expression:

```console
DELETE _project_routing/origin-only
```

::::{note}
When using the `_project_routing` API to create, retrieve, or delete expressions, do not prefix the expression name with `@`. The `@` prefix is required only when referencing a named expression in the `project_routing` parameter of API endpoints that support it.
::::
