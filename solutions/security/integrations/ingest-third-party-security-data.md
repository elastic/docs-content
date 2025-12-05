---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-third-party-cloud-security-data.html
  - https://www.elastic.co/guide/en/serverless/current/ingest-third-party-cloud-security-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Ingest third-party security data

This section describes how to ingest security data from third-party tools into {{es}}. Once ingested, this data can provide additional context and enrich your {{elastic-sec}} workflows.

You can ingest both third-party workload protection data and third-party security posture and vulnerability data. 

:::{note}
This page lists only third-party integrations that collect data that can directly appear in {{elastic-sec}} workflows. For a complete list of integrations, many of which can collect security-related data, refer to [Integrations](https://www.elastic.co/docs/reference/integrations).
:::


## Ingest third-party workload protection data [_ingest_third_party_workload_protection_data]

You can ingest third-party security alerts into {{elastic-sec}} to view them on the [Alerts page](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md#alerts-page) and incorporate them into your triage and threat hunting workflows.

* Learn to [ingest alerts from Sysdig Falco](/solutions/security/integrations/cncf-falco.md).


## Ingest third-party security posture and vulnerability data [_ingest_third_party_security_posture_and_vulnerability_data]

You can ingest third-party data into {{elastic-sec}} to review and investigate it alongside data collected by {{elastic-sec}}'s native integrations. Once ingested, security posture and vulnerability data appears on the [**Findings**](/solutions/security/cloud/findings-page.md) page and in the [entity details](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-details-flyout) and [alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) flyouts.

::::{note}
Data from third-party integrations does not appear on the [CNVM dashboard](/solutions/security/cloud/cnvm-dashboard.md) or the [Cloud Posture dashboard](/solutions/security/dashboards/cloud-security-posture-dashboard.md),
::::

Data from each of the following integrations can feed into at least some of these workflows:

* [AWS Config](/solutions/security/integrations/aws-config.md)
* [AWS Inspector](/solutions/security/integrations/aws-inspector.md)
* [AWS Security Hub](/solutions/security/integrations/aws-security-hub.md)
* [Google Security Command Center](/solutions/security/integrations/google-security-command-center.md)
* [Microsoft Defender for Cloud](/solutions/security/integrations/microsoft-defender-for-cloud.md)
* [Microsoft Defender for Endpoint](/solutions/security/integrations/microsoft-defender-for-endpoint.md)
* [Microsoft Defender XDR](/solutions/security/integrations/microsoft-defender-xdr.md)
* [Qualys VMDR](/solutions/security/integrations/qualys.md)
* [Rapid7 InsightVM](/solutions/security/integrations/rapid7.md)
* [Tenable VM](/solutions/security/integrations/tenablevm.md)
* [Wiz](/solutions/security/integrations/wiz.md)
