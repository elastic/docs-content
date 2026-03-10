---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Cross-project search"
---

# Configure {{cps}} [configure-cross-project-search]

::::{admonition} 🚧 WIP 🚧 
This page is in progress. See [issue](https://github.com/elastic/docs-content-internal/issues/30) 

**THIS PAGE WILL BE BROKEN INTO SEVERAL PAGES**
::::

With {{cps}} ({{cps-init}}), users in your organization can search across multiple {{serverless-full}} projects at once, instead of searching each project individually.

This page explains how to set up and manage {{cps}} for your organization, including linking projects, managing user access, and refining scope.

## Key concepts

% SNIPPET CANDIDATE: origin/linked definitions

{{cps-cap}} runs across _origin_ and _linked_ projects within your {{ecloud}} organization:

- **Origin project:** The base project where you create links and run cross-project searches. 
- **Linked projects:** The projects you connect to the origin project. Data in the linked projects becomes searchable from the origin project.

For details about project IDs and aliases (used in search expressions), refer to [Project ID and aliases](/explore-analyze/cross-project-search.md#project-id-and-aliases).
    
% SNIPPET CANDIDATE: searches run across all linked projects by default

After you link projects, searches from the origin project run across the origin and all linked projects by default. To adjust this, you can [configure the default CPS scope](#cps-search-scope).

This page describes {{cps}} configuration. For details about _using_ {{cps}}, including search expressions, tags, and project routing, refer to [](/explore-analyze/cross-project-search.md) in **Explore and analyze**.

:::{note}
{{cps-cap}} is available for {{serverless-full}} projects only. For other deployment types, refer to [{{ccs}}](/explore-analyze/cross-cluster-search.md).
:::

## Before you begin [cps-prerequisites]

To configure {{cps}}, make sure you meet these prerequisites:

- You must be an organization owner or project administrator.
- Your origin and linked projects must be [compatible](#cps-compatibility).
- For programmatic access, you must use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md), **not** project-scoped API keys. {{ecloud}} API keys can authenticate across project boundaries. Project-scoped API keys (such as {{es}}) API keys) can't search across project boundaries and return origin-only results.

% update wrt UIAM docs (esp links); subscription/licensing?
% TODO confirm project-scopedAPI keys silently return origin-only results (no error) (ES API in E&A)

## Projects available for linking [cps-compatibility]

::::{important}
:applies_to: serverless: preview
**Origin projects must be new**: During technical preview, only newly created projects can be origin projects for {{cps}}. Existing projects can be _linked_ to an origin project, but they can't serve as origin projects themselves. To get started, create a new {{serverless-short}} project and link it to your existing projects.
::::

You can link any combination of {{product.elasticsearch}}, {{product.observability}}, and {{product.security}} projects, with the following requirements and limitations:

- {{es}} projects require the **Serverless Plus** add-on.
- {{sec-serverless}} and {{obs-serverless}} projects require the **Complete** feature tier. Projects on the **Essentials** tier are not compatible with {{cps}}.
- Workplace AI projects are not compatible with {{cps}}.

Only compatible projects appear in the [{{cps}} linking wizard](#cps-link-projects).

% TODO cf https://github.com/elastic/docs-content/pull/5190


## Plan your {{cps-init}} architecture [cps-arch]

When configuring {{cps}}, consider how the {{cps-init}} architecture (or linking pattern) will affect searches, dashboards, and alerting across your organization. {{cps-cap}} supports three patterns, each with a different level of operational risk.

### Recommended: Overview project [cps-arch-overview]

For most deployments, we recommend creating a dedicated **overview project** that can act as an origin project. You can also think of this as a hub-and-spoke model.

In this architecture, you create a new, empty project and link existing projects to it. You run all cross-project searches and dashboards from the new overview project, while your actual active projects continue to operate independently. The linked ("spoke") projects are not linked to each other. 

TODO add diagram

The overview project becomes a central point for broad searches, dashboards, and investigations, without affecting your existing setup (for example, isolated projects stay isolated).

:::{note}
If your overview project handles high search volumes, monitor its performance. Even if the project doesn't store data, it uses compute resources to coordinate searches across linked projects.
:::

### Other supported patterns

The overview project model is strongly recommended and appropriate for most {{cps-init}} configurations. These additional patterns are valid, but they involve additional risk and require careful configuration:

- **Shared data project (N-to-1):** A single project stores data from a shared service (for example, logs). Multiple origin projects link to this central data project. 

    The N-to-1 pattern is often used when several teams need to query shared data independently. The main risk is that linking to a shared data project affects searches, dashboards, and alerts in each origin project. If the shared project is a large, active project, the expanded dataset might cause unexpected behavior. If you're using this pattern, make sure to [manage user access](#manage-user-access) and consider [CPS scope](#cps-search-scope).

- **Data mesh (N-to-N):** Multiple active projects link directly to each other. 

    The N-to-N pattern is the most complex and involves the highest risk. After you link projects, all searches, dashboards, and alerting rules in each origin project will query data from every linked project by default, which might make workflows unpredictable. Make sure you check alerting rules, which might be applied to data that the rule was never intended to evaluate.


## Link projects [cps-link-projects]

🚧 TODO: Reconcile with Explore and Analyze pages, recently restructured


:::{tip}
Before linking projects, make sure to consider {{cps}} [architecture patterns](#cps-arch).
:::

To link projects, use the {{cps}} linking wizard in the {{ecloud}} UI:

1. On the home screen, find the project you want to use as the origin project and click **Manage**.

    :::{important} 
    :applies_to: serverless: preview
    During technical preview, only newly created projects can function as origin projects.
    :::

1. Click **Configure** on the **{{cps-cap}}** tile. Or navigate to **{{cps-cap}}** in the sidebar.
1. Click **Link projects**. Browse or search for projects to link to the origin project. Only [compatible projects](#cps-compatibility) appear in the project list. You can filter by type, cloud provider, region, and tags.
1. Select the checkbox for each project you want to link. You can link up to 20 projects per origin project.

    If a project you expected to link to is missing from the list, it might not be [compatible](#cps-compatibility) with the origin project. 

1. Complete the remaining steps in the wizard to review and save your selections. In the last step, you can click **View API request** to see the equivalent API request for linking to the selected projects.

% SNIPPET CANDIDATE: searches run across all linked projects by default

::::{important}
After you link projects, all searches from the origin project query data from **every** linked project by default. This applies immediately to all queries, including those from existing dashboards and alerting rules.

To limit searches, you can configure a [default {{cps}} scope](#cps-search-scope) for each space. Users can override the default by setting scope on a per-query basis.
::::

## Manage linked projects [cps-manage-linked-projects]

🚧 TODO: Reconcile with Explore and Analyze pages, recently restructured

On the origin project's **{{cps-cap}}** page, you can reconfigure {{cps}} as needed:

- **Link additional projects:**  Click **Link projects** to add more linked projects, up to the 20-project maximum per origin project.
- **Unlink projects:** Remove connections by [unlinking projects](#cps-unlink-projects).
- **Open space settings in {{kib}}:**  Click **Manage spaces** to set or adjust the default [CPS scope](#cps-search-scope) for the space.

### Unlink projects [cps-unlink-projects]

To remove a linked project from the current {{cps-init}} configuration, navigate to the **{{cps-cap}}** page. Select the checkbox next to the projects you want to disconnect, then click **Unlink**.

After you confirm, searches from the origin project will no longer include data from the unlinked projects.

::::{note}
You can't delete a project that's linked to an origin project. To delete a linked project, first unlink it from every origin project it's connected to, then delete it.
::::

## Manage user access

Access to data in linked projects is determined by the [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md) assigned to the user in each project. Whether a user queries a project directly or through {{cps}}, the same permissions apply.

When a {{cps}} query reaches a linked project, the system verifies the user's identity and evaluates the roles assigned to that user in the linked project. Users can only access resources if their roles permit. This means {{cps}} results can vary by user, depending on each user's role assignments across projects.

For example, if a user has read access to the `logs` index in Project B but not in Project C, a cross-project search for `logs` returns documents from Project B and silently excludes Project C.

For the full security model, including how authentication and authorization work across projects, refer to [Security](/explore-analyze/cross-project-search.md#security) in **Explore and analyze**.

### Administrator tasks

- Make sure that users who need to search across linked projects have a [role assigned](/deploy-manage/users-roles.md) on each linked project they need to access. Authorization is evaluated on the linked project, without regard to the origin project.
- If a user reports missing data from a linked project, check their role assignment on that specific linked project first.

% TODO alerting impacts of user role changes 

## 🚧 Manage {{cps}} scope [cps-search-scope]

### About CPS scope   

The CPS _scope_ is the set of searchable resources included in a {{cps}}. The scope can be:

- Origin project + all linked projects (default)
- Origin project + a set of linked projects, as defined by project routing
- Origin project only

The scope is further restricted by the user's or key's permissions. 

Users can also set the scope on a per-query basis as needed, using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) or [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

By default, an unqualified search from an origin project targets the searchable resources in **all** linked projects, plus the searchable resources in the origin project. This default scope is intentionally broad, to provide the best user experience for searching across linked projects. 

:::{important}
The broad default CPS scope could cause unexpected behavior, especially for alerts and dashboards. Make sure to test the scope and make adjustments _before_ your users start working with {{cps}}.
:::

The following actions change the scope of {{cps}}es:

- **Administrator actions:** 
  - Setting the [default {{cps}} scope for a space](#cps-default-search-scope)
  - Adjusting [user permissions](#manage-user-access) via roles or API keys (for example, creating {{ecloud}} API keys that span multiple projects)
- **User actions:**
  - Using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)
  - Using [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)

The scope controls which projects receive the search request, while _filtering_ controls which results are returned by the search.

### Set the default {{cps-init}} scope for a space [cps-default-search-scope]

You can adjust the broad {{cps-init}} default by setting a narrower {{cps}} scope for each space. This setting determines the _default_ search scope for all users in that space. Users can override the default by setting scope on a per-query basis. 

Space settings are managed in {{kib}}. To open space settings, click **Manage spaces** at the top of the **{{cps-cap}}** page. Select the space you want to configure.  

% ::::{important}
% If you don't adjust the default search scope, all searches, dashboards
% visualizations, and alerting rules in the origin project will query data from 
% **every** linked project.
% ::::

In the general space settings, find the **{{cps-cap}}** panel and set the default scope for the space:
   - **All projects:** (default) Searches run across the origin project and all linked projects.
   - **This project:**  Searches run only against the origin project's data.

% (not yet) - **Specific projects:** Select individual linked projects to include in the default scope.

::::{note}
The default {{cps}} scope is a space setting, not an access control. You can also [](#manage-user-access).
::::

### How CPS scope works in {{kib}}

When processing a search request, {{kib}} applies the most specific scope setting available:

1. **Saved object scope (most specific):** Explicit project routing saved on a specific rule, dashboard panel, or other saved object (for example, `project_routing: _origin`).
2. **Space-level default:** The default {{cps}} scope that an administrator configures for a space.
3. **{{cps-init}} default (least specific):** The default broad setting, which searches the origin project and all linked projects.

New dashboards, rules, and saved searches automatically adopt the space's default scope. Existing saved objects that don't have an explicit project routing also follow the space-level default.


## Feature impacts [cps-feature-impacts]

Enabling {{cps}} affects several features in the origin project:

% TODO billing?

- **Alerting:** By default, alerting rules in the origin project run against the **combined dataset** of the origin and all linked projects. Rules that were tuned for a single project's data might produce false positives when they evaluate a larger dataset. This is one reason we recommend using a dedicated [overview project](#cps-arch-overview), so that existing alerting rules on data projects are not affected.

% TODO link to alerting impacts doc  when available

- **Dashboards and visualizations:** Existing dashboards and visualizations in the origin project will query all linked projects by default. To control this, set the [default {{cps}} sco pe](#cps-default-search-scope) for each space, or save explicit project routing on individual dashboard panels.

- **User permissions:** {{cps}} results are filtered by each user's role assignments across projects. Users with different roles will see different results from the same query. Refer to [Manage user access](#manage-user-access).


## Limitations [cps-limitations]

 🚧 TODO reorganize/table

- {applies_to}`serverless: preview` **New projects only:** During technical preview, only newly created projects can function as origin projects.
- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **Chaining/transitivity not supported:** If Project A links to Project B, and Project B links to Project C, Project A cannot automatically search Project C. Each link is independent.
- **Links are unidirectional:** Searches that run from a linked project do **not** run against the origin project. If you need bidirectional search, link the projects twice, in both directions.
- **System indices are excluded:** System indices (such as `.security` and `.fleet-*`) are excluded from {{cps}}.
- {applies_to}`serverless: preview` **ML and transforms:** ML anomaly detection jobs and transforms are not supported in the technical preview. They continue to run on origin project data only. 
- **Unavailable APIs:** `_transform` and `_fleet_search` requests do not support {{cps-init}}. 
- {applies_to}`serverless: preview` **Failure store:** 🚧 TODO
- **Workplace AI projects:** Workplace AI projects are not compatible with {{cps}}.
- {applies_to}`serverless: preview` **Project aliases:** During technical preview, you can't edit a project's alias on the **{{cps-cap}}** page.

## 🚧 Using APIs with {{cps-init}} [cps-apis]

You can also link and unlink projects using the {{ecloud}} API. In the linking wizard, click **View API request** on the review step to see the equivalent API call for your current selection.

For information about searching across linked projects using APIs, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md#cps-supported-apis).

% Parking lot
% - Tag management / custom tags
% - Licensing / subscription tier requirements
