---
navigation_title: Troubleshoot linked project unavailable
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot linked project unavailable

When a linked project in the {{dfeed}}'s scope is **skipped** during a search cycle, {{es}} fails the entire extraction cycle instead of continuing on the remaining projects. Partial cross-project results could produce spurious anomalies, so the cycle produces no data, the error is audited, and the {{dfeed}} retries on its next scheduled cycle. You see repeated extraction errors in job messages and gaps in results for the affected time buckets until every project in scope is reachable again or you narrow `project_routing`. A hard cluster failure (status `FAILED`, not `SKIPPED`) surfaces through the ordinary search-failure path with different job message text.

## Where to look

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

## Linked project skipped during extraction

### What you see

Skipped or failed linked projects surface in the {{anomaly-job}}'s **Job messages** tab (or `.ml-notifications-*`). The outer audit entry wraps the skip summary as its cause:

```txt
Datafeed is encountering errors extracting data: [1] remote clusters out of [3] were skipped when performing datafeed search
```

The bracketed skip and total counts vary with how many linked projects are in scope. The wrapped text is the message thrown when any linked project is skipped during the search.

Inspect `remote_cluster_stats` using [get datafeed stats]({{es-apis}}operation/operation-ml-get-datafeed-stats).

During an active skip outage, `skipped_clusters` can remain `0` while skip errors repeat in job messages because extraction aborts before stats are updated.

After cycles complete successfully, compare `per_cluster_consecutive_skips` and `availability_ratio` with `project_routing` from `GET _ml/datafeeds/{datafeed_id}` and linked projects from `GET /_project/tags` or the Cloud console.

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

| Pattern | Likely cause |
| --- | --- |
| One {{dfeed}} skips a project that other {{dfeeds}} search successfully. `project_routing` names an unlinked alias or a project that is no longer linked | Configuration: stale or wrong routing |
| Many unrelated {{dfeeds}} skip the **same** linked project at the same time. Cross-project queries fail broadly | Platform outage or regional {{cps}} connectivity degradation |

For routing or stale alias problems, see [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

An internal cloud API key problem can also stop cross-project searches. The distinguishing signal is a credential-specific message in job messages, for example an authentication failure on the internal cloud API key or a forbidden response while using that key, rather than a skip summary. See [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).

### Fix

If the linked project was removed or never linked, re-establish it in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), then wait for the next extraction cycle or restart the {{dfeed}}.

When a project stays unreachable and you need the {{dfeed}} to keep producing results from the remaining scope, narrow `project_routing` to an `_alias:` expression that excludes the unavailable project. Stop the {{dfeed}} and close the {{anomaly-job}} before running this update.

```console
POST _ml/datafeeds/{datafeed_id}/_stop
POST _ml/anomaly_detectors/{job_id}/_close
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

Use an expression that matches only the linked projects you still need. Changing scope can affect the model. See [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md).

When the underlying link or platform issue clears, the {{dfeed}} recovers on the next successful cycle without configuration changes. Job messages might show:

```txt
Datafeed has recovered data extraction and analysis
```

After a long period with no ingested data, you might also see:

```txt
Datafeed has started retrieving data again
```

Each failed extraction cycle leaves a gap in the time series the {{anomaly-job}} analyzes. If a project stays out of scope for an extended period (whether because of outages or because you narrowed routing), the model adapts to the changed data distribution. See [Changing project scope](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) for rollback options.

### Verify

Job messages should stop reporting new extraction errors for the skip cause. After at least one successful completed cycle, `remote_cluster_stats` should show `skipped_clusters` at `0` and no non-zero entries in `per_cluster_consecutive_skips`.

### When to contact support

If many unrelated {{dfeeds}} still skip the same linked project after you confirm the project link and `project_routing` are correct, contact Elastic support with the project id, {{dfeed}} id, and the extraction error message text.
