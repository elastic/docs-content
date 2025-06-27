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

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. The quickest way to get started with this quickstart is using a trial project on [Elastic serverless](https://docs.elastic.co/serverless/quickstart-monitor-hosts-with-otel.html).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* An Elastic Distribution of OpenTelemetry (EDOT) Collector or the upstream OpenTelemetry Collector running on the host.

:::

:::{tab-item} Serverless
:sync: serverless

* An {{observability}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
* An Elastic Distribution of OpenTelemetry (EDOT) Collector or the upstream OpenTelemetry Collector running on the host.

:::
::::

## Install the EDOT Collector [_install_edot_collector]

The EDOT Collector in [Agent mode](opentelemetry://reference/edot-collector/modes.md#edot-collector-as-agent) collects infrastructure and application telemetry data sent by the EDOT SDKs and forwards it to Elastic.

Refer to the [EDOT Quickstarts](opentelemetry://reference/quickstart/index.md) to install the EDOT Collector for your deployment mode.

## Collect application telemetry data [_collect_your_data]

Follow these steps to collect application telemetry data using the EDOT SDKs:

:::::{tab-set}
:group: stack-serverless

::::{tab-item} Elastic Stack
:sync: stack

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Application**, and then select **OpenTelemetry**.
3. Follow the instructions to install the EDOT SDK for your application:

   - [.NET](opentelemetry://reference/edot-sdks/dotnet/setup/index.md)
   - [Java](opentelemetry://reference/edot-sdks/java/setup/index.md)
   - [Node.js](opentelemetry://reference/edot-sdks/nodejs/setup/index.md)
   - [PHP](opentelemetry://reference/edot-sdks/php/setup/index.md)
   - [Python](opentelemetry://reference/edot-sdks/python/setup/index.md)
4. Configure your EDOT SDK to send data to the APM endpoint. The **OpenTelemetry** tab provides the required configuration values.

:::{note}
If your application runs on Kubernetes, the OpenTelemetry operator automatically instruments your application, provided you've added language-specific annotations. Refer to [Auto-instrument applications](opentelemetry://reference/quickstart/self-managed/k8s.md).
:::

::::

::::{tab-item} Serverless
:sync: serverless

1. [Create a new {{obs-serverless}} project](/solutions/observability/get-started.md), or open an existing one.
2. Under **What do you want to monitor?** select **Application**, and then select **OpenTelemetry**.
3. Follow the instructions to install the EDOT SDK for your application:

   - [.NET](opentelemetry://reference/edot-sdks/dotnet/setup/index.md)
   - [Java](opentelemetry://reference/edot-sdks/java/setup/index.md)
   - [Node.js](opentelemetry://reference/edot-sdks/nodejs/setup/index.md)
   - [PHP](opentelemetry://reference/edot-sdks/php/setup/index.md)
   - [Python](opentelemetry://reference/edot-sdks/python/setup/index.md)
4. Configure your EDOT SDK to send data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md). The **OpenTelemetry** tab provides the required configuration values.

:::{note}
If your application runs on Kubernetes, the OpenTelemetry operator automatically instruments your application, provided you've added language-specific annotations. Refer to [Auto-instrument applications](opentelemetry://reference/quickstart/serverless/k8s.md).
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

* Use [machine learning](/solutions/observability/apm/machine-learning.md) to quickly pinpoint anomalous transactions and see the health of any upstream and downstream services.

Refer to the [Elastic Observability](/solutions/observability.md) for a description of other useful features.