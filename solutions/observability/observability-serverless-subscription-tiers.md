---
navigation_title: Serverless subscription tiers
applies_to:
  serverless: ga
products:
  - id: observability
---

# {{obs-serverless}} subscription tiers

{{obs-serverless}} projects are available in the following tiers of carefully selected features to enable common observability operations:

* **Observability Logs Essentials**: everything you need to store and analyze logs at scale.
* **Observability Complete**: full-stack observability capabilities to monitor cloud-native and hybrid environments.

For pricing information, refer to [Elastic Observability Serverless pricing](https://www.elastic.co/pricing/serverless-observability).

## Feature comparison

The following table provides an in-depth feature comparison between Observability Complete and Observability Logs Essentials:

| **Feature** | Observability Complete | Observability Logs Essentials |
|---------|----------------------|-----------------------------------|
| **Ad-hoc analytics** | ✅ | ✅ |
| **[Out-of-the-box dashboards](/explore-analyze/dashboards.md)** | ✅ | ✅ |
| **[Custom dashboards](/explore-analyze/dashboards/create-dashboard.md)** | ✅ | ✅ |
| **[Alerting and notifications](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md)** | ✅ | ✅ |
| **[Integrations](https://www.elastic.co/integrations/data-integrations?solution=observability)** | ✅ | ✅ |
| **[Machine learning](/explore-analyze/machine-learning.md)** | ✅ | ❌ |
| **Rate and pattern analysis** | ✅ | ❌ |
| **[Service level objectives (SLO)](/solutions/observability/incident-management/service-level-objectives-slos.md)** | ✅ | ❌ |
| **Multi-signal investigations** | ✅ | ❌ |
| **[APM](/solutions/observability/apm/index.md)** | ✅ | ❌ |
| **[AI Assistant](/solutions/observability/observability-ai-assistant.md)** and Elastic Managed LLM | ✅ | ❌ |
| **[Custom knowledge bases](/solutions/observability/observability-ai-assistant.md#obs-ai-kb-ui)** | ✅ | ❌ |
| **[Synthetics testing and browser experience monitoring](/solutions/observability/synthetics/index.md)** | ✅ | ❌ |

## Upgrade from Observability Logs Essentials to Observability Complete

:::{warning}
Upgrading from Observability Logs Essentials to Observability Complete is permanent and cannot be reversed.
:::

To access the additional features available in Observability Complete, upgrade your Observability Logs Essentials subscription by completing the following steps:

1. From the [{{ecloud}} Console](https://cloud.elastic.co), select **Manage** next to the Observability Logs Essentials serverless project you want to upgrade.
1. Next to **Project features**, select **Edit**.
1. Select **Observability Complete**.

## Ingest data into a Logs Essentials project

Use the [Elastic Cloud Managed OTLP Endpoint](opentelemetry://reference/motlp.md) to ingest data into your Logs Essentials project. For more information, refer to the [Elastic Cloud Serverless quickstart](opentelemetry://quickstart/serverless).