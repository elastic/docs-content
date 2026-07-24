---
navigation_title: Create field library fields
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
type: how-to
description: Create global and reusable fields in the case field library, choose field types, and set validation and display rules.
---

# Create fields in the case field library [create-case-field-library]

Use the **field library** to define custom case fields once and reuse them across templates, so your team collects the same information the same way. This page shows you how to create field library entries, choose field types, and set validation and display rules.

## Before you begin

* Your role needs **Manage templates** sub-feature privilege for **Cases**. Refer to [Control access to cases](control-case-access.md#give-manage-templates-access) for more information.
* Understand [how templates and the field library work together](manage-case-templates.md#case-templates-field-library).

## Choose a field scope [case-templates-field-library]

When you create a field, leave **Global field** cleared for a reusable field, or select it for a global field. For when to use each scope, refer to [About the field library](manage-case-templates.md#case-templates-field-library).

You can define up to 200 fields in the library for each Cases app. On {{stack}}, that's **{{stack-manage-app}}**, **{{observability}}**, and **Security**. On {{serverless-short}}, that's **{{observability}}** and **Security**.

## Field types [case-templates-field-types]

When you create a field, set its type to control what input appears on the case form and what kind of value it accepts. For example, set the type to Text for a single line of text, Number for a numeric value, or Dropdown for a list of choices.

In YAML, the type is the `control` key (for example, `INPUT_TEXT` for Text or `SELECT_BASIC` for Dropdown). Refer to [Field types and metadata](yaml-template-schema-reference.md#case-templates-field-types-ref) for the full mapping.

| Type | Description |
| --- | --- |
| Text | A single line of text. |
| Text area | Multiple lines of text. Supports Markdown formatting. |
| Number | A numeric value. |
| Dropdown | A single choice from a list of options. |
| Radio buttons | A single choice from 2 to 20 options. |
| Checkboxes | A multi-select from up to 30 options. |
| Date/time picker | A date, optionally with a time and time zone. |
| User selection | One or more {{kib}} users. |

## Create a field [case-templates-create-field]

You define a field's properties in YAML. For example, the following creates a required text field with a default value:

```yaml
name: summary
control: INPUT_TEXT
type: keyword
label: Summary
metadata:
  default: Default summary text
validation:
  required: true
```

To create a field:

1. Find **Cases** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), select **Templates** > **Field library**, then click **Create field definition**.

   :::{note}
   Cases are [scoped by solution](create-cases.md#cases-limitations). On {{stack}}, search for `Security/Cases` or `Observability/Cases`, or go to **{{stack-manage-app}}** > **Cases**. On {{serverless-short}}, search for `Cases` in {{elastic-sec}} or {{observability}}.
   :::

2. (Optional) Add a description.
3. Leave **Global field** cleared to create a reusable field, or select it if the field should apply to every case.
4. In the YAML editor, define the field's `name`, `label`, and `control` (field type). Refer to the [YAML schema reference](yaml-template-schema-reference.md) for supported keys and values.
5. (Optional) Add type-specific options, such as a list of choices, and set validation or display rules.
6. Check the live preview. Changes you make in the preview sync back to the YAML.
7. Click **Save**. Global fields are added to all new and existing cases immediately. Reusable fields become available to [add to a template](create-case-templates.md#case-templates-field-ref). Existing cases don't include a reusable field until you create a case from a template that adds it, or [apply that template](manage-cases.md#apply-case-template) to the case.

The editor validates your YAML and suggests values as you type. While you're editing, your changes are saved as a draft so you don't lose your work. Select **Reset** to discard the draft and return to the last saved version.

## Set validation and display rules [case-templates-validation]

Each field supports the following validation options.

| Option | Effect |
| --- | --- |
| Required | The field must have a value before you can create or save the case. |
| Required on close | The field must have a value before you can close the case. |
| Default value | Pre-fills the field with a value that users can override. |
| Minimum or maximum | Limits a number to a range, or text to a length. |
| Pattern | Checks the value against a custom format and shows a custom error message. |

Adding a required-on-close field doesn't affect cases that were created before the field existed.

You can also show or hide a field, or make it required, based on the value of another field. For the YAML keys and condition syntax, refer to [Validation keys](yaml-template-schema-reference.md#case-templates-validation-keys), [Display keys](yaml-template-schema-reference.md#case-templates-display-keys), and [Conditions](yaml-template-schema-reference.md#case-templates-conditions).

## What to do next with the field library [case-field-library-next-steps]

From here, you can add fields to templates and look up YAML keys.

- [Create case templates](create-case-templates.md): Add your library fields to a template and set their default values.
- [YAML schema reference](yaml-template-schema-reference.md): Look up supported keys, field types, and validation options.
