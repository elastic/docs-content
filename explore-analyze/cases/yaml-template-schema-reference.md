---
navigation_title: YAML schema reference
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
type: reference
description: Look up valid YAML keys, field types, and validation and display options for case templates and field library entries.
---

# YAML schema reference for case templates and the field library [yaml-template-schema-reference]

Use this page to look up valid keys and values when writing YAML for case templates and field library entries.

:::{tip}
Before writing YAML by hand, try the **Actions menu** in the template editor: it scaffolds field definitions, library references, validation rules, and conditional logic for you. Use this reference when you need to verify a specific key, customize beyond what the scaffolding provides, or work with templates outside the editor.
:::

For concepts and step-by-step instructions, refer to [Case templates](manage-case-templates.md), [Create fields in the case field library](create-case-field-library.md), and [Create case templates](create-case-templates.md).

## Limits [case-templates-field-library-limits]

Case templates and field library entries have the following limits:

| Limit | Value |
|---|---|
| Templates per solution | 200 |
| Fields per template | 200 |
| Template definition (YAML) size | 30,000 characters |
| Field value or default value size | 30,000 UTF-8 bytes |

These limits apply to new writes only. Existing templates or values that already exceed a limit keep working and can still be edited. If a solution already has 200 templates, you must delete one before you can add another.

## Template fields

These fields go at the top level of a template's YAML definition and pre-fill matching fields on the case.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `name` | string | Any string | Optional case title to pre-fill. |
| `description` | string | Any string | Optional case description to pre-fill. |
| `tags` | array of strings | Array of strings | Optional case tags to pre-fill. |
| `severity` | string | `low`, `medium`, `high`, or `critical` | Optional case severity to pre-fill. |
| `category` | string | Any string | Optional case category to pre-fill. |
| `fields` | array | Array of field references, or inline field definitions | Optional. The custom fields the template pre-fills. Use `$ref` for reusable library fields. You can also define a field inline with the same keys as a library entry when it isn't shared. Field names must be unique within the template. See [Field definition keys](#case-templates-field-keys) and [Reference a field from the library](#case-templates-field-ref-schema). |

:::{note}
The template's own name, description, and tags (used in the **Templates** list), plus its default connector and case settings (**Sync alerts** and **Extract observables**), aren't part of the YAML. You set them on the **Configuration** tab. **Extract observables** is available in {{elastic-sec}} only.
:::

## Field definition keys [case-templates-field-keys]

A field library entry, and each entry in a template's `fields` array, uses these keys. Field library entries are edited on their own, without a `fields` wrapper.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `name` | string | Any string | The field's name. Required. |
| `label` | string | Any string | Optional display label shown on the case form. |
| `control` | string | `INPUT_TEXT`, `INPUT_NUMBER`, `SELECT_BASIC`, `TEXTAREA`, `DATE_PICKER`, `CHECKBOX_GROUP`, `RADIO_GROUP`, `USER_PICKER`, `TOGGLE`, or `MARKDOWN` | The field type. Required. See [Field types and metadata](#case-templates-field-types-ref). |
| `type` | string | Depends on `control` | The underlying data type. `keyword` for most controls. See [Field types and metadata](#case-templates-field-types-ref) for exceptions. Required. |
| `metadata` | object | Control-specific keys | Optional. Holds the default value and any other options the control requires, such as a list of choices. See [Field types and metadata](#case-templates-field-types-ref). |
| `validation` | object | See [Validation keys](#case-templates-validation-keys) | Optional. Determines whether the field is required and what values it accepts. |
| `display` | object | See [Display keys](#case-templates-display-keys) | Optional. Determines whether the field is shown. |

## Field types and metadata [case-templates-field-types-ref]

The `metadata` keys a field supports depend on its `control`.

| Control | UI label | `type` value | Metadata keys | Description |
|---|---|---|---|---|
| `INPUT_TEXT` | Text | `keyword` | `default` (string) | A single line of text. |
| `INPUT_NUMBER` | Number | One of `long`, `integer`, `short`, `byte`, `double`, `float`, `half_float`, `scaled_float`, or `unsigned_long` | `default` (number) | A numeric value. |
| `SELECT_BASIC` | Dropdown | `keyword` | `options` (array of strings, required), `default` (string) | A single choice from a list of options. |
| `TEXTAREA` | Text area | `keyword` | `default` (string), `markdown` (boolean) | Multiple lines of text. Set `markdown: true` to render a Markdown editor instead of plain text. |
| `DATE_PICKER` | Date/time picker | `date` | `default` (string, ISO 8601 datetime), `show_time` (boolean), `timezone` (`utc` or `local`) | A date, optionally with a time and time zone. `timezone` defaults to `utc`. |
| `CHECKBOX_GROUP` | Checkboxes | `keyword` | `options` (array of strings, required, max 30, unique), `default` (array of strings, must match `options`) | A multi-select from up to 30 options. |
| `RADIO_GROUP` | Radio buttons | `keyword` | `options` (array of strings, required, 2–20 items, unique), `default` (string, must match `options`) | A single choice from 2 to 20 options. |
| `USER_PICKER` | User selection | `keyword` | `multiple` (boolean), `default` (array of objects with `uid` and `name`) | One or more {{kib}} users. Set `multiple: false` to restrict to a single selection. |
| `TOGGLE` | Toggle | `boolean` | `default` (boolean) | An on/off toggle. |
| `MARKDOWN` | Markdown (display only) | `keyword` | `content` (string) | A display-only Markdown block. Use `content` for the Markdown to render. |

:::{note}
There are two Markdown options. Use the `MARKDOWN` control for a display-only block that users can't edit. To let users enter and edit Markdown, use the `TEXTAREA` control with `markdown: true` instead.
:::

For example, `MARKDOWN` and `TOGGLE` fields look like this:

```yaml
- name: instructions
  type: keyword
  control: MARKDOWN
  metadata:
    content: "### Instructions"
- name: field_name_3
  label: Label
  control: TOGGLE
  type: boolean
  metadata:
    default: false
```

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

## Reference a field from the library [case-templates-field-ref-schema]

Reference a reusable field from the library with `$ref` and the field's `name` (not its label). Global fields appear on every case automatically and don't need a `$ref`. For a how-to example, refer to [Add reusable fields from the library](create-case-templates.md#case-templates-field-ref).

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `$ref` | string | Name of a field library entry | Required. The library field's `name` (not its label) to reuse. |
| `name` | string | Any string | Optional local alias for this template. If omitted, the library field's own name is used. |
| `metadata.default` | Depends on the referenced field's control | Any value valid for that control | Optional. Overrides the referenced field's default value for this template only. |
