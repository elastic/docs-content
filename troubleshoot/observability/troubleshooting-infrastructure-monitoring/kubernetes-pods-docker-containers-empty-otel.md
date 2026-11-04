---
navigation_title: Kubernetes Pods and Docker Containers views empty with {{edot}}
description: Learn why the Kubernetes Pods and Docker Containers views in the Infrastructure Inventory are empty when using {{edot}}, and how to resolve it.
applies_to:
  stack: ga 9.2+
  serverless: ga
products:
  - id: observability
---

# Kubernetes Pods and Docker Containers views empty when using {{edot}} [kubernetes-pods-docker-containers-empty-otel]

After configuring {{agent}} to monitor a Kubernetes cluster on version 9.2 or later, several views in the {{kib}} Infrastructure Inventory might appear empty.

## Symptoms [symptoms-kubernetes-pods-docker-containers-empty]

Under **{{observability}} → Infrastructure → Inventory**, the **Docker Containers** view shows no data, and so do the main summary metrics (CPU, memory, traffic) at the top of the Inventory page.

:::{note}
:applies_to: {"stack": "ga 9.2, removed 9.6", "serverless": "removed"}
Like the **Docker Containers** view, the **{{k8s}} Pods** view shows no data. From 9.6, the **{{k8s}} Pods** view supports OpenTelemetry, so an empty view has a different cause. Refer to [Resolution for {{k8s}} Pods](#resolution-kubernetes-pods-empty-otel) for how to troubleshoot it on 9.6 and later.
:::

The **Hosts** view (also under **Inventory**) works correctly and displays data.

## Cause [cause-kubernetes-pods-docker-containers-empty]

For the Docker Containers view, this is expected behavior, not a configuration error in {{agent}}.

In version 9.2.0, the `inframetrics` processor was removed from the {{agent}} Helm charts for {{k8s}} and on-premises deployments. Without this processor, data shipped by {{edot}} is not in the format the Docker Containers view of the Infrastructure UI expects.

:::{note}
:applies_to: {"stack": "ga 9.2, removed 9.6", "serverless": "removed"}
The {{k8s}} Pods view is affected for the same reason. From 9.6, the Infrastructure UI reads {{k8s}} pod metrics collected by the `kubeletstats` receiver directly, so this cause no longer applies to pods.
:::

## Resolution for {{k8s}} Pods [resolution-kubernetes-pods-empty-otel]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

The Infrastructure UI shows {{k8s}} pods collected using OpenTelemetry. If the **{{k8s}} Pods** view is empty, check the following:

:::::{stepper}

::::{step} Check the selected schema
Set **Show** to **{{k8s}} Pods** and confirm the **Schema** menu is set to **OpenTelemetry**. If it's set to **Elastic System Integration**, you only see pods collected by the {{k8s}} integration. Refer to [Select the data collection schema](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#pod-schema-selector) for how the **Schema** menu works.
::::

::::{step} Check your time range
The **Schema** menu only offers the schemas that have data in the current time range. Widen the time range if you expect OpenTelemetry pods but can't select the schema.
::::

::::{step} Check that pod metrics are arriving
Confirm that documents with `data_stream.dataset: kubeletstatsreceiver.otel` exist for your time range. If none exist, verify the `kubeletstats` receiver in your Collector configuration. Refer to the [default {{k8s}} configuration](elastic-agent://reference/edot-collector/config/default-config-k8s.md) for the expected receiver settings.
::::

::::{step} Check Group by
Switching **Schema** doesn't clear **Group by**. A field left over from the other schema can leave the map empty. Clear or reselect **Group by**.
::::

:::::

## Resolution for Docker Containers [resolution-kubernetes-pods-docker-containers-empty]

Use the out-of-the-box dashboards provided by the Kubernetes and System OpenTelemetry Assets integrations.

:::::{stepper}

::::{step} Install the required integrations
Use one of these methods:

- **Recommended: Use the {{kib}} Add Data wizard**

  1. In {{kib}}, click **Add Data** on the Observability home page.
  2. Select **Kubernetes**.
  3. Choose the **OpenTelemetry: Full Observability** guide.
  4. The wizard automatically installs the [Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md) package and provides the correct configuration steps for {{agent}}.

- **Manual installation**

  1. In {{kib}}, go to **Data management → Integrations**.
  2. Search for and install the [Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md) integration.
  3. Repeat for the **System OpenTelemetry Assets** integration, which is required for host-level metrics on the nodes.
::::

::::{step} Access the dashboards
1. In {{kib}}, go to **Dashboards**.
2. In the search bar, type `OTEL`.
3. Select the **[OTEL][Metrics Kubernetes] Cluster Overview** dashboard to view your cluster's performance.
::::

:::::

For a full end-to-end setup guide, refer to [Quickstart: Unified Kubernetes Observability with {{edot}}](/solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md).

On {{stack}} versions before 9.6, use these dashboards for {{k8s}} pods as well.

## Workaround [workaround-kubernetes-pods-docker-containers-empty]

You can re-add the `inframetrics` processor as it was configured in versions 9.1.x YAML and Helm charts for the {{edot}} Kubernetes use case. This is not recommended — the future-proof solution is to use the OpenTelemetry Assets dashboards.
