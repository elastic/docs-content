---
navigation_title: Kubernetes Pods and Docker Containers views empty with EDOT
description: Learn why the Kubernetes Pods and Docker Containers views in the Infrastructure Inventory are empty when using EDOT, and how to resolve it.
applies_to:
  stack: ga 9.2+
  serverless: ga
products:
  - id: observability
---

# Kubernetes Pods and Docker Containers views empty when using EDOT [kubernetes-pods-docker-containers-empty-otel]

After configuring the Elastic Distribution of OpenTelemetry (EDOT) Collector to monitor a Kubernetes cluster on version 9.2 or later, several views in the {{kib}} Infrastructure Inventory might appear empty.

## Symptoms [symptoms-kubernetes-pods-docker-containers-empty]

The following views under **Observability → Infrastructure → Inventory** show no data:

- **Kubernetes Pods**
- **Docker Containers**
- The main summary metrics (CPU, memory, traffic) at the top of the Inventory page

The **Hosts** view (also under **Inventory**) works correctly and displays data.

## Cause [cause-kubernetes-pods-docker-containers-empty]

This is expected behavior, not a configuration error in the EDOT Collector.

In version 9.2.0, the `inframetrics` processor was removed from the EDOT Collector Helm charts for Kubernetes and on-premises deployments. Without this processor, data shipped by EDOT is no longer compatible with the Kubernetes Pods and Docker Containers views of the Infrastructure UI, which only support Elastic Agent data formats.

## Resolution [resolution-kubernetes-pods-docker-containers-empty]

Use the out-of-the-box dashboards provided by the Kubernetes and System OpenTelemetry Assets integrations.

**Step 1: Install the required integrations**

Use one of these methods:

- **Recommended: Use the {{kib}} Add Data wizard**

  1. In {{kib}}, click **Add Data** on the Observability home page.
  2. Select **Kubernetes**.
  3. Choose the **OpenTelemetry: Full Observability** guide.
  4. The wizard automatically installs the [Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md) package and provides the correct configuration steps for the EDOT Collector.

- **Manual installation**

  1. In {{kib}}, go to **Data management → Integrations**.
  2. Search for and install the [Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md) integration.
  3. Repeat for the **System OpenTelemetry Assets** integration, which is required for host-level metrics on the nodes.

**Step 2: Access the dashboards**

1. In {{kib}}, go to **Dashboards**.
2. In the search bar, type `OTEL`.
3. Select the **[OTEL][Metrics Kubernetes] Cluster Overview** dashboard to view your cluster's performance.

For a full end-to-end setup guide, refer to [Quickstart: Unified Kubernetes Observability with EDOT](/solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md).

## Workaround [workaround-kubernetes-pods-docker-containers-empty]

You can re-add the `inframetrics` processor as it was configured in versions 9.1.x YAML and Helm charts for the EDOT Kubernetes use case. This is not recommended — the future-proof solution is to use the OpenTelemetry Assets dashboards.
