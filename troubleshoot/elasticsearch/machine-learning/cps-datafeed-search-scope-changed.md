---
navigation_title: Search scope changed
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Search scope changed [cps-datafeed-search-scope-changed]

When linked projects are added or removed, a {{cps}} {{ml}} {{dfeeds}} may search a different set of projects than when the {{anomaly-jobs}} model was trained. {{es}} records scope changes after they stabilize across several extraction cycles. Temporary anomalies are expected while the model adapts to the new data distribution.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose search scope changed [diagnose-cps-datafeed-search-scope-changed]

**Error messages**

Scope changes appear in {{ml}} job **Messages** ({{kib}} **Machine Learning → Anomaly Detection → your job → Messages**, or the `.ml-notifications-*` index). When a project is newly linked, you may see:

```txt
Datafeed search scope changed: [project] linked. Data distribution may have changed due to new data sources, which can cause temporary anomalies while the model adapts. If detection quality degrades, consider specifying the source clusters explicitly and reviewing recent model snapshots for potential rollback.
```

When a project is unlinked, you may see:

```txt
Datafeed search scope changed: [project] unlinked. Data distribution may have changed due to removed data sources, which can cause temporary anomalies as patterns the model learned are no longer present. If detection quality degrades, consider specifying the source clusters explicitly and reviewing recent model snapshots for potential rollback.
```

Replace `[project]` with the linked project alias from your message.

**Check annotations**

{{es}} also writes `SEARCH_SCOPE_CHANGED` annotations to `.ml-annotations-*` for the job id. Search that index for the job id and annotation type `search_scope_changed` to see when scope stabilized and which projects changed.

**Check datafeed statistics**

Use the [get datafeed stats API]({{es-apis}}operation/operation-ml-get-datafeed-stats) to compare linked-project visibility over recent cycles:

```console
GET _ml/datafeeds/{datafeed_id}/_stats
```

Inspect `remote_cluster_stats` together with `project_routing` from `GET _ml/datafeeds/{datafeed_id}` to confirm whether the effective search scope matches your intent.

## Resolve search scope changed [resolve-cps-datafeed-search-scope-changed]

**Restore or narrow the project link**

If the scope change was unintentional, re-establish the project link in {{ecloud}} project settings, or update `project_routing` so the {{dfeeds}} searches only the projects you want:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

Use `_origin` or `_alias:_origin` for local-only analysis. For syntax details, see [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

**Roll back the model if detection quality degrades**

If anomalies persist after the scope change and are not meaningful, revert to a model snapshot taken before the change:

1. Close the job.
2. In {{kib}}, open **Machine Learning → Anomaly Detection → your job → Model snapshots**, select a snapshot from before the scope change, and revert.
3. Restart the {{dfeeds}} after confirming `project_routing` matches your intended scope.

If you deliberately widened scope, {{es}} may retain a snapshot automatically when you update `project_routing` with the job closed — use that retained snapshot for rollback.

**Verify recovery**

After fixing the link or routing, confirm new `SEARCH_SCOPE_CHANGED` annotations stop appearing and that **Messages** no longer report scope-change warnings on every cycle.
