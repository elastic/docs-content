---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Link and manage projects"
---

# Link and manage projects for {{cps}} [cps-link-and-manage]

This page explains how to link {{serverless-full}} projects for {{cps}}, manage your linked projects, and unlink projects you no longer need to search across.

For an overview and prerequisites, refer to [Configure {{cps}}](/deploy-manage/cross-project-search-config.md#cps-prerequisites).

## Link projects [cps-link-projects]

:::{tip}
Before linking projects, review the [architecture patterns](/deploy-manage/cross-project-search-config.md#cps-arch) to choose the right linking topology for your organization.
:::

::::{include} /deploy-manage/_snippets/cps-link-projects-procedure.md
::::


::::{important}
After you link projects, all searches from the origin project query data from **every** linked project by default. This applies immediately to all queries, including those from existing dashboards and alerting rules.

To limit searches, you can configure a [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space. Users can override the default by setting scope on a per-query basis.
::::

## Manage linked projects [cps-manage-linked-projects]

On the origin project's **{{cps-cap}}** page, you can reconfigure {{cps}} as needed:

- **Link additional projects:**  Click **Link projects** to add more linked projects, up to the 20-project maximum per origin project.
- **Unlink projects:** Remove connections by [unlinking projects](#cps-unlink-projects).
- **Open space settings in {{kib}}:**  Click **Manage spaces** to set or adjust the default [{{cps-init}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-search-scope) for the space.

## Unlink projects [cps-unlink-projects]

To remove a linked project from the current {{cps-init}} configuration, navigate to the **{{cps-cap}}** page. Select the checkbox next to the projects you want to disconnect, then click **Unlink**.

After you confirm, searches from the origin project will no longer include data from the unlinked projects.

::::{note}
You can't delete a project that's linked to an origin project. To delete a linked project, first unlink it from every origin project it's connected to, then delete it.
::::
