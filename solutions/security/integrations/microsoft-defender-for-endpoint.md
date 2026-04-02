---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Microsoft Defender for Endpoint

This page explains how to make data from the Microsoft Defender for Endpoint integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.


In order for Microsoft Defender for Endpoint data to appear in these workflows:

* Follow the steps to [set up the Microsoft Defender for Endpoint integration](https://www.elastic.co/docs/reference/integrations/microsoft_defender_endpoint).
* Make sure the integration version is at least 3.0.0.
* Ensure you have `read` privileges for the following index: `security_solution-*.vulnerability_latest`.