---
description: Learn how to monitor your application performance using the Elastic Distribution of OpenTelemetry (EDOT) SDKs and Elastic APM.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Quickstart: Monitor your application performance [quickstart-monitor-your-application-performance]

In this quickstart guide, you’ll learn how to instrument your application using the Elastic Distribution of OpenTelemetry (EDOT) SDKs. You’ll also learn how to use {{observability}} features to gain deeper insight into your application telemetry data after collecting it.

## Prerequisites [_prerequisites]

::::{applies-switch}

:::{applies-item} stack:

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. The quickest way to get started with this quickstart is using a trial project on [Elastic serverless](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* An Elastic Distribution of OpenTelemetry (EDOT) Collector or the contrib OpenTelemetry Collector running on the host.

:::

:::{applies-item} serverless:

* An {{observability}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
* An Elastic Distribution of OpenTelemetry (EDOT) Collector or the contrib OpenTelemetry Collector running on the host.

:::
::::

## Install the EDOT Collector [_install_edot_collector]

The EDOT Collector in [Agent mode](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-agent) collects infrastructure and application telemetry data sent by the EDOT SDKs and forwards it to Elastic.

Refer to the [EDOT Quickstarts](/solutions/observability/get-started/opentelemetry/quickstart/index.md) to install the EDOT Collector for your deployment mode.

## Collect application telemetry data [_collect_your_data]

Follow these steps to collect application telemetry data using the EDOT SDKs:

:::::{applies-switch}

::::{applies-item} stack:

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Application**, and then select **OpenTelemetry**.
3. Follow the instructions to install the EDOT SDK for your application:

   - [Android](apm-agent-android://reference/edot-android/index.md)
   - [.NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
   - [iOS](apm-agent-ios://reference/edot-ios/index.md)
   - [Java](elastic-otel-java://reference/edot-java/setup/index.md)
   - [Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
   - [PHP](elastic-otel-php://reference/edot-php/setup/index.md)
   - [Python](elastic-otel-python://reference/edot-python/setup/index.md)
4. Configure your EDOT SDK to send data to the APM endpoint. The **OpenTelemetry** tab provides the required configuration values.

:::{note}
If your application runs on Kubernetes, the OpenTelemetry operator automatically instruments your application, provided you've added language-specific annotations. Refer to [Auto-instrument applications](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md).
:::

::::

::::{applies-item} serverless:

1. [Create a new {{obs-serverless}} project](/solutions/observability/get-started.md), or open an existing one.
2. Under **What do you want to monitor?** select **Application**, and then select **OpenTelemetry**.
3. Follow the instructions to install the EDOT SDK for your application:

   - [Android](apm-agent-android://reference/edot-android/index.md)
   - [.NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
   - [iOS](apm-agent-ios://reference/edot-ios/index.md)
   - [Java](elastic-otel-java://reference/edot-java/setup/index.md)
   - [Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
   - [PHP](elastic-otel-php://reference/edot-php/setup/index.md)
   - [Python](elastic-otel-python://reference/edot-python/setup/index.md)
4. Configure your EDOT SDK to send data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md). The **OpenTelemetry** tab provides the required configuration values.
5. (Optional) Activate Central Configuration to configure your EDOT SDKs from within {{product.kibana}}. Refer to [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md).

:::{note}
If your application runs on {{k8s}}, the OpenTelemetry operator automatically instruments your application, provided you've added language-specific annotations. Refer to [Auto-instrument applications](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md).
:::

::::
:::::

## Gain deeper insight into your application data  [_get_value_out_of_your_data]

After using the **Applications** page and **Discover** to confirm you’ve ingested all the application traces, metrics, and logs you want to monitor, use Elastic {{observability}} to gain deeper insight into your application data with the following capabilities and features:

* In the [Applications UI](/solutions/observability/apm/view-analyze-data.md), analyze and compare data collected from your application. You can also:

    * [Drill down into data](/solutions/observability/apm/drill-down-into-data.md) to view details about specific transactions and spans.
    * [Find transaction latency and failure correlations](/solutions/observability/apm/find-transaction-latency-failure-correlations.md) to identify root causes.
    * [Create alerts](/solutions/observability/apm/create-apm-rules-alerts.md) that notify you when an anomaly is detected or a metric exceeds a given value.

* In [Service Map](/solutions/observability/apm/service-map.md), explore how your services are connected and check health indicators. You can also:

* Use [machine learning](/solutions/observability/apm/machine-learning.md) to quickly pinpoint anomalous transactions and see the health of any contrib and downstream services.

Refer to the [Elastic Observability](/solutions/observability.md) for a description of other useful features.
