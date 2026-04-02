---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/otlp-visualize.html
applies_to:
  serverless:
---

# Visualize OpenTelemetry data

:::{tip}
To ingest OpenTelemetry data, refer to [](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md).
:::

## Get creative with Discover

Discover allows you to quickly search and filter your data, get information about the structure of the fields in your data, and display your findings in a visualization.
Find **Discover** in your {{obs-serverless}} project's UI under **Analyze** --> **Discover**.

Attributes and resource attributes are prefixed with `attributes.*` and `resource.attributes.*`.
You can correlate all signals with a single `resource.attributes.*`.

:::{image} ../images/resource-attrs.png
:screenshot:
:alt: resource attributes
:::

Refer to [](/explore-analyze/discover.md) to learn more.

## Monitor application performance

The Applications UI allows you to monitor your software services and applications in real-time. You can visualize detailed performance information on your services, identify and analyze errors, and monitor host-level metrics.

## Check the health of your infrastructure

To access the **Hosts** page, in your {{obs-serverless}} project, go to
**Infrastructure** → **Hosts**.

On the Hosts page, you can view health and performance metrics to help you quickly:

* Analyze and compare hosts without having to build new dashboards.
* Identify which hosts trigger the most alerts.
* Troubleshoot and resolve issues quickly.

:::{image} ../images/hosts-ui-otlp.png
:screenshot:
:alt: resource attributes
:::

See [](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md) to learn more.

### (Optional) Install the OpenTelemetry Assets integration

Install the OpenTelemetry Assets integrations to access the "[OTEL][Metrics Kubernetes] Cluster Overview" dashboard.

In your {{obs-serverless}} project, go to **Integrations** and toggle **Display beta integrations**.
Search for "OpenTelemetry" to select and install **Kubernetes OpenTelemetry Assets**.
