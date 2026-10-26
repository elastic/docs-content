---
navigation_title: Case templates
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
type: overview
description: Learn how case templates and the field library work together to standardize case creation.
---

# Case templates [create-manage-case-templates]

Case templates pre-fill case fields such as severity, tags, title, description, and custom fields, so your team can create consistent, complete cases faster. When someone creates a case, they can select a template and use its values as is or override them. Cases already created from a template aren't affected if you update or delete it.

This page explains what templates contain and how they use the field library.

## What's in a template [case-templates-anatomy]

A template is made up of the following components:

* **Template identity**: Identifies the template in the templates list with a name, description, and tags. These values don't become case field defaults.
* **Case defaults**: Pre-fill the case with a title, description, severity, category, and tags when someone uses the template.
* **Custom fields**: Typed inputs, such as dropdowns, text boxes, and date pickers, that appear on cases created from the template. Define them inline (specific to that template) or reference fields from the field library.
* **Case settings**: (Optional) Default values for **Sync alerts** and **Extract observables** ({{elastic-sec}} only), applied to every case created from the template.
* **Connector**: (Optional) An external system ({{jira}}, {{sn}}, and others) to pre-select on the case.

You set case settings and the connector on the template's **Configuration** tab. Case defaults and custom fields are defined in YAML on the **Fields** tab.

## About the field library [case-templates-field-library]

The field library is an optional catalog where you can define a field once and reuse it across multiple templates. It's not required. Templates can define all their custom fields inline. Fields in the library come in two scopes:

* **Global fields** appear on every case, whether or not a template was used.
* **Reusable fields** appear only when a template that references them is used to create a case, or [applied to an existing case](manage-cases.md#apply-case-template).

For how to create fields and select a scope in the UI, refer to [Create fields in the case field library](create-case-field-library.md).

## What to do next with case templates [case-templates-next-steps]

Start by defining any custom fields your cases need, then build a template and use it when opening cases.

- [Create fields in the case field library](create-case-field-library.md): Add global fields for every case, or reusable fields for specific templates.
- [Create case templates](create-case-templates.md): Set case defaults and attach field library fields.
- [Create a case](create-cases.md): Select a template to pre-fill fields when opening a case.
