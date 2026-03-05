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
::::

With {{cps}} ({{cps-init}}), users in your organization can search across multiple {{serverless-full}} projects at once, instead of searching each project individually.

This page explains how to configure and manage {{cps}} for your users, including linking projects, managing user access, and configuring search scope.

### {{cps-cap}} concepts

{{cps-cap}} runs across _origin_ and _linked_ projects within your {{ecloud}} organization:

- **Origin project:** The base project where you create links and run searches. 
- **Linked projects:** The projects you connect to the origin project. 
    
After you link projects, searches from the origin project run across the origin and all linked projects by default. To adjust this, you can [configure the default search scope](#cps-search-scope).

For more information about using {{cps}}, including search expressions, tags, and project routing, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md).

:::{note}
{{cps-cap}} is available for {{serverless-short}} projects only. For other deployment types, refer to [{{ccs}}](/explore-analyze/cross-cluster-search.md).
:::

## Before you begin [cps-prerequisites]

To configure {{cps}}, make sure you meet these prerequisites:

- You must be an organization owner or project administrator.
- Your origin and linked projects must be [compatible](#cps-compatibility).
- Your projects must use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md).

% subscription/licensing?

:::{tip}
Before linking projects, make sure to consider {{cps}} [architecture patterns](#plan-your-architecture).
:::

## Projects available for linking [cps-compatibility]

::::{important}
:applies_to: serverless: preview
**Origin projects must be new**: During technical preview, only newly created projects can be origin projects for {{cps}}. To get started, create a new {{serverless-short}} project and link it to your existing projects.
::::

When you configure {{cps}}, only compatible projects are available for linking:

### Project types

| Origin project type | Can link to |
|---|---|
| {{product.elasticsearch}} | {{product.elasticsearch}} |
| {{product.observability}} | {{product.observability}}, {{product.security}} |
| {{product.security}} | {{product.security}}, {{product.observability}} |

Workplace AI projects are not compatible with {{cps}}.

### Feature tiers  

{{cps-cap}} is available for the following feature tiers:

- {{es}} projects require the Serverless Plus add-on.
- {{sec-serverless}} and {{obs-serverless}} projects require the **Complete** feature tier. 

## Link projects [cps-link-projects]

To link projects, use the {{cps}} linking wizard in the Cloud UI:

1. On the home screen, find the project you want to use as the origin project and click **Manage**.
2. Click **Link projects** on the **{{cps-cap}}** tile. Or click **{{cps-cap}}** in the navigation, then click **Link projects**.
3. Browse or search for projects to link to the origin project. Only [compatible projects](#cps-compatibility) appear in the project list. You can filter the project list by type, cloud provider, region, and tags.
4. Select the checkbox for each project you want to link. You can link up to 20 projects per origin project.

    ::::{note}
    If a project you expected to link to is missing from the list, it might not be [compatible](#cps-compatibility) with the origin project. 
    ::::

5. Complete the remaining steps in the wizard to review and save your selections. In the last step, you can click **View API request** to see the equivalent API request for linking to the selected projects.

::::{important}
After you link projects, all searches from the origin project automatically query **every** linked project by default. This applies immediately to all queries, including those from existing dashboards and alerting rules.

To limit the search, you can [define a default {{cps}} scope](#cps-search-scope). Even after you set a default, users can select the scope of their choice when searching and filtering data and when running queries.
::::

## Manage linked projects [cps-manage-linked-projects]

On the origin project's **{{cps-cap}}** page, you can reconfigure {{cps}} as needed:

- **Link additional projects:**  Click **Link projects** to add more linked projects, up to the 20-project maximum.
- **Unlink projects:** Remove connections by [unlinking projects](#cps-unlink-projects).
- **Open space settings in {{kib}}:**  Click **Manage Space** to set or adjust the default [search scope](#cps-search-scope).

% TODO move [project ID and alias info](/explore-analyze/cross-project-search.md#project-id-and-aliases) here from E&A

### Unlink projects [cps-unlink-projects]

You can remove linked projects from your origin project at any time. Select the checkbox next to the projects you want to remove from {{cps}}, then click **Unlink**.

After you confirm, searches from the origin project will no longer include data from the unlinked projects.

::::{important}
You can't delete a linked project. To delete a project, first unlink it everywhere it's linked, then delete it.
::::

### Manage user access

{{cps-cap}} respects user permissions across projects. When a user runs a {{cps}} from the origin project, results are filtered based on that user's permissions in each **linked project.** 

% TODO stop conflating nouns: credentials/identity/permissions/role 

For example, if Project A is linked to Projects B and C, but a user only has access to Projects A and B, that user's cross-project searches will return results from A and B only. Results from Project C are excluded because the user does not have the necessary credentials.

As an administrator, make sure that users who need to search across linked projects have the appropriate roles and API keys. Authorization for {{cps}} is evaluated on the linked project, without regard to the origin project.

TODO expand including how to diagnose access troubles

% TODO confirm: "if I create an API key from inside of my project for personal use, do I get CPS results at all?"
% TODO link to UIAM docs and summarize effects
% TODO altering impacts of user role changes 

For details about managing roles and API keys, refer to [Users and roles](/deploy-manage/users-roles.md) and [API keys](/deploy-manage/api-keys.md).

## Manage search scope [cps-search-scope]

:::{admonition} 🚧 WIP 🚧 
This section is particularly rough
:::

### About search scope

The _search scope_ is the set of searchable resources included in a {{cps}}. The scope can be:

- Origin project + all linked projects (default)
- Origin project + a set of linked projects, as defined by project routing
- Origin project only

The search scope is further restricted by the user's or key's permissions.

By default, an unqualified search from an origin project targets the searchable resources in **all** linked projects, plus the searchable resources in the origin project. This default search scope is intentionally broad, to provide the best user experience for searching across linked projects. 

Because this broad default could cause unexpected workflow behavior, especially for alerts, it's important to consider the search scope before your users start working with {{cps}}.

The following actions change the search scope:

- **Administrator actions:** 
  - [Setting the default {{cps}} scope for a space](#cps-default-search-scope)
  - Adjusting user permissions based on roles or API keys
- **User actions:**
  - [Using qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)
  - [Using project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)

The search scope controls which projects receive the search request, while filtering controls which results are returned by the search.

### Set the default {{cps}} scope for a space [cps-default-search-scope]

To open space settings in {{kib}}, click **Configure Space settings in {{kib}}** in the banner that appears when you link projects. Or click **Manage Space** at the top of the project page. Select the space you want to configure.  

% ::::{important}
% If you don't adjust the default search scope, all searches, dashboards
% visualizations, and alerting rules in the origin project will query data from 
% **every** linked project.
% ::::

In the {{cps}} scope settings, choose the default scope:
   - **All projects:** (default) Searches run across the origin project and all linked projects.
   - **Origin project only:**  Searches run only against the origin project's data.
   - **Specific projects:** Select individual linked projects to include in the default scope.

:::{note}
The default {{cps}} scope is a space setting, not an access control. Even after you set a default, users can select their preferred scope and can access data in linked projects outside the default scope.
:::

% alt
% ::::{note}
% The {{cps}} scope is a setting, not a security control. It determines the default search scope, but it does not restrict access to data in linked projects.
% ::::

Users can also set the search scope on a per-query basis as needed, using [qualified search expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) or [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

## Plan your architecture

When configuring {{cps}}, consider these architecture options. Each pattern has a different effect on how {{cps}} functions in your organization.

### Recommended: Overview project [cps-arch]

When you set up {{cps}}, consider creating a dedicated **overview project** that can act as an origin project. You can also think of this as a hub-and-spoke model or a single-pane-of-glass setup.

In this architecture, you create a new, empty project and link existing projects to it. You run all cross-project searches and dashboards from the new overview project, while your actual active projects continue to operate independently. The linked ("spoke") projects are not linked to each other. Using this pattern helps you ensure that existing configurations are preserved (for example, isolated projects stay isolated).

TODO add diagram

% The overview project becomes a central point for broad searches, dashboards, and investigations, without affecting your existing setup (for example, isolated projects stay isolated).

% :::{note}
% If your overview project handles high search volumes, monitor its performance. Even if the project doesn't store data, it uses compute resources to run searches.
% :::

### Other supported patterns

The overview project model is strongly recommended and appropriate for most deployments, but {{cps}} supports other linking patterns. These patterns are valid but involve additional risk and require careful configuration.

**Shared data project (N-to-1):** A single project stores data from a shared service (for example, logs). Multiple origin projects link to this central data project. This pattern is often used when several teams need to query the shared data independently. The main risk is that if the shared data project is a large, active project, linking it could affect the search scope and alerting behavior in each origin project. If you're using this pattern, it's especially important to manage [user access](#manage-user-access) and [search scope](#cps-search-scope).

**Data mesh (N-to-N):** Multiple active projects link directly to each other. This pattern is the most complex and involves the highest risk. After you link projects, all searches, dashboards, and alerting rules in each origin project will query data from every linked project by default, which might make workflows unpredictable. Make sure you check alerting rules, which might be applied to data that the rule was never intended to evaluate.


## Feature impacts [cps-feature-impacts]

Enabling {{cps}} affects several features in the origin project:

- **Billing and data transfer:** TODO

- **Alerting:** By default, alerting rules in the origin project run against the combined dataset of the origin and all linked projects. This is one reason we recommend using a dedicated [overview project](#cps-arch), to ensure that existing alerting rules are not affected.

% TODO link to alerting impacts doc when available

- **Dashboards and visualizations:** After you link projects, existing dashboards and visualizations in the origin project will query all linked projects. To limit this scope, refer to [Manage search scope](#cps-search-scope).

## Limitations [cps-limitations]

- {applies_to}`serverless: preview` **New projects only:** During technical preview, only newly created projects can function as origin projects. This is a temporary restriction.
- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **Chaining/transitivity not supported:** If Project A links to Project B, and Project B links to Project C, Project A cannot automatically search Project C. Each link is independent.
- **Links are unidirectional:** Searches that run from a linked project do **not** run against the origin project. If you need bidirectional search, link the projects twice, in both directions.
- **System indices are excluded:** System indices (such as `.security` and `.fleet-*`) are excluded from {{cps}}.
- **Some APIs are not supported:** `_reindex` (cross-project), `_transform`, and `_fleet_search` are not supported for cross-project use.
- {applies_to}`serverless: preview` **Failure store:** 🚧 TODO
- **Workplace AI projects:** Workplace AI projects are not compatible with {{cps}}.
- {applies_to}`serverless: preview` **Project aliases:** During technical preview, you can't edit a project's alias on the **{{cps-cap}}** page.

## 🚧 Using APIs with {{cps-init}} [cps-apis]

You can also link and unlink projects using the {{ecloud}} API. In the linking wizard, click **View API request** on the review step to see the equivalent API call for your current selection.

For information about searching across linked projects using the API, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md#cps-supported-apis).

% Parking lot
% - Tag management / custom tags
% - Manage access with keys and roles
%    - Create API keys that span multiple projects
%    - Make sure users have correct permissions on linked projects (auth happens there)
% - Licensing / subscription tier requirements
