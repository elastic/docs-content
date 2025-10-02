---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_panels_and_visualizations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Panels and visualizations [_panels_and_visualizations]

{{kib}} provides many options to create panels with visualizations of your data and add content to your dashboards. From advanced charts, maps, and metrics to plain text and images, multiple types of panels with different capabilities are available.

Use one of the editors to create visualizations of your data. Each editor offers various capabilities.

$$$panels-editors$$$

| **Content** | **Panel type** | **Description** |
| --- | --- | --- |
| Visualizations | [Lens](visualize/lens.md) | Create powerful [charts](visualize/supported-chart-types.md) in {{kib}}. This is the default editor. |
|  | [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md) | Create visualizations from {{esql}} queries |
|  | [Maps](visualize/maps.md) | Create beautiful displays of your geographical data |
|  | [Alerts](visualize/alert-panels.md) | View Observability or Security alerts in your dashboard |
|  | [Custom visualizations](visualize/custom-visualizations-with-vega.md) | Use Vega to create new types of visualizations |
|  | | |
| Annotations and navigation | [Collapsible sections](dashboards/arrange-panels.md#collapsible-sections) | Organize your dashboard into sections that can be collapsed and save loading time |
|  | [Markdown text](visualize/text-panels.md) | Add context to your dashboard with markdown-based **text** |
|  | [Image](visualize/image-panels.md) | Personalize your dashboard with custom images |
|  | [Links](visualize/link-panels.md) | Add links to other dashboards or to external websites |
|  | | |
| Machine Learning and Analytics | [Anomaly swim lane](machine-learning/anomaly-detection/ml-ad-view-results.md) | Display the results from machine learning anomaly detection jobs |
|  | [Anomaly chart](machine-learning/anomaly-detection/ml-ad-view-results.md) | Display an anomaly chart from the **Anomaly Explorer** |
|  | [Single metric viewer](machine-learning/anomaly-detection/ml-ad-view-results.md) | Display an anomaly chart from the **Single Metric Viewer** |
|  | [Change point detection](machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection) | Display a chart to visualize change points in your data |
|  | | |
| Observability | [SLO overview](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize a selected SLO’s health, including name, current SLI value, target, and status |
|  | [SLO Alerts](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize one or more SLO alerts, including status, rule name, duration, and reason. In addition, configure and update alerts, or create cases directly from the panel. |
|  | [SLO Error Budget](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize the consumption of your SLO’s error budget |
|  | | |
| Legacy | [Aggregation based](visualize/legacy-editors/aggregation-based.md) | Create visualizations including area, line, and pie charts and split them up to three aggregation levels. While these panel types are still available, we recommend using [Lens](visualize/lens.md) instead. |
|  | [TSVB](visualize/legacy-editors/tsvb.md) | Visualize time-based data through various panel types |

:::{note}
Legacy panel types only appear in the **Add panel** dashboard menu if you already have such panels in your dashboards. If you have never used these panel types, use Lens instead.
:::