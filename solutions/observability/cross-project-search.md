---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: observability
navigation_title: "Cross-project search"
description: Learn how cross-project search (CPS) works in Elastic Observability, including app compatibility, scope selector behavior, and known limitations.
---

# {{cps-cap}} in {{observability}} [obs-cross-project-search]

[{{cps-cap}} ({{cps-init}})](/explore-analyze/cross-project-search.md) lets you run a single search request across multiple {{serverless-short}} projects. When your observability data is split across projects to organize ownership, use cases, or environments, {{cps}} lets you query all that data from a single origin project without searching each project individually.

When projects are linked, platform apps like Discover and Dashboards automatically include data from all linked projects. {{observability}} apps have partial {{cps-init}} support. Some apps show cross-project data automatically; others remain scoped to the origin project. {{cps-cap}} is unavailable for Logs Essentials projects.

For full details on {{cps-init}} concepts, configuration, and search syntax, refer to:

* [{{cps-cap}} overview](/explore-analyze/cross-project-search.md)
* [Configure {{cps}}](/deploy-manage/cross-project-search-config.md)
* [Manage {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md)

## {{observability}} app compatibility [obs-cps-compatibility]

The following table shows how each {{observability}} app behaves with {{cps-init}}.

::::{include} /solutions/_snippets/cps-obs-compatibility.md
::::


## {{cps-cap}} scope selector in {{observability}} apps [obs-cps-scope-selector]

How you set project scope depends on the app.

APM, Infrastructure, and Synthetics use the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) ({icon}`cross_project_search`) in the project header, as do platform apps like Discover, Dashboards, and Lens.

When you [create an SLO](/solutions/observability/incident-management/create-an-slo.md#slo-cps-scope), specify an SLO-specific **Project scope** to choose which linked projects the SLO monitors.

For other {{observability}}-specific apps, the scope selector is not available. This means:

* Those apps operate in their default scope, which varies by app (refer to [{{observability}} app compatibility](#obs-cps-compatibility)).
* The scope you select in platform apps like Discover does not carry over to {{observability}} apps that don't support it.
* Data volumes might change when switching between Discover (which shows cross-project data by default) and features in the {{observability}} app (which is scoped to the origin project) for the same index pattern.

To learn how to use the scope selector to include or exclude linked projects, refer to [Managing {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md).

## Navigating between Discover and {{observability}} apps [obs-cps-discover-navigation]

When {{cps-init}} is enabled, Discover shows documents from all linked projects by default, unless the space-level default scope has been changed. {{observability}} apps might not have the same scope, which can lead to differences when navigating between them.

### Discover to Streams

Streams remains scoped to the origin project only and does not support {{cps-init}}. If you open a stream from Discover and the document is from a linked project, {{observability}} shows a warning that the stream is remote. The Streams UI then shows origin project data only, so counts can differ from Discover.

## Identifying the location of a document [obs-cps-identify-documents]

To determine whether a document comes from the origin project or a linked project, refer to [Identifying the location of a document](/explore-analyze/cross-project-search.md#cps-identify-documents).

## Known issues and limitations [obs-cps-known-issues]

The following known issues and limitations apply to {{cps-init}} in {{observability}} apps. For an overview of {{observability}} app compatibility, refer to [{{observability}} app compatibility](#obs-cps-compatibility).

### Rules data scope inconsistency [obs-cps-rules-scope]

SLO burn rate rules query the SLO's [SLI and summary indices](/solutions/observability/incident-management/create-an-slo-burn-rate-rule.md#indices-used-by-this-rule), not the SLO's source data view. Those indices reflect the **Project scope** stored on the SLO. Discover uses the session scope on that source data view. If those scopes differ, Discover can show more or fewer documents than the rule evaluates.

{{ml-cap}} rules query the {{anomaly-job}}'s results, not the job's source data. Those results reflect the **Project scope** stored on the [job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md).

<!--Update to anchor #ml-ad-cps-create after https://github.com/elastic/docs-content/pull/7814 ships-->

Synthetics status and TLS rules query origin-project monitors only, even when the scope selector includes linked projects.

### SLO visibility [obs-cps-slo-remote]

Only origin SLOs are visible, even when connected to a linked project. To monitor SLO breaches across {{es}} projects, create SLOs in this project and [scope them](/solutions/observability/incident-management/create-an-slo.md#slo-cps-scope) to linked projects.

### Alerts are origin only [obs-cps-overview-alerts]

**Alerts** are from the origin project only, even when rules are configured to act on cross-project data.
