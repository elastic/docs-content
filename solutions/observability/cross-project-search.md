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

When projects are linked, platform apps like Discover and Dashboards automatically include data from all linked projects. {{observability}} apps have varying levels of {{cps-init}} support. Some apps show cross-project data automatically; others remain scoped to the origin project. {{cps-cap}} is unavailable for Logs Essentials projects.

For full details on {{cps-init}} concepts, configuration, and search syntax, refer to:

* [{{cps-cap}} overview](/explore-analyze/cross-project-search.md)
* [Configure {{cps}}](/deploy-manage/cross-project-search-config.md)
* [Manage {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md)

## {{observability}} app compatibility [obs-cps-compatibility]

The following table shows how each {{observability}} app behaves with {{cps-init}} at technical preview.

::::{include} /solutions/_snippets/cps-obs-compatibility.md
::::


## {{cps-cap}} scope selector in {{observability}} apps [obs-cps-scope-selector]

The **{{cps-init}} scope** selector ({icon}`cross_project_search`) in the project header lets you search **This project** or **All projects**. It is available in platform apps like Discover, Dashboards, and Lens, as well as in APM and Infrastructure apps.

For other {{observability}}-specific apps, the scope selector is not available. This means:

* Those apps operate in their default scope, which varies by app (refer to [{{observability}} app compatibility](#obs-cps-compatibility)).
* The scope you select in platform apps like Discover does not carry over to {{observability}} apps that don't support it.
* Data volumes might change when switching between Discover (which shows cross-project data by default) and an {{observability}} app (which is scoped to the origin project) for the same index pattern.

For apps where the scope selector is available, refer to [Managing {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md).

## Navigating between Discover and {{observability}} apps [obs-cps-discover-navigation]

When {{cps-init}} is enabled, Discover shows documents from all linked projects by default, unless the space-level default scope has been changed. {{observability}} apps may not have the same scope, which can lead to differences when navigating between them.

### Discover to Streams

Streams remains scoped to the origin project only and does not support {{cps-init}}. If you open a stream from Discover and the document is from a linked project, {{observability}} shows a warning that the stream is remote. The Streams UI then shows origin project data only, so counts can differ from Discover.

## Identifying the location of a document [obs-cps-identify-documents]

To determine whether a document comes from the origin project or a linked project, refer to [Identifying the location of a document](/explore-analyze/cross-project-search.md#cps-identify-documents).

## Known issues and limitations [obs-cps-known-issues]

The following known issues and limitations apply to {{cps-init}} in {{observability}} apps. For an overview of {{observability}} app compatibility, refer to [{{observability}} app compatibility](#obs-cps-compatibility).

### Rules data scope inconsistency [obs-cps-rules-scope]

SLO burn rate rules query only origin project data, even when the underlying data view (for example, `logs-*`) returns cross-project data in Discover. This means Discover and rules may show different results for the same data view.

{{ml-cap}} rules are not available in {{cps-init}}.

### SLO visibility [obs-cps-slo-remote]

Only origin SLOs are visible, even when connected to a linked project.

Tracking: [kibana#252955](https://github.com/elastic/kibana/issues/252955)

### No default data views in origin projects [obs-cps-no-data-views]

In a {{cps-init}} origin project, Discover may show no data even when linked projects contain data due to missing data views in the origin project.

Tracking: [kibana#260930](https://github.com/elastic/kibana/issues/260930)

### Alerts are origin only [obs-cps-overview-alerts]

**Alerts** are from the origin project only, even when rules are configured to act on cross-project data.

### Synthetics is not available in {{cps-init}} [obs-cps-synthetics]

Synthetics monitors and TLS certificates are bound to saved objects and remain scoped to the origin project. Monitors from linked projects do not appear in the Synthetics UI of the origin project.