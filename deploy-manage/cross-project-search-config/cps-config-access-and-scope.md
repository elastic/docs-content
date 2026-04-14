---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Access and scope"
---

# Manage access and scope for {{cps}} [cps-access-and-scope]

This page explains how user permissions and scope affect [{{cps}}](/deploy-manage/cross-project-search-config.md) ({{cps-init}}) behavior, and how to set a default scope at the space level.

For details about how {{cps-init}} scope works in {{kib}}, refer to [](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md).

## Manage user and API key access

:::{include} /explore-analyze/cross-project-search/_snippets/cps-security.md
:::

### How access is evaluated

:::{include} /explore-analyze/cross-project-search/_snippets/cps-access-evaluation.md
:::

## Administrator tasks

- Make sure that users who need to search across linked projects have a [role assigned](/deploy-manage/users-roles.md) on each linked project they need to access, and are granted **Cloud Console, {{es}}, and {{kib}}** access to those projects. Authorization is evaluated on the linked project, without regard to the origin project.
- If a user reports missing data from a linked project, check their role assignment on that specific linked project first.
- For programmatic access, make sure the {{ecloud}} API key has the appropriate [roles](/deploy-manage/api-keys/elastic-cloud-api-keys.md#roles) on each project the key needs to access, and is granted **Cloud, {{es}}, and {{kib}} API access** to those projects.

## Manage {{cps}} scope [cps-search-scope]

### About {{cps-init}} scope   

The {{cps-init}} _scope_ is the set of searchable resources included in a {{cps}}. The scope can be:

- Origin project + all linked projects (default)
- Origin project + a set of linked projects, as defined by project routing
- Origin project only

The scope is further restricted by the user's or key's permissions. 

Users can also set the scope at the query level, using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) or [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

By default, an unqualified search from an origin project targets the searchable resources in **all** linked projects, plus the searchable resources in the origin project. This default scope is intentionally broad, to provide the best user experience for searching across linked projects. 

:::{important}
The system-level default {{cps-init}} scope can cause unexpected behavior, especially for alerts and dashboards that operate on the new combined dataset of the origin and all linked projects. To limit this behavior, set the [default {{cps-init}} scope for each space](#cps-default-search-scope), _before_ you link projects.
:::

The following actions change the scope of {{cps}}es:

- **Administrator actions:** 
  - Setting the [default {{cps}} scope for a space](#cps-default-search-scope)
  - Adjusting [user permissions](#manage-user-and-api-key-access) using roles or API keys (for example, creating {{ecloud}} API keys that span multiple projects)
- **User actions:**
  - Using the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in the project header
  - Using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)
  - Using [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)

The scope controls which projects receive the search request, while [querying and filtering](/explore-analyze/query-filter.md) determine which results are returned by the search.

### Set the default {{cps-init}} scope for a space [cps-default-search-scope]

You can adjust the {{cps-init}} system-level default scope by setting a narrower {{cps}} scope for each space. This setting determines the default search scope for the space. Users can override both the system-level default and the space-level default by setting their preferred scope when searching, filtering, or running queries. 

:::{tip}
For best results, set the default {{cps-init}} scope for each space **before** you link projects.
:::

Space settings are managed in {{kib}}. 

1. To open space settings, click **Manage spaces** at the top of the **{{cps-cap}}** page. Select the space you want to configure.  

% ::::{important}
% If you don't adjust the default search scope, all searches, dashboards
% visualizations, and alerting rules in the origin project will query data from 
% **every** linked project.
% ::::

2. In the general space settings, find the **{{cps-cap}}** panel and set the default scope for the space:
   - **All projects:** (default) Searches run across the origin project and all linked projects.
   - **This project:**  Searches run only against the origin project's data.

3. Click **Apply changes** to save the scope setting.

% (not yet) - **Specific projects:** Select individual linked projects to include in the default scope.

::::{note}
The default {{cps}} scope is a space setting, not an access control. Users can still set the scope at the query level. You can also [manage user access](#manage-user-and-api-key-access).
::::

## Next steps

- Review [](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md) for more information about how {{cps-init}} works with compatible {{kib}} apps, including how users can adjust search scope. 
- Review [](/explore-analyze/cross-project-search/cross-project-search-search.md) for more information about how to build queries in a {{cps-init}} context, including how to restrict search scope using qualified search expressions and project routing.