---
applies_to:
  stack: all 
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---


# Tenable VM  
This page explains how to make data from the Tenable Vulnerability Management integration (Tenable VM) appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.

In order for Tenable VM data to appear in these workflows:

- Ensure you have read privileges for the following index: `security_solution-*.vulnerability_latest`.
- Follow the steps to [set up the Tenable VM integration](https://www.elastic.co/docs/reference/integrations/tenable_io).
- ({{stack}} users) Ensure you're on at least v9.1.
- Make sure the Tenable VM version is at least 4.0.0.

::::{note}
You can ingest data from the Tenable VM integration for other purposes without following these steps.
::::
