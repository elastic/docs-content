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

# Wiz

This page explains how to make data from the Wiz integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab and the [Misconfiguations](/solutions/security/cloud/findings-page.md) tab.
- **Alert and Entity details flyouts**: Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).


In order for Wiz data to appear in these workflows:

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

Your Wiz data should now appear throughout {{elastic-sec}}.

:::{image} /solutions/images/security-wiz-findings.png
:alt: Wiz data on the Findings page
:::
