---
navigation_title: Field mapping conflicts
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Field mapping conflicts [cps-datafeed-field-mappings]

A {{cps}} {{dfeed}} merges search results across linked projects, so a field name must represent the same analytical type everywhere. When mappings disagree, {{es}} may log a report-only warning after a confirmed scope change, exclude one project from the current run, or refuse to start the {{dfeed}} — depending on whether the field is optional or the required time field.

## Diagnose field mapping conflicts [diagnose-cps-datafeed-field-mappings]

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

**Error messages**

Search **Job messages** (or `.ml-notifications-*`) for these patterns. The bracketed datafeed id, field name, project aliases, and type detail vary with your configuration.

*Optional field — after project scope stabilizes following a link or routing change, {{es}} re-checks field capabilities and logs a report-only warning; the {{dfeed}} continues:*

```txt
Cross-project field conflict for datafeed [my-datafeed]: field [status] has incompatible types across linked projects: keyword in [prod-us], long in [prod-eu]. Align index mappings across projects or narrow project_routing to projects with a consistent schema.
```

*Required time field — fail-fast when {{es}} builds the extractor (start or preview); the {{dfeed}} does not run:*

```txt
Cannot run datafeed [my-datafeed]: required time field [@timestamp] has conflicting types across projects in scope: date in [prod-us], long in [prod-eu]. Fix mappings so [@timestamp] uses the same type in every project in scope, or exclude the conflicting project(s) via project_routing.
```

*Required time field — mid-run project exclusion after a scope change; the {{dfeed}} keeps running on the remaining projects:*

```txt
Datafeed [my-datafeed] excluded project [prod-eu] from this run: required time field [@timestamp] has conflicting types: date in [prod-us], long in [prod-eu]. Fix mappings in [prod-eu] to resume searching it, or remove it from project_routing.
```

The type detail after the colon lists each conflicting type and the project aliases that use it, for example `keyword in [prod-us], long in [_origin, prod-eu]`.

**Type compatibility**

For the **time field**, only `date` and `date_nanos` are treated as compatible.

For **optional fields**, {{es}} groups types into analytical families and warns when a field's types span more than one family:

| Family | Types |
| --- | --- |
| Integral | `long`, `integer`, `short`, `byte` |
| Floating point | `double`, `float`, `half_float`, `scaled_float` |
| Date/time | `date`, `date_nanos` |
| Keyword-like | `keyword`, `constant_keyword`, `wildcard` |
| Text-like | `text`, `match_only_text` |
| Boolean | `boolean` |
| IP | `ip` |
| Geo point | `geo_point` |
| Geo shape | `geo_shape` |
| Object/nested | `object`, `nested` |

Types within the same family do not trigger a warning (for example `long` in one project and `integer` in another). Types from different families do (for example `keyword` and `long`). If any type is outside these families, {{es}} suppresses the optional-field warning.

**Compare mappings across projects**

Run [field capabilities]({{es-apis}}operation/operation-field-caps) on the indices the {{dfeed}} queries — one call per project in scope:

```console
GET _origin:logs-*/_field_caps?fields=@timestamp,status&include_unmapped
GET prod-us:logs-*/_field_caps?fields=@timestamp,status&include_unmapped
```

Use the `_origin:` qualifier for the origin project and the linked project's alias for remote projects. In each response, inspect the field entry's type keys and compare them across calls using the compatibility families above — multiple keys in the same family (for example `long` and `integer`) are compatible; keys spanning different families indicate a conflict.

**A mapping changed after the {{dfeed}} was created**

Index templates, ingest pipelines, or explicit mapping updates in one linked project can introduce conflicts that were not present at create time. A mapping rollout alone does not trigger {{es}}'s field-conflict recheck. Symptoms of mapping drift include:

* **Job messages** report a new extraction error even though routing and credentials are unchanged.
* The {{dfeed}} fails to start or preview after a restart because the time field now conflicts at extractor build time.

Optional-field conflict warnings and time-field project exclusions appear only when {{es}} re-checks field capabilities after project scope stabilizes — for example after a project is linked or `project_routing` changes — not from a mapping change by itself. When that recheck runs, you may also see:

* An optional-field conflict warning (see above).
* A project-exclusion message for the time field (see above).

Example extraction error after mapping drift:


```txt
Datafeed is encountering errors extracting data: Cannot parse field [status] of type [long] in document with id 'abc123'
```

The text after the colon is the underlying cause and varies (parse failure, missing field, incompatible type, and so on). During active extraction problems, **Job messages** are authoritative.

## Resolve field mapping conflicts [resolve-cps-datafeed-field-mappings]

**Align the mappings**

Standardize the conflicting field to a compatible type in every linked project — especially the time field (use `date` with a consistent format, or `date_nanos` everywhere). Update index templates or reindex where needed, then restart or preview the {{dfeed}}.

**Exclude the conflicting project**

When mappings cannot be aligned immediately, narrow `project_routing` to projects with a consistent schema. For routing syntax and stale-alias problems, see [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

:::{include} /troubleshoot/_snippets/cps-ml-update-preconditions.md
:::

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:prod-us"
}
```

Replace the routing expression with one that omits the conflicting project while keeping the {{anomaly-job}}'s intended coverage elsewhere.

**Re-validate after a mapping change**

After mappings stabilize:

1. Stop the {{dfeed}}.
2. Update the job query or aggregations if field names or types changed.
3. Preview the {{dfeed}} in {{kib}} or with `POST _ml/datafeeds/{datafeed_id}/_preview` and confirm data returns from every project still in scope.
4. Start the {{dfeed}}.

**Protect the model before a planned mapping change**

Before rolling out breaking mapping changes to projects in an active {{anomaly-job}}'s scope, close the job so {{es}} retains a model snapshot. If detection quality degrades after the change, revert using the procedure in [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md).

**Verify**

* `_field_caps` shows one compatible type per field across every project in scope.
* **Job messages** no longer report field conflicts or extraction errors caused by mapping drift.
* Preview returns documents from each project matched by `project_routing`.
