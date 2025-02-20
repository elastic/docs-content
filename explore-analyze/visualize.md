---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_panels_and_visualizations.html
---

# Panels and visualizations [_panels_and_visualizations]

{{kib}} provides many options to create panels with visualizations of your data and add content to your dashboards. From advanced charts, maps, and metrics to plain text and images, multiple types of panels with different capabilities are available.

Use one of the editors to create visualizations of your data. Each editor offers various capabilities.

$$$panels-editors$$$

| **Content** | **Panel type** | **Description** |
| --- | --- | --- |
| Visualizations | |  |
| [Lens](visualize/lens.md) | The default editor for creating powerful [charts](visualize/supported-chart-types.md) in {{kib}} |
| [ES&#124;QL](/explore-analyze/query-filter/languages/esql-kibana.md) | Create visualizations from ES&#124;QL queries |
| [Maps](visualize/maps.md) | Create beautiful displays of your geographical data |
| [Field statistics](visualize/field-statistics.md) | Add a field statistics view of your data to your dashboards |
| [Custom visualizations](visualize/custom-visualizations-with-vega.md) | Use Vega to create new types of visualizations |
| Annotations and navigation | | |
| [Text](visualize/text-panels.md) | Add context to your dashboard with markdown-based **text** |
| [Image](visualize/image-panels.md) | Personalize your dashboard with custom images |
| [Links](visualize/link-panels.md) | Add links to other dashboards or to external websites |
| Machine Learning and Analytics | | |
| [Anomaly swim lane](machine-learning/machine-learning-in-kibana/xpack-ml-anomalies.md) | Display the results from machine learning anomaly detection jobs |
| [Anomaly chart](machine-learning/machine-learning-in-kibana/xpack-ml-anomalies.md) | Display an anomaly chart from the **Anomaly Explorer** |
| [Single metric viewer](machine-learning/machine-learning-in-kibana/xpack-ml-anomalies.md) | Display an anomaly chart from the **Single Metric Viewer** |
| [Change point detection](machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection) | Display a chart to visualize change points in your data |
| Observability | | |
| [SLO overview](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize a selected SLO’s health, including name, current SLI value, target, and status |
| [SLO Alerts](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize one or more SLO alerts, including status, rule name, duration, and reason. In addition, configure and update alerts, or create cases directly from the panel |
| [SLO Error Budget](/solutions/observability/incident-management/service-level-objectives-slos.md) | Visualize the consumption of your SLO’s error budget |
| Legacy | | |
| [Log stream](https://www.elastic.co/guide/en/kibana/current/observability.html#logs-app) (deprecated) | Display a table of live streaming logs |
| [Aggregation based](visualize/legacy-editors/aggregation-based.md) | While these panel types are still available, we recommend to use [Lens](visualize/lens.md) |
| [TSVB](visualize/legacy-editors/tsvb.md) |
