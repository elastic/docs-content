---
navigation_title: Field mapping mismatch
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Field mapping mismatch [cps-datafeed-field-mapping-mismatch]

{{cps}} {{ml}} {{dfeeds}} merge search results across linked projects. When the same field name maps to **incompatible types** in different projects, {{anomaly-jobs}} may exclude the field, fail to start, or drop a conflicting project from the run depending on whether the field is optional or required (such as the time field).

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose field mapping mismatch [diagnose-cps-datafeed-field-mapping-mismatch]

**Error messages**

Search for these exact patterns in {{ml}} job **Messages** or API error responses.

*Optional field conflict (datafeed continues; field may be dropped):*

```txt
Cross-project field conflict for datafeed `[my-datafeed]`: field `[status]` has incompatible types across linked projects — `keyword` in `[prod-us]`, `long` in `[prod-eu]`. Align index mappings across projects or narrow `project_routing` to projects with a consistent schema.
```

*Required time field — creation fail-fast:*

```txt
Cannot run datafeed `[my-datafeed]`: required time field `@timestamp` has conflicting types across projects in scope — `date` in `[prod-us]`, `long` in `[prod-eu]`. Fix mappings so `@timestamp` uses the same type in every project in scope, or exclude the conflicting project(s) via `project_routing`.
```

*Required time field — mid-run project exclusion:*

```txt
Datafeed `[my-datafeed]` excluded project `[prod-eu]` from this run: required time field `@timestamp` has conflicting types — `date` in `[prod-us]`, `long` in `[prod-eu]`. Fix mappings in `[prod-eu]` to resume searching it, or remove it from `project_routing`.
```

Replace bracketed placeholders with your {{dfeeds}} id, field names, project aliases, and types.

**Compare mappings across projects**

Run [field capabilities]({{es-apis}}operation/operation-field-caps) on the datafeed indices in each project in scope. Use qualified index names when projects differ:

```console
GET prod-us:logs-*/_field_caps?fields=@timestamp,status&include_unmapped
GET prod-eu:logs-*/_field_caps?fields=@timestamp,status&include_unmapped
```

Compare `type` (and `metadata`) for each field across projects. `date` and `date_nanos` are treated as compatible for the time field; other type pairs are not.

**Check {{ml}} job Messages**

Open **ML → Anomaly Detection → your job → Messages** for mapping conflict warnings or project-exclusion errors. Mid-run exclusions can be easy to miss if the {{dfeeds}} stays `started`.

## Resolve field mapping mismatch [resolve-cps-datafeed-field-mapping-mismatch]

**Align index mappings (recommended)**

Standardize the conflicting field to the same type in every linked project — especially `@timestamp` (use `date` with a consistent format). Update index templates or reindex where needed, then update or restart the {{dfeeds}}.

**Narrow `project_routing`**

If you cannot align mappings immediately, limit scope to projects with a consistent schema:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:prod-us"
}
```

For a single conflicting project, remove it from routing instead of dropping the entire cross-project scope.

**Verify recovery**

After mapping fixes or routing changes:

```console
GET _ml/datafeeds/{datafeed_id}/_stats
```

Confirm the {{dfeeds}} searches the intended projects and **Messages** no longer report field conflicts. For time-field fail-fast errors, start the {{dfeeds}} again after mappings are aligned.

If conflicts persist after aligned `_field_caps` results, contact Elastic support with field names, project aliases, and the conflict message text.
