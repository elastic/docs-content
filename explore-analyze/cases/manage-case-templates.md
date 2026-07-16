---
navigation_title: Manage case templates
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

# Manage case templates [manage-case-templates]

Case templates let you pre-fill case fields—such as severity, tags, title, description, and custom fields—so your team can create consistent, complete cases faster. Templates are built from a **field library**, where you define custom fields once and reuse them across as many templates as you need. When creating a case, users select a template and can use its values as-is or override them; updating or deleting a template later doesn't affect cases that were already created from it.

To manage the field library and templates, you must have [full access](control-case-access.md) to the **Cases** feature.

## About the field library [case-templates-field-library]

The field library is where you define custom fields before adding them to templates. Each field has one of the following scopes:

* **Global fields** apply to every case in the solution, regardless of which template (or no template) was used to create the case. Use global fields for information you always want to capture, such as an internal tracking ID.
* **Reusable fields** are defined once in the library and then added to one or more templates as needed. Use reusable fields for information that only applies to certain case types.

## Field types [case-templates-field-types]

When you create a field in the library, choose one of the following types:

* Text
* Toggle
* Number
* Dropdown (select)
* Date/time picker
* Checkboxes
* Radio buttons
* User selection

For any field, you can also:

* Mark it as **required** so users must provide a value before creating or saving a case.
* Turn on **Required on close** so the field must have a value before a case can be closed, even if it wasn't required at creation time.
* Set a default value that's used unless a user overrides it.

## Create a field in the library [case-templates-create-field]

1. In case settings, go to the **Field library** section and click **Add field**.
2. Enter a field label and select a field type.
3. Choose the field scope: **Global** to apply the field to all cases, or leave it as a reusable field to add to specific templates.
4. Configure any type-specific options (such as dropdown choices), and optionally set the field as required, required on close, and/or provide a default value.
5. Click **Save**.

Global fields are added to all new and existing cases immediately. Reusable fields become available to select when you build or edit a template.

## Create a template [case-templates-create-template]

Templates are defined using a YAML editor with a live preview panel, so you can see how the fields will appear on a case as you write the template.

1. In case settings, go to the **Templates** section and click **Add template**.
2. Enter a template name and, optionally, a description and tags.
3. In the YAML editor, define the case fields you want the template to pre-fill, such as severity, title, description, category, and any fields from your field library. Use the live preview panel to check how the template will render on the case creation form.
4. Optionally configure defaults that also apply on a per-case basis outside templates:

    * A default **connector** to push cases created from this template to an external system.
    * Whether **Sync alert status** is on or off by default.
    * Whether **Auto-extract observables** is on or off by default.

5. Click **Save**.

You can edit or delete templates from the **Templates** section at any time. Changes to a template only affect cases created after the change.

## Import and export templates [case-templates-import-export]

Export a template to share it with another space or deployment, or to back it up before making changes. Import a previously exported template file to add it to the current space's template list without re-creating it manually.

## Use a template when creating a case [case-templates-use]

When you [create a case](create-cases.md), you can select a template to pre-fill its fields, including any values from the field library. You can override any pre-filled value before saving the case.

## Migrating from the previous template system [case-templates-migration]

When you upgrade to 9.5, your existing custom fields and templates are automatically migrated to the new system:

* Existing custom fields become **global fields** in the field library.
* Existing templates are migrated to use the new YAML-based format.

You don't need to take any action for the migration to happen, and you can continue to edit the migrated fields and templates like any others.

## Related pages

* [Configure case settings](configure-case-settings.md)
* [Create cases](create-cases.md)
* [Use cases as data](cases-as-data.md)
