---
navigation_title: Linked project unavailable
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Linked project unavailable [cps-datafeed-linked-project-unavailable]

When a linked project in the {{dfeed}}'s scope is skipped or fails during a search cycle, {{es}} fails the entire extraction cycle instead of continuing on the remaining projects. Partial cross-project results could produce spurious anomalies, so the cycle produces no data, the error is audited, and the {{dfeed}} retries on its next scheduled cycle. You see repeated extraction errors in **Job messages** and gaps in results for the affected time buckets until every project in scope is reachable again or you narrow `project_routing`.

## Diagnose linked project unavailable [diagnose-cps-datafeed-linked-project-unavailable]

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

**Error messages**

Skipped or failed linked projects surface in the {{anomaly-job}}'s **Job messages** tab (or `.ml-notifications-*`). The outer audit entry wraps the skip summary as its cause:

```txt
Datafeed is encountering errors extracting data: [1] remote clusters out of [3] were skipped when performing datafeed search
```

The bracketed skip and total counts vary with how many linked projects are in scope. The wrapped text is the message thrown when any linked project is skipped during the search.

**Read the per-project statistics**

Use [get datafeed stats]({{es-apis}}operation/operation-ml-get-datafeed-stats) to inspect `remote_cluster_stats` from the latest extraction cycles:

```console
GET _ml/datafeeds/{datafeed_id}/_stats
```

The fields that matter for this problem:

* `skipped_clusters` — how many linked projects were skipped or unavailable in the last recorded cycle.
* `per_cluster_consecutive_skips` — a map from project alias to the number of consecutive cycles that project has been skipped or failed; resets to `0` when the project becomes available again.
* `availability_ratio` — `available_clusters` divided by `total_clusters` for the last cycle (also see `total_clusters` and `available_clusters`).

Example excerpt (field names and structure match the stats API; values vary):

```json
"remote_cluster_stats": {
  "total_clusters": 3,
  "available_clusters": 2,
  "skipped_clusters": 1,
  "availability_ratio": 0.6666666666666666,
  "stabilized_cluster_aliases": ["origin", "production"],
  "per_cluster_consecutive_skips": {
    "staging": 4
  }
}
```

Compare `per_cluster_consecutive_skips` with `project_routing` from `GET _ml/datafeeds/{datafeed_id}` and linked projects from `GET /_project/tags` or the Cloud console.

**Distinguish configuration from an outage**

| Pattern | Likely cause |
| --- | --- |
| One {{dfeed}} skips a project that other {{dfeeds}} search successfully; `project_routing` names an unlinked alias or a project that is no longer linked | Configuration — stale or wrong routing |
| Many unrelated {{dfeeds}} skip the **same** linked project at the same time; cross-project queries fail broadly | Platform outage or regional {{cps}} connectivity degradation |

For routing or stale alias problems, see [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

**Rule out an authorization failure**

An internal cloud credential problem can also stop cross-project searches. The distinguishing signal is a credential-specific message in **Job messages** — for example an authentication failure on the internal cloud API key or a forbidden response while using that key — rather than the skip summary above. See [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).

## Resolve linked project unavailable [resolve-cps-datafeed-linked-project-unavailable]

**Restore the project link**

If the linked project was removed or never linked, re-establish it in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), then wait for the next extraction cycle or restart the {{dfeed}}.

**Remove the unavailable project from scope**

When a project stays unreachable and you need the {{dfeed}} to keep producing results from the remaining scope, narrow `project_routing` to an `_alias:` expression that excludes the unavailable project:

:::{include} /troubleshoot/_snippets/cps-ml-update-preconditions.md
:::

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

Use an expression that matches only the linked projects you still need. Changing scope can affect the model; see [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md).

**Wait out a transient outage**

When the underlying link or platform issue clears, `per_cluster_consecutive_skips` for that alias returns to `0` on the next successful cycle and the {{dfeed}} recovers without configuration changes. **Job messages** may show:

```txt
Datafeed has recovered data extraction and analysis
```

After a long period with no ingested data, you may also see:

```txt
Datafeed has started retrieving data again
```

**Consider the model impact**

Each failed extraction cycle leaves a gap in the time series the {{anomaly-job}} analyzes. If a project stays out of scope for an extended period — whether because of outages or because you narrowed routing — the model adapts to the changed data distribution. See [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) for rollback options.

**Verify**

`GET _ml/datafeeds/{datafeed_id}/_stats` should show `skipped_clusters` at `0`, no non-zero entries in `per_cluster_consecutive_skips`, and **Job messages** should stop reporting new extraction errors for the skip cause.

**When to contact support**

If many unrelated {{dfeeds}} still skip the same linked project after you confirm the project link and `project_routing` are correct, contact Elastic support with the project id, {{dfeed}} id, and the extraction error message text.
