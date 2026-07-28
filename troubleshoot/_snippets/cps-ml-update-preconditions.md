Stop the {{dfeed}} before updating it. If the {{dfeed}} is still running, the update fails with:

```txt
Cannot update datafeed [my-datafeed] while its status is started
```

The bracketed datafeed id and status vary with your configuration.

When a `project_routing` update changes the effective search scope, {{es}} retains the job's current model snapshot as a rollback point before applying the change. That rollback gate requires the {{anomaly-job}} to be closed. If the job is still open, the update fails with:

```txt
Cannot update project_routing for datafeed [my-datafeed] while job [my-job] is opened. Close the job so a rollback model snapshot can be retained.
```

The bracketed datafeed id, job id, and job state vary with your configuration.

The rollback gate also requires an existing model snapshot. If the job has never produced one, the update fails with:

```txt
Cannot update project_routing for datafeed [my-datafeed] because job [my-job] has no model snapshot to use as a rollback point. Open the job, ingest data, then close it before changing scope.
```

A job that has never run has no snapshot. Open it, let it process data, then close it before changing project scope.

{{es}} records the retained rollback snapshot in the job's **Job messages** (or `.ml-notifications-*`), for example:

```txt
Rollback model snapshot [1720000000] retained before project_routing scope change: Automatic rollback snapshot retained before project_routing scope change [_alias:_origin] -> [_alias:prod-*]
```

You can revert to that snapshot if detection quality degrades after a scope change.

Exception: assigning `_alias:_origin` for the first time to a {{dfeed}} that had no `project_routing` preserves the existing local-only scope. That update bypasses the rollback gate entirely — neither the closed-job check nor the snapshot requirement applies.
