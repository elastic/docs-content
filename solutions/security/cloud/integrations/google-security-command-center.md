---
applies_to:
  stack: ga 9.2
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Google Security Command Center

This page explains how to make data from the Google Security Command Center integration appear in the following workflows within {{elastic-sec}}:

- **Findings page**: Data appears on the [Findings page's](/solutions/security/cloud/findings-page.md) **Vulnerabilities** tab and **Misconfigurations** tab.
- **Alert and Entity details flyouts**: Data appears in the **Insights** section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.


In order for Google Security Command Center data to appear in these workflows:

* Follow the steps to [set up the Google Security Command Center integration](https://www.elastic.co/docs/reference/integrations/google_scc).
* Make sure the integration version is at least 2.0.0.
* Ensure you have `read` privileges for the following indices: `security_solution-*.misconfiguration_latest`, `security_solution-*.vulnerability_latest`.