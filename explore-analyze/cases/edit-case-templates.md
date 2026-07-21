---
navigation_title: Edit and share templates
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
type: how-to
description: Edit, clone, delete, or disable case templates, manage field library entries, and import or export templates between spaces or deployments.
---

# Edit and share case templates [edit-case-templates]

Update existing case templates, make copies, or move them between spaces and deployments. Changes to a template only affect cases created after the change. You can also edit or delete fields in the field library.

## Before you begin

* Your role must have the **Manage templates** sub-feature privilege for **Cases**. Refer to [Control access to cases](control-case-access.md#give-manage-templates-access).
* Understand [what's in a template](manage-case-templates.md#case-templates-anatomy).

## Edit, clone, or delete a template [case-templates-manage-template]

You can edit, clone, or delete a template from the **Templates** page at any time. You can also turn a template off to hide it from the case creation flow without deleting it.

1. Find **Cases** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Templates**.
2. From the templates list, edit, clone, delete, or disable the template you want to change.

While you're editing, your changes are saved as a draft so you don't lose your work. Select **Reset** to discard the draft and return to the last saved version.

## Edit or delete a field library entry [case-templates-manage-field]

Field library entries are managed on the **Field library** page, separately from templates.

1. Find **Cases** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Templates** > **Field library**.
2. Open the field you want to change, edit its YAML, then save. Or delete the field if it's no longer needed.

Changing a library field updates the definition for templates that reference it. Deleting a reusable field that's still referenced by a template can break that template until you remove or replace the reference.

## Import and export templates [case-templates-import-export]

To share a template with another space or deployment, or to back it up, export it from the **Templates** page. To add templates from an exported file, click **Import**, upload the file, then choose which templates to add to the current space.

Import and export apply to templates only. Field library entries aren't included. If a template references reusable fields, those fields must already exist in the destination field library (with matching `name` values) before or after you import the template.
