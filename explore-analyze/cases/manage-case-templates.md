---
navigation_title: Manage templates
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Build a reusable field library and YAML-defined templates to standardize case creation with global fields, expanded field types, and import and export support.
---

# Create and manage case templates [create-manage-case-templates]

Case templates pre-fill case fields such as severity, tags, title, description, and custom fields, so your team can create consistent, complete cases faster. When someone creates a case, they can select a template and use its values as is or override them, and updating or deleting a template later doesn't affect cases already created from it.

Managing templates and the field library requires the **Manage templates** sub-feature privilege for **Cases**. Refer to [Control access to cases](control-case-access.md#give-manage-templates-access).

:::{important}
When you upgrade to 9.5, your existing custom fields and templates are automatically migrated to the new system: custom fields become **global fields** in the field library, and templates are migrated to the new YAML-based format. You don't need to take any action, and you can continue to edit the migrated fields and templates like any others.
:::

## What's in a template [case-templates-anatomy]

A template has a name, description, tags, severity, and category. These same values identify the template in the **Templates** list and pre-fill the matching fields on a case created from it, with the template's name becoming the case's title.

A template can also include:

* Fields from the field library, which pre-fill custom fields on the case.
* A default connector, which pre-fills the case's connector.
* Default case settings (**Sync alert status** and **Auto-extract observables**).

You set the connector and case settings separately, in the template's **Settings** tab.

## About the field library [case-templates-field-library]

Templates draw their custom fields from a **field library**, where you define each field once and reuse it across as many templates as you need. Fields in the library have one of two scopes:

* **Global fields** - Global fields apply to every case, no matter which template was used to create it, or whether a template was used at all. Use global fields for information you always want to capture, such as an internal tracking ID.
* **Reusable fields** - Reusable fields are defined once and added to one or more templates as needed. Use reusable fields for information that only applies to certain case types.

You can define up to 200 fields in the library for each owner. Owners are **{{manage-app}}**, **{{observability}}**, and **Security**.

Each field has one of the following types.

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

## Create a field in the library [case-templates-create-field]

To create a field:

1. From the **Templates** page, select **Field library**, then click **Create field definition**.
2. Optionally add a description, and turn on **Global field** if the field should apply to every case.
3. In the YAML editor, define the field's name, label, and type. Add any options the type requires, such as a list of choices, and set validation and display rules if needed. The editor validates your YAML and suggests values as you type. A live preview shows how the field will render, and changes you make in the preview sync back to the YAML.
4. Click **Save**.

Global fields are added to all new and existing cases immediately. Reusable fields become available to add to a template by referencing the field's name.

## Create a template [case-templates-create-template]

The template editor has a YAML pane and a preview pane with **Fields** and **Settings** tabs. **Fields** previews how the template's fields will render on a case, and **Settings** is where you set a default connector and default case settings.

To create a template:

1. From the **Templates** page, click **Create**.
2. In the YAML editor, define the template's name, description, tags, severity, category, and the fields you want it to pre-fill. Add any fields from your field library by name.
3. Select the **Settings** tab to optionally set a default connector and default case settings (**Sync alert status** and **Auto-extract observables**).
4. Turn the template on so it's available when creating a case, then click **Save**.

As you edit, the editor validates your YAML and suggests values, and the **Fields** tab shows a live preview of how the template will render on the case creation form. Changes you make in the preview sync back to the YAML.

## Edit, clone, or delete a template [case-templates-manage-template]

You can edit, clone, or delete a template from the **Templates** page at any time. Changes to a template only affect cases created after the change. You can also turn a template off to hide it from the case creation flow without deleting it.

While you're editing a field or template, your changes are saved as a draft so you don't lose your work. Select **Reset** to discard the draft and return to the last saved version.

## Import and export templates [case-templates-import-export]

To share a template with another space or deployment, or to back it up, export it from the **Templates** page. To add templates from an exported file, click **Import**, upload the file, then choose which templates to add to the current space.

## Set validation and display rules for fields [case-templates-validation]

Each field in a template or the field library supports the following validation options.

| Option | Effect |
| --- | --- |
| Required | The field must have a value before you can create or save the case. |
| Required on close | The field must have a value before you can close the case. |
| Default value | Pre-fills the field with a value that users can override. |
| Minimum or maximum | Limits a number to a range, or text to a length. |
| Pattern | Checks the value against a custom format and shows a custom error message. |

Adding a required-on-close field to a template doesn't affect cases that were created before the field existed.

You can also show or hide a field based on the value of another field. For example, you can show an escalation reason field only when severity is set to critical. The same rule can also make a field required only under that condition.

## Apply a template [case-templates-apply]

You can apply a template when you create a case, or apply a different template to a case later.

* **When creating a case**: [Create a case](create-cases.md) and select a template to pre-fill its fields, including any values from the field library. You can override any pre-filled value before saving the case.
* **On an existing case**: Open the case, select **Apply template** from the case actions menu, then choose an enabled template. Applying a template updates the case's fields. It doesn't change the case's existing connector.

## Search cases by template field values [case-templates-search]

Cases are searchable by their template and field library values, using the field's label rather than its internal name. Refer to [Search cases](search-share-cases.md#search-cases).
