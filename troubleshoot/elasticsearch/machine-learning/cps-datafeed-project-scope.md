---
navigation_title: Troubleshoot datafeed project scope
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot anomaly detection datafeed project scope

The `project_routing` field decides which linked projects a {{cps}} {{dfeed}} searches. This page covers routing that matches nothing, routing that matches too many projects, references to projects that no longer exist under an alias, and copies that inherit the source {{anomaly-job}}'s scope.

## Before you update

:::{include} /troubleshoot/_snippets/cps-ml-update-preconditions.md
:::

## Where to look

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

### Check the effective scope in {{kib}}

Open **Machine Learning > Anomaly Detection** and review the **Project scope** column. Each cell shows a parsed count out of the total project count (origin plus linked projects). For example, `2/5` means the expression targets 2 projects out of 5 available.

The parsed count comes from the routing expression text, not from resolving which aliases actually match at runtime:

* Omitted or `null` routing shows `1` (origin only).
* `_alias:*` shows the full origin-plus-linked total.
* `_alias:_origin` shows `1`.
* A single wildcard expression like `_alias:production-*` shows `1`, even if it matches several linked projects at runtime.

Select the count to open a popover that displays the routing expression stored on the {{dfeed}}. A legacy job with no stored routing shows `_alias:_origin` in the popover.

## Routing matches no project

### What you see

During create, update, or extraction, job messages or the API can report one of these {{ml}}-enriched errors.

On create or update (validate-before-mint):

Create failures use the same *Cannot update datafeed* wording even though the request is a put.

```txt
Cannot update datafeed [my-datafeed]: project_routing [_alias:nonexistent-*] matched no linked project (no matching project after applying project routing [_alias:nonexistent-*]). Link the missing project in Elastic Cloud project settings, or update project_routing to a valid linked alias (for example _origin for local-only scope).
```

During extraction or preview:

```txt
Datafeed [my-datafeed] cannot search any project: project_routing [_alias:nonexistent-*] matched no linked projects at run time (no matching project after applying project routing [_alias:nonexistent-*]). Link the missing project(s) in Elastic Cloud project settings, or update project_routing to an expression that matches at least one linked project (for example _origin for local-only scope).
```

The bracketed datafeed id, routing expression, and parenthesised cause vary with your configuration. The parenthesised text comes from {{es}} itself, typically in one of these forms:

```txt
no matching project after applying project routing [_alias:nonexistent-*]
```

```txt
No such project: [missing-project] with project routing [_alias:production-*]
```

The suggested `_origin` example in the {{ml}} messages is not a valid routing value. Use `_alias:_origin` for origin-project-only scope instead. See [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

| Situation | Typical behavior |
| --- | --- |
| Flat-world {{dfeed}} (empty `project_routing`, unqualified index patterns) with no linked projects | Create or update can succeed. The first run-time search fails |
| Flat-world {{dfeed}} (unqualified index patterns) with `_alias:` expression that matches no linked tags, including typos | Create or update can succeed. The first run-time search fails |
| {{dfeed}} with qualified `project:index` patterns and `project_routing` that matches no linked tags | Fails immediately on create or update (validate-before-mint) |
| Qualified `project:index` references a project that does not exist or is unauthorized | Fails immediately on create or update |

Validate-before-mint defers a no-match `project_routing` to run time only when every entry in `indices` is unqualified (flat-world). Any qualified `project:index` pattern, including one whose project alias is missing, fails immediately on create or update.

### Fix

Update routing to a valid `_alias:` expression:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

If routing references a project that should be in scope, establish the link in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), then update routing or wait for the next extraction cycle.

### Verify

* The **Project scope** column shows the intended parsed/total count and popover expression.
* `GET _ml/datafeeds/{datafeed_id}` returns the expected `project_routing` value.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles.

## Scope is wider than intended

### What you see

* {{dfeed}} extraction cycles take noticeably longer after new projects were linked.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows `remote_cluster_stats` fanning out to many linked projects you do not need.
* `project_routing` is empty, omitted, or uses a wide expression such as `_alias:*` that matches most linked aliases.
* The {{anomaly-job}} was created without an explicit routing expression and now searches all linked projects by default.

### Fix

When you only need data from the local project, set origin-project-only routing:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:_origin"
}
```

To search a subset of linked projects, update routing to a narrower `_alias:` expression:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

### Verify

* The **Project scope** column shows the intended parsed/total count and popover expression.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows `remote_cluster_stats` listing only the intended projects.
* Extraction cycle duration returns to expected levels.

## Stale project reference

### What you see

* Job messages or extraction errors reference a project alias that no longer appears in `GET /_project/tags` or the Cloud console linked-project list.
* `project_routing` still contains an `_alias:` tag that matched a project before it was renamed or unlinked.
* A qualified index pattern such as `old-alias:logs-*` names a project alias that is no longer linked.

### Fix

When `indices` contains a qualified `project:index` pattern, update both `project_routing` and the qualified index reference after a rename or unlink:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*",
  "indices": ["new-alias:logs-*"]
}
```

Changing `indices` also changes the cross-project search surface, which can re-key the internal cloud API key. See [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).

If the project should still be in scope, re-establish the link in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md).

### Verify

* `GET _ml/datafeeds/{datafeed_id}` returns updated `project_routing` and `indices` values.
* Job messages no longer reference the stale alias.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles.

## Cloned job inherits wrong scope

### What you see

* A copied {{anomaly-job}} searches more linked projects than intended.
* `GET _ml/datafeeds/{datafeed_id}` on the copy shows the same `project_routing` as the source {{dfeed}}.
* Job creation reuses the wizard, which copies the source {{dfeed}} configuration (including `project_routing`) into the new job before you confirm create.

### Fix

When creating or copying a job in {{kib}}, set **Project scope** before you finish the wizard:

* On **Select data view or saved Discover session**, use the **Project scope** control to pick routing before you choose the data source.
* On later wizard steps (including the datafeed step), the **Project scope** section shows the label **Project scope** with the description *Select the project routing for the job.* Adjust routing there if the copy inherited a broader scope than you need.

To fix an existing job, update `project_routing` through the API:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:_origin"
}
```

### Verify

* The **Project scope** column shows the intended parsed/total count and popover expression.
* `GET _ml/datafeeds/{datafeed_id}` returns the expected `project_routing` value.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows `remote_cluster_stats` listing only the intended projects.
