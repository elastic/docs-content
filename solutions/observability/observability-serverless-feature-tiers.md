---
navigation_title: Serverless feature tiers
applies_to:
  serverless: ga
products:
  - id: observability
---

# {{obs-serverless}} feature tiers

{{obs-serverless}} projects are available in the following tiers, each with a carefully selected set of features to enable common observability operations:

* **Observability Logs Essentials**: Provides everything you need to ingest and analyze your logs. This includes **[Discover](/solutions/observability/logs/discover-logs.md)** to explore your logs, pre-configured and custom dashboards to visualize and gain insight from your logs, and alerting to notify you of potential issues.
* **Observability Complete**: Provides full-stack observability capabilities to monitor cloud-native and hybrid environments. This includes everything in the Logs Essentials tier, as well as machine learning and AI capabilities, APM, and more.

Refer to the [feature comparison table](#obs-subscription-features) for a more detailed comparison between the tiers.

## Subscription tier pricing [obs-subscription-pricing]

For pricing information, refer to [Elastic Observability Serverless pricing](https://www.elastic.co/pricing/serverless-observability).

## Feature comparison [obs-subscription-features]

The following table compares features available in Observability Complete and Observability Logs Essentials:

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
| **[AI Assistant](/solutions/observability/observability-ai-assistant.md)** including Elastic Managed LLM | ✅ | ❌ |
| **[Custom knowledge bases](/solutions/observability/observability-ai-assistant.md#obs-ai-kb-ui)** | ✅ | ❌ |
| **[Synthetics testing and browser experience monitoring](/solutions/observability/synthetics/index.md)** | ✅ | ❌ |

## Upgrade from Observability Logs Essentials to Observability Complete [obs-subscription-upgrade]

:::{warning}
Upgrading from Observability Logs Essentials to Observability Complete is permanent and is not reversible.
:::

To access the additional features available in Observability Complete, upgrade your Observability Logs Essentials subscription by completing the following steps:

1. From the [{{ecloud}} Console](https://cloud.elastic.co), select **Manage** next to the Observability Logs Essentials serverless project you want to upgrade.
1. Next to **Project features**, select **Edit**.
1. Select **Observability Complete**.

% not sure if there is a last step here (like users needing to save) because i'm not able to see a project starting in logs essentials.

## Ingest data into a Logs Essentials project [obs-subscription-ingest]

Use the [Elastic Cloud Managed OTLP Endpoint](opentelemetry://reference/motlp.md) to ingest data into your Logs Essentials project. For more information on getting started, refer to the [Elastic Cloud Serverless quickstart](opentelemetry://reference/quickstart/serverless/index.md).