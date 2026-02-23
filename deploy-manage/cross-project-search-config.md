---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Cross-project search"
---

# Configure {{cps}} [configure-cross-project-search]

% TODO reconcile with E&A doc
% TODO match phrasing of admin docs (esp you/user)
% TODO apply our new content types
% TODO fix applies-tos at all levels

With {{cps}} ({{cps-init}}), users can search across multiple linked {{serverless-full}} projects from a single origin project. This page explains how to configure and manage {{cps}} for your users, including linking projects, managing user access, and configuring search scopes.

% TODO expand overview

{{cps-cap}} runs across _origin_ and _linked_ projects within your {{ecloud}} organization:

- **Origin project:** The base project where you create links and run searches. 
- **Linked projects:** The projects you connect to the origin project. 
    
After you link projects, searches from the origin project run across the origin and all linked projects by default. To adjust this, you can [configure the default search scope](#cps-search-scope).

% TODO diagram?

% TODO check consistency w/ dev docs

For more information about using {{cps}}, including search expressions, tags, and project routing, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md).

:::{note}
{{cps-cap}} is available for {{serverless-short}} projects only. For other deployment types, refer to [{{ccs}}](/explore-analyze/cross-cluster-search.md).
:::

## Before you begin [cps-prerequisites]

To configure {{cps}}, make sure you meet these prerequisites:

- You must be an organization owner or project administrator.
- Your origin and linked projects must be compatible, as explained in the next section.

% TODO add licensing/subscription tier requirements 

## Project availability for linking [cps-compatibility]

% TODO expand
% TODO match to Learn More link(s)

::::{important}
% TODO applies-to
**Preview: Origin projects must be new**<br>
During technical preview, only newly created projects can be origin projects for {{cps}}. To get started, create a new {{serverless-short}} project and link it to your existing projects.
::::

When you configure {{cps}}, only compatible projects are available for linking:

| Origin project type | Can link to |
|---|---|
| {{product.elasticsearch}} | {{product.elasticsearch}} |
| {{product.observability}} | {{product.observability}}, {{product.security}} |
| {{product.security}} | {{product.security}}, {{product.observability}} |

Workplace AI projects are not compatible with {{cps}}.

{{sec-serverless}} and {{obs-serverless}} projects require the **Complete** feature tier. During technical preview, {{cps}} linking is supported for Complete-to-Complete project connections.

% TODO add licensing/subscription tier details incl Platform+ pack

## Link projects [cps-link-projects]

To link projects, use the Cloud UI. Open your origin project and use the {{cps}} linking wizard:

% TODO revise/expand (copied from other stub)

