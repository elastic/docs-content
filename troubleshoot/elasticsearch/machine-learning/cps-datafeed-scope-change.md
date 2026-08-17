---
navigation_title: Troubleshoot project scope changes
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot project scope changes

Changing `project_routing` (the **Project scope** field in {{kib}}) decides which linked projects a {{cps}} {{dfeed}} searches. This page covers three related problems: {{es}} or {{kib}} rejects the change, a bulk update succeeds for some jobs but not others, or the change took effect and the {{anomaly-job}} model is reacting to a different data set.

## Before you update

:::{include} /troubleshoot/_snippets/cps-ml-update-preconditions.md
:::

## Where to look

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

## Scope change rejected

### What you see

The most common rejection is an open {{anomaly-job}}. Changing `project_routing` to a new effective scope requires a closed job so {{es}} can retain the current model snapshot as a rollback point.

From the API, a rejected update returns HTTP `409` (datafeed still running or job still open) or `400` (no model snapshot). The response body repeats the messages shown in the preconditions block above.

From {{kib}}, the bulk **Change project scope** action (multi-select jobs list) opens the flyout titled **Update project routing for *N* anomaly detection jobs**.

The bulk update stops and restarts a running {{dfeed}} for you, but it does **not** close the {{anomaly-job}}. Because a `project_routing` change requires a closed job, open jobs fail the bulk update even though their {{dfeed}} was stopped automatically. Close those jobs first, then run the update again.

The single-job path has the same datafeed gate: open **Machine Learning → Anomaly Detection**, edit the job, open the **Datafeed** tab, and adjust **Project scope**. While the {{dfeed}} is running, the tab shows:

```txt
Datafeed settings cannot be edited while the datafeed is running. Please stop the job if you wish to edit these settings.
```

### Fix

| Entry point | Fix |
| --- | --- |
| API update | Stop the {{dfeed}}, close the {{anomaly-job}}, confirm a model snapshot exists, then retry `POST _ml/datafeeds/{datafeed_id}/_update`. |
| {{kib}} bulk **Change project scope** | Close every open job in the selection (the bulk action does not close jobs for you), then re-run the update. |
| {{kib}} single-job **Datafeed** tab | Stop the {{dfeed}} so **Project scope** becomes editable, close the job if you are changing to a new effective scope, then save. |

