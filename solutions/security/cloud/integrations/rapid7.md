---
applies_to:
  stack: all 
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---


# Rapid7
This page explains how to make data from the Rapid7 InsightVM integration (Rapid7) appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.


In order for Rapid7 data to appear in these workflows:

- Ensure you have read privileges for the following index: `security_solution-*.vulnerability_latest`.
- Follow the steps to [set up the Rapid7 integration](https://www.elastic.co/docs/reference/integrations/rapid7_insightvm).
- ({{stack}} users) Ensure you're on at least v9.1.
- Make sure the Rapid7 version is at least 2.0.0.

:::{note}
You can ingest data from the Rapid7 integration for other purposes without following these steps.
:::
