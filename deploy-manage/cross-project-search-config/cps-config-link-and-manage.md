---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Link and manage projects"
---

# Link and manage projects for {{cps}} [cps-link-and-manage]

This page explains how to link {{serverless-full}} projects for {{cps}} ({{cps-init}}), manage your linked projects, and unlink projects you no longer need to search across.

For more details about {{cps-init}} configuration, refer to [](/deploy-manage/cross-project-search-config.md). For information about _using_ {{cps-init}}, refer to [](/explore-analyze/cross-project-search.md).

## Link projects [cps-link-projects]

:::{tip}
Before linking projects, review the [architecture patterns](/deploy-manage/cross-project-search-config.md#cps-arch) to choose the right linking topology for your organization. You might also want to adjust the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space.
:::

To link projects, use the {{cps}} linking wizard in the {{ecloud}} UI:

1. On the home screen, find the project you want to use as the origin project and click **Manage**.

1. Use the sidebar to navigate to the **{{cps-cap}}** page.

1. Click **Link projects**. Browse or search for projects to link to the origin project. Only compatible projects appear in the project list. You can filter by type, cloud provider, region, and tags.

1. Select the checkbox for each project you want to link. You can link up to 20 projects to each origin project.

    If a project you expected to link to is missing from the list, it might not be compatible with the origin project, or you might not have [access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-access) to the linked project.

1. Complete the remaining steps in the wizard to review and save your selections. In the last step, you can click **View API request** to see the equivalent API request for linking to the selected projects.

::::{important}
After you link projects, all searches from the origin project query data from **every** linked project by default. This applies immediately to all queries, including those from existing dashboards and alerting rules.

To limit searches, you can configure a [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space. Users can override the default by setting scope when searching, filtering, or running queries.
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
