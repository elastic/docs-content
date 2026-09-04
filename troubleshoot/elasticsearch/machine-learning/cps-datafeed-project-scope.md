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

The `project_routing` field decides which linked projects a {{cps}} {{dfeed}} searches. This page covers routing that matches nothing, routing that matches too many projects, references to projects that no longer exist under an alias, and display counts that do not match the projects you expect.

Common symptoms include no results or origin-only results, slower extraction after linking projects, and job messages that reference a project alias that no longer exists.

## Where to look

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

### Check the effective scope in {{kib}}

Open **Machine Learning → Anomaly Detection** and review the **Project scope** column. Each cell shows a parsed count out of the total project count (origin plus linked projects). For example, `2/5` means the expression targets 2 projects out of 5 available.

The parsed count comes from the routing expression text, not from which aliases match at runtime. Select the value in the **Project scope** column to see the expression stored on the {{dfeed}}.

A single wildcard expression like `_alias:production-*` shows `1`, even if it matches several linked projects at runtime.

When the parsed count is lower than the number of projects named in the expression, your user might lack permission to view one or more linked projects. The column reflects what you can see, not every alias the expression could match.

## Routing matches no project

### What you see

During create, update, or extraction, job messages or the API can report one of these {{ml}}-enriched errors.

On create or update:

Create failures use the same *Cannot update datafeed* wording even though the request is a put.

```txt
Cannot update datafeed [my-datafeed]: project_routing [_alias:nonexistent-*] matched no linked project (no matching project after applying project routing [_alias:nonexistent-*]). Link the missing project in Elastic Cloud project settings, or update project_routing to a valid linked alias (for example _origin for local-only scope).
```

During extraction or preview:

```txt
Datafeed [my-datafeed] cannot search any project: project_routing [_alias:nonexistent-*] matched no linked projects at run time (no matching project after applying project routing [_alias:nonexistent-*]). Link the missing project(s) in Elastic Cloud project settings, or update project_routing to an expression that matches at least one linked project (for example _origin for local-only scope).
```

The bracketed datafeed id, routing expression, and parenthesized cause vary with your configuration. The parenthesized text comes from {{es}} itself, typically in one of these forms:

```txt
no matching project after applying project routing [_alias:nonexistent-*]
```

```txt
No such project: [missing-project] with project routing [_alias:production-*]
```

The suggested `_origin` example in the {{ml}} messages is not a valid routing value. Use `_alias:_origin` for origin-project-only scope instead. See [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

| Situation | Typical behavior |
| --- | --- |
| {{dfeed}} with empty `project_routing` and unqualified index patterns, with no linked projects | Create or update can succeed. The first run-time search fails |
| {{dfeed}} with unqualified index patterns and a `_alias:` expression that matches no linked tags, including typos | Create or update can succeed. The first run-time search fails |
| {{dfeed}} with qualified `project:index` patterns and `project_routing` that matches no linked tags | Fails immediately on create or update |
| Qualified `project:index` references a project that does not exist or is unauthorized | Fails immediately on create or update |

A `project_routing` value that matches nothing is deferred to run time only when every entry in `indices` is unqualified. Any qualified `project:index` pattern, including one whose project alias is missing, fails immediately on create or update.

### Fix

Update routing to a valid `_alias:` expression, or link the missing project in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md). For step-by-step guidance on setting scope in {{kib}} or through the API, see [Change the project scope of an anomaly detection job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md).
% TODO: link to ml-ad-run-jobs.md#ml-ad-cps-update when PR #7814 merges

### Verify

* The **Project scope** column shows the intended parsed/total count and popover expression.
* `GET _ml/datafeeds/{datafeed_id}` returns the expected `project_routing` value.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles.

## Scope is wider than intended

### What you see

* {{dfeed}} extraction cycles take noticeably longer after new projects were linked.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows `remote_cluster_stats` fanning out to many linked projects you do not need.

### Fix

Narrow `project_routing` to the projects you need. See [Change the project scope of an anomaly detection job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) for how to set **Project scope** in {{kib}} or update routing through the API. Before you change scope, review [Before you update](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md#before-you-update).
% TODO: link to ml-ad-run-jobs.md#ml-ad-cps-update when PR #7814 merges

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

When `indices` contains a qualified `project:index` pattern, update both `project_routing` and the qualified index reference after a rename or unlink. See [Change the project scope of an anomaly detection job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md).
% TODO: link to ml-ad-run-jobs.md#ml-ad-cps-update when PR #7814 merges

Changing `indices` also changes the cross-project search surface, which can re-key the internal cloud API key. See [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).

If the project should still be in scope, re-establish the link in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md).

### Verify

* `GET _ml/datafeeds/{datafeed_id}` returns updated `project_routing` and `indices` values.
* Job messages no longer reference the stale alias.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles.
