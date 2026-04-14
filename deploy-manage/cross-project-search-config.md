---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Cross-project search"
---

# Configure {{cps}} [configure-cross-project-search]

::::{include} /deploy-manage/_snippets/cps-definition.md
::::

{{cps-cap}} is the {{serverless-short}} equivalent of [{{ccs}}](/explore-analyze/cross-cluster-search.md), with a few differences and enhancements:

* Setting up {{cps}} doesn't require an understanding of your deployment architecture or complex security configurations.
* Permissions stay consistent across projects, and you can always adjust scope and access as needed.
* Searches are performed across projects by default, reducing the need to refactor your queries as you link additional projects.

This section explains how to set up and manage {{cps}} for your organization, including linking projects, managing user access, and refining scope. For information on using {{cps}}, including syntax and examples, refer to [](/explore-analyze/cross-project-search.md).

:::{note}
{{cps-cap}} is available for {{serverless-full}} projects only. For other deployment types, refer to [{{ccs}}](/explore-analyze/cross-cluster-search.md).
:::

## Key concepts

::::{include} /deploy-manage/_snippets/cps-origin-linked-definitions.md
::::

### Projects and search scope

::::{include} /explore-analyze/cross-project-search/_snippets/cps-default-search-behavior.md
::::

Administrators can also adjust the search scope by [configuring the {{cps-init}} scope for each space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope). For best results, set this space-level default before you link projects.

