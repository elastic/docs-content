---
navigation_title: Clone project routing
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Clone project routing [cps-datafeed-clone-project-routing]

Cloning an {{ml}} {{anomaly-jobs}} copies the source job's {{dfeeds}} configuration, including `project_routing`. If you clone a job that searches linked projects, the new job inherits the same cross-project scope unless you change it during clone.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose clone project routing [diagnose-cps-datafeed-clone-project-routing]

**Symptoms**

* A cloned job searches more linked projects than you expected.
* The new job's {{dfeeds}} shows the same `project_routing` as the source job in `GET _ml/datafeeds/{datafeed_id}`.
* Detection results or extraction timing on the clone match the source even though you intended a narrower scope.

**Check the clone configuration**

After creating the clone, expand the job row in the {{anomaly-jobs}} list or call:

```console
GET _ml/datafeeds/{new_datafeed_id}
```

Compare `project_routing` on the clone with the source {{dfeeds}}. If they match and you did not edit scope in the clone dialog, the clone inherited the source routing.

## Resolve clone project routing [resolve-cps-datafeed-clone-project-routing]

**Review search scope in the clone dialog**

When cloning a job in {{kib}}, open the **Search scope** section before confirming create. The default shows the source `project_routing`. Edit it if the clone should search fewer projects — for example, `_origin` for local-only analysis.

**Edit routing before creating the clone**

Set the intended `project_routing` in the clone wizard rather than updating after create. Changing scope later on a running job may require closing the job and retaining a model snapshot.

**Verify after create**

Expand the new job in the {{anomaly-jobs}} list and confirm the displayed search scope matches your intent. Optionally confirm with:

```console
GET _ml/datafeeds/{new_datafeed_id}/_stats
```

If the clone is too broad, see [Scope too broad](cps-datafeed-scope-too-broad.md) for how to narrow `project_routing`.
