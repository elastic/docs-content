---
navigation_title: Scope too broad
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Scope too broad [cps-datafeed-scope-too-broad]

A {{cps}} {{ml}} {{dfeeds}} with flat-world routing (empty `project_routing`) or a broad `_alias:` expression searches every matching linked project on each extraction cycle. As you link more projects, run times increase and the {{anomaly-jobs}} model ingests more data than necessary for your use case.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose scope too broad [diagnose-cps-datafeed-scope-too-broad]

**Symptoms**

* {{dfeeds}} extraction cycles take noticeably longer after new projects were linked.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows searches fanning out to many linked projects you do not need for detection.
* `project_routing` is empty, omitted, or uses a wide wildcard such as `_alias:*` that matches most linked aliases.
* The job was created via API without an explicit routing expression and now searches all linked projects by default.

**Check effective scope**

```console
GET _ml/datafeeds/{datafeed_id}
GET _ml/datafeeds/{datafeed_id}/_stats
GET _remote/info
```

Compare `project_routing` with the number of linked projects in `_remote/info` and the per-project activity in `remote_cluster_stats`.

## Resolve scope too broad [resolve-cps-datafeed-scope-too-broad]

**Narrow `project_routing`**

Close the job, then update routing to include only the projects you need. {{es}} may retain a model snapshot when you change scope with the job closed — use it if detection shifts after narrowing.

Examples:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_origin"
}
```

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

* `_origin` or `_alias:_origin` — local project only.
* `_alias:production-*` — linked projects whose tags match the expression.

See [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) and the [`project_routing` quick reference](/troubleshoot/elasticsearch/machine-learning.md#project_routing-quick-reference).

**Set routing at create time**

When creating {{dfeeds}} through the API, set `project_routing` explicitly instead of relying on flat-world defaults if you do not intend to search all linked projects.

**Verify improvement**

After narrowing scope, compare extraction timing in `_stats` and confirm `remote_cluster_stats` lists only the intended projects.
