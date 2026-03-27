---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Cross-project search"
---

# Configure {{cps}} [configure-cross-project-search]

With {{cps}} ({{cps-init}}), users in your organization can search across multiple {{serverless-full}} projects at once, instead of searching each project individually. When your data is split across projects to organize ownership, use cases, or environments, {{cps}} lets you query all the data from a single place. 

{{cps-cap}} is the {{serverless-short}} equivalent of [{{ccs}}](/explore-analyze/cross-cluster-search.md), without requiring an understanding of deployment architecture. Permissions stay consistent across projects, and you can always adjust scope and access as needed.

This section explains how to set up and manage {{cps}} for your organization, including linking projects, managing user access, and refining scope.

* [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md): Link projects in the {{ecloud}} UI, manage linked projects, and unlink projects.
* [Access and scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md): Manage user access across linked projects and configure the default {{cps}} scope per space.
* [Impacts and limitations](/deploy-manage/cross-project-search-config/cps-config-impacts-and-limitations.md): Understand how {{cps}} affects alerting, dashboards, and other features, and review current limitations.

These topics cover {{CPS}} configuration and management. For information on _using_ {{cps}}, including syntax and examples, refer to [](/explore-analyze/cross-project-search.md).

:::{note}
{{cps-cap}} is available for {{serverless-full}} projects only. For other deployment types, refer to [{{ccs}}](/explore-analyze/cross-cluster-search.md).
:::

## Key concepts

::::{include} /deploy-manage/_snippets/cps-origin-linked-definitions.md
::::

::::{include} /explore-analyze/cross-project-search/_snippets/cps-default-search-behavior.md
::::

To adjust the default scope, you can [configure the default CPS scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space.

For details about project IDs and aliases (used in search expressions), refer to [Project IDs and aliases](/explore-analyze/cross-project-search.md#project-id-and-aliases).

## Before you begin [cps-prerequisites]

To configure {{cps}}, make sure you meet these prerequisites:

- You must be an organization owner or project administrator.
- Your origin and linked projects must meet certain [requirements](#cps-compatibility).
- For programmatic access, you must use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md), **not** project-scoped API keys. {{ecloud}} API keys can authenticate across project boundaries. Project-scoped API keys (such as {{es}} API keys) can't search across project boundaries, so they return origin-only results.

% update wrt UIAM docs (esp links); subscription/licensing?
% TODO confirm project-scoped API keys silently return origin-only results (no error) (ES API in E&A)

## Projects available for linking [cps-compatibility]

::::{important} - Origin projects must be new
:applies_to: serverless: preview
During technical preview, only newly created projects can be origin projects for {{cps}}. Existing projects can be _linked_ to an origin project, but they can't serve as origin projects themselves. To get started, create a new {{serverless-short}} project and link it to your existing projects.
::::

You can link any combination of {{product.elasticsearch}}, {{product.observability}}, and {{product.security}} projects, with the following requirements and limitations:

- {{es}} projects require the **Serverless Plus** add-on.
- {{sec-serverless}} and {{obs-serverless}} projects require the **Complete** feature tier. Projects on the **Essentials** tier are not compatible with {{cps}}.
- Workplace AI projects are not compatible with {{cps}}.

Only compatible projects appear in the [{{cps}} linking wizard](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md#cps-link-projects).

% TODO cf https://github.com/elastic/docs-content/pull/5190

## Plan your {{cps-init}} architecture [cps-arch]

When configuring {{cps}}, consider how the {{cps-init}} architecture (or linking pattern) will affect searches, dashboards, and alerting across your organization. {{cps-cap}} supports three patterns, each with a different level of operational risk.

### Recommended: Overview project [cps-arch-overview]

For most deployments, we recommend creating a dedicated **overview project** that can act as an origin project. You can also think of this as a hub-and-spoke model.

In this architecture, you create a new, empty project and link existing projects to it. You run all cross-project searches and dashboards from the new overview project, while your actual active projects continue to operate independently. The linked ("spoke") projects are not linked to each other. 

![Overview project architecture for cross-project search](images/serverless-cross-project-search-arch.svg)

The overview project becomes a central point for broad searches, dashboards, and investigations, without affecting your existing setup (for example, isolated projects stay isolated).

:::{note}
If your overview project handles high search volumes, monitor its performance. Even if the project doesn't store data, it uses compute resources to coordinate searches across linked projects.
:::

### Other supported patterns

The overview project model is strongly recommended and appropriate for most {{cps-init}} configurations. These additional patterns are valid, but they involve additional risk and require careful configuration:

- **Shared data project (N-to-1):** A single project stores data from a shared service (for example, logs). Multiple origin projects link to this central data project. 

    The N-to-1 pattern is often used when several teams need to query shared data independently. The main risk is that linking to a shared data project affects searches, dashboards, and alerts in each origin project. If the shared project is a large, active project, the expanded dataset might cause unexpected behavior. If you're using this pattern, make sure to [manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-access) and consider [CPS scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-search-scope).

- **Data mesh (N-to-N):** Multiple active projects link directly to each other.

    The N-to-N pattern is the most complex and involves the highest risk. After you link projects, all searches, dashboards, and alerting rules in each origin project will query data from every linked project by default, which might make workflows unpredictable. Make sure you check alerting rules, which might be applied to data that the rule was never intended to evaluate.


## Using APIs with {{cps-init}} [cps-apis]

You can also link and unlink projects using the {{ecloud}} API. In the linking wizard, click **View API request** on the review step to see the equivalent API call for your current selection.

For information about searching across linked projects using APIs, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md#cps-supported-apis).

% Parking lot
% - Tag management / custom tags
% - Licensing / subscription tier requirements
