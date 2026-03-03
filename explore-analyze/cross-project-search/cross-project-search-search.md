---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
description: Learn how search expressions, search options, and index resolution work in cross-project search (CPS).
---

# Search in {{cps-init}} [cps-search]

This page explains how search works in {{cps-init}}, including:

* the {{cps-init}} search model
* **unqualified search expressions** (for example, `logs` and `logs*`), **qualified search expressions** (expressions with a project alias prefix, for example `project1:logs`) and how they control search scope
* how search options such as `ignore_unavailable` and `allow_no_indices` behave in {{cps-init}}
* common edge cases and examples involving mixed qualified and unqualified expressions

For an overview of {{cps}} concepts such as origin projects, linked projects, and project aliases, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md).

## {{cps-init}} search model

With {{cps-init}}, searches are resolved across all linked projects by default—not just the origin project.
You explicitly need to limit the scope of your search to override this behavior. Refer to the [Unqualified and qualified search expressions](#search-expressions) section to learn more.
When you refer to a resource (such an index, a data stream, or an alias) by a name, {{cps-init}} resolves that name across the origin project and all of its linked projects.
This means that when you run a search from the origin project and refer to a searchable resource such as `logs`, the search is executed against all resources named `logs` across the origin project and its linked projects, for example:

```console
GET logs/_search
```

For each linked project, the search runs only if a resource named `logs` exists.
If a linked project does not have a `logs` resource, that project is skipped and the search continues without returning an error. No error is returned as long as at least one project has the `logs` resource.

## Unqualified and qualified search expressions [search-expressions]

{{cps-cap}} supports two types of search expressions: unqualified and qualified. The type of search expression determines where a search request runs and how errors are handled.

* **Unqualified search expressions** follow the {{cps}} model and represent the default, native behavior in {{cps-init}}. An unqualified search expression does not include a project alias prefix. In this case, the search runs against the origin project and all its linked projects.
* **Qualified search expressions** explicitly override the default behavior, enabling you to precisely control which projects a search runs on and how errors are handled. It includes additional qualifiers, such as project alias prefixes, that explicitly control the scope of the search.

For example, the following qualified search expression request searches only the origin project:

```console
GET _origin:logs/_search
```

For additional examples of qualified search expressions, refer to the [examples section](/explore-analyze/cross-project-search.md#cps-examples).

::::{tip}
[Project routing expressions](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) provide an additional way for you to control which projects the query is routed to, but they serve a different purpose than qualified search expressions.
While qualified search expressions control scope by explicitly naming projects by their project aliases in the index expression, project routing expressions enable you to route the query to projects dynamically based on other project metadata.
You can use qualified search expressions and project routing expressions together, depending on whether you want to scope searches by explicitly identifying projects or by selecting projects based on shared attributes.
::::

### `ignore_unavailable` and `allow_no_indices`

The distinction between qualified and unqualified search expressions affects how the `ignore_unavailable` and `allow_no_indices` search options are applied in {{cps}}.
When you use an **unqualified** expression, index resolution is performed against the merged project view. In this case, search options are evaluated based on whether the target resources exist in any of the searched projects, not only in the origin project.

Project routing expressions do not affect the behavior of the `ignore_unavailable` or `allow_no_indices` settings.

::::{important}
The way that missing resources are interpreted differs between unqualified and qualified expressions, refer to the [Unqualified expression behavior](#behavior-unqualified) and [Default (non-CPS) and qualified expression behavior](#behavior-default-qualified) sections for a detailed explanation.
::::

#### Default (non-CPS) and qualified expression behavior [behavior-default-qualified]

The following describes the standard {{es}} behavior:

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

When you use a **qualified search expression**, the default behavior of `ignore_unavailable` and `allow_no_indices` outlined above applies independently to each qualified project.

The next section explains how this behavior differs when using unqualified search expressions in {{cps-init}}.

#### Unqualified expression behavior [behavior-unqualified]

When you use an **unqualified search expression**, the behavior is different:

* As long as the targeted resources exist in at least one of the searched projects, the request succeeds, even if `ignore_unavailable` or `allow_no_indices` are set to false.
* The request returns an error only if:
  * the targeted resources are missing from all searched projects, or
  * a search expression explicitly targets a specific project and the resource is missing from that project.

#### Examples

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

Refer to [the examples section](/explore-analyze/cross-project-search.md#cps-examples) for more.

## Dot-prefixed and system indices

Indices with names that start with a dot (`.`) but are not system indices behave the same as other non-system indices in {{cps-init}}. They are resolved across the origin project and all linked projects according to the unqualified and qualified expression rules.

System indices are not accessible through {{cps}} or local search.
