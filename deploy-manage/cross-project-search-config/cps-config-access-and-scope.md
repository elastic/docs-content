---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Access and scope"
---

# Manage access and scope for {{cps}} [cps-access-and-scope]

This page explains how user permissions and scope affect {{cps}} ({{cps-init}}) behavior. 

For more details about {{cps-init}} configuration, refer to [](/deploy-manage/cross-project-search-config.md). For information about _using_ {{cps-init}}, refer to [](/explore-analyze/cross-project-search.md).

## Manage user access [manage-user-access]

Access to data in linked projects is determined by the [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md) assigned to the user in each project. Whether a user queries a project directly or through {{cps}}, the same permissions apply.

When a {{cps}} query reaches a linked project, the system verifies the user's identity and evaluates the roles assigned to that user in the linked project. Users can only access resources if their roles permit. This means {{cps}} results can vary by user, depending on each user's role assignments across projects.

For example, if a user has read access to the `logs` index in Project B but not in Project C, a {{cps}} for `logs` returns documents from Project B and silently excludes Project C.

### Administrator tasks

- Make sure that users who need to search across linked projects have a [role assigned](/deploy-manage/users-roles.md) on each linked project they need to access. Authorization is evaluated on the linked project, without regard to the origin project.
- If a user reports missing data from a linked project, check their role assignment on that specific linked project first.

% TODO alerting impacts of user role changes 

### Programmatic access [cps-programmatic-access]

The same role-based access model applies to programmatic access through API keys. For {{cps}}, you must use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md), which can authenticate across project boundaries.

Project-scoped API keys (such as {{es}} API keys) cannot search across project boundaries. If a project-scoped API key is used in a {{cps}} context, it silently returns results from the origin project only (no error is returned).

Each {{ecloud}} API key inherits the permissions of the user who created it. Make sure the user who creates the key has the appropriate [roles](/deploy-manage/users-roles.md) on each project the key needs to access.

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
The broad default {{cps-init}} scope can cause unexpected behavior, especially for alerts and dashboards that operate on the new combined dataset of the origin and all linked projects. Make sure to consider the search scope, including the [default {{cps-init}} scope for the space](#cps-default-search-scope), _before_ your users start working with {{cps}}.
:::

The following actions change the scope of {{cps}}es:

- **Administrator actions:** 
  - Setting the [default {{cps}} scope for a space](#cps-default-search-scope)
  - Adjusting [user permissions](#manage-user-access) using roles or API keys (for example, creating {{ecloud}} API keys that span multiple projects)
- **User actions:**
  - Using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)
  - Using [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)

The scope controls which projects receive the search request, while [querying and filtering](/explore-analyze/query-filter.md) determine which results are returned by the search.

### Set the default {{cps-init}} scope for a space [cps-default-search-scope]

You can adjust the broad {{cps-init}} default by setting a narrower {{cps}} scope for each space. This setting determines the _default_ search scope for the space. Users can override the default by setting their preferred scope when searching, filtering, or running queries. 

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
The default {{cps}} scope is a space setting, not an access control. Users can still set the scope at the query level. You can also [manage user access](#manage-user-access).
::::

### How {{cps-init}} scope works in {{kib}}

When processing a search request, {{kib}} applies the most specific scope setting available:

1. **Query-level override (most specific):** Explicit [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) or [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) set on an individual query, dashboard panel, or saved object (for example, `project_routing: _origin`).
2. **Session scope:** The scope set by the user using the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in the project header. This selection persists as the user navigates between apps, and resets to the space default when a new session starts.
3. **Space default (least specific):** The [default {{cps}} scope](#cps-default-search-scope) configured for the space. If no default is explicitly configured, the space default is **All projects** (origin project and all linked projects).

For details on which {{kib}} apps support the scope selector and query-level overrides, refer to [{{cps-cap}} availability by app](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-availability).
