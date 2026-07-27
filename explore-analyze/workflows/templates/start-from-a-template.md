---
navigation_title: Start from a template
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Browse curated, pre-built workflow templates in the Template library, preview them, and add one as your own workflow to customize and run.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Create a workflow from a template [workflows-templates-start]

Instead of building a workflow from a blank editor, start from a curated, pre-built template in the **Template library**. Templates are ready-made examples of common automation patterns that you can preview, add as your own workflow, and customize for your environment. It's the fastest way to go from an idea to a working workflow.

With the Template library, you can:

- Browse curated templates by solution and category.
- Preview a template's definition, including the connectors and step types it uses, before you commit to it.
- Add a template as a workflow you own, then edit, enable, and run it like any other workflow.

Because templates live in a central catalog, Elastic can publish new and updated templates without requiring a {{kib}} upgrade.

## Before you begin [workflows-templates-before-you-begin]

- Workflows must be available in your deployment. Refer to [](/explore-analyze/workflows/get-started/setup.md).
- You need the **`All`** privilege for **Analytics → Workflows** to create workflows and use **Add workflow**.
- The Template library is turned off by default. An administrator must enable it before you can use it. Refer to [Enable the Template library](/explore-analyze/workflows/get-started/setup.md#workflows-templates-enable).

## Browse and filter templates [workflows-templates-browse]

If the library is empty, no templates are available for your {{kib}} version yet.

1. Open **Workflows** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the library:
   - Select **Template library** in the Workflows navigation, or
   - If you don't have any workflows yet, select **Explore library** when accessing the **Workflows** page.
3. Find a template that matches your use case.
   - Narrow the results with **Categories**.

Each template card shows step and trigger icons, so you can tell which connectors and step types a template uses before you open it.

## Preview a template [workflows-templates-preview]

Preview a template to confirm it fits your use case before you add it.

1. Select a template card to open its detail page. The detail page shows the template's name, description, tags, solutions, and version.
2. Inspect the read-only **Preview** of the workflow definition (YAML) to see the triggers and steps the template uses.

## Add a template as your workflow [workflows-templates-add]

When you add a template, {{kib}} creates a copy that you own and can modify freely.

1. On the template detail page, select **Add workflow**.
2. {{kib}} opens the workflow editor with the template's YAML already loaded as an unsaved workflow.
3. Customize the workflow for your environment. For example, select a connector and set indices or other step parameters. The editor flags steps that still need configuration, such as an unset connector. For more about editing workflows, refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
4. Save the workflow. It appears on the **Workflows** list, and you can edit, enable, and run it like any other workflow.

::::{tip}
Adding a template creates a copy you own. Catalog updates apply only to new additions, not to workflows you've already added. To use a later version of a template, add it again from the library.
::::

## Related [workflows-templates-related]

- [](/explore-analyze/workflows/get-started/setup.md)
- [](/explore-analyze/workflows/get-started/build-your-first-workflow.md)
- [](/explore-analyze/workflows/authoring-techniques/manage-workflows.md)
- [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md)
- [](/explore-analyze/workflows/use-cases.md)
