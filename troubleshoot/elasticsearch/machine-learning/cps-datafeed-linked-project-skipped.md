---
navigation_title: Linked project skipped
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Linked project skipped [cps-datafeed-linked-project-skipped]

When a {{ml}} {{dfeeds}} fans out across linked projects in {{serverless-full}}, unavailable or misconfigured projects are skipped for that search cycle. The {{dfeeds}} continues on remaining scope, but {{anomaly-jobs}} may train on incomplete cross-project data until you restore the missing projects or narrow `project_routing`.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose linked project skipped [diagnose-cps-datafeed-linked-project-skipped]

**Error messages**

Skipped linked projects surface in {{ml}} job **Messages** (Kibana **ML → Anomaly Detection → your job → Messages**, or the `.ml-notifications-*` index). The outer extraction error wraps the skip cause:

```txt
Datafeed is encountering errors extracting data: {0}
```

The inner cause often includes the skip summary:

```txt
[N] remote clusters out of [M] were skipped when performing datafeed search
```

Replace `[N]` and `[M]` with the counts from your message (for example, `[1] remote clusters out of [2] were skipped when performing datafeed search`).

**Check datafeed statistics**

Use the [get datafeed stats API]({{es-apis}}operation/operation-ml-get-datafeed-stats) to see which projects were skipped and how often:

```console
GET _ml/datafeeds/{datafeed_id}/_stats
```

Inspect `remote_cluster_stats` — especially `skippedClusters` and per-cluster consecutive skip counters — and compare them with the datafeed's `project_routing` value from `GET _ml/datafeeds/{datafeed_id}`.

**Distinguish user configuration from platform outage**

| Pattern | Likely cause |
|---------|----------------|
| One {{dfeeds}} skips a project that others reference; `project_routing` names an unlinked alias or a removed project link | User configuration — wrong routing or stale project reference |
| Many unrelated {{dfeeds}} skip the **same** linked project at the same time; cross-project queries fail broadly | Platform outage or regional {{cps}} connectivity degradation |

For routing or reference problems, see [Stale project reference](cps-datafeed-stale-project-reference.md). When linked projects are added or removed and scope stabilizes, see [Search scope changed](cps-datafeed-search-scope-changed.md).

## Resolve linked project skipped [resolve-cps-datafeed-linked-project-skipped]

**Restore the project link**

If the linked project was removed or never linked, re-establish the link in {{ecloud}} project settings, then wait for the next {{dfeeds}} cycle or restart the {{dfeeds}}.

**Fix `project_routing`**

Update the datafeed so routing matches only linked, reachable projects:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:prod-*"
}
```

Use `_origin` or `_alias:_origin` when you need local-only analysis until cross-project access is restored ([{{cps-init}}](/deploy-manage/cross-project-search.md)).

**Verify recovery**

After fixing the link or routing, confirm skips stop:

```console
GET _ml/datafeeds/{datafeed_id}/_stats
```

`remote_cluster_stats` should show the previously skipped projects as available. Check **Messages** for new extraction errors.

If many {{dfeeds}} still skip the same project after your configuration is correct, contact Elastic support with your project id, {{dfeeds}} id, and the skip message text.
