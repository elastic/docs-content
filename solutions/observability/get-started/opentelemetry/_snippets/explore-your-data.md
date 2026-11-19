After data starts flowing, confirm that it's arriving, then use {{product.observability}} to explore and act on it.

**Dashboards**
:   Go to **Dashboards** and open a dashboard that the content packs installed, such as **[OTel] Hosts Overview**, **[Kubernetes OTel] Overview**, or **[Metrics Docker] Overview**, depending on which packs you installed. These dashboards are the quickest way to confirm that metrics are arriving.

**Metrics and infrastructure**
:   In the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md), view your hosts and their metrics. For {{k8s}} pods and Docker containers, use the content pack dashboards instead: the Infrastructure UI views for them don't show {{edot}} data in all versions. Refer to [{{k8s}} Pods and Docker Containers views empty](/troubleshoot/observability/troubleshooting-infrastructure-monitoring/kubernetes-pods-docker-containers-empty-otel.md) for details. You can also [create alerts](/solutions/observability/incident-management/create-manage-rules.md) that notify you when a metric exceeds a given value.

    For the full set of metrics exploration options, including which metrics UI to use for your version, refer to [Explore metrics](/solutions/observability/metrics/explore.md).

**Logs**
:   In [Discover](/solutions/observability/logs/discover-logs.md) in {{kib}}, search and filter your log data, inspect the structure of log fields, and display your findings in a visualization. You can also [monitor log data set quality](/solutions/observability/data-set-quality-monitoring.md) to find degraded documents and [run a pattern analysis](/explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#log-pattern-analysis) to find patterns in unstructured log messages.

**Traces**
:   If you instrumented your applications, open the [Service inventory](/solutions/observability/apm/services.md) under **Applications** to confirm that your services appear. Open a service to view its transactions, errors, and dependencies, use the [Traces](/solutions/observability/apm/traces-ui.md) view to follow a request end to end, and use the [service map](/solutions/observability/apm/service-map.md) to see how your services connect.

**{{ml-cap}}**
:   Use [{{ml}}](/explore-analyze/machine-learning/machine-learning-in-kibana.md) to apply predictive analytics: [detect anomalies](/explore-analyze/machine-learning/anomaly-detection.md) by comparing real-time and historical data, [analyze log spikes and drops](/explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#log-rate-analysis), and [detect change points](/explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection) in your time series data.

If data is missing from any of these views, refer to [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md).
