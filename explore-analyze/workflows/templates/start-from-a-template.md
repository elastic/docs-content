---
navigation_title: Start from a template
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Browse curated, pre-built workflow templates in the Template library, preview them, and build a workflow from one to customize and run.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Create a workflow from a template [workflows-templates-start]

Instead of building a workflow from a blank editor, start from a curated, pre-built template in the **Template library**. Templates are ready-made examples of common automation patterns that you can preview, build a workflow from, and customize for your environment. It's the fastest way to go from an idea to a working workflow.

With the Template library, you can:

- Browse curated templates by solution and category.
- Preview a template's definition, including the connectors and step types it uses, before you commit to it.
- Build a workflow from a template, then edit, enable, and run it like any other workflow.

Because templates live in a central catalog, Elastic can publish new and updated templates without requiring a {{kib}} upgrade.

## Before you begin [workflows-templates-before-you-begin]

- Workflows must be available in your deployment. Refer to [](/explore-analyze/workflows/get-started/setup.md).
- You need the **`All`** privilege for **Analytics → Workflows** to create workflows, including workflows built from templates.
- The Template library is turned off by default. An administrator must enable it before you can use it. Refer to [Enable the Template library](/explore-analyze/workflows/get-started/setup.md#workflows-templates-enable).

## Browse and filter templates [workflows-templates-browse]

1. Open **Workflows** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the library:
   - Select **Template library** in the Workflows navigation, or
   - If you don't have any workflows yet, select **Explore library** when accessing the **Workflows** page.
3. Find a template that matches your use case.
   - Narrow the results with **Categories**.
   - Templates are pre-filtered to your current solution. If your view isn't scoped to a solution, use the **Solution** dropdown to filter by solution.

Each template card shows step and trigger icons, so you can tell which connectors and step types a template uses before you open it.

:::{note}
If the library is empty, templates aren't available for your {{kib}} version yet.
:::

## Use templates [workflows-templates-use]

Before you commit to a template, you can review its name, description, tags, solutions, and version, along with a read-only view of its workflow definition (YAML) showing the triggers and steps it uses. Use this to confirm the template fits your use case.

When you're ready, build a new workflow based on the template. {{kib}} creates a copy of the template's YAML definition as your own workflow, without affecting the original template or any other workflows built from it.

Customize the workflow for your environment. For example, select a connector and set indices or other step parameters. The editor flags steps that still need configuration, such as an unset connector. For more about editing workflows, refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).

After you save the workflow, it appears on the **Workflows** list, and you can edit, enable, and run it like any other workflow.

::::{tip}
If Elastic publishes an updated version of a template, workflows you've already built from it aren't affected. Build a new workflow from the updated template to get changes from the newer version.
::::

## Related [workflows-templates-related]

- [](/explore-analyze/workflows/get-started/setup.md)
- [](/explore-analyze/workflows/get-started/build-your-first-workflow.md)
- [](/explore-analyze/workflows/authoring-techniques/manage-workflows.md)
- [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md)
- [](/explore-analyze/workflows/use-cases.md)
