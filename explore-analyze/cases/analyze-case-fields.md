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

Choose a method based on the tool you want to work in and what you need to do:

| Method | Tool | Use it when |
| --- | --- | --- |
| [Typed fields](#analyze-case-fields-typed) | Discover and Lens | You want to explore and visualize fields with numeric, date, and boolean operators. |
| [`FIELD_EXTRACT`](#analyze-case-fields-field-extract) | {{esql}} | You want to query any field, including one without a typed field. |
| [`terms` aggregation](#analyze-case-fields-terms) | {{es}} API | You want to aggregate directly on a field key. |

## Use typed fields in Discover and Lens [analyze-case-fields-typed]

A typed field is a version of a case field that the managed Case Analytics {{data-source}} publishes with a specific data type, named `case.<name>_as_<type>` (for example, `case.effort_as_integer`). The {{data-source}} publishes one for each templated or global field. Because a typed field has a real type, you get numeric, date, and boolean operators in Discover and Lens instead of text matching on the raw value stored in `case.extended_fields`.

:::{note}
Typed fields exist only in the managed Case Analytics {{data-source}}, not in the underlying index. In the index, every value nests under `case.extended_fields` as `case.extended_fields.<name>_as_<type>`, where `extended_fields` is a `flattened` field, so each value is stored as a keyword. The {{data-source}} adds a runtime field that applies the real data type (from the field's template definition) and lifts it up a level to `case.<name>_as_<type>` for convenience.
:::

### Which fields get a typed field [analyze-case-fields-typed-availability]

{{kib}} publishes a typed field only when both of these are true:

- A current template uses the field, or the global field library defines it.
- The field name uses only letters, digits, and underscores. Fields created before {{stack}} 9.5 might have hyphenated keys, so {{kib}} doesn't publish a typed field for them.

A newly added field can take a short time to appear. To refresh the field list immediately, restart {{kib}} or ask an administrator to refresh the {{data-source}}.

Fields without a typed field are still stored in `case.extended_fields`, so you can always reach them with `FIELD_EXTRACT` or a `terms` aggregation.

## Use `FIELD_EXTRACT` in {{esql}} [analyze-case-fields-field-extract]

`FIELD_EXTRACT` returns a string, so cast the value to the type you need, then aggregate:

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
