---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/what-is-observability-serverless.html
  - https://www.elastic.co/guide/en/observability/current/index.html
  - https://www.elastic.co/guide/en/kibana/current/observability.html
applies_to:
  stack:
  serverless:
products:
  - id: cloud-serverless
  - id: observability
  - id: kibana
  - id: edot-collector
---

# Observability

{{observability}} accelerates problem resolution with open, flexible, and unified observability powered by advanced machine learning and analytics. Elastic ingests all operational and business telemetry and correlates for faster root cause detection.

## Get started [_get_started]

Read the following quickstart guides to get started with {{observability}}:

* [**Get started**](/solutions/observability/get-started.md): Discover more about our observability features and how to get started.

Ingest observability data using OpenTelemetry:

* [**Quickstart: Monitor hosts with OpenTelemetry**](/solutions/observability/get-started/quickstart-monitor-hosts-with-opentelemetry.md)
* [**Quickstart: Monitor Kubernetes with OpenTelemetry**](/solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md)
* [**Quickstart: Send data to the Elastic Cloud Managed OTLP Endpoint**](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md)

Use the Elastic Agent to ingest data:

* [**Quickstart: Monitor hosts with Elastic Agent**](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md): Scan your host to detect and collect logs and metrics.
* [**Quickstart: Monitor your Kubernetes cluster with Elastic Agent**](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md): Create the Kubernetes resources that are required to monitor your cluster infrastructure.

Explore your data:

* [**Get started with Logs**](/solutions/observability/logs/get-started-with-system-logs.md): Add your log data to {{observability}} and start exploring your logs.
* [**Get started with traces and APM**](/solutions/observability/apm/get-started.md): Collect Application Performance Monitoring (APM) data and visualize it in real time.
* [**Get started with metrics**](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md): Add your metrics data to {{observability}} and visualize it in real time.

## How to [_how_to]

After you've collected your data, you can:

* [**Explore log data**](/solutions/observability/logs/discover-logs.md): Use Discover to explore your log data.
* [**Trigger alerts and triage problems**](/solutions/observability/incident-management/create-manage-rules.md): Create rules to detect complex conditions and trigger alerts.
* [**Track and deliver on your SLOs**](/solutions/observability/incident-management/service-level-objectives-slos.md): Measure key metrics important to the business.
* [**Detect anomalies and spikes**](/explore-analyze/machine-learning/anomaly-detection.md): Find unusual behavior in time series data.
* [**Monitor application performance**](/solutions/observability/apm/index.md): Monitor your software services and applications in real time.
* [**Integrate with OpenTelemetry**](/solutions/observability/apm/use-opentelemetry-with-apm.md): Reuse existing APM instrumentation to capture logs, traces, and metrics.
* [**Monitor your hosts and services**](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md): Get a metrics-driven view of your hosts backed by an interface called Lens.