---
navigation_title: Workflow templates
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Explore pre-built workflow templates, or browse and add curated templates from the Template Library.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

<!--
Open questions for SME review (docs-content-internal#1456):
1. Go/no-go for 9.5 — confirm before publish (draft assumes experimental 9.5+ / serverless experimental for the Template Library).
2. Serverless — code supports the library; confirm it ships and keep serverless: experimental on the library sections.
3. Issue mentioned a connector-type filter and guided install — neither is in the current UI.
   Confirm we should omit them until they ship (cards show connector/step icons; Add workflow prefills YAML with install-form defaults only).
4. Enablement is via uiSettings.overrides / global settings API (setting is read-only in Advanced Settings).
   Confirm this is the intended customer-facing enablement path to document.
-->

# Workflow templates [workflows-templates]

Workflow templates are pre-built workflows that you can use as a starting point. Instead of building automations from scratch, pick a template and customize it to fit your needs. For example, templates are useful for:

- Automating a common task
- Learning how workflows work
- Saving time with a ready-made example of a common automation pattern

::::::{applies-switch}

:::::{applies-item} { "stack": "preview 9.3, ga 9.4", "serverless": "ga" }

## Access templates [workflows-templates-access]

[Browse](https://github.com/elastic/workflows/) available templates and examples to find one that matches your use case. Refer to the readme to get started using templates.

:::::

:::::{applies-item} { "stack": "experimental 9.5+", "serverless": "experimental" }

## Browse the Template Library [workflows-templates-library]

Use the **Template Library** to start from curated, out-of-the-box workflow templates instead of a blank editor. Browse templates by solution and category, preview a template's definition and connectors, then add it as a workflow you own and customize.

The library is experimental. The page shows an **Experimental** badge. Templates can update without a Kibana upgrade. Contributors author templates in the [elastic/workflows](https://github.com/elastic/workflows) repository.

### Before you begin [workflows-templates-before-you-begin]

::::{admonition} Requirements
- Workflows must be available in your deployment. Refer to [](/explore-analyze/workflows/get-started/setup.md).
- You need privileges to create workflows (**Analytics > Workflows** write access) to use **Add workflow**.
- An administrator must enable the Template Library. It is turned off by default.
::::

### Enable the Template Library [workflows-templates-enable]

Turn on **Workflow Template Library** (`workflowsManagement:library:enabled`). This setting is read-only in **Advanced Settings**, so an administrator enables it in `kibana.yml` or with the Kibana settings API, then reloads the page.

::::{tab-set}

:::{tab-item} kibana.yml
Add the following to `kibana.yml` and restart Kibana:

```yaml
uiSettings.overrides:
  workflowsManagement:library:enabled: true
```
:::

:::{tab-item} API
With the `manage_advanced_settings` privilege, call the Kibana settings API:

```bash
curl -X POST "<kibana-host>/internal/kibana/global_settings" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{"changes":{"workflowsManagement:library:enabled":true}}'
```

Reload the Kibana page after the setting changes.
:::

::::

After you enable the library:

- **Template Library** appears in the Workflows navigation.
- An empty workflows list shows **Explore library**.

::::{tip}
Without the library, browse example workflows in the [elastic/workflows](https://github.com/elastic/workflows) repository.
::::

### Browse templates [workflows-templates-browse]

1. Open **Workflows** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the library:
   - Select **Template Library** in the Workflows navigation, or
   - On an empty workflows list, select **Explore library**.
3. Find a template:
   - Search by name or description.
   - Filter by **solution** (for example Security or Observability). In some Kibana apps, the solution filter is already set for you.
   - Narrow results with **Categories**.

Template cards show step and trigger icons so you can see which connectors and step types a template uses before you open it.

**Checkpoint:** Templates for your Kibana version appear in the library. If the list is empty, no templates are available for this version yet.

### Preview a template [workflows-templates-preview]

1. Select a template card to open its detail page.
2. Review the name, description, categories, solutions, and version.
3. Inspect the read-only **Preview** of the workflow definition (YAML).

**Checkpoint:** Confirm the template matches your use case and that you can provide any connectors or configuration the steps require.

### Add a template as your workflow [workflows-templates-add]

1. On the template detail page, select **Add workflow**.
2. Kibana opens the create workflow editor with the template definition prefilled.
3. Customize the workflow for your environment — for example, choose connectors and set indexes or other step parameters.
4. Save the workflow. You can edit, enable, and run it like any other workflow.

**Checkpoint:** The new workflow appears on the **Workflows** list and opens in the editor with the template YAML as the starting point.

::::{tip}
Adding a template creates a copy you own. Catalog updates apply only to new additions, not to workflows you already added. To use a newer template version, add it again from the library.
::::

### Contribute templates [workflows-templates-contribute]

Templates are authored and reviewed in the [elastic/workflows](https://github.com/elastic/workflows) repository. From the Template Library, select **Contribute a template** to open that repository. Follow the repository readme for contribution guidelines.

### Related [workflows-templates-related]

- [](/explore-analyze/workflows/get-started/setup.md)
- [](/explore-analyze/workflows/get-started/build-your-first-workflow.md)
- [](/explore-analyze/workflows/authoring-techniques/manage-workflows.md)
- [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md)
- [](/explore-analyze/workflows/use-cases.md)

:::::

::::::
