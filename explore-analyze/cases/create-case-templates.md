---
navigation_title: Create templates
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
type: how-to
description: Create YAML-defined case templates that pre-fill case defaults, field library values, connectors, and case settings.
---

# Create case templates [create-case-templates]

Create a case template to pre-fill case defaults whenever your team opens a similar case. On the **Configuration** tab, you also set the template's identity, optional case settings, and an optional external connector. This guide shows you how to configure a template and author its YAML.

## Before you begin

* Your role must have the **Manage templates** sub-feature privilege for **Cases**. Refer to [Control access to cases](control-case-access.md#give-manage-templates-access).
* Review [what's in a template](manage-case-templates.md#case-templates-anatomy) and how it uses the [field library](manage-case-templates.md#case-templates-field-library).
* (Optional) [Create reusable fields](create-case-field-library.md) that the template should include.

## Create a template [case-templates-create-template]

The template editor has a YAML pane and a preview pane with **Fields** and **Configuration** tabs:

* **Fields**: Define case defaults and custom fields in YAML, and preview how they render on a case. Changes in the preview sync back to the YAML.
* **Configuration**: Set the template's identity, case settings, and an optional external connector. These values aren't part of the YAML definition.

To create a template:

1. Find **Cases** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Templates** > **Create**.


   Cases are [scoped by solution](create-cases.md#cases-limitations). On {{stack}}, search for `Security/Cases` or `Observability/Cases`, or go to **{{stack-manage-app}}** > **Cases**. On {{serverless-short}}, search for `Cases` in {{elastic-sec}} or {{observability}}.


2. On the **Fields** tab, define case defaults and the fields to pre-fill. [Add reusable fields from your field library](#case-templates-field-ref). Refer to the [YAML schema reference](yaml-template-schema-reference.md) for supported keys.

3. On the **Configuration** tab, enter a template name. Optionally add a description, tags, case settings (**Sync alerts** and **Extract observables**), and an external connector. 

   :::{note}
   **Extract observables** is available in {{elastic-sec}} only.
   :::

4. Click **Create**. The template is enabled by default so it's available when creating a case.

As you edit, the editor validates your YAML and suggests values. While you're editing, your changes are saved as a draft so you don't lose your work. Select **Reset** to discard the draft and return to the last saved version.

### Add reusable fields from the library [case-templates-field-ref]

Global fields appear on every case automatically, so you don't add them to a template. To include a reusable field, add it in the YAML on the **Fields** tab. Use `$ref` with the field's `name` (not its label). Use the `name` in YAML when you author templates. Use the field's `label` when you [search cases](search-share-cases.md#search-case-field-values).

For example, to add the `summary` field from the library:

```yaml
fields:
  - $ref: summary
```

A reference can also use a different name for that template, or override the field's default value, without changing the original field in the library:

```yaml
fields:
  - $ref: summary
    name: incident_summary
    metadata:
      default: A different default for this template
```

## What to do next with case templates [create-case-templates-next-steps]

From here, you can use the template on cases and update it later if your workflow changes.

- [Create a case](create-cases.md): Select a template to pre-fill fields when opening a case.
- [Apply a template to an existing case](manage-cases.md#apply-case-template): Update an open case with values from an enabled template.
- [Edit and share case templates](edit-case-templates.md): Edit, clone, delete, or import and export templates.
