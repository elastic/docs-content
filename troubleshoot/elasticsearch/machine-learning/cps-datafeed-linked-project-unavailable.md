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

Inspect `remote_cluster_stats` via [get datafeed stats]({{es-apis}}operation/operation-ml-get-datafeed-stats). It reflects the **last completed extraction cycle**, not a cycle still in progress or one that failed mid-extraction.

During an active skip outage, **Job messages** are the authoritative signal. Extraction aborts when a project is skipped, before stats are updated, so `skipped_clusters` can remain `0` while skip errors repeat in **Job messages**.

After cycles complete successfully, these fields help track recovery:

* `skipped_clusters`: linked projects skipped in the last completed cycle.
* `per_cluster_consecutive_skips`: consecutive skip/fail counts per alias from completed cycles. Resets to `0` when a cycle completes with that project available.
* `availability_ratio`: `available_clusters` divided by `total_clusters` for the last completed cycle (also see `total_clusters` and `available_clusters`).

Example excerpt (field names and structure match the stats API, values vary):

```json
"remote_cluster_stats": {
  "total_clusters": 3,
  "available_clusters": 3,
  "skipped_clusters": 0,
  "availability_ratio": 1.0,
  "stabilized_cluster_aliases": ["origin", "production", "staging"],
  "per_cluster_consecutive_skips": {}
}
```

Compare `per_cluster_consecutive_skips` with `project_routing` from `GET _ml/datafeeds/{datafeed_id}` and linked projects from `GET /_project/tags` or the Cloud console.

**Distinguish configuration from an outage**

| Pattern | Likely cause |
| --- | --- |
| One {{dfeed}} skips a project that other {{dfeeds}} search successfully. `project_routing` names an unlinked alias or a project that is no longer linked | Configuration: stale or wrong routing |
| Many unrelated {{dfeeds}} skip the **same** linked project at the same time. Cross-project queries fail broadly | Platform outage or regional {{cps}} connectivity degradation |

For routing or stale alias problems, see [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

**Rule out an authorization failure**

An internal cloud credential problem can also stop cross-project searches. The distinguishing signal is a credential-specific message in **Job messages**, for example an authentication failure on the internal cloud API key or a forbidden response while using that key, rather than the skip summary above. See [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).

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

Use an expression that matches only the linked projects you still need. Changing scope can affect the model. See [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md).

**Wait out a transient outage**

When the underlying link or platform issue clears, the {{dfeed}} recovers on the next successful cycle without configuration changes. **Job messages** might show:

```txt
Datafeed has recovered data extraction and analysis
```

After a long period with no ingested data, you might also see:

```txt
Datafeed has started retrieving data again
```

**Consider the model impact**

Each failed extraction cycle leaves a gap in the time series the {{anomaly-job}} analyzes. If a project stays out of scope for an extended period (whether because of outages or because you narrowed routing), the model adapts to the changed data distribution. See [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) for rollback options.

**Verify**

**Job messages** should stop reporting new extraction errors for the skip cause. After at least one successful completed cycle, `remote_cluster_stats` should show `skipped_clusters` at `0` and no non-zero entries in `per_cluster_consecutive_skips`.

**When to contact support**

If many unrelated {{dfeeds}} still skip the same linked project after you confirm the project link and `project_routing` are correct, contact Elastic support with the project id, {{dfeed}} id, and the extraction error message text.
