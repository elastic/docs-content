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

When projects are linked, platform apps like Discover and Dashboards automatically include data from all linked projects — sometimes called "flat world" behavior. {{observability}} apps have varying levels of {{cps-init}} support. Some apps show cross-project data automatically; others remain scoped to the local project.

For full details on {{cps-init}} concepts, configuration, and search syntax, refer to:

* [{{cps-cap}} overview](/explore-analyze/cross-project-search.md)
* [Configure {{cps}}](/deploy-manage/cross-project-search-config.md)
* [Manage {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md)

## {{observability}} app compatibility [obs-cps-compatibility]

The following table shows how each {{observability}} app behaves with {{cps-init}} at technical preview. The **CCS in {{ech}}** column shows the baseline cross-cluster search support in {{ech}}, which {{cps-init}} in {{serverless-short}} is intended to mirror.

::::{include} /solutions/_snippets/cps-obs-compatibility.md
::::

:::{note}
In {{serverless-short}}, {{observability}} apps do not expose index configuration settings the way {{ech}} does. For example, APM index settings are not available in the Serverless UI. {{cps-init}} in Serverless is configured at the project level through the Cloud UI, not within individual app settings. Refer to [Configure {{cps}}](/deploy-manage/cross-project-search-config.md) for setup instructions.
:::

## {{cps-cap}} scope selector in {{observability}} apps [obs-cps-scope-selector]

The **{{cps-init}} scope** selector ({icon}`cross_project_search`) found in the project header for platform apps like Discover, Dashboards, and Lens, allows you to search "This project" or "All projects."

In {{observability}} apps, the scope selector is not available. This means:

* {{observability}} apps operate in their default scope, which varies by app (refer to [{{observability}} app compatibility](#obs-cps-compatability)).
* The scope you select in platform apps like Discover does not carry over to {{observability}} apps.
* Data volumes might change when switching between Discover (which shows cross-project data by default) and an {{observability}} app (which is scoped to a local project) for the same index pattern.

For apps where the scope selector is available, refer to [Managing {{cps}} scope in your project apps](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md).

## Navigating between Discover and {{observability}} apps [obs-cps-discover-navigation]

When {{cps-init}} is enabled, Discover operates in "flat world" mode and shows documents from all linked projects by default. {{observability}} apps may not have the same scope, which can lead to differences when navigating between them.

% DOCS NOTE — CONDITIONAL: Include the following subsection only if APM/Infra CPS work (observability-dev#5328, observability-dev#5374) has NOT shipped. Remove it when that work lands.

### Discover to {{product.apm}} and Infrastructure

**Open in {{product.apm}}** and **Open in Infra** links in the Discover document flyout may not resolve correctly for documents from linked projects. Because {{product.apm}} and Infrastructure are scoped to the local project, clicking a link for a remote document may fail to load the expected data. If a remote service shares the same name as a local service, the local service may open instead.

A future update will address this when {{cps-init}} is enabled in APM and Infrastructure.

### Discover to Streams

Opening a stream name from Discover may show different document counts in Streams, because Streams does not support {{cps-init}}. For example, Discover may show 20 documents for a stream while the Streams UI shows only 10 (local only).

## Identifying remote and local documents [obs-cps-identify-documents]

To determine whether a document comes from the local project or a linked project, examine the `_index` field.

Remote documents include the linked project's alias as a prefix, separated by a colon:

```
my-linked-project-abc123:.ds-logs-generic.otel-default-2026.03.02-000001
```

Local documents have no prefix:

```
.ds-logs-generic.otel-default-2026.03.02-000001
```

In {{esql}}, the `_index` field is not returned by default. To include it, use the `METADATA` keyword:

```esql
FROM logs-* METADATA _index
| WHERE @timestamp > "2026-03-16T15:15:00Z"
| KEEP @timestamp, _index, message
```

## Known issues and limitations [obs-cps-known-issues]

The following known issues and limitations apply to {{cps-init}} in {{observability}} apps. For an overview of {{observability}} app compatibility, refer to [{{observability}} app compatibility](#obs-cps-compatibility).

### Rules data scope inconsistency [obs-cps-rules-scope]

Custom threshold and SLO burn rate rules query only local project data, even when the underlying data view (for example, `logs-*`) returns cross-project data in Discover. This means:

* A rule simulation may show a condition is violated, but the rule itself may not trigger an alert because it evaluates only local data.
* Discover and rules may show different results for the same data view.

APM-specific rules (APM anomaly, error count threshold, failed transaction rate threshold, latency threshold) and Infrastructure Inventory rules are not fully tested with {{cps-init}}.

Tracking: [kibana#257714](https://github.com/elastic/kibana/issues/257714)

### SLO remote actions not available [obs-cps-slo-remote]

Remote SLOs appear in the SLO list with a "remote" badge, but **edit**, **disable**, and **clone** actions are not available for remote SLOs. Only local SLOs are manageable, even when connected to a remote project.

Tracking: [kibana#252955](https://github.com/elastic/kibana/issues/252955)

% DOCS NOTE — CONDITIONAL: Include the following "Discover flyout links" subsection only if APM/Infra CPS work (observability-dev#5328, observability-dev#5374) has NOT shipped. Remove it when that work lands.

### Discover flyout links for remote documents [obs-cps-discover-flyout]

The following Discover flyout links do not work correctly for documents from linked projects:

* Trace document flyout transaction name links ([kibana#256211](https://github.com/elastic/kibana/issues/256211))
* Span links from linked projects ([kibana#256190](https://github.com/elastic/kibana/issues/256190))
* "Explain this log entry" for linked project logs ([kibana#256168](https://github.com/elastic/kibana/issues/256168))
* Log flyout stream links ([kibana#256075](https://github.com/elastic/kibana/issues/256075))
* Trace flyout charts don't respect project selector ([kibana#256072](https://github.com/elastic/kibana/issues/256072))

These issues will be resolved when {{cps-init}} is enabled in APM and Infrastructure.

### {{observability}} Overview alerts are local only [obs-cps-overview-alerts]

The **Alerts** section of the {{observability}} overview page shows alerts from the local project only, even when rules are configured to act on cross-project data.

### Logs Essentials projects cannot use {{cps-init}} [obs-cps-logs-essentials]

{{cps-init}} is unavailable for Logs Essentials projects.

### Synthetics is not affected by {{cps-init}} [obs-cps-synthetics]

Synthetics monitors and TLS certificates are bound to saved objects and remain scoped to the local project. Monitors from linked projects do not appear in the Synthetics UI of the origin project.

## What's next [obs-cps-whats-next]

Native {{cps-init}} support for additional {{observability}} apps is planned. When {{cps-init}} is enabled in an app, the scope selector will become available in that app, matching the experience in Discover and Dashboards.

* SLO {{cps-init}} readiness: [kibana#252955](https://github.com/elastic/kibana/issues/252955)
* Rules {{cps-init}} readiness: [kibana#257714](https://github.com/elastic/kibana/issues/257714)
