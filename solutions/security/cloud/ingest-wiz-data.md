---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-wiz-data.html
  - https://www.elastic.co/guide/en/serverless/current/ingest-wiz-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Ingest Wiz data

In order to enrich your {{elastic-sec}} workflows with third-party cloud security posture and vulnerability data collected by Wiz:

* Follow the steps to [set up the Wiz integration](https://docs.elastic.co/en/integrations/wiz).
* Make sure the integration version is at least 2.0.1.
* Ensure you have `read` privileges for the following indices: `security_solution-*.misconfiguration_latest`, `security_solution-*.vulnerability_latest`.
* While configuring the Wiz integration, turn on **Cloud Configuration Finding logs** and **Vulnerability logs**. We recommend you also set the **Initial Interval** values for both settings to `2160h` (equivalent to 90 days) to ingest existing logs.

:::{image} /solutions/images/security-wiz-config-finding-logs.png
:alt: Wiz integration settings showing the findings toggle
:::

:::{image} /solutions/images/security-wiz-config-vuln-logs.png
:alt: Wiz integration settings showing the vulnerabilities toggle
:::

After you’ve completed these steps, Wiz data will appear on the [Misconfiguations](/solutions/security/cloud/findings-page.md) and [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tabs of the Findings page.

:::{image} /solutions/images/security-wiz-findings.png
:alt: Wiz data on the Findings page
:::

Any available findings data will also appear in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) for related alerts. If alerts are present for a user or host that has findings data from Wiz, the findings will appear on the [entity details flyout](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-details-flyout).
