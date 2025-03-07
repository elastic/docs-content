---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-mapping-fields.html
applies_to:
  stack: ga
  serverless: ga
---

# Map a runtime field [runtime-mapping-fields]

You map runtime fields by adding a `runtime` section under the mapping definition and defining [a Painless script](../../../explore-analyze/scripting/modules-scripting-using.md). This script has access to the entire context of a document, including the original `_source` via `params._source` and any mapped fields plus their values. At query time, the script runs and generates values for each scripted field that is required for the query.

::::{admonition} Emitting runtime field values
When defining a Painless script to use with runtime fields, you must include the [`emit` method](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md) to emit calculated values.

::::


For example, the script in the following request calculates the day of the week from the `@timestamp` field, which is defined as a `date` type. The script calculates the day of the week based on the value of `timestamp`, and uses `emit` to return the calculated value.

```console
PUT my-index-000001/
{
  "mappings": {
    "runtime": {
      "day_of_week": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ENGLISH))"
        }
      }
    },
    "properties": {
      "@timestamp": {"type": "date"}
    }
  }
}
```

The `runtime` section can be any of these data types:

* `boolean`
* `composite`
* `date`
* `double`
* `geo_point`
* `ip`
* `keyword`
* `long`
* [`lookup`](retrieve-runtime-field.md#lookup-runtime-fields)

Runtime fields with a `type` of `date` can accept the [`format`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md) parameter exactly as the `date` field type.

Runtime fields with a `type` of `lookup` allow retrieving fields from related indices. See [`retrieve fields from related indices`](retrieve-runtime-field.md#lookup-runtime-fields).

If [dynamic field mapping](dynamic-field-mapping.md) is enabled where the `dynamic` parameter is set to `runtime`, new fields are automatically added to the index mapping as runtime fields:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic": "runtime",
    "properties": {
      "@timestamp": {
        "type": "date"
      }
    }
  }
}
```

## Define runtime fields without a script [runtime-fields-scriptless]

Runtime fields typically include a Painless script that manipulates data in some way. However, there are instances where you might define a runtime field *without* a script. For example, if you want to retrieve a single field from `_source` without making changes, you don’t need a script. You can just create a runtime field without a script, such as `day_of_week`:

```console
PUT my-index-000001/
{
  "mappings": {
    "runtime": {
      "day_of_week": {
        "type": "keyword"
      }
    }
  }
}
```

When no script is provided, {{es}} implicitly looks in `_source` at query time for a field with the same name as the runtime field, and returns a value if one exists. If a field with the same name doesn’t exist, the response doesn’t include any values for that runtime field.

In most cases, retrieve field values through [`doc_values`](elasticsearch://reference/elasticsearch/mapping-reference/doc-values.md) whenever possible. Accessing `doc_values` with a runtime field is faster than retrieving values from `_source` because of how data is loaded from Lucene.

However, there are cases where retrieving fields from `_source` is necessary. For example, `text` fields do not have `doc_values` available by default, so you have to retrieve values from `_source`. In other instances, you might choose to disable `doc_values` on a specific field.

::::{note}
You can alternatively prefix the field you want to retrieve values for with `params._source` (such as `params._source.day_of_week`). For simplicity, defining a runtime field in the mapping definition without a script is the recommended option, whenever possible.
::::



## Ignoring script errors on runtime fields [runtime-errorhandling]

Scripts can throw errors at runtime, e.g. on accessing missing or invalid values in documents or because of performing invalid operations. The `on_script_error` parameter can be used to control error behaviour when this happens. Setting this parameter to `continue` will have the effect of silently ignoring all errors on this runtime field. The default `fail` value will cause a shard failure which gets reported in the search response.


## Updating and removing runtime fields [runtime-updating-scripts]

You can update or remove runtime fields at any time. To replace an existing runtime field, add a new runtime field to the mappings with the same name. To remove a runtime field from the mappings, set the value of the runtime field to `null`:

```console
PUT my-index-000001/_mapping
{
 "runtime": {
   "day_of_week": null
 }
}
```
% TEST[continued]

:::::{admonition} Downstream impacts
Updating or removing a runtime field while a dependent query is running can return inconsistent results. Each shard might have access to different versions of the script, depending on when the mapping change takes effect.

::::{warning}
Existing queries or visualizations in {{kib}} that rely on runtime fields can fail if you remove or update the field. For example, a bar chart visualization that uses a runtime field of type `ip` will fail if the type is changed to `boolean`, or if the runtime field is removed.
::::


:::::



