---
navigation_title: Scale and architect a deployment
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-scale-and-architect.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-scale-and-architect.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
description: Advanced guidance for scaling and designing Elastic Synthetics deployments, including cross-project and cross-cluster search support, tagging strategies, and custom dashboards.
---

# Scale and architect a Synthetics deployment [synthetics-scale-and-architect]

Use these advanced considerations when you use the {{synthetics-app}} for large and complex use cases.

## View monitor data from linked projects [synthetics-cps-settings]
```{applies_to}
serverless: ga
stack: unavailable
```

On {{serverless-full}}, you can view monitor data from linked projects alongside monitors from the origin project, directly in the Synthetics UI.

This view is read-only, meaning Synthetics builds it from monitor check data when you load the page. Monitor definitions stay as saved objects on the project where they were created. To create, edit, or delete those monitors, manage them directly in the Synthetics UI on that project.

To include these monitors, [link projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md). Refer to [Monitors from linked projects](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-linked-monitors) for details.

## View monitor data from remote clusters [synthetics-ccs-settings]
```{applies_to}
stack: ga 9.5+
serverless: unavailable
```

Previously, the Synthetics UI couldn’t display data from remote clusters through {{ccs-init}}/{{ccr-init}}, so this setup was discouraged. However, synthetics now includes a built-in {{ccs}} integration that lets you view monitor data from remote {{es}} clusters alongside your local monitors, directly in the Synthetics UI.

This view is read-only, meaning that the integration queries each remote cluster’s `synthetics-*` data indices at query time, but monitor definitions and settings stay as saved objects on the {{kib}} where they were created (saved objects aren’t shared across clusters). To create, edit, or delete those monitors, manage them directly in the Synthetics UI on the remote {{kib}}.

To enable it, go to **{{synthetics-app}} → Settings → Remote clusters**. You can select which remote clusters to query and which {{kib}} spaces the settings apply to. Refer to [Remote clusters](/solutions/observability/synthetics/configure-settings.md#synthetics-settings-remote-clusters) for details.

## Do not use the Synthetics UI with {{ccs-init}}/{{ccr-init}} [synthetics-no-ccs-ccr]
```{applies_to}
stack: removed 9.5+
serverless: unavailable
```

Do not use {{ccs}} ({{ccs-init}}) or {{ccr}} ({{ccr-init}}) to federate Synthetics data across deployments. The Synthetics UI manages monitors and settings as {{kib}} saved objects. Because these saved objects are not shared using {{ccs-init}} or {{ccr-init}}, the Synthetics UI doesn't show remote monitor data when you configure {{ccs-init}} or {{ccr-init}} directly. Use the {{synthetics-app}} on the cluster where the monitors are defined.

You can, however, use [Dashboards](/explore-analyze/dashboards.md) or [Discover](/explore-analyze/discover.md) with {{ccs-init}} to query `synthetics-*` indices directly.

## View autodiscovered Heartbeat and Elastic Agent monitors [synthetics-autodiscovered-monitors]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

The {{synthetics-app}} displays monitors run by {{heartbeat}} or {{agent}}, including monitors created through {{k8s}} or Docker autodiscovery. These monitors are read-only because their definitions aren't stored in Synthetics. Use **Display options** on the **Overview** tab to show or hide them.

Monitor results must be stored in `synthetics-*` data streams to appear in the {{synthetics-app}}:

* Monitors managed by {{agent}}, including monitors created through {{k8s}} or Docker autodiscovery, appear automatically.
* Standalone {{heartbeat}} browser monitors appear automatically.
* Standalone {{heartbeat}} HTTP, TCP, and ICMP monitors require a `data_stream` configuration that routes their results to `synthetics-*`. Without this configuration, results are stored in `heartbeat-*` indices and don't appear in the {{synthetics-app}}.

For a standalone lightweight monitor, add this block to its monitor definition:

```yaml
data_stream:
  namespace: default
```

Create, edit, and delete these monitors in their {{heartbeat}} or {{agent}} configuration, not in the {{synthetics-app}}.

## View autodiscovered monitors in earlier versions [synthetics-no-autodiscovery-for-k8s-infra]
```{applies_to}
stack: ga 9.0-9.5
serverless: unavailable
```

In earlier versions, the {{synthetics-app}} only shows monitors created through the [Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md) or a [Synthetics project](/solutions/observability/synthetics/create-monitors-with-projects.md). To monitor infrastructure or {{k8s}} targets through autodiscovery, run [{{heartbeat}} with autodiscovery](beats://reference/heartbeat/configuration-autodiscover.md) and view the results in the deprecated [{{uptime-app}}](/solutions/observability/uptime/index.md).

## Manage large numbers of Synthetic monitors with tags [synthetics-tagging]

When you manage larger numbers of synthetic monitors, use tags to keep them organized. Many of the views in the Synthetics UI are tag-aware and can group data by tag.

## Create custom dashboards [synthetics-custom-dashboards]

If the {{synthetics-app}} doesn't include a UI for your exact needs, you can use [dashboards](/explore-analyze/dashboards.md) to build custom visualizations. For a complete list of fields used by the Synthetics UI, refer to [{{heartbeat}}'s exported fields](beats://reference/heartbeat/exported-fields.md).