For details about project IDs and aliases used in search expressions, refer to [Project IDs and aliases](/explore-analyze/cross-project-search.md#project-ids-and-aliases).

## Before you begin [cps-prerequisites]

Before you configure {{cps}}, review these prerequisites and best practices:

- You must be an organization owner or project administrator:
  - **Organization owners** can link any projects within the organization.
  - **Project administrators** must have admin access on both the origin project and each linked project.
- Your origin and linked projects must meet certain [requirements](#cps-compatibility).
- Consider the [architecture patterns](#cps-arch) and choose the right linking topology for your organization.

### Projects available for linking [cps-compatibility]

::::{important} - Origin project limitations

* During technical preview, only newly created projects can be origin projects for {{cps}}. Existing projects can be linked from an origin project, but they can't serve as origin projects themselves. To get started, create a new {{serverless-short}} project and link it to your existing projects.
* At this time, you should not use an {{elastic-sec}} project as an origin project for {{cps}} in production. Some {{elastic-sec}} features are not fully functional when {{cps-init}} is enabled on an {{elastic-sec}} origin project. You can still link {{elastic-sec}} projects _to_ an origin project of another type.
::::

To be available for linking, projects must meet the following requirements:

- The origin project and all linked projects must be in the same {{ecloud}} organization.
- You can link any combination of {{product.elasticsearch}}, {{product.observability}}, and {{product.security}} projects in the same organization.
- {{sec-serverless}} and {{obs-serverless}} projects require the **Complete** feature tier. Projects on the **Essentials** tier are not compatible with {{cps}}.

Only compatible projects appear in the [{{cps}} linking wizard](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md#cps-link-projects). If a project you expected to link to is missing from the list, it might not meet the requirements, or you might not have the necessary [permissions](#cps-compatibility) on the project.


## Plan your {{cps-init}} architecture [cps-arch]

When configuring {{cps}}, consider how the {{cps-init}} architecture (or linking pattern) will affect searches, dashboards, and alerting across your organization. {{cps-cap}} supports three patterns, each with a different level of operational risk.

### Recommended: Overview project [cps-arch-overview]

For most deployments, we recommend creating a dedicated **overview project** that can act as an origin project. You can also think of this as a hub-and-spoke model.

In this architecture, you create a new, empty project and link existing projects to it. You run all cross-project searches from the new overview project, while your actual active projects continue to operate independently. The linked ("spoke") projects are not linked to each other.

![Overview project architecture for cross-project search](images/serverless-cross-project-search-arch.svg)

The overview project becomes a central point for broad searches, dashboards, and investigations, without affecting your existing setup.

### Other supported patterns

The overview project model is strongly recommended and appropriate for most {{cps-init}} configurations. These additional patterns are valid, but they involve additional risk and require careful configuration:

- **Shared data project (N-to-1):** A single project stores data from a shared service (for example, logs). Multiple origin projects link to this central data project.

    The N-to-1 pattern is often used when several teams need to query shared data independently. The main risk is that linking to a shared data project affects searches, dashboards, and alerts in each origin project. If the shared project is a large, active project, the expanded dataset might cause unexpected behavior. If you're using this pattern, make sure to [manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-and-api-key-access) and consider [CPS scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-search-scope).

- **Data mesh (N-to-N):** Multiple active projects link directly to each other.

    The N-to-N pattern is the most complex and involves the highest risk. After you link projects, all searches, dashboards, and alerting rules in each origin project will query data from every linked project by default, which might make workflows unpredictable. Make sure you check alerting rules, which might be applied to data that the rule was never intended to evaluate.

## Configure {{cps-init}}

After reviewing the architecture patterns, you can configure {{cps-init}} scope and manage linked projects. For best results, complete these tasks in order:

1. [Set space scope defaults](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#about-cps-init-scope): Configure the default {{cps}} scope for each space that will be used with {{cps}}.
1. [Manage user access and programmatic access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md): Confirm user roles in both the origin and linked projects, as well as roles granted to [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md#roles) that will be used with {{cps}}.
1. [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md): Link projects in the {{ecloud}} UI, manage linked projects, and unlink projects.

Make sure to also review the [feature impacts](#cps-feature-impacts) and [limitations](#cps-limitations) of {{cps-init}}.

## Billing [cps-billing]

::::{include} /deploy-manage/_snippets/cps-billing.md
::::

## Feature impacts [cps-feature-impacts]

When you link projects for {{cps}}, the expanded dataset can affect existing features in the origin project.

- **Alerts:** By default, rules in the origin project run against the **combined dataset** of the origin and all linked projects. Rules tuned for a single project's data might produce false positives when they evaluate a larger dataset. This is one reason we recommend using a dedicated [overview project](/deploy-manage/cross-project-search-config.md#cps-arch-overview), so that existing rules on data projects are not affected. Make sure to also consider the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual rules.

- **Dashboards and visualizations:** Existing dashboards and visualizations in the origin project will query all linked projects by default. To control this, set the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual dashboard panels.

- **User permissions:** {{cps-cap}} results are filtered by each user's role assignments across projects. Users with different roles will see different results from the same query. Refer to [Manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-and-api-key-access).

- **{{product.painless}} scripting:** The [{{product.painless}} execute API](/explore-analyze/cross-project-search.md#cps-painless-scripting) does not search across linked projects. It resolves index names against the origin project only. You can target a linked project by prefixing the index with the project alias (for example, `projectAlias:myindex`).

## Limitations [cps-limitations]

{{cps-cap}} has the following limitations:

::::{include} /deploy-manage/_snippets/cps-limitations-core.md
::::
* Additional limitations apply to Elastic {{observability}} and {{elastic-sec}} projects.

### {{elastic-sec}} apps

::::{warning}
:::{include} /explore-analyze/cross-project-search/_snippets/cps-security-recommendation.md
:::
::::

:::{include} /explore-analyze/cross-project-search/_snippets/cps-availability-security-apps.md
:::

### Elastic {{observability}} apps

{{observability}} apps have limited {{cps-init}} support. The scope selector is not available in {{observability}} apps, and most apps remain scoped to the origin project.

For specific app details, refer to [{{cps-cap}} in {{observability}}](/solutions/observability/cross-project-search.md).

## Using {{cps-init}}

After you configure {{cps}} and link projects, users can start searching across linked projects from the origin project. For search syntax, scope controls, and examples, refer to the following pages:

- [{{cps-cap}} overview](/explore-analyze/cross-project-search.md): Learn how to build queries in a {{cps-init}} context, including how to restrict search scope.
- [](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md): Learn how {{cps-init}} works with compatible {{kib}} apps, including how to adjust search scope.
