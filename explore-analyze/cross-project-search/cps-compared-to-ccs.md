---
applies_to:
  stack: ga
  serverless: preview
products:
  - id: elasticsearch
description: Compare cross-project search (CPS) and cross-cluster search (CCS) syntax, behavior, and query patterns to help you transition from CCS to CPS.
navigation_title: "Compare with CCS"
---

# {{cps-cap}} compared to {{ccs}}

{{cps-cap}} (CPS) provides {{serverless-full}} with cross-project search capabilities similar to [{{ccs}}](/explore-analyze/cross-cluster-search.md) (CCS). 

Both features let you search data across multiple deployments from a single request, but the query syntax, default scope, and configuration requirements are different.

This page highlights the key differences and shows side-by-side query examples to help you transition from CCS to CPS.

## Key differences

The following sections describe how CCS and CPS differ in availability, setup, query syntax, and scope behavior.

**Availability**
:   CCS is for {{es}} clusters on self-managed, {{ece}}, {{eck}}, and {{ech}} deployments. CPS is for {{serverless-full}} projects. Use CCS when searching across clusters and CPS when searching across serverless projects.

**Prerequisites and configuration**
:   CCS requires remote cluster connectivity and security configuration across clusters. CPS only requires project linking in the {{ecloud}} UI, with no transport-layer setup. For details, refer to [CCS prerequisites](/explore-analyze/cross-cluster-search.md#_prerequisites) and [CPS prerequisites](/deploy-manage/cross-project-search-config.md#cps-prerequisites).

**Cross-environment support**
:   CCS can connect clusters across organizations and infrastructure boundaries. CPS is limited to projects within the same {{ecloud}} organization.

**Default search scope**
:   In CCS, a query runs against the **local cluster only** unless you explicitly include remote clusters. In CPS, a query runs against the **origin project and all linked projects** by default, so you don't need to rewrite queries as you link additional projects.

**Naming**
:   CCS uses **remote cluster names** as prefixes. CPS uses **project aliases**. Project aliases are derived from the project's [connection alias](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-connection-aliases), while remote cluster names come from the cluster settings configuration.

**Referencing the local cluster or origin project**
:   In CCS, the local cluster appears as `(local)` in search responses and has no explicit prefix in query expressions. If no prefix is provided, the query runs against the local cluster only. In CPS, the origin project appears as `_origin` in responses and can be targeted with the `_origin:` prefix in query expressions.

**Missing resources**
:   In CCS, searching for an index that doesn't exist on a cluster returns an error unless `ignore_unavailable` is set to `true`. In CPS, unqualified expressions succeed as long as the target resource exists in at least one searched project. Projects that don't have the resource are silently skipped, which means queries work without error even when projects have different index sets. Qualified expressions behave like CCS: if you target a specific project and the resource is missing, the request returns an error. For details, refer to [Search in CPS](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions).

**Selecting which clusters or projects to search**
:   In CCS, you select which clusters to search by listing cluster names or using wildcards on cluster names in the index expression. CPS introduces [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md), which selects projects based on project metadata, including project aliases, cloud provider, region, and custom tags. Project routing supports boolean logic (`AND`, `OR`, `NOT`), grouping with parentheses, and reusable [named expressions](/explore-analyze/cross-project-search/cross-project-search-project-routing.md#named-routing-expressions). Routing is evaluated before the query runs, so excluded projects are never searched. CPS also provides a [scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in {{kib}} apps for controlling which projects are searched without modifying queries.

## Syntax comparison quick reference

The following tables summarize how common search tasks translate between CCS and CPS for Query DSL and ES|QL. The CCS examples assume a local cluster with a remote cluster named cluster_one. The CPS examples assume an origin project with a linked project whose alias is linked_project.

For full examples, refer to the [examples](#examples) section.

### `_search`


| Task | CCS | CPS |
|---|---|---|
| [Search local/origin only](#ex-local-origin) | `GET my-index/_search` | `GET _origin:my-index/_search` |
| [Search one remote/linked](#ex-one-remote) | `GET cluster_one:my-index/_search` | `GET linked_project:my-index/_search` |
| [Search all](#ex-search-all) | `GET my-index,*:my-index/_search` | `GET my-index/_search` (default) |
| [Exclude one](#ex-exclude) | `GET my-index,*:my-index,-cluster_one:*/_search` | `GET my-index,-linked_project:*/_search` |
| [Route by metadata](#ex-route-tags) | Not available | `project_routing` |
| [Identify origin in responses](#ex-identify-origin) | `(local)` in `_clusters`; no prefix in `_index` | `_origin` in `_clusters`; no prefix in `_index` |
| [Identify remote/linked in responses](#ex-identify-origin) | `cluster_one:my-index` in `_index` | `linked_project:my-index` in `_index` |

### ES|QL

| Task | CCS | CPS |
|---|---|---|
| [Search local/origin only](#ex-local-origin) | `FROM my-index` | `FROM _origin:my-index` |
| [Search one remote/linked](#ex-one-remote) | `FROM cluster_one:my-index` | `FROM linked_project:my-index` |
| [Search all](#ex-search-all) | `FROM my-index,cluster_one:my-index` | `FROM my-index` (default) |
| [Exclude one](#ex-exclude) | `FROM my-index,*:my-index,-cluster_one:*` | `FROM my-index,-linked_project:*` |
| [Route by metadata](#ex-route-tags) | Not available | `SET project_routing` |
| [Identify origin in responses](#ex-identify-origin) | No prefix in `METADATA _index` | No prefix in `METADATA _index` |
| [Identify remote/linked in responses](#ex-identify-origin) | `cluster_one:my-index` in `METADATA _index` | `linked_project:my-index` in `METADATA _index` |

## Examples

The following examples compare equivalent tasks in CCS and CPS. The CCS examples assume a local cluster with a remote cluster named `cluster_one`. The CPS examples assume an origin project with a linked project whose alias is `linked_project`.

### Search the local cluster or origin project only [ex-local-origin]

Restrict a query to a single cluster or project without including results from remote clusters or linked projects. Use this when you need to isolate results to one cluster or project, for example when debugging a local issue.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
In CCS, a plain index name targets the local cluster only. No prefix is needed.

**`_search`**
```console
GET my-index/_search
```

**ES|QL**
```esql
FROM my-index
| LIMIT 10
```
:::

:::{tab-item} CPS
:sync: cps
In CPS, a plain index name searches all projects. To restrict to the origin project, use the `_origin:` prefix.

**`_search`**
```console
GET _origin:my-index/_search
```

**ES|QL**
```esql
FROM _origin:my-index
| LIMIT 10
```
:::

::::

### Search one remote cluster or linked project [ex-one-remote]

Target a specific remote cluster or linked project. Use this when you want to check data from a single cluster or project without pulling in results from others.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
Prefix the index with the remote cluster name.

**`_search`**
```console
GET cluster_one:my-index/_search
```

**ES|QL**
```esql
FROM cluster_one:my-index
| LIMIT 10
```
:::

:::{tab-item} CPS
:sync: cps
Prefix the index with the linked project alias.

**`_search`**
```console
GET linked_project:my-index/_search
```

**ES|QL**
```esql
FROM linked_project:my-index
| LIMIT 10
```
:::

::::

### Search local and all remotes, or all projects [ex-search-all]

Search an index across every available cluster or project at once. Use this when you want to correlate data from all clusters or projects, for example during an incident investigation that spans multiple clusters or projects.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
List the local index and each remote cluster explicitly, or use a wildcard for remote clusters.

**`_search`**
```console
GET my-index,cluster_one:my-index/_search
```

Or, using a wildcard to include all remote clusters:
```console
GET my-index,*:my-index/_search
```

**ES|QL**

List each cluster explicitly in the `FROM` command.
```esql
FROM my-index,cluster_one:my-index
| LIMIT 10
```
:::

:::{tab-item} CPS
:sync: cps
Use the index name with no prefix. All linked projects are searched by default.

**`_search`**
```console
GET my-index/_search
```

**ES|QL**
```esql
FROM my-index
| LIMIT 10
```
:::

::::

### Exclude clusters or projects [ex-exclude]

Search broadly but skip one or more clusters or projects. Use this when you need results from most clusters or projects but want to leave some out, for example to exclude development or staging projects. In CPS, because all projects are searched by default, you only need to specify what to skip.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
Prefix the cluster name with `-` and use `*` in the index position. You can chain multiple exclusions.

**`_search`**
```console
GET my-index,*:my-index,-cluster_one:*,-cluster_two:*/_search
```

**ES|QL**
```esql
FROM my-index,*:my-index,-cluster_one:*,-cluster_two:*
| LIMIT 10
```
:::

:::{tab-item} CPS
:sync: cps
Use the same `-` prefix with the project alias. An exclusion pattern requires a preceding inclusion pattern. You can exclude multiple projects.

**`_search`**
```console
GET my-index,-linked_project:*,-staging_project:*/_search
```

**ES|QL**
```esql
FROM my-index,-linked_project:*,-staging_project:*
| LIMIT 10
```
:::

::::

### Identify where a document came from [ex-identify-origin]

Determine which cluster or project returned a specific document. Use this when you want to trace a result back to its source when searching across multiple clusters or projects.

In both CCS and CPS, the `_index` field in the response indicates where each document originated.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
Documents from a remote cluster include the cluster name as a prefix: `cluster_one:my-index`. Documents from the local cluster have no prefix: `my-index`.

**`_search`**
```console
GET my-index,cluster_one:my-index/_search
```

Example response:
```json
{
  "hits": {
    "hits": [
      { "_index": "my-index", "_id": "1", "_source": { "message": "local doc" } },
      { "_index": "cluster_one:my-index", "_id": "2", "_source": { "message": "remote doc" } }
    ]
  },
  ...
}
```

**ES|QL**

Use `METADATA _index` to include the field:
```esql
FROM my-index,cluster_one:my-index METADATA _index
| KEEP _index, message
| LIMIT 10
```

Example results:

```json
{
  "columns": [
    { "name": "_index", "type": "keyword" },
    { "name": "message", "type": "keyword" }
  ],
  "values": [
    [ "my-index", "local doc" ],
    [ "cluster_one:my-index", "remote doc" ]
  ]
}
```

:::

:::{tab-item} CPS
:sync: cps
Documents from a linked project include the project alias as a prefix: `linked_project:my-index`. Documents from the origin project have no prefix: `my-index`.

**`_search`**
```console
GET my-index/_search
```

Example response:
```json
{
  "hits": {
    "hits": [
      { "_index": "my-index", "_id": "1", "_source": { "message": "origin doc" } },
      { "_index": "linked_project:my-index", "_id": "2", "_source": { "message": "linked doc" } }
    ]
  },
  ...
}
```

**ES|QL**

Use `METADATA _index` to include the field:
```esql
FROM my-index METADATA _index
| KEEP _index, message
| LIMIT 10
```

Example results:

```json
{
  "columns": [
    { "name": "_index", "type": "keyword" },
    { "name": "message", "type": "keyword" }
  ],
  "values": [
    [ "my-index", "origin doc" ],
    [ "linked_project:my-index", "linked doc" ]
  ]
}
```

You can also use [project tags](/explore-analyze/cross-project-search/cross-project-search-tags.md#tag-queries) like `_project._alias` in `METADATA` (ES|QL) or `fields` (`_search`) to identify the source project directly, without parsing the `_index` prefix.

:::

::::

### Route by metadata [ex-route-tags]

Route a query to a subset of projects based on project metadata like cloud provider, region, or custom tags, rather than using the index expression alone. This capability is new in CPS and has no CCS equivalent.

::::{tab-set}
:group: ccs-cps

:::{tab-item} CCS
:sync: ccs
In CCS, you select clusters by naming them in the index expression. You can't route queries based on cluster metadata.

**`_search`**
```console
GET cluster_one:logs-*,cluster_two:logs-*/_search
```

**ES|QL**
```esql
FROM cluster_one:logs-*,cluster_two:logs-*
| STATS COUNT(*) BY service.name
```
:::

:::{tab-item} CPS
:sync: cps
In CPS, use [`project_routing`](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) to select projects dynamically. Project routing supports boolean logic (`AND`, `OR`, `NOT`) and wildcards.

**`_search`**
```console
GET logs-*/_search
{
  "project_routing": "_csp:aws AND _region:us*"
}
```

**ES|QL**
```esql
SET project_routing="_csp:aws AND _region:us*";
FROM logs-*
| STATS COUNT(*) BY service.name
```

You can also define reusable [named expressions](/explore-analyze/cross-project-search/cross-project-search-project-routing.md#named-routing-expressions) and reference them with the `@` prefix:

**`_search`**
```console
GET logs-*/_search
{
  "project_routing": "@us-aws"
}
```

**ES|QL**
```esql
SET project_routing="@us-aws";
FROM logs-*
| STATS COUNT(*) BY service.name
```
:::

::::