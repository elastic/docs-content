---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Impacts and limitations"
---

# {{cps-cap}} impacts and limitations [cps-impacts-and-limitations]

This page explains how setting up {{cps}} ({{cps-init}}) affects features in the origin project, and lists overall limitations of {{cps-init}}.

For more details about {{cps-init}} configuration, refer to [](/deploy-manage/cross-project-search-config.md). For information about _using_ {{cps-init}}, refer to [](/explore-analyze/cross-project-search.md).

## Feature impacts [cps-feature-impacts]

% TODO billing: {{cps-init}} generates network egress when the origin project queries linked projects. Data transfer fees may apply, especially for cross-region or cross-cloud-provider queries.
% TODO link to billing docs (D3B) when available. Exact billing SKU may still be TBD.

- **Alerting:** By default, alerting rules in the origin project run against the **combined dataset** of the origin and all linked projects. Alerting rules tuned for a single project's data might produce false positives when they evaluate a larger dataset. This is one reason we recommend using a dedicated [overview project](/deploy-manage/cross-project-search-config.md#cps-arch-overview), so that existing alerting rules on data projects are not affected.

% TODO link to alerting impacts doc when available

- **Dashboards and visualizations:** Existing dashboards and visualizations in the origin project will query all linked projects by default. To control this, set the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual dashboard panels.

- **User permissions:** {{cps-cap}} results are filtered by each user's role assignments across projects. Users with different roles will see different results from the same query. Refer to [Manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-access).

- **{{product.painless}} scripting:** The [{{product.painless}} execute API](/explore-analyze/cross-project-search.md#cps-painless-execute) does not search across linked projects. It resolves index names against the origin project only. You can target a linked project by prefixing the index with the project alias (for example, `projectAlias:myindex`).

## {{observability}} app impacts [obs-cps-impacts]

The following known issues and limitations apply to {{cps-init}} in {{observability}} apps at technical preview. For an overview of {{observability}} app compatibility, refer to [{{cps-cap}} in {{observability}}](/solutions/observability/cross-project-search.md).

### Navigation from Discover to {{observability}} apps [obs-cps-discover-navigation]

When {{cps-init}} is enabled, Discover shows documents from all linked projects by default. {{observability}} apps may not have the same scope, which can lead to differences when navigating between them.

% DOCS NOTE — CONDITIONAL: Include the following "Discover to APM and Infrastructure" item only if APM/Infra CPS work (observability-dev#5328, observability-dev#5374) has NOT shipped. Remove it when that work lands.

* **Discover to APM and Infrastructure:** "Open in APM" and "Open in Infra" links in the Discover document flyout may not resolve correctly for documents from linked projects. Because APM and Infrastructure are scoped to the local project, clicking a link for a remote document may fail to load the expected data. If a remote service shares the same name as a local service, the local service may open instead. This will be addressed when {{cps-init}} is enabled in APM and Infrastructure.
* **Discover to Streams:** Opening a stream name from Discover may show different document counts in Streams, because Streams does not support {{cps-init}}.

### Rules data scope inconsistency [obs-cps-rules-scope]

Custom Threshold and SLO Burn Rate rules query only local project data, even when the underlying data view (for example, `logs-*`) returns cross-project data in Discover. This means:

* A rule simulation may show a condition is violated, but the rule itself may not fire because it evaluates only local data.
* Discover and rules may show different results for the same data view.

APM-specific rules (APM anomaly, error count threshold, failed transaction rate threshold, latency threshold) and Infrastructure Inventory rules have not been fully validated with {{cps-init}}.

Tracking: [kibana#257714](https://github.com/elastic/kibana/issues/257714)

### SLO remote actions not available [obs-cps-slo-remote]

Remote SLOs appear in the SLO list with a "remote" badge, but edit, disable, and clone actions are not available for remote SLOs. Only local SLOs are manageable, even when connected to a remote project.

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

### Observability Overview alerts are local only [obs-cps-overview-alerts]

The Alerts section of the Observability Overview page shows alerts from the local project only, even when rules are configured to act on cross-project data. This is consistent with CCS behavior in {{ech}} — alerts are generated and stored locally.

### Logs Essentials projects cannot use {{cps-init}} [obs-cps-logs-essentials]

Logs Essentials projects cannot participate in cross-project search.

### Synthetics is not affected by {{cps-init}} [obs-cps-synthetics]

Synthetics monitors and TLS Certificates are bound to saved objects and remain scoped to the local project. This is consistent with CCS behavior in {{ech}}. Monitors from linked projects do not appear in the Synthetics UI of the origin project.

## Limitations [cps-limitations]

::::{include} /deploy-manage/_snippets/cps-limitations-core.md
::::
