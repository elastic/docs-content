---
navigation_title: Bulk migration partial failure
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Bulk migration partial failure [cps-datafeed-bulk-migration-partial]

When you migrate legacy {{ml}} {{anomaly-jobs}} to {{cps}} in {{kib}}, the **Migrate all legacy jobs** action updates each job's {{dfeeds}} in turn. Some jobs may succeed while others fail — for example, because validate-before-mint rejected a search probe or a job owner account is invalid.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose bulk migration partial failure [diagnose-cps-datafeed-bulk-migration-partial]

**Symptoms**

* The bulk migration summary reports a mix of succeeded and failed jobs.
* Some jobs show an **API key error** indicator in the {{anomaly-jobs}} list; others show as migrated.
* Failed jobs still use legacy credentials or lack `project_routing` while succeeded neighbors were updated.

**Identify failed jobs**

Note every `job_id` listed as failed in the migration summary. For each failed job:

1. Open the job in **Machine Learning → Anomaly Detection** and review **Messages** for the API error text.
2. Check `GET _ml/datafeeds/{datafeed_id}` for missing `authorization.cloud_api_key.id` on jobs that should have migrated.

For mint-time errors on individual jobs, see [Cloud token mint failure](cps-datafeed-cloud-token-mint-failure.md). For routing or project-reference failures, see [Routing matches no project](cps-datafeed-routing-no-match.md) and [Stale project reference](cps-datafeed-stale-project-reference.md).

## Resolve bulk migration partial failure [resolve-cps-datafeed-bulk-migration-partial]

**Record failed job ids**

Keep the list of failed `job_id` values from the summary. Bulk migration does not automatically retry failed jobs.

**Retry each job individually**

For each failed job:

1. Fix the underlying error (project link, `project_routing`, ownership, or permissions).
2. Migrate that job alone from the jobs list flyout or run a single-job update:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_origin"
}
```

Adjust `project_routing` to the scope you selected during bulk migration (bulk migration defaults to `_origin` unless you chose another scope).

**Use the single-job migration path**

The per-job migration flyout lets you confirm search scope before retrying. Prefer this over re-running bulk migration for the entire list.

**Verify recovery**

After individual retries, confirm the API key error indicator clears and that `GET _ml/datafeeds/{datafeed_id}` shows the expected `project_routing` and cloud API key id for every previously failed job.
