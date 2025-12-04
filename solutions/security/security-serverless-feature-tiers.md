---
navigation_title: Serverless feature tiers
applies_to:
  serverless: ga
products:
  - id: security
---

# {{elastic-sec}} feature tiers

{{sec-serverless}} projects are available in the following tiers, each with a carefully selected set of features to enable security operations:

* **Elastic AI SOC Engine (EASE)**: Use Elastic's AI-powered threat hunting and alert triage capabilities to complement a third-party SIEM deployment. 
* **Security Analytics Essentials**: Everything most organizations need to operationalize traditional SIEM.
* **Security Analytics Complete**: All the capabilities included in **Security Analytics Essentials**, plus additional features that provide a more complete toolset.

Both of the **Security Analytics** tiers have **Add-on options** for endpoint protection and cloud protection.

Refer to the [feature comparison table](#sec-subscription-features) for a more detailed comparison between the tiers.

## Feature tier pricing [sec-subscription-pricing]

For pricing information, refer to [Elastic Security Serverless pricing](https://www.elastic.co/pricing/serverless-security).

## Security Analytics feature comparison [sec-subscription-features]

The following table compares features available in each feature tier:

| **Feature Name** | **Security Analytics Complete** | **Security Analytics Essentials** | **EASE** |
| :--- | :---: | :---: | :---: |
| **[Cases](/solutions/security/investigate/cases.md) (collect and share information)** | ✅ | ✅ | ✅ |
| **Collaboration workflows** | ✅ | ✅ | ✅ |
| **[Native integrations](https://www.elastic.co/docs/reference/integrations) with third-party SIEM and EDR platforms** | ✅ | ✅ | ✅ |
| **Out of the box [dashboards](/solutions/security/dashboards.md)** | ✅ | ✅ | ❌ |
| **Prebuilt and custom [detection rules](/solutions/security/detect-and-alert.md)** | ✅ | ✅ | ❌ |
| **[Machine learning](/solutions/security/advanced-entity-analytics/anomaly-detection.md)** | ✅ | ✅ | ❌ |
| **[Triage](/solutions/security/detect-and-alert/manage-detection-alerts.md), [investigation](/solutions/security/investigate.md), and [hunting](https://www.elastic.co/security/threat-hunting)** | ✅ | ✅ | ❌ |
| **[Threat intelligence integration](/solutions/security/get-started/enable-threat-intelligence-integrations.md)** | ✅ | ✅ | ❌ |
| **[AI Assistant](/solutions/security/ai/ai-assistant.md) with custom knowledge support** | ✅ | ❌ | ✅ |
| **[Attack Discovery](/solutions/security/ai/attack-discovery.md) (AI-powered alert correlation)** | ✅ | ❌ | ✅ |
| **[Automatic Import](/solutions/security/get-started/automatic-import.md) (AI-powered custom integrations)** | ✅ | ❌ | ❌ |
| **[Entity analytics / UEBA](/solutions/security/advanced-entity-analytics.md)** | ✅ | ❌ | ❌ |
| **Extended security content** | ✅ | ❌ | ❌ |
| **Threat intelligence management** | ✅ | ❌ | ❌ |


## Add-on options

Both the **Security Analytics Complete** and **Security Analytics Essentials** feature tiers optional add-ons for **Endpoint protection** and **Cloud protection**. The features included in each add on vary by feature tier, as follows:

**Endpoint protection add-on:**

| Feature Name | Complete | Essentials |
| :--- | :---: | :---: |
| **[Malware prevention](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection)** | ✅ | ✅ |
| **[Ransomware protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#ransomware-protection)** | ✅ | ✅ |
| **[Memory](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#memory-protection) and [behavior prevention](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#behavior-protection)** | ✅ | ✅ |
| **[Endpoint response actions](/solutions/security/endpoint-response-actions.md)** | ✅ | ❌ |
| **Advanced [endpoint policy management](/solutions/security/manage-elastic-defend/endpoints.md)** | ✅ | ❌ |

**Cloud protection add-on:**

| Feature Name | Complete | Essentials |
| :--- | :---: | :---: |
| **[Workload runtime protection](/solutions/security/cloud/cloud-workload-protection-for-vms.md)** | ✅ | ✅ |
| **[Cloud native posture management](/solutions/security/cloud/security-posture-management-overview.md) for Kubernetes, AWS, GCP & more** | ✅ | ✅ |
| **Drift protection for containers** | ✅ | ❌ |
| **[Response actions](/solutions/security/endpoint-response-actions.md)** | ✅ | ❌ |


## Upgrade to a higher feature tier [sec-subscription-upgrade]

:::{warning}
Upgrading a project to a higher feature tier is permanent.
:::

To access the additional features available in a higher feature tier:

1. From the [{{ecloud}} Console](https://cloud.elastic.co), select **Manage** next to the {{serverless-short}} project you want to upgrade.
1. Next to **Project features**, select **Edit**.
1. Select your desired feature tier.
1. Select **Save** to complete the upgrade.