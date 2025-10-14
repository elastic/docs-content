---
navigation_title: Serverless feature tiers
applies_to:
  serverless: ga
products:
  - id: observability
---

# {{obs-serverless}} feature tiers

{{obs-serverless}} projects are available in the following tiers, each with a carefully selected set of features to enable common observability operations:

* **Observability Logs Essentials**: Includes everything you need to store and analyze logs at scale.
* **Observability Complete**: Adds full-stack observability capabilities to monitor cloud-native and hybrid environments.

Refer to the [feature comparison table](#obs-subscription-features) for a more detailed comparison between the tiers.

## Feature tier pricing [obs-subscription-pricing]

For pricing information, refer to [Elastic Observability Serverless pricing](https://www.elastic.co/pricing/serverless-observability).

## Feature comparison [obs-subscription-features]

The following table compares features available in Observability Complete and Observability Logs Essentials:

| **Feature** | Observability Complete | Observability Logs Essentials |
|---------|----------------------|-----------------------------------|
| **[Ad-hoc analytics](/explore-analyze/discover.md)** | ✅ | ✅ |
| **[Out-of-the-box dashboards](/explore-analyze/dashboards.md)** | ✅ | ✅ |
| **[Custom dashboards](/explore-analyze/dashboards.md)** | ✅ | ✅ |
| **[Alerting and notifications](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md)** | ✅ | ✅ |
| **[Integrations](https://www.elastic.co/integrations/data-integrations?solution=observability)** | ✅ | ✅ |
| **[Machine learning](/explore-analyze/machine-learning.md)** | ✅ | ❌ |
| **[Rate and pattern analysis](/explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md)** | ✅ | ❌ |
| **[Service level objectives (SLO)](/solutions/observability/incident-management/service-level-objectives-slos.md)** | ✅ | ❌ |
| **[Infrastructure and hosts](/solutions/observability/infra-and-hosts.md)** | ✅ | ❌ |
| **[APM](/solutions/observability/apm/index.md)** | ✅ | ❌ |
| **[AI Assistant](/solutions/observability/observability-ai-assistant.md)** including Elastic Managed LLM | ✅ | ❌ |
| **[Custom knowledge bases](/solutions/observability/observability-ai-assistant.md#obs-ai-kb-ui)** | ✅ | ❌ |
| **[Synthetics testing and browser experience monitoring](/solutions/observability/synthetics/index.md)** | ✅ | ❌ |

## Add data to a serverless project [obs-subscription-ingest]

From the main navigation menu, select **Add data**. Select what you want to monitor and how you want to monitor it, then follow the instructions for your system.

* **Logs Essentials**: For more on adding data to a Logs Essentials project, refer to [Get started with Logs Essentials](../observability/get-started/logs-essentials.md).

* **Observability Complete**: For more on adding data to a Observability Complete project, refer to [Get started with Elastic Observability](../observability/get-started.md).

## Upgrade from Observability Logs Essentials to Observability Complete [obs-subscription-upgrade]

:::{warning}
Upgrading from Observability Logs Essentials to Observability Complete is permanent and is not reversible.
:::

To access the additional features available in Observability Complete, upgrade your Observability project feature tier by completing the following steps:

1. From the [{{ecloud}} Console](https://cloud.elastic.co), select **Manage** next to the Observability Logs Essentials serverless project you want to upgrade.
1. Next to **Project features**, select **Edit**.
1. Select **Observability Complete**.
1. Select **Save** to complete the upgrade.