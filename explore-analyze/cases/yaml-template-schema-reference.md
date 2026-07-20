---
navigation_title: YAML template schema reference
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: "YAML definitions for case templates and field library entries support fields for identity, case defaults, field types, and validation and display rules. Reference tables list valid field values."
---

# YAML schema reference for case templates [yaml-template-schema-reference]

This page lists valid fields for YAML template and field library definitions. For authoring guidance, refer to [Manage case templates](manage-case-templates.md).

## Template fields

These fields go at the top level of a template's YAML definition.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `name` | string | Any string | The template's name. Required. Max 100 characters. Also becomes the case's title when someone creates a case from the template. |
| `description` | string | Any string | Optional description of the template. |
| `tags` | array of strings | Array of strings | Optional tags for organizing and finding the template. |
| `severity` | string | `low`, `medium`, `high`, or `critical` | Optional case severity to pre-fill. |
| `category` | string | Any string | Optional case category to pre-fill. |
| `fields` | array | Array of field definitions or field references | Optional. The custom fields the template pre-fills. Field names must be unique within the template. See [Field definition keys](#case-templates-field-keys) and [Reference a field from the library](#case-templates-field-ref). |

:::{note}
A template's default connector and default case settings (**Sync alert status** and **Auto-extract observables**) aren't part of the YAML. You set them separately, in the template's **Settings** tab.
:::

## Field definition keys [case-templates-field-keys]

A field library entry, and each entry in a template's `fields` array, uses these keys. Field library entries are edited on their own, without a `fields` wrapper.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `name` | string | Any string | The field's name. Required. |
| `label` | string | Any string | Optional display label shown on the case form. |
| `control` | string | `INPUT_TEXT`, `INPUT_NUMBER`, `SELECT_BASIC`, `TEXTAREA`, `DATE_PICKER`, `CHECKBOX_GROUP`, `RADIO_GROUP`, or `USER_PICKER` | The field type. Required. See [Field types and metadata](#case-templates-field-types-ref). |
| `type` | string | Depends on `control` | The underlying data type. `keyword` for most controls. See [Field types and metadata](#case-templates-field-types-ref) for exceptions. Required. |
| `metadata` | object | Control-specific keys | Optional. Holds the default value and any other options the control requires, such as a list of choices. See [Field types and metadata](#case-templates-field-types-ref). |
| `validation` | object | See [Validation keys](#case-templates-validation-keys) | Optional. Determines whether the field is required and what values it accepts. |
| `display` | object | See [Display keys](#case-templates-display-keys) | Optional. Determines whether the field is shown. |

## Field types and metadata [case-templates-field-types-ref]

The `metadata` keys a field supports depend on its `control`.

| Control | `type` value | Metadata keys | Description |
|---|---|---|---|
| `INPUT_TEXT` | `keyword` | `default` (string) | A single line of text. |
| `INPUT_NUMBER` | One of `long`, `integer`, `short`, `byte`, `double`, `float`, `half_float`, `scaled_float`, or `unsigned_long` | `default` (number) | A numeric value. |
| `SELECT_BASIC` | `keyword` | `options` (array of strings, required), `default` (string) | A single choice from a list of options. |
| `TEXTAREA` | `keyword` | `default` (string), `markdown` (boolean) | Multiple lines of text. Set `markdown: true` to render a Markdown editor instead of plain text. |
| `DATE_PICKER` | `date` | `default` (string, ISO 8601 datetime), `show_time` (boolean), `timezone` (`utc` or `local`) | A date, optionally with a time and time zone. `timezone` defaults to `utc`. |
| `CHECKBOX_GROUP` | `keyword` | `options` (array of strings, required, max 30, unique), `default` (array of strings, must match `options`) | A multi-select from up to 30 options. |
| `RADIO_GROUP` | `keyword` | `options` (array of strings, required, 2–20 items, unique), `default` (string, must match `options`) | A single choice from 2 to 20 options. |
| `USER_PICKER` | `keyword` | `multiple` (boolean), `default` (array of objects with `uid` and `name`) | One or more {{kib}} users. Set `multiple: false` to restrict to a single selection. |

## Validation keys [case-templates-validation-keys]

Set these keys under a field's `validation` key.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `required` | boolean | `true` or `false` | The field must have a value before you can create or save the case. |
| `required_when` | condition | See [Conditions](#case-templates-conditions) | The field is required only when the condition is met. |
| `required_on_close` | boolean | `true` or `false` | The field must have a value before you can close the case. |
| `pattern.regex` | string | A regular expression | The value must match this pattern. |
| `pattern.message` | string | Any string | Optional custom error message shown when `pattern.regex` doesn't match. |
| `min` | number | Any number | Minimum value. Applies to `INPUT_NUMBER` fields. |
| `max` | number | Any number | Maximum value. Applies to `INPUT_NUMBER` fields. |
| `min_length` | number | Any number | Minimum text length. Applies to text-based fields. |
| `max_length` | number | Any number | Maximum text length. Applies to text-based fields. |

## Display keys [case-templates-display-keys]

Set this key under a field's `display` key.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `show_when` | condition | See [Conditions](#case-templates-conditions) | The field is shown only when the condition is met. Otherwise it's hidden and excluded from validation. |

## Conditions [case-templates-conditions]

A condition is either a single rule or a compound rule that combines several single rules.

**Single rule**

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `field` | string | Any field name | The name of the field to evaluate. |
| `operator` | string | `eq`, `neq`, `contains`, `empty`, or `not_empty` | How to compare the field's current value. `contains` checks whether a value is present in a `CHECKBOX_GROUP` or `USER_PICKER` selection, or whether a substring is present in text. `empty` and `not_empty` don't use `value`. |
| `value` | string or number | Any string or number | The value to compare against. Not used with `empty` or `not_empty`. |

**Compound rule**

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `combine` | string | `all` or `any` | Whether every rule must match (`all`) or at least one rule must match (`any`). Defaults to `all`. |
| `rules` | array | One or more single rules | The rules to evaluate. |

## Reference a field from the library [case-templates-field-ref]

Instead of redefining a field inline, a template can reference a field library entry by name.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `$ref` | string | Name of a field library entry | Required. The library field to reuse. |
| `name` | string | Any string | Optional local alias for this template. If omitted, the library field's own name is used. |
| `metadata.default` | Depends on the referenced field's control | Any value valid for that control | Optional. Overrides the referenced field's default value for this template only. |

## Related pages

- [Manage case templates](manage-case-templates.md): Authoring guidance for the field library and template editors.