For routing expressions that match no project or reference stale aliases, see [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

### Verify

The update succeeds without HTTP `409` or `400`. `GET _ml/datafeeds/{datafeed_id}` returns the new `project_routing` value.

## Bulk update partly succeeded

### What you see

Select the {{anomaly-jobs}} in the jobs list, then choose **Change project scope** from the multi-select action menu. That action opens the bulk flyout titled **Update project routing for *N* anomaly detection jobs**, which shows a **Project scope** picker for the routing expression and an **Update *N* jobs** button.

When you pick any routing expression other than `_alias:_origin`, the flyout shows a warning callout titled **Non-default project scope selected**:

```txt
Using a project routing scope other than _alias:_origin may negatively affect the job's anomaly detection results.
```

That warning reflects the risk of a data-distribution shift, not a hard block. Cross-project scope is appropriate when the {{anomaly-job}} should analyze linked-project data; use `_alias:_origin` only when origin-project-only search is intended.

Clicking **Update *N* jobs** opens a confirmation dialog titled **Update project scope?** (or **Change project scope for *job id*?** / **Change project scope for *N* jobs?** for specific selections). The dialog body reads:

```txt
The model for this job was trained on a specific set of data. Changing this data set may cause temporary model instability and an increase in false-positives. Are you sure you want to apply these changes?
```

When you select more than one job, the dialog also lists **Affected jobs** with per-job added and removed project counts so you can review the scope delta before confirming.

Confirm with **Yes, save** or cancel with **Cancel**.

Failed jobs display no inline error text in the flyout, only the job id and a cross icon. To learn why a job failed, open **Job messages** for that job or retry the update through the API and read the error response.

If the flyout cannot load the job list, {{kib}} shows **Could not load jobs for project routing update**. If the bulk API call fails before per-job results are returned, {{kib}} shows **Project routing update failed**. Both differ from the per-job cross-icon path above.

After submission, result toasts report:

* All succeeded: *Successfully updated project routing for *N* jobs.*
* All failed: *Project routing was not updated for any job.*
* Partial: *Project routing was updated for *X* of *Y* jobs. Any jobs that were previously running will need to be restarted if their update failed.*

Jobs that fail show a cross icon in the flyout job list. Jobs that succeed show a check icon. A separate toast appears if {{kib}} could not restart a {{dfeed}} after a successful routing change: **Failed to restart datafeed for job *job id***.

When a legacy job is migrated without an explicit scope choice, {{es}} defaults routing to preserve local-only search and writes this audit entry in job messages:

```txt
CPS migration: project_routing defaulted to [_alias:_origin] to preserve local search scope. Use the update API to change the scope.
```

The bracketed routing value is always `_alias:_origin` for first-time CPS migration defaults.

### Fix

1. Note every job id that shows a cross icon in the flyout (or that appeared in the partial-failure toast).
2. For each failed job, open **Job messages** and read the API error. Common causes are an open job, a missing model snapshot, invalid `project_routing`, or a credential problem.
3. Fix the underlying cause per job. For credential failures, see [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md).
4. Re-run the update for the failed jobs only. Select just those jobs and use **Change project scope** again.
5. When one job keeps failing, use the single-job path: edit the job, open the **Datafeed** tab, set **Project scope**, and save after closing the job.

Example retry for one job after closing it:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

Adjust `project_routing` to the scope you chose in the bulk flyout. The legacy migration default is `_alias:_origin`.

### Verify

Every selected job shows a check icon in the flyout, or the success toast reports all jobs updated.

## Scope changed and model is reacting

### What you see

When linked projects are added or removed (whether because you changed `project_routing`, linked or unlinked a project in {{ecloud}}, or a migration defaulted routing), the {{dfeed}} might search a different set of projects than when the model was trained. {{es}} records scope changes only after they stabilize (see below). Temporary anomalies are expected while the model adapts.

Scope-change confirmations appear in job messages once stabilization completes. Examples with realistic alias names (linked/unlinked aliases vary):

When a project is newly linked:

```txt
Datafeed search scope changed: [staging] linked. Data distribution may have changed due to new data sources, which can cause temporary anomalies while the model adapts. If detection quality degrades, consider specifying the source clusters explicitly and reviewing recent model snapshots for potential rollback.
```

When a project is unlinked:

```txt
Datafeed search scope changed: [staging] unlinked. Data distribution may have changed due to removed data sources, which can cause temporary anomalies as patterns the model learned are no longer present. If detection quality degrades, consider specifying the source clusters explicitly and reviewing recent model snapshots for potential rollback.
```

When both happen in the same stabilization window:

```txt
Datafeed search scope changed: [production] linked, [staging] unlinked. Data distribution may have changed, which can cause temporary anomalies while the model adapts. If detection quality degrades, consider specifying the source clusters explicitly and reviewing recent model snapshots for potential rollback.
```

If anomaly scores spike after a confirmed change, job messages might also show:

```txt
Elevated anomaly scores detected after search scope change at [2026-07-28T10:15:00.000Z] (production linked). [12] buckets with anomaly score >= 75 observed since the scope change. This is likely caused by the data distribution shift. Consider reviewing model snapshots if the anomalies are not meaningful.
```

The timestamp, change summary in parentheses, and bucket count vary with your job.

By default, {{es}} confirms a scope change only after the linked-project set stays stable for **12 consecutive extraction cycles** and at least **5 minutes** of wall-clock time since the change was first observed. Until both conditions are met, you will not see scope-change messages or annotations even if projects were linked or unlinked in {{ecloud}}.

{{es}} writes scope-change annotations to `.ml-annotations-*`. The annotation `event` field carries `search_scope_changed`. Search that index for the job id and filter on `event: search_scope_changed` to see when scope stabilized.

### Fix

If the scope change was intentional, allow several extraction cycles for the model to adapt. Monitor job messages and annotations until elevated-score warnings stop.

If the change was unintentional (for example a project was unlinked in {{ecloud}} or migration defaulted routing to `_alias:_origin`), restore the link or update `project_routing` to the intended expression. See [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) for routing syntax.

If detection quality degrades and anomalies are not meaningful, roll back to the model snapshot {{es}} retained before the scope change (see the preconditions block) or to an earlier snapshot:

1. Close the {{anomaly-job}}.
2. In {{kib}}, open **Machine Learning → Anomaly Detection → your job → Model snapshots**, select a snapshot from before the scope change (or the automatic rollback snapshot), and revert.
3. Confirm `project_routing` on the {{dfeed}} matches your intended scope with `GET _ml/datafeeds/{datafeed_id}`.
4. Start the {{dfeed}}.

### Verify

New `search_scope_changed` annotations stop appearing and job messages no longer report scope-change or elevated-score warnings on every cycle. `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles with `remote_cluster_stats` listing only the intended projects.
