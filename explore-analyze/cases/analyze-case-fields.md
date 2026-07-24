---
navigation_title: Analyze fields
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Query and aggregate case template and custom field values in the case analytics indices.
---

# Analyze case fields [analyze-case-fields]

{{kib}} stores case template values (called extended fields) together in `case.extended_fields`, keyed as `<name>_as_<type>` (for example, `effort_as_integer`). These keys don't appear as separate fields in Discover or Lens, so you query them in one of three ways.

:::{note}
Legacy custom fields live in a separate `case.customFields` field, which you can't query with {{esql}}.
:::

## Ways to query case fields [analyze-case-fields-methods]

| Method | Tool | Use it when |
| --- | --- | --- |
| [Typed fields](#analyze-case-fields-typed) | Discover and Lens | You want to explore and visualize fields with numeric, date, and boolean operators. |
| [`FIELD_EXTRACT`](#analyze-case-fields-field-extract) | {{esql}} | You want to query any field, including one without a typed field. |
| [`terms` aggregation](#analyze-case-fields-terms) | {{es}} API | You want to aggregate directly on a field key. |

## Use typed fields in Discover and Lens [analyze-case-fields-typed]

The managed **Case Analytics** {{data-source}} publishes each templated or global field as a typed field named `case.<name>_as_<type>` (for example, `case.effort_as_integer`), so you get numeric, date, and boolean operators instead of text matching.

:::{note}
{{kib}} publishes a typed field only for fields that a current template uses or the global field library defines, and only when the field name uses letters, digits, and underscores. Fields migrated from before 9.5 keep hyphenated keys, so they don't get a typed field, and a newly added field can take a short time to appear. To refresh the field list immediately, restart {{kib}} or ask an administrator to refresh the {{data-source}}.

Fields without a typed field are still stored in `case.extended_fields`, so you can always reach them with `FIELD_EXTRACT` or a `terms` aggregation.
:::

## Use `FIELD_EXTRACT` in {{esql}} [analyze-case-fields-field-extract]

`FIELD_EXTRACT` {applies_to}`stack: preview` {applies_to}`serverless: preview` returns a string, so cast the value to the type you need, then aggregate:

```esql
FROM .cases
| EVAL effort = FIELD_EXTRACT(case.extended_fields, "effort_as_integer")::double
| WHERE effort IS NOT NULL
| STATS avg_effort = AVG(effort), with_value = COUNT(effort), total = COUNT(*)
```

## Use a `terms` aggregation in the {{es}} API [analyze-case-fields-terms]

Use a `terms` aggregation to group directly on a field key, even if it has no typed field:

```console
GET .cases/_search
{
  "size": 0,
  "aggs": {
    "by_effort": {
      "terms": { "field": "case.extended_fields.effort_as_integer" }
    }
  }
}
```
