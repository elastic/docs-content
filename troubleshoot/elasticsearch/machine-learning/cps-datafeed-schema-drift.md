---
navigation_title: Schema drift
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Schema drift [cps-datafeed-schema-drift]

A {{cps}} {{ml}} {{dfeeds}} assumes consistent field mappings across the projects it searches. When a linked project changes its index mapping after the {{dfeeds}} was created, extraction can fail suddenly even though routing and credentials are valid.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose schema drift [diagnose-cps-datafeed-schema-drift]

**Symptoms**

* **Messages** report new data extraction errors after a mapping change in one linked project.
* Anomalies or charts show gaps for buckets that previously had data.
* The same {{dfeeds}} worked before an index template, ingest pipeline, or field type change rolled out to a subset of projects.

**Error messages**

Extraction problems surface as:

```txt
Datafeed is encountering errors extracting data: {0}
```

The wrapped cause often describes a parse failure, missing field, or incompatible field type. Search `.ml-notifications-*` for the job id to see the full message.

**Compare mappings across projects**

For each project in scope, check mappings on the indices the {{dfeeds}} queries:

```console
GET _ml/datafeeds/{datafeed_id}
GET logs-*/_mapping
GET linked-alias:logs-*/_mapping
```

Look for fields used in the {{dfeeds}} `query` or `aggregations` that differ in type or presence between origin and linked projects.

## Resolve schema drift [resolve-cps-datafeed-schema-drift]

**Confirm the mapping change was intentional**

Coordinate with the team that owns the linked project index. If the change was accidental, revert the mapping or reindex to a consistent schema.

**Update or re-validate the {{dfeeds}}**

After mappings stabilize:

1. Stop the {{dfeeds}}.
2. Update the job query or aggregations if field names or types changed.
3. Use the datafeed preview in {{kib}} or `POST _ml/datafeeds/{datafeed_id}/_preview` to confirm extraction succeeds across all projects in scope.
4. Restart the {{dfeeds}}.

**Take a model snapshot before large schema changes**

Before rolling out breaking mapping changes to projects in an active {{anomaly-jobs}} scope, close the job and store a model snapshot with a clear description. If detection quality degrades after the change, revert to that snapshot.

**Verify recovery**

Confirm **Messages** no longer report extraction errors and that preview returns data from every project matched by `project_routing`.
