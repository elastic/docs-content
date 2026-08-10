---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
description: Learn how to use project routing to limit cross-project search (CPS) queries to specific projects based on tag values.
navigation_title: "Project routing"
---

# Using project routing to limit {{cps}} scope [cps-project-routing]

Project routing enables you to limit a search to a subset of projects, including the origin project and linked projects, based on tag values.

When you use project routing, the routing decision is made before the search request is performed.
Based on the specified tags, {{cps}} determines which projects the query is sent to, and the search is performed only on those projects.

For an overview of {{cps}} concepts, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md). For details on available tags, refer to [Tags in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-tags.md).

The `project_routing` parameter is available on all {{cps-init}}-enabled endpoints. Refer to the [supported APIs](/explore-analyze/cross-project-search.md#cps-supported-apis) for a full list of endpoints.

For example, the following request searches the `logs` resource only on projects that have the `_alias:my_search_project` tag.

```console
GET logs/_search
{
  "project_routing": "_alias:my_search_project"
}
```

Project routing expressions use Lucene query syntax, so you're not limited to a single tag or an exact match. You can route on any predefined tag, such as `_alias`, `_csp`, or `_region`, or on any custom tag you define in the {{ecloud}} UI. In an expression, the colon (`:`) separates a tag from its value.

You can combine tags with the `AND`, `OR`, and `NOT` operators and group terms with parentheses. You can also use prefix or suffix wildcards to match part of a tag value. Tag value matching is case-insensitive, so `_csp:AWS` matches the value `aws`. Tag names are case-sensitive, so use `_csp`, not `_CSP`. The syntax is the same for the `_search` API and {{esql}}.

:::{note}
You can optionally add the `_project.` prefix to a tag name, for example `_project._csp:aws`. This is the same prefix used to reference tags in queries. In project routing the prefix is optional, so `_csp:aws` and `_project._csp:aws` are equivalent.
:::

For example, the following request routes the search to projects on Amazon Web Services (AWS) in a US region, or to any project on Google Cloud:

::::{tab-set}

:::{tab-item} API request
```console
GET logs/_search
{
  "project_routing": "(_region:us-* AND _csp:aws) OR _csp:gcp"
}
```
:::

:::{tab-item} ES|QL
```esql
SET project_routing="(_region:us-* AND _csp:aws) OR _csp:gcp";
FROM logs
| STATS COUNT(*)
```
:::

::::

Value matching is case-insensitive. For example, `_csp:GCP` matches the same projects as `_csp:gcp`.

::::{note}
Every term in an expression needs a tag name, and every tag must be defined. These expressions fail:

* `_csp:aws OR gcp` fails because the bare term `gcp` has no tag name. Use `_csp:aws OR _csp:gcp` instead.
* `_foo:bar` fails because `_foo` isn't a defined tag.
* `NOT _csp:azure` fails because an expression can't be only a negation. To match every project except Azure, include first and then exclude: `_csp:* AND NOT _csp:azure`.
::::

Refer to [the examples section](/explore-analyze/cross-project-search.md#cps-examples) for more. You can also refer to [Query across Serverless projects with ES|QL](elasticsearch://reference/query-languages/esql/esql-cross-serverless-projects.md) for more ES|QL examples.

## Using named project routing expressions [named-routing-expressions]

You can define named project routing expressions and reference them in the `project_routing` parameter of any {{cps}}-enabled endpoint that supports project routing.

Named expressions enable you to assign a reusable name to a routing expression. This makes complex routing rules easier to reference and reuse across multiple requests.

To reference a named project routing expression in a `project_routing` parameter, prefix its name with the `@` character.

For example, the following [`_search` API]({{es-apis}}v9/operation/operation-search) request and [ES|QL query]({{es-apis}}v9/operation/operation-esql-query) search the `logs` resource only on projects that match the `@custom-expression` routing rule.

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
```esql
SET project_routing="@custom-expression";
FROM logs
| STATS COUNT(*)
```
:::

::::

::::{note}
Reference a named expression on its own. You can't combine it with a direct expression or with another named expression. Both of these fail:

* `@aws-us-only OR _csp:gcp` mixes a named expression with a direct expression.
* `@aws-us-only OR @aws-eu-only` combines two named expressions.
::::

### Creating and managing named project routing expressions

You can use the `_project_routing` API to create and manage named project routing expressions.

::::{note}
Named project routing expressions are project-specific. An expression can be used only in the project where it was created.
::::

The following request creates a named expression called `origin-only` that matches a single tag:

```console
PUT _project_routing/origin-only
{
  "expression": "_alias:_origin"
}
```

Expressions can be more complex. The following request creates a named expression called `aws-us-only` that matches AWS projects in a US region:

```console
PUT _project_routing/aws-us-only
{
  "expression": "_csp:aws AND _region:us*"
}
```

You can also create multiple named expressions in a single request:

```console
PUT _project_routing
{
  "aws-us-only": { "expression": "_csp:aws AND _region:us*" },
  "aws-eu-only": { "expression": "_csp:aws AND _region:eu*" },
  "linked-security": { "expression": "_alias:*sec*" }
}
```

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