1. On the home screen, find the project you want to use as the origin project and click **Manage**.
2. Click **Link projects** on the **{{cps-cap}}** tile. Or click **{{cps-cap}}** in the navigation, then click **Link projects**.
3. Browse or search for projects to link to the origin project. Only [compatible projects](#cps-compatibility) appear in the project list. You can filter the project list by type, cloud provider, region, and tags (custom or predefined).
4. Select the checkbox for each project you want to link. You can link up to 20 projects per origin project.

    ::::{note}
    If a project you expected to link to is missing from the list, it might not be [compatible](#cps-compatibility) with the origin project. 
    ::::

5. Complete the remaining steps in the wizard to review and save your selections. In the last step, you can click **View API request** to see the equivalent API request for linking to the selected projects.

% TODO rephrase? just pasted in UI copy for now

::::{important}
After you link projects, all searches from the origin project automatically query **every** linked project by default. This applies immediately to all queries, including those from existing dashboards and alerting rules.

To limit the search, you can [define a default {{cps}} scope](#cps-search-scope). Even after you set a default, users can select the scope of their choice when searching and filtering data and when running queries.
::::

## Manage linked projects [cps-manage-linked-projects]

On the origin project's **{{cps-cap}}** page, you can reconfigure {{cps}} as needed:

- **Link additional projects:**  Click **Link projects** to add more linked projects, up to the 20-project maximum.
- **Unlink projects:** Remove connections by [unlinking projects](#cps-unlink-projects).
- **Open space settings in {{kib}}:**  Click **Manage Space** to set or adjust the default search scope.

% TODO repetitive    

### Unlink projects [cps-unlink-projects]

You can remove linked projects from your origin project at any time. Select the checkbox next to the projects you want to remove from {{cps}}, then click **Unlink**.

% TODO confirm the unlinking?? not a word

After you confirm, searches from the origin project will no longer include data from the unlinked projects.

::::{warning}
If you delete a {{serverless-short}} project that's linked to an origin project, cross-project searches that rely on the project's data might return incomplete results, or fail. For best results, first unlink the project (everywhere it's linked), then delete it.
::::

### Manage user access

{{cps-cap}} respects user permissions across projects. When a user runs a {{cps}} from the origin project, results are filtered based on that user's permissions in each linked project (not just the origin). A user only sees results from linked projects where they have the necessary roles.

For example, if Project A is linked to Projects B and C, but a user only has access to Projects A and B, that user's cross-project searches will return results from A and B only. Results from Project C are excluded because the user does not have the necessary role assignments on that project.

As an administrator, make sure that users who need to search across linked projects have the appropriate roles on each project they need to access. Authorization for {{cps}} is evaluated on the linked project side, based on the user's role assignments on that project.

% TODO confirm: "if I create an API key from inside of my project for personal use, do I get CPS results at all?"
% TODO link to UIAM docs and summarize?
% TODO altering impacts of user role changes 

## Configure the default search scope [cps-search-scope]

By default, all linked projects are included in cross-project searches. You can restrict the scope per space so that users query a subset of linked projects instead of the combined set.

To open space settings in {{kib}}, click **Configure Space settings in {{kib}}** in the banner that appears when you link projects. Or click **Manage Space** at the top of the project page. Select the space you want to configure.  

% ::::{important}
% If you don't adjust the default search scope, all searches, dashboards, visualizations, and alerting rules in the origin project will query data from % **every** linked project.
% ::::

% TODO verify steps; fix repetition

% TODO confirm steps and UI labels; not available yet

In the {{cps}} scope settings, choose the default scope:
   - **All projects:** (default) Searches run across the origin project and all linked projects.
   - **Origin project only:**  Searches run only against the origin project's data.
   - **Specific projects:** Select individual linked projects to include in the default scope.

:::{note}
The {{cps}} scope is a setting, not an access control. Even after you set a default, users can select their preferred scope and can access data in linked projects outside the default scope.
:::

% alt
% ::::{note}
% The {{cps}} scope is a setting, not a security control. It determines the default search scope, but it does not restrict access to data in linked projects.
% ::::

Users can also set the search scope on a per-query basis as needed, using [qualified search expressions](/explore-analyze/cross-project-search.md#search-expressions) or [project routing](/explore-analyze/cross-project-search.md#project-routing).

% TODO check original source for this

:::{important}
{{ml-jobs-cap}} and persistent tasks (such as transforms) might not inherit the space-level scope defaults. If you use ML or transforms, consider configuring the scope explicitly using [project routing](/explore-analyze/cross-project-search.md#project-routing).
:::

% TODO link to alerting impacts and ML/transform considerations



## Recommended architecture [cps-arch]

When you set up {{cps}}, consider creating a dedicated **overview project** that can act as an origin project. You can also think of this as a hub-and-spoke pattern.

In this architecture, you create a new, empty project and link existing projects to it. You run all cross-project searches, dashboards, and investigations from the overview project, while your existing projects continue to operate independently.

% TODO diagram?

The hub-and-spoke architecture offers the following benefits:

- **Reduces alert noise:** After you link projects, searches from the origin project query every linked project by default. If you link active projects directly, existing alerting rules will execute against the combined dataset of **all** linked projects, generating false positives.
- **Protects ML models:** {{ml-jobs-cap}} and transforms designed for a specific project's data could become inaccurate when data from other projects is included.
- **Centralizes visibility:** The overview project becomes a central point for broad searches, dashboards, and investigations, without affecting the operational isolation of individual projects.

A project can act as both an origin project and a linked project (the configurations are independent). For most use cases, the hub-and-spoke pattern with a dedicated overview project is the simplest and safest approach.

:::{note}
If your overview project handles high search volumes, monitor its performance. Even if the project doesn't store data, it uses compute resources to run searches.
:::

% TODO check autoscaling concerns (empty overview projects and OOM errors)

## Feature impacts [cps-feature-impacts]

Enabling {{cps}} affects several features in the origin project:

% TODO cf original sources

- **Billing and data transfer:** {{cps-cap}} generates network egress traffic. When the origin project queries the linked projects, data transfer occurs between projects. Data transfer fees might apply, especially for cross-region or cross-cloud-provider queries.

% TODO link to billing docs

- **Alerting:** By default, alerting rules in the origin project run against the combined dataset of the origin and all linked projects. (This is one reason we recommend a [hub-and-spoke architecture](#cps-arch) with a dedicated overview project, to ensure that the alerting rules on your existing projects are not affected.)

% TODO link to alerting impacts when available

- **Dashboards and visualizations:** After you link projects, existing dashboards and visualizations in the origin project will query all linked projects. To limit this scope, refer to [Configure the default search scope](#cps-search-scope).

% TODO check for repetition 

## Limitations [cps-limitations]

% TODO applies-to badges as needed
% TODO double-check all sources 
% TODO are all of these limitations? do some belong in the overview?

- **New projects only (technical preview):** During the technical preview, only newly created projects can function as origin projects. This is a temporary restriction.
- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **No chaining or transitivity:** If Project A links to Project B, and Project B links to Project C, Project A cannot search Project C. Each link is independent.
- **Links are unidirectional:** Searches that run from a linked project do **not** run against the origin project. If you need bidirectional search, link the projects twice, in both directions.
- **System indices are excluded:** System indices (such as `.security` and `.fleet-*`) are excluded from {{cps}}.
- **Some APIs are not supported.** `_reindex` (cross-project), `_transform`, and `_fleet_search` are not supported for cross-project use.
- **Failure store:** Failure store does not work with {{cps}} in the technical preview.
- **Workplace AI projects:** Workplace AI projects are not compatible with {{cps}}.
% TODO applies to preview for the next one
- **Project aliases:** In technical preview, you can't edit a project's alias on the **{{cps-cap}}** page.

% TODO ^^ is that last one something we don't want to mention?

## Using APIs with {{cps-init}}

TODO expand

You can also link and unlink projects using the API. In the linking wizard, click **View API request** on the review step to see the equivalent API call for your current selection.

For information about searching across linked projects using the API, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md#cps-supported-apis).

## Parking lot

- Tag management / custom tags
- Manage access with keys and roles
    - Create API keys that span multiple projects
    - Make sure users have correct permissions on linked projects (auth happens there)
- Licensing / subscription tier requirements (waiting on proposal?)

% add to github issue
% - Create reusable snippets from dev docs (#31)
% - Reconcile with other cps docs  